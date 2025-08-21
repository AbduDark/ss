#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional Customer Management System Launcher
Production-ready version with error handling
"""

import sys
import os
import traceback
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_modules = []
    
    try:
        import sqlite3
    except ImportError:
        missing_modules.append("sqlite3")
    
    try:
        from tkinter import ttk
    except ImportError:
        missing_modules.append("tkinter")
    
    if missing_modules:
        error_msg = f"المكونات التالية مفقودة: {', '.join(missing_modules)}"
        print(f"Error: {error_msg}")
        return False
    
    return True

def setup_error_handling():
    """Setup global error handling"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = f"حدث خطأ غير متوقع:\n\n{exc_type.__name__}: {exc_value}"
        
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            messagebox.showerror("خطأ في التطبيق", error_msg)
            root.destroy()
        except:
            print(f"Critical Error: {error_msg}")
        
        # Log the error
        with open('error_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Error occurred at: {__import__('datetime').datetime.now()}\n")
            f.write(f"Error: {exc_type.__name__}: {exc_value}\n")
            f.write("Traceback:\n")
            traceback.print_exc(file=f)
            f.write(f"{'='*50}\n")
    
    sys.excepthook = handle_exception

def main():
    """Main application launcher"""
    print("🚀 بدء تشغيل نظام إدارة عملاء الشبكات المصرية...")
    
    # Setup error handling
    setup_error_handling()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ فشل في التحقق من المتطلبات")
        return 1
    
    print("✅ تم التحقق من جميع المتطلبات")
    
    try:
        # Import and run the main application
        from main import ProfessionalMainApplication
        
        print("📱 تشغيل التطبيق...")
        app = ProfessionalMainApplication()
        app.run()
        
        print("✅ تم إغلاق التطبيق بنجاح")
        return 0
        
    except ImportError as e:
        error_msg = f"فشل في تحميل التطبيق: {str(e)}"
        print(f"❌ {error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ في بدء التطبيق", error_msg)
            root.destroy()
        except:
            pass
        
        return 1
        
    except Exception as e:
        error_msg = f"خطأ في تشغيل التطبيق: {str(e)}"
        print(f"❌ {error_msg}")
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ في التطبيق", error_msg)
            root.destroy()
        except:
            pass
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)