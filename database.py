#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database manager for Egyptian Carriers Customer Management System
Handles SQLite database operations
"""

import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="customers.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    national_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    notes TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Add notes column if it doesn't exist (for existing databases)
            try:
                cursor.execute('ALTER TABLE customers ADD COLUMN notes TEXT DEFAULT ""')
                conn.commit()
            except sqlite3.OperationalError:
                # Column already exists
                pass

            # Create phone_numbers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS phone_numbers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_national_id TEXT NOT NULL,
                    carrier TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    has_wallet BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_national_id) REFERENCES customers (national_id) ON DELETE CASCADE,
                    UNIQUE(customer_national_id, carrier, phone_number)
                )
            ''')

            # Create indexes for better performance
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_phone_numbers_customer 
                ON phone_numbers (customer_national_id)
            ''')

            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_phone_numbers_carrier 
                ON phone_numbers (carrier)
            ''')

            conn.commit()

    def add_customer(self, national_id, name, notes=''):
        """Add a new customer"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customers (national_id, name, notes)
                VALUES (?, ?, ?)
            ''', (national_id, name, notes))
            conn.commit()

    def get_customer(self, national_id):
        """Get customer by national ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT national_id, name, notes, created_at, updated_at
                FROM customers
                WHERE national_id = ?
            ''', (national_id,))

            row = cursor.fetchone()
            if row:
                return {
                    'national_id': row[0],
                    'name': row[1],
                    'notes': row[2] or '',
                    'created_at': row[3],
                    'updated_at': row[4]
                }
            return None

    def update_customer(self, national_id, name, notes=''):
        """Update customer information"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE customers 
                SET name = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE national_id = ?
            ''', (name, notes, national_id))
            conn.commit()

    def delete_customer(self, national_id):
        """Delete customer and all associated phone numbers"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM customers WHERE national_id = ?', (national_id,))
            conn.commit()

    def get_all_customers(self):
        """Get all customers"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT national_id, name, notes, created_at, updated_at
                FROM customers
                ORDER BY name
            ''')

            customers = []
            for row in cursor.fetchall():
                customers.append({
                    'national_id': row[0],
                    'name': row[1],
                    'notes': row[2] or '',
                    'created_at': row[3],
                    'updated_at': row[4]
                })

            return customers

    def add_phone_number(self, customer_national_id, carrier, phone_number, has_wallet=False):
        """Add a phone number for a customer"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO phone_numbers (customer_national_id, carrier, phone_number, has_wallet)
                    VALUES (?, ?, ?, ?)
                ''', (customer_national_id, carrier, phone_number, has_wallet))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                # Phone number already exists for this customer and carrier
                return False

    def get_customer_phone_numbers(self, customer_national_id):
        """Get all phone numbers for a customer"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, carrier, phone_number, has_wallet, created_at
                FROM phone_numbers
                WHERE customer_national_id = ?
                ORDER BY carrier, phone_number
            ''', (customer_national_id,))

            phone_numbers = []
            for row in cursor.fetchall():
                phone_numbers.append({
                    'id': row[0],
                    'carrier': row[1],
                    'phone_number': row[2],
                    'has_wallet': bool(row[3]),
                    'created_at': row[4]
                })

            return phone_numbers

    def update_phone_number_wallet_status(self, phone_id, has_wallet):
        """Update wallet status for a phone number"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE phone_numbers 
                SET has_wallet = ?
                WHERE id = ?
            ''', (has_wallet, phone_id))
            conn.commit()

    def delete_phone_number(self, phone_id):
        """Delete a phone number"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM phone_numbers WHERE id = ?', (phone_id,))
            conn.commit()

    def get_all_customers_with_phones(self):
        """Get all customers with their phone numbers organized by carrier"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    c.national_id,
                    c.name,
                    c.notes,
                    p.carrier,
                    p.phone_number,
                    p.has_wallet,
                    p.id as phone_id
                FROM customers c
                LEFT JOIN phone_numbers p ON c.national_id = p.customer_national_id
                ORDER BY c.name, p.carrier, p.phone_number
            ''')

            # Organize data by customer
            customers = {}
            for row in cursor.fetchall():
                national_id = row[0]
                if national_id not in customers:
                    customers[national_id] = {
                        'national_id': national_id,
                        'name': row[1],
                        'notes': row[2] or '',
                        'carriers': {
                            'اورانج': [],      # Orange
                            'فودافون': [],     # Vodafone  
                            'اتصالات': [],     # Etisalat
                            'وي': []           # WE
                        }
                    }

                # Add phone number if exists
                if row[3]:  # carrier
                    carrier = row[3]
                    if carrier in customers[national_id]['carriers']:
                        customers[national_id]['carriers'][carrier].append({
                            'phone_number': row[4],
                            'has_wallet': bool(row[5]),
                            'phone_id': row[6]
                        })

            return list(customers.values())

    def search_customers(self, search_term):
        """Search customers by name, national ID, notes, or phone numbers"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Search in customers table (name, national_id, notes) and phone numbers
            cursor.execute('''
                SELECT DISTINCT c.national_id, c.name, c.notes, c.created_at, c.updated_at
                FROM customers c
                LEFT JOIN phone_numbers p ON c.national_id = p.customer_national_id
                WHERE c.name LIKE ? 
                   OR c.national_id LIKE ? 
                   OR c.notes LIKE ?
                   OR p.phone_number LIKE ?
                ORDER BY c.name
            ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

            customers = []
            for row in cursor.fetchall():
                customers.append({
                    'national_id': row[0],
                    'name': row[1],
                    'notes': row[2] or '',
                    'created_at': row[3],
                    'updated_at': row[4]
                })

            return customers

    def get_statistics(self):
        """Get database statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total customers
            cursor.execute('SELECT COUNT(*) FROM customers')
            total_customers = cursor.fetchone()[0]

            # Total phone numbers
            cursor.execute('SELECT COUNT(*) FROM phone_numbers')
            total_phones = cursor.fetchone()[0]

            # Phone numbers by carrier
            cursor.execute('''
                SELECT carrier, COUNT(*) 
                FROM phone_numbers 
                GROUP BY carrier
            ''')
            carriers_stats = dict(cursor.fetchall())

            # Wallet statistics
            cursor.execute('''
                SELECT carrier, COUNT(*) 
                FROM phone_numbers 
                WHERE has_wallet = 1
                GROUP BY carrier
            ''')
            wallet_stats = dict(cursor.fetchall())

            return {
                'total_customers': total_customers,
                'total_phones': total_phones,
                'carriers_stats': carriers_stats,
                'wallet_stats': wallet_stats
            }