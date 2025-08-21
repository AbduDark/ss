#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer management logic for Egyptian Carriers Customer Management System
Business logic layer for customer operations
"""

import re
from database import DatabaseManager

class CustomerManager:
    def __init__(self, db_manager):
        self.db = db_manager
        
        # Egyptian mobile number patterns
        self.mobile_patterns = {
            'اورانج': [r'010\d{8}', r'012\d{8}'],      # Orange
            'فودافون': [r'010\d{8}', r'011\d{8}'],     # Vodafone
            'اتصالات': [r'011\d{8}', r'012\d{8}'],     # Etisalat
            'وي': [r'015\d{8}']                         # WE
        }
    
    def add_customer(self, national_id, name, notes=''):
        """Add a new customer with validation"""
        # Validate national ID
        if not self.validate_national_id(national_id):
            raise ValueError("الرقم القومي غير صحيح")
        
        # Validate name
        if not name or len(name.strip()) < 2:
            raise ValueError("اسم العميل يجب أن يكون أكثر من حرفين")
        
        # Check if customer already exists
        existing = self.db.get_customer(national_id)
        if existing:
            raise ValueError("عميل بهذا الرقم القومي موجود بالفعل")
        
        # Add customer
        self.db.add_customer(national_id, name.strip(), notes.strip())
    
    def update_customer(self, national_id, name, notes=''):
        """Update customer information"""
        # Validate name
        if not name or len(name.strip()) < 2:
            raise ValueError("اسم العميل يجب أن يكون أكثر من حرفين")
        
        # Check if customer exists
        customer = self.db.get_customer(national_id)
        if not customer:
            raise ValueError("العميل غير موجود")
        
        # Update customer
        self.db.update_customer(national_id, name.strip(), notes.strip())
    
    def delete_customer(self, national_id):
        """Delete a customer and all associated data"""
        # Check if customer exists
        customer = self.db.get_customer(national_id)
        if not customer:
            raise ValueError("العميل غير موجود")
        
        # Delete customer (cascade will handle phone numbers)
        self.db.delete_customer(national_id)
    
    def get_customer(self, national_id):
        """Get customer by national ID"""
        return self.db.get_customer(national_id)
    
    def get_all_customers(self):
        """Get all customers"""
        return self.db.get_all_customers()
    
    def get_all_customers_with_phones(self):
        """Get all customers with their phone numbers"""
        return self.db.get_all_customers_with_phones()
    
    def add_phone_number(self, customer_national_id, carrier, phone_number, has_wallet=False):
        """Add a phone number for a customer with validation"""
        # Validate customer exists
        customer = self.db.get_customer(customer_national_id)
        if not customer:
            raise ValueError("العميل غير موجود")
        
        # Validate carrier
        if carrier not in ['اورانج', 'فودافون', 'اتصالات', 'وي']:
            raise ValueError("شبكة الاتصالات غير صحيحة")
        
        # Validate phone number
        if not self.validate_phone_number(phone_number, carrier):
            raise ValueError(f"رقم الهاتف غير صحيح لشبكة {carrier}")
        
        # Add phone number
        success = self.db.add_phone_number(customer_national_id, carrier, phone_number, has_wallet)
        if not success:
            raise ValueError("رقم الهاتف موجود بالفعل لهذا العميل")
    
    def validate_national_id(self, national_id):
        """Validate Egyptian national ID"""
        if not national_id or len(national_id) != 14:
            return False
        
        if not national_id.isdigit():
            return False
        
        # Basic validation for Egyptian national ID format
        # First digit should be 2 or 3 (for 20th or 21st century)
        if national_id[0] not in ['2', '3']:
            return False
        
        return True
    
    def validate_phone_number(self, phone_number, carrier):
        """Validate phone number for specific carrier"""
        if not phone_number or len(phone_number) != 11:
            return False
        
        if not phone_number.isdigit():
            return False
        
        # Check against carrier patterns
        patterns = self.mobile_patterns.get(carrier, [])
        for pattern in patterns:
            if re.match(pattern, phone_number):
                return True
        
        return False
    
    def search_customers(self, search_term):
        """Search customers by name, national ID, notes, or phone numbers"""
        if not search_term or len(search_term.strip()) < 1:
            return []
        
        return self.db.search_customers(search_term.strip())
    
    def get_customer_phone_numbers(self, customer_national_id):
        """Get all phone numbers for a customer"""
        return self.db.get_customer_phone_numbers(customer_national_id)
    
    def update_phone_wallet_status(self, phone_id, has_wallet):
        """Update wallet status for a phone number"""
        self.db.update_phone_number_wallet_status(phone_id, has_wallet)
    
    def delete_phone_number(self, phone_id):
        """Delete a phone number"""
        self.db.delete_phone_number(phone_id)
    
    def get_statistics(self):
        """Get system statistics"""
        return self.db.get_statistics()
    
    def normalize_carrier_name(self, carrier_text):
        """Normalize carrier name from OCR text"""
        carrier_text = carrier_text.lower().strip()
        
        # Mapping for different variations
        carrier_mappings = {
            'orange': 'اورانج',
            'اورانج': 'اورانج',
            'أورانج': 'اورانج',
            'vodafone': 'فودافون', 
            'فودافون': 'فودافون',
            'etisalat': 'اتصالات',
            'اتصالات': 'اتصالات',
            'we': 'وي',
            'وي': 'وي'
        }
        
        for key, value in carrier_mappings.items():
            if key in carrier_text:
                return value
        
        return None
    
    def extract_phone_numbers_from_text(self, text):
        """Extract Egyptian mobile numbers from text"""
        # Pattern for Egyptian mobile numbers
        phone_pattern = r'\b(010|011|012|015)\d{8}\b'
        
        matches = re.findall(phone_pattern, text)
        phone_numbers = []
        
        for match in re.finditer(phone_pattern, text):
            phone_numbers.append(match.group())
        
        return phone_numbers
    
    def determine_carrier_from_number(self, phone_number):
        """Determine carrier from phone number"""
        if not phone_number or len(phone_number) != 11:
            return None
        
        prefix = phone_number[:3]
        
        # Egyptian mobile prefixes
        if prefix in ['010']:
            return 'اورانج'  # Orange uses 010 (shared with Vodafone)
        elif prefix in ['011']:
            return 'فودافون'  # Vodafone uses 011 (shared with Etisalat)
        elif prefix in ['012']:
            return 'اتصالات'  # Etisalat uses 012 (shared with Orange)
        elif prefix in ['015']:
            return 'وي'       # WE uses 015
        
        return None
    
    def batch_add_phone_numbers(self, customer_national_id, phone_data_list):
        """Add multiple phone numbers for a customer"""
        results = {
            'success': [],
            'errors': []
        }
        
        for phone_data in phone_data_list:
            try:
                self.add_phone_number(
                    customer_national_id,
                    phone_data['carrier'],
                    phone_data['phone_number'],
                    phone_data.get('has_wallet', False)
                )
                results['success'].append(phone_data)
            except Exception as e:
                results['errors'].append({
                    'phone_data': phone_data,
                    'error': str(e)
                })
        
        return results
