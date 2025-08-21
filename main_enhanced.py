#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced methods for the main application
"""

import tkinter as tk
from tkinter import ttk, messagebox

def setup_window_styling(self):
    """Setup window styling and properties"""
    # Try to set window icon (if available)
    try:
        # You can add an icon file here later
        pass
    except:
        pass
    
    # Configure window properties
    self.root.configure(bg='#f8f9fa')
    self.root.attributes("-fullscreen", True)

def setup_modern_styling(self):
    """Setup modern visual styling"""
    # Configure modern color scheme
    self.colors = {
        'primary': '#4F81BD',
        'secondary': '#6c757d', 
        'success': '#28a745',
        'warning': '#ffc107',
        'danger': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#2c3e50',
        'white': '#ffffff'
    }
    
    # Set application-wide style
    self.root.configure(bg=self.colors['light'])

def configure_ttk_styles(self):
    """Configure TTK widget styles"""
    style = ttk.Style()
    
    # Configure notebook style for modern tabs
    style.configure('Modern.TNotebook', 
                   background=self.colors['light'],
                   borderwidth=0)
    
    style.configure('Modern.TNotebook.Tab',
                   background=self.colors['white'],
                   foreground=self.colors['dark'],
                   padding=[20, 10],
                   font=self.button_font)
    
    # Configure modern button styles
    style.configure('Success.TButton', 
                   background=self.colors['success'],
                   foreground='white',
                   font=self.button_font,
                   borderwidth=0,
                   focuscolor='none',
                   padding=[20, 10])
    
    style.map('Success.TButton',
              background=[('active', '#218838'),
                         ('pressed', '#1e7e34')])
    
    style.configure('Warning.TButton', 
                   background=self.colors['warning'],
                   foreground='black',
                   font=self.button_font,
                   borderwidth=0,
                   focuscolor='none',
                   padding=[20, 10])
    
    style.map('Warning.TButton',
              background=[('active', '#e0a800'),
                         ('pressed', '#d39e00')])
    
    style.configure('Danger.TButton', 
                   background=self.colors['danger'],
                   foreground='white',
                   font=self.button_font,
                   borderwidth=0,
                   focuscolor='none',
                   padding=[20, 10])
    
    style.map('Danger.TButton',
              background=[('active', '#c82333'),
                         ('pressed', '#bd2130')])
    
    style.configure('Info.TButton', 
                   background=self.colors['info'],
                   foreground='white',
                   font=self.button_font,
                   borderwidth=0,
                   focuscolor='none',
                   padding=[20, 10])
    
    style.map('Info.TButton',
              background=[('active', '#138496'),
                         ('pressed', '#117a8b')])

def center_window(self):
    """Center the main window on screen"""
    self.root.update_idletasks()
    width = self.root.winfo_width()
    height = self.root.winfo_height()
    x = (self.root.winfo_screenwidth() // 2) - (width // 2)
    y = (self.root.winfo_screenheight() // 2) - (height // 2)
    self.root.geometry(f'{width}x{height}+{x}+{y}')

def show_success_message(self, message):
    """Show success message with custom styling"""
    success_dialog = tk.Toplevel(self.root)
    success_dialog.title("نجح العملية")
    success_dialog.geometry("400x200")
    success_dialog.configure(bg='#ffffff')
    success_dialog.grab_set()
    success_dialog.transient(self.root)
    
    # Center dialog
    success_dialog.update_idletasks()
    x = (success_dialog.winfo_screenwidth() // 2) - 200
    y = (success_dialog.winfo_screenheight() // 2) - 100
    success_dialog.geometry(f'400x200+{x}+{y}')
    
    # Content frame
    content_frame = tk.Frame(success_dialog, bg='#ffffff')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Success icon
    tk.Label(
        content_frame,
        text="✅",
        font=('Arial Unicode MS', 32),
        bg='#ffffff',
        fg='#28a745'
    ).pack(pady=(0, 15))
    
    # Success message
    tk.Label(
        content_frame,
        text=message,
        font=self.arabic_font,
        bg='#ffffff',
        fg='#28a745',
        wraplength=350,
        justify=tk.CENTER
    ).pack(pady=(0, 20))
    
    # OK button
    tk.Button(
        content_frame,
        text="حسناً",
        command=success_dialog.destroy,
        font=(self.arabic_font[0], self.arabic_font[1], 'bold'),
        bg='#28a745',
        fg='white',
        bd=0,
        padx=30,
        pady=10,
        cursor='hand2'
    ).pack()
    
    # Auto-close after 3 seconds
    self.root.after(3000, success_dialog.destroy)

def show_error_message(self, message):
    """Show error message with custom styling"""
    error_dialog = tk.Toplevel(self.root)
    error_dialog.title("خطأ")
    error_dialog.geometry("400x200")
    error_dialog.configure(bg='#ffffff')
    error_dialog.grab_set()
    error_dialog.transient(self.root)
    
    # Center dialog
    error_dialog.update_idletasks()
    x = (error_dialog.winfo_screenwidth() // 2) - 200
    y = (error_dialog.winfo_screenheight() // 2) - 100
    error_dialog.geometry(f'400x200+{x}+{y}')
    
    # Content frame
    content_frame = tk.Frame(error_dialog, bg='#ffffff')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Error icon
    tk.Label(
        content_frame,
        text="❌",
        font=('Arial Unicode MS', 32),
        bg='#ffffff',
        fg='#dc3545'
    ).pack(pady=(0, 15))
    
    # Error message
    tk.Label(
        content_frame,
        text=message,
        font=self.arabic_font,
        bg='#ffffff',
        fg='#dc3545',
        wraplength=350,
        justify=tk.CENTER
    ).pack(pady=(0, 20))
    
    # OK button
    tk.Button(
        content_frame,
        text="حسناً",
        command=error_dialog.destroy,
        font=(self.arabic_font[0], self.arabic_font[1], 'bold'),
        bg='#dc3545',
        fg='white',
        bd=0,
        padx=30,
        pady=10,
        cursor='hand2'
    ).pack()

def show_warning_message(self, message):
    """Show warning message with custom styling"""
    warning_dialog = tk.Toplevel(self.root)
    warning_dialog.title("تحذير")
    warning_dialog.geometry("400x200")
    warning_dialog.configure(bg='#ffffff')
    warning_dialog.grab_set()
    warning_dialog.transient(self.root)
    
    # Center dialog
    warning_dialog.update_idletasks()
    x = (warning_dialog.winfo_screenwidth() // 2) - 200
    y = (warning_dialog.winfo_screenheight() // 2) - 100
    warning_dialog.geometry(f'400x200+{x}+{y}')
    
    # Content frame
    content_frame = tk.Frame(warning_dialog, bg='#ffffff')
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Warning icon
    tk.Label(
        content_frame,
        text="⚠️",
        font=('Arial Unicode MS', 32),
        bg='#ffffff',
        fg='#ffc107'
    ).pack(pady=(0, 15))
    
    # Warning message
    tk.Label(
        content_frame,
        text=message,
        font=self.arabic_font,
        bg='#ffffff',
        fg='#856404',
        wraplength=350,
        justify=tk.CENTER
    ).pack(pady=(0, 20))
    
    # OK button
    tk.Button(
        content_frame,
        text="حسناً",
        command=warning_dialog.destroy,
        font=(self.arabic_font[0], self.arabic_font[1], 'bold'),
        bg='#ffc107',
        fg='#000000',
        bd=0,
        padx=30,
        pady=10,
        cursor='hand2'
    ).pack()

# Add methods to MainApplication class
def enhance_main_application():
    """Add enhancement methods to MainApplication class"""
    from main import MainApplication
    
    MainApplication.setup_window_styling = setup_window_styling
    MainApplication.setup_modern_styling = setup_modern_styling
    MainApplication.configure_ttk_styles = configure_ttk_styles
    MainApplication.center_window = center_window
    MainApplication.show_success_message = show_success_message
    MainApplication.show_error_message = show_error_message
    MainApplication.show_warning_message = show_warning_message