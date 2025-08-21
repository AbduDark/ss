
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Egyptian Carriers Customer Management System
Professional desktop application for managing telecom customers
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
import sys
from database import DatabaseManager
from customer_manager import CustomerManager
from gui_components import CustomerTableGUI
from enhanced_dialogs import ModernCustomerDialog, PhoneManagementDialog, SmartOCRDialog

class EnhancedOCRProcessor:
    """Basic OCR processor fallback if external module fails"""
    def __init__(self):
        self.available = False
        try:
            import pytesseract
            from PIL import Image, ImageGrab
            self.available = True
        except ImportError:
            print("تحذير: مكتبات OCR غير متوفرة")

    def extract_from_clipboard(self):
        """Extract phone numbers from clipboard image"""
        if not self.available:
            return []
        
        try:
            from PIL import ImageGrab
            import pytesseract
            
            # Get image from clipboard
            image = ImageGrab.grabclipboard()
            if not image:
                return []
            
            # Extract text
            text = pytesseract.image_to_string(image, lang='ara+eng')
            
            # Extract phone numbers
            phone_pattern = r'\b(010|011|012|015)\d{8}\b'
            import re
            phones = re.findall(phone_pattern, text)
            
            result = []
            for phone in phones:
                carrier = self.determine_carrier_from_number(phone)
                result.append({
                    'phone_number': phone,
                    'carrier': carrier,
                    'has_wallet': False
                })
            
            return result
        except Exception as e:
            print(f"OCR Error: {e}")
            return []

    def extract_from_file(self, file_path):
        """Extract phone numbers from image file"""
        if not self.available:
            return []
            
        try:
            from PIL import Image
            import pytesseract
            
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, lang='ara+eng')
            
            # Extract phone numbers
            phone_pattern = r'\b(010|011|012|015)\d{8}\b'
            import re
            phones = re.findall(phone_pattern, text)
            
            result = []
            for phone in phones:
                carrier = self.determine_carrier_from_number(phone)
                result.append({
                    'phone_number': phone,
                    'carrier': carrier,
                    'has_wallet': False
                })
            
            return result
        except Exception as e:
            print(f"OCR Error: {e}")
            return []

    def determine_carrier_from_number(self, phone_number):
        """Determine carrier from phone number"""
        if not phone_number or len(phone_number) != 11:
            return 'اورانج'  # Default
        
        prefix = phone_number[:3]
        
        if prefix == '010':
            return 'اورانج'
        elif prefix == '011':
            return 'فودافون'
        elif prefix == '012':
            return 'اتصالات'
        elif prefix == '015':
            return 'وي'
        
        return 'اورانج'  # Default

class ProfessionalMainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_application()

        # Initialize components
        self.db_manager = DatabaseManager()
        self.customer_manager = CustomerManager(self.db_manager)

        # Setup UI
        self.create_professional_interface()

        # Add sample data and load
        self.add_sample_data_if_empty()
        self.refresh_data()

    def setup_application(self):
        """Setup application window and properties"""
        # Window configuration
        self.root.title("نظام إدارة عملاء الشبكات المصرية - الإصدار المحترف")
        self.root.state('zoomed')
        # Try to maximize window (cross-platform compatible)
        try:
            self.root.state('zoomed')  # Windows
        except:
            try:
                self.root.attributes('-zoomed', True)  # Linux
            except:
                pass  # Fallback to normal geometry
        self.root.configure(bg='#f5f7fa')

        # Modern fonts
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'),
            'header': ('Segoe UI', 18, 'bold'),
            'subheader': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 12),
            'button': ('Segoe UI', 11, 'bold'),
            'small': ('Segoe UI', 10)
        }

        # Professional color scheme
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#F18F01',
            'warning': '#C73E1D',
            'info': '#6A994E',
            'light': '#f5f7fa',
            'dark': '#2d3436',
            'white': '#ffffff',
            'accent': '#00b894',
            'muted': '#636e72',
            'border': '#ddd'
        }

        # Configure styles
        self.setup_professional_styles()

        # Center window
        self.center_window()

    def setup_professional_styles(self):
        """Setup professional TTK styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Professional button styles
        style.configure('Professional.TButton',
                       background=self.colors['primary'],
                       foreground='white',
                       font=self.fonts['button'],
                       padding=(20, 12),
                       borderwidth=0,
                       focuscolor='none')

        style.map('Professional.TButton',
                  background=[('active', '#1e5f85'),
                             ('pressed', '#1a4f6f')])

        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       font=self.fonts['button'],
                       padding=(20, 12))

        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       font=self.fonts['button'],
                       padding=(20, 12))

        style.configure('Info.TButton',
                       background=self.colors['info'],
                       foreground='white',
                       font=self.fonts['button'],
                       padding=(20, 12))

    def create_professional_interface(self):
        """Create professional main interface"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Header section
        self.create_professional_header(main_container)

        # Navigation and actions
        self.create_action_toolbar(main_container)

        # Statistics dashboard
        self.create_statistics_panel(main_container)

        # Main content area
        self.create_main_content_area(main_container)

        # Status bar
        self.create_status_bar(main_container)

    def create_professional_header(self, parent):
        """Create professional header with branding"""
        header_frame = tk.Frame(parent, bg=self.colors['primary'], height=120)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)

        # Left side - Logo and title
        left_header = tk.Frame(header_content, bg=self.colors['primary'])
        left_header.pack(side=tk.LEFT, fill=tk.Y)

        # App title
        title_label = tk.Label(
            left_header,
            text="🏢 نظام إدارة عملاء شبكات الاتصالات",
            font=self.fonts['title'],
            bg=self.colors['primary'],
            fg='white'
        )
        title_label.pack(anchor='w')

        # Subtitle
        subtitle_label = tk.Label(
            left_header,
            text="إدارة متكاملة للعملاء عبر جميع الشبكات المصرية (أورانج • فودافون • اتصالات • وي)",
            font=self.fonts['body'],
            bg=self.colors['primary'],
            fg='#b8d4e3'
        )
        subtitle_label.pack(anchor='w', pady=(5, 0))

        # Right side - Quick stats
        right_header = tk.Frame(header_content, bg=self.colors['primary'])
        right_header.pack(side=tk.RIGHT, fill=tk.Y)

        # Quick stats will be populated dynamically
        self.stats_frame = right_header

    def create_action_toolbar(self, parent):
        """Create professional action toolbar"""
        toolbar_frame = tk.Frame(parent, bg='white', relief=tk.FLAT, bd=0)
        toolbar_frame.pack(fill=tk.X, padx=0, pady=0)

        # Toolbar content
        toolbar_content = tk.Frame(toolbar_frame, bg='white')
        toolbar_content.pack(fill=tk.X, padx=40, pady=20)

        # Action buttons with icons
        actions = [
            ("👤 إضافة عميل جديد", self.add_customer, self.colors['success'], "إضافة عميل جديد إلى النظام"),
            ("✏️ إدارة العملاء", self.edit_customer, self.colors['info'], "تعديل بيانات وأرقام العملاء"),
            ("🗑️ حذف عميل", self.delete_customer, self.colors['warning'], "حذف عميل من النظام"),
            ("📷 استخراج من صورة", self.extract_from_image, self.colors['secondary'], "استخراج أرقام من الصور"),
            ("🔄 تحديث البيانات", self.refresh_data, self.colors['muted'], "إعادة تحميل البيانات")
        ]

        for text, command, color, tooltip in actions:
            btn_frame = tk.Frame(toolbar_content, bg='white')
            btn_frame.pack(side=tk.LEFT, padx=10)

            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                font=self.fonts['button'],
                bg=color,
                fg='white',
                bd=0,
                padx=25,
                pady=12,
                cursor='hand2',
                relief=tk.FLAT,
                activebackground=self.darken_color(color),
                activeforeground='white'
            )
            btn.pack()

            # Tooltip label
            tooltip_label = tk.Label(
                btn_frame,
                text=tooltip,
                font=self.fonts['small'],
                bg='white',
                fg=self.colors['muted']
            )
            tooltip_label.pack(pady=(5, 0))

    def create_statistics_panel(self, parent):
        """Create statistics dashboard panel"""
        stats_frame = tk.Frame(parent, bg=self.colors['light'])
        stats_frame.pack(fill=tk.X, padx=40, pady=(0, 20))

        self.stats_cards = {}

        # Stats cards
        stats_data = [
            ("👥", "إجمالي العملاء", "0", self.colors['primary']),
            ("📱", "إجمالي الأرقام", "0", self.colors['success']),
            ("💰", "أرقام بمحفظة", "0", self.colors['info']),
            ("📊", "متوسط الأرقام", "0.0", self.colors['secondary'])
        ]

        for icon, title, value, color in stats_data:
            card = self.create_stat_card(stats_frame, icon, title, value, color)
            card.pack(side=tk.LEFT, padx=10, pady=10)
            self.stats_cards[title] = card

    def create_stat_card(self, parent, icon, title, value, color):
        """Create individual statistics card"""
        card_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        card_frame.configure(width=200, height=120)
        card_frame.pack_propagate(False)

        # Card content
        content_frame = tk.Frame(card_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Icon and value section
        top_section = tk.Frame(content_frame, bg='white')
        top_section.pack(fill=tk.X)

        # Icon
        icon_label = tk.Label(
            top_section,
            text=icon,
            font=('Segoe UI', 24),
            bg='white',
            fg=color
        )
        icon_label.pack(side=tk.LEFT)

        # Value
        value_label = tk.Label(
            top_section,
            text=value,
            font=('Segoe UI', 20, 'bold'),
            bg='white',
            fg=color
        )
        value_label.pack(side=tk.RIGHT)

        # Title
        title_label = tk.Label(
            content_frame,
            text=title,
            font=self.fonts['subheader'],
            bg='white',
            fg=self.colors['dark']
        )
        title_label.pack(anchor='w', pady=(10, 0))

        # Store references for updating  
        setattr(card_frame, 'value_label', value_label)

        return card_frame

    def create_main_content_area(self, parent):
        """Create main content area with table"""
        content_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, bd=2)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 20))

        # Content header
        content_header = tk.Frame(content_frame, bg='white')
        content_header.pack(fill=tk.X, padx=20, pady=20)

        header_label = tk.Label(
            content_header,
            text="📋 قائمة العملاء وأرقام الهواتف",
            font=self.fonts['header'],
            bg='white',
            fg=self.colors['dark']
        )
        header_label.pack(side=tk.LEFT)

        # Search section
        search_frame = tk.Frame(content_header, bg='white')
        search_frame.pack(side=tk.RIGHT)

        tk.Label(
            search_frame,
            text="🔍 البحث:",
            font=self.fonts['body'],
            bg='white',
            fg=self.colors['muted']
        ).pack(side=tk.LEFT, padx=(0, 10))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.fonts['body'],
            width=25,
            bd=2,
            relief=tk.GROOVE
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind('<KeyRelease>', self.perform_search)

        # Search help label
        search_help = tk.Label(
            search_frame, 
            text="(البحث في: الاسم، الرقم القومي، الملاحظات، أرقام الهواتف)", 
            font=(self.fonts['body'][0], self.fonts['body'][1]-2),
            fg='#6c757d'
        )
        search_help.pack(side=tk.LEFT, padx=(5, 0))

        # Table container
        table_container = tk.Frame(content_frame, bg='white')
        table_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Customer table
        self.table_gui = CustomerTableGUI(table_container, self.fonts['body'], self.customer_manager)
        self.table_gui.frame.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self, parent):
        """Create professional status bar"""
        status_frame = tk.Frame(parent, bg=self.colors['primary'], height=40)
        status_frame.pack(fill=tk.X)
        status_frame.pack_propagate(False)

        # Status content
        status_content = tk.Frame(status_frame, bg=self.colors['primary'])
        status_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)

        # Left status
        self.status_var = tk.StringVar(value="جاهز للعمل")
        status_label = tk.Label(
            status_content,
            textvariable=self.status_var,
            font=self.fonts['body'],
            bg=self.colors['primary'],
            fg='white'
        )
        status_label.pack(side=tk.LEFT)

        # Right status - version info
        version_label = tk.Label(
            status_content,
            text="الإصدار 1.0 - نظام إدارة عملاء الشبكات المصرية",
            font=self.fonts['small'],
            bg=self.colors['primary'],
            fg='#b8d4e3'
        )
        version_label.pack(side=tk.RIGHT)

    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def darken_color(self, color):
        """Darken a hex color"""
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        dark_rgb = tuple(max(0, int(c * 0.8)) for c in rgb)
        return f"#{dark_rgb[0]:02x}{dark_rgb[1]:02x}{dark_rgb[2]:02x}"

    def update_statistics(self):
        """Update statistics cards"""
        try:
            customers = self.customer_manager.get_all_customers_with_phones()

            total_customers = len(customers)
            total_phones = sum(
                len(c['carriers']['اورانج']) + 
                len(c['carriers']['فودافون']) + 
                len(c['carriers']['اتصالات']) + 
                len(c['carriers']['وي'])
                for c in customers
            )

            wallet_phones = sum(
                sum(1 for p in c['carriers']['اورانج'] if p['has_wallet']) +
                sum(1 for p in c['carriers']['فودافون'] if p['has_wallet']) +
                sum(1 for p in c['carriers']['اتصالات'] if p['has_wallet']) +
                sum(1 for p in c['carriers']['وي'] if p['has_wallet'])
                for c in customers
            )

            avg_phones = total_phones / total_customers if total_customers > 0 else 0

            # Update cards
            self.stats_cards["إجمالي العملاء"].value_label.config(text=str(total_customers))
            self.stats_cards["إجمالي الأرقام"].value_label.config(text=str(total_phones))
            self.stats_cards["أرقام بمحفظة"].value_label.config(text=str(wallet_phones))
            self.stats_cards["متوسط الأرقام"].value_label.config(text=f"{avg_phones:.1f}")

        except Exception as e:
            print(f"Error updating statistics: {e}")

    def add_sample_data_if_empty(self):
        """Add sample data if database is empty"""
        try:
            customers = self.customer_manager.get_all_customers()
            if not customers:
                # Add sample customers
                sample_customers = [
                    ("30303032123456", "أحمد محمد علي"),
                    ("30130310654321", "محمد أحمد حسن"),
                    ("29512345987654", "فاطمة علي محمد"),
                    ("30203021234567", "سارة محمود أحمد"),
                    ("29912348765432", "علي حسن محمد")
                ]

                for national_id, name in sample_customers:
                    try:
                        self.customer_manager.add_customer(national_id, name)
                    except:
                        pass

                # Add sample phone numbers
                sample_phones = [
                    ("30303032123456", "اورانج", "01012346790", True),
                    ("30303032123456", "فودافون", "01112346790", False),
                    ("30303032123456", "اتصالات", "01212346790", True),
                    ("30303032123456", "وي", "01512346790", False),

                    ("30130310654321", "اورانج", "01012346791", False),
                    ("30130310654321", "فودافون", "01112346791", True),
                    ("30130310654321", "اتصالات", "01212346791", False),
                    ("30130310654321", "وي", "01512346791", True),

                    ("29512345987654", "اورانج", "01012346792", True),
                    ("29512345987654", "فودافون", "01112346792", True),
                    ("29512345987654", "اتصالات", "01212346792", False),

                    ("30203021234567", "فودافون", "01123456789", True),
                    ("30203021234567", "اتصالات", "01234567890", False),

                    ("29912348765432", "اورانج", "01098765432", True),
                    ("29912348765432", "وي", "01587654321", True),
                ]

                for national_id, carrier, phone, wallet in sample_phones:
                    try:
                        self.customer_manager.add_phone_number(national_id, carrier, phone, wallet)
                    except:
                        pass
        except Exception as e:
            print(f"Error adding sample data: {e}")

    def add_customer(self):
        """Add new customer with phone numbers"""
        dialog = ModernCustomerDialog(
            self.root, 
            "إضافة عميل جديد", 
            self.fonts['body'],
            self.customer_manager
        )
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            try:
                customer_data = dialog.result

                # Add customer with notes
                self.customer_manager.add_customer(
                    customer_data['national_id'],
                    customer_data['name'],
                    customer_data.get('notes', '')
                )

                # Add phone numbers if any
                if customer_data.get('phone_numbers'):
                    success_count = 0
                    for phone in customer_data['phone_numbers']:
                        try:
                            self.customer_manager.add_phone_number(
                                customer_data['national_id'],
                                phone['carrier'],
                                phone['phone_number'],
                                phone['has_wallet']
                            )
                            success_count += 1
                        except Exception as e:
                            print(f"Error adding phone {phone['phone_number']}: {e}")

                    if success_count > 0:
                        self.show_success_notification(f"تم إضافة العميل مع {success_count} رقم هاتف بنجاح")
                    else:
                        self.show_success_notification("تم إضافة العميل بنجاح")
                else:
                    self.show_success_notification("تم إضافة العميل بنجاح")

                self.refresh_data()
            except Exception as e:
                self.show_error_notification(f"فشل في إضافة العميل: {str(e)}")

    def edit_customer(self):
        """Edit selected customer with phone management"""
        selected = self.table_gui.get_selected_customer()
        if not selected:
            self.show_warning_notification("يرجى اختيار عميل للتعديل")
            return

        dialog = PhoneManagementDialog(
            self.root, 
            selected,
            self.customer_manager,
            self.fonts['body']
        )

        self.root.wait_window(dialog.dialog)
        self.refresh_data()

    def delete_customer(self):
        """Delete selected customer"""
        selected = self.table_gui.get_selected_customer()
        if not selected:
            self.show_warning_notification("يرجى اختيار عميل للحذف")
            return

        if messagebox.askyesno(
            "تأكيد الحذف", 
            f"هل أنت متأكد من حذف العميل {selected['name']}؟\n\nسيتم حذف جميع أرقام الهاتف المرتبطة بهذا العميل.",
            icon='warning'
        ):
            try:
                self.customer_manager.delete_customer(selected['national_id'])
                self.show_success_notification("تم حذف العميل بنجاح")
                self.refresh_data()
            except Exception as e:
                self.show_error_notification(f"فشل في حذف العميل: {str(e)}")

    def extract_from_image(self):
        """Extract phone numbers from image using smart OCR dialog"""
        dialog = SmartOCRDialog(
            self.root,
            self.fonts['body'],
            self.customer_manager
        )

        self.root.wait_window(dialog.dialog)
        self.refresh_data()

    def perform_search(self, event=None):
        """Perform comprehensive search input"""
        search_term = self.search_var.get().strip()

        if not search_term:
            # Show all customers if search is empty
            self.refresh_data()
            return

        try:
            # Search customers using the enhanced search
            customers = self.customer_manager.search_customers(search_term)

            if customers:
                # Get customers with phones for matching customers
                all_customers_with_phones = self.customer_manager.get_all_customers_with_phones()
                filtered_customers = [
                    customer for customer in all_customers_with_phones 
                    if customer['national_id'] in [c['national_id'] for c in customers]
                ]

                self.table_gui.update_data(filtered_customers)
                self.status_var.set(f"تم العثور على {len(customers)} عميل مطابق للبحث: '{search_term}'")
            else:
                self.table_gui.update_data([])
                self.status_var.set(f"لم يتم العثور على أي عملاء مطابقين للبحث: '{search_term}'")

        except Exception as e:
            self.show_error_notification(f"فشل في البحث: {str(e)}")
            self.status_var.set("خطأ في البحث")

    def refresh_data(self):
        """Refresh the customer data display"""
        try:
            self.status_var.set("جاري تحديث البيانات...")
            self.root.update()

            customers = self.customer_manager.get_all_customers_with_phones()
            self.table_gui.update_data(customers)
            self.update_statistics()

            self.status_var.set("تم تحديث البيانات بنجاح")
            self.root.after(3000, lambda: self.status_var.set("جاهز للعمل"))

        except Exception as e:
            self.show_error_notification(f"فشل في تحديث البيانات: {str(e)}")
            self.status_var.set("خطأ في تحديث البيانات")

    def show_success_notification(self, message):
        """Show success notification"""
        self.show_notification(message, "نجح", self.colors['success'])

    def show_error_notification(self, message):
        """Show error notification"""
        self.show_notification(message, "خطأ", self.colors['warning'])

    def show_warning_notification(self, message):
        """Show warning notification"""
        self.show_notification(message, "تحذير", self.colors['info'])

    def show_info_notification(self, message):
        """Show info notification"""
        self.show_notification(message, "معلومات", self.colors['primary'])

    def show_notification(self, message, title, color):
        """Show professional notification popup"""
        notification = tk.Toplevel(self.root)
        notification.title(title)
        notification.geometry("450x200")
        notification.configure(bg='white')
        notification.resizable(False, False)
        notification.grab_set()
        notification.transient(self.root)

        # Center notification
        notification.update_idletasks()
        x = (notification.winfo_screenwidth() // 2) - 225
        y = (notification.winfo_screenheight() // 2) - 100
        notification.geometry(f'450x200+{x}+{y}')

        # Main frame
        main_frame = tk.Frame(notification, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # Icon and title
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 20))

        icon_map = {
            "نجح": "✅",
            "خطأ": "❌", 
            "تحذير": "⚠️",
            "معلومات": "ℹ️"
        }

        icon_label = tk.Label(
            header_frame,
            text=icon_map.get(title, "ℹ️"),
            font=('Segoe UI', 28),
            bg='white',
            fg=color
        )
        icon_label.pack(side=tk.LEFT, padx=(0, 15))

        title_label = tk.Label(
            header_frame,
            text=title,
            font=self.fonts['header'],
            bg='white',
            fg=color
        )
        title_label.pack(side=tk.LEFT, anchor='w')

        # Message
        message_label = tk.Label(
            main_frame,
            text=message,
            font=self.fonts['body'],
            bg='white',
            fg=self.colors['dark'],
            wraplength=380,
            justify=tk.RIGHT
        )
        message_label.pack(pady=(0, 20))

        # OK button
        ok_button = tk.Button(
            main_frame,
            text="حسناً",
            command=notification.destroy,
            font=self.fonts['button'],
            bg=color,
            fg='white',
            bd=0,
            padx=30,
            pady=10,
            cursor='hand2'
        )
        ok_button.pack()

        # Auto-close for success notifications
        if title == "نجح":
            self.root.after(2500, notification.destroy)

    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("خطأ في التطبيق", f"حدث خطأ غير متوقع: {str(e)}")

def main():
    """Main application entry point"""
    try:
        app = ProfessionalMainApplication()
        app.run()
    except Exception as e:
        messagebox.showerror("خطأ في بدء التطبيق", f"فشل في بدء التطبيق: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
