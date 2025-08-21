#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced dialog components for Customer Management System
Beautiful and modern dialog boxes with OCR integration
"""

import tkinter as tk
from tkinter import ttk , messagebox, filedialog, simpledialog
from PIL import Image, ImageTk
from ocr_processor import EnhancedOCRProcessor

class SmartOCRDialog:
    """Smart OCR dialog that can search for customers and add phones"""
    def __init__(self, parent, font, customer_manager):
        self.font = font
        self.customer_manager = customer_manager
        self.result = None
        self.extracted_phones = []

        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🔍 استخراج الأرقام الذكي من الصور")
        self.dialog.attributes("-fullscreen", True)
        self.dialog.resizable(True, True)
        self.dialog.configure(bg='white')
        self.dialog.grab_set()
        self.dialog.transient(parent)

        # Center dialog
        self.center_dialog(parent)

        # Setup UI
        self.setup_ui()

        # Initialize OCR
        try:
            from ocr_processor import EnhancedOCRProcessor
            self.ocr_processor = EnhancedOCRProcessor()
        except (ImportError, Exception):
            self.ocr_processor = None
            print("تحذير: مكتبة OCR غير متوفرة")

    def center_dialog(self, parent):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400)
        y = (self.dialog.winfo_screenheight() // 2) - (350)
        self.dialog.geometry(f'+{x}+{y}')

    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        header_label = tk.Label(
            main_frame,
            text="🔍 استخراج الأرقام الذكي من الصور",
            font=(self.font[0], self.font[1]+4, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        header_label.pack(pady=(0, 20))

        # Action buttons في الأعلى (سيتم نقلها للأسفل لاحقاً)
        self.setup_action_buttons(main_frame)

        # إطار للمحتوى الرئيسي
        content_frame = tk.Frame(main_frame, bg='white')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Step 1: Customer search/selection
        self.setup_customer_section(content_frame)

        # Step 2: OCR extraction
        self.setup_ocr_section(content_frame)

        # Step 3: Results display
        self.setup_results_section(content_frame)

    def setup_customer_section(self, parent):
        """Setup customer search and selection section"""
        customer_frame = tk.LabelFrame(
            parent,
            text="🔍 البحث عن العميل",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        customer_frame.pack(fill=tk.X, pady=10)

        # Enhanced search section
        search_frame = tk.Frame(customer_frame, bg='white')
        search_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            search_frame,
            text="🔍 البحث:",
            font=(self.font[0], self.font[1], 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side=tk.RIGHT, padx=(10, 0))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.font,
            width=25,
            bd=2,
            relief=tk.GROOVE
        )
        self.search_entry.pack(side=tk.RIGHT, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self.perform_search)

        search_btn = tk.Button(
            search_frame,
            text="🔍 بحث",
            command=self.perform_search,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#007bff',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        search_btn.pack(side=tk.RIGHT, padx=(0, 10))

        new_customer_btn = tk.Button(
            search_frame,
            text="👤 عميل جديد",
            command=self.create_new_customer,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        new_customer_btn.pack(side=tk.LEFT)

        # Search help label
        search_help = tk.Label(
            search_frame,
            text="(البحث في: الاسم، الرقم القومي، الملاحظات، أرقام الهواتف)",
            font=(self.font[0], self.font[1]-2),
            bg='white',
            fg='#6c757d'
        )
        search_help.pack(side=tk.LEFT, padx=(10, 0))

        # Search results frame
        self.search_results_frame = tk.Frame(customer_frame, bg='white')
        self.search_results_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        # Customer info display
        self.customer_info_frame = tk.Frame(customer_frame, bg='white')
        self.customer_info_frame.pack(fill=tk.X, padx=15, pady=(0, 15))

        self.customer_info_label = tk.Label(
            self.customer_info_frame,
            text="لم يتم اختيار عميل بعد",
            font=self.font,
            bg='#f8f9fa',
            fg='#6c757d',
            bd=1,
            relief=tk.SOLID,
            padx=10,
            pady=8
        )
        self.customer_info_label.pack(fill=tk.X)

        self.selected_customer = None

    def perform_search(self, event=None):
        """Perform comprehensive search"""
        search_term = self.search_var.get().strip()

        # Clear previous search results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

        if not search_term:
            # Hide search results if search is empty
            self.selected_customer = None
            self.update_customer_selection_display()
            return

        try:
            # Search customers using the enhanced search
            customers = self.customer_manager.search_customers(search_term)

            if customers:
                self.display_search_results(customers, search_term)
            else:
                # Show no results message
                no_results_label = tk.Label(
                    self.search_results_frame,
                    text=f"لم يتم العثور على أي عملاء مطابقين للبحث: '{search_term}'",
                    font=self.font,
                    bg='#f8d7da',
                    fg='#721c24',
                    bd=1,
                    relief=tk.SOLID,
                    padx=10,
                    pady=8
                )
                no_results_label.pack(fill=tk.X, pady=5)

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في البحث: {str(e)}")

    def display_search_results(self, customers, search_term):
        """Display search results in a selectable list"""
        # Results header
        header_label = tk.Label(
            self.search_results_frame,
            text=f"📋 نتائج البحث ({len(customers)} عميل):",
            font=(self.font[0], self.font[1], 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        header_label.pack(anchor='w', pady=(5, 10))

        # Create scrollable results area
        results_canvas = tk.Canvas(self.search_results_frame, bg='white', height=150)
        results_scrollbar = ttk.Scrollbar(self.search_results_frame, orient="vertical", command=results_canvas.yview)
        results_scrollable_frame = tk.Frame(results_canvas, bg='white')

        results_scrollable_frame.bind(
            "<Configure>",
            lambda e: results_canvas.configure(scrollregion=results_canvas.bbox("all"))
        )

        results_canvas.create_window((0, 0), window=results_scrollable_frame, anchor="nw")
        results_canvas.configure(yscrollcommand=results_scrollbar.set)

        # Display each customer as clickable result
        for i, customer in enumerate(customers):
            self.create_customer_result_item(results_scrollable_frame, customer, i)

        results_canvas.pack(side="left", fill="both", expand=True)
        results_scrollbar.pack(side="right", fill="y")

    def create_customer_result_item(self, parent, customer, index):
        """Create a clickable customer result item"""
        # Customer item frame
        item_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.RAISED, bd=1, cursor='hand2')
        item_frame.pack(fill=tk.X, padx=5, pady=2)

        # Customer info
        info_frame = tk.Frame(item_frame, bg='#f8f9fa')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)

        # Customer name and ID
        name_label = tk.Label(
            info_frame,
            text=f"👤 {customer['name']}",
            font=(self.font[0], self.font[1], 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        name_label.pack(anchor='w')

        id_label = tk.Label(
            info_frame,
            text=f"🆔 {customer['national_id']}",
            font=(self.font[0], self.font[1]-1),
            bg='#f8f9fa',
            fg='#6c757d'
        )
        id_label.pack(anchor='w')

        # Notes if available
        if customer.get('notes'):
            notes_label = tk.Label(
                info_frame,
                text=f"📝 {customer['notes'][:50]}{'...' if len(customer['notes']) > 50 else ''}",
                font=(self.font[0], self.font[1]-1),
                bg='#f8f9fa',
                fg='#6c757d'
            )
            notes_label.pack(anchor='w')

        # Select button
        select_btn = tk.Button(
            item_frame,
            text="✅ اختيار",
            command=lambda c=customer: self.select_customer(c),
            font=(self.font[0], self.font[1]-1, 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        select_btn.pack(side=tk.RIGHT, padx=15, pady=10)

        # Make the whole frame clickable
        def on_click(event, customer=customer):
            self.select_customer(customer)

        item_frame.bind('<Button-1>', on_click)
        for widget in item_frame.winfo_children():
            widget.bind('<Button-1>', on_click)
            for subwidget in widget.winfo_children():
                subwidget.bind('<Button-1>', on_click)

    def select_customer(self, customer):
        """Select a customer from search results"""
        self.selected_customer = customer
        self.update_customer_selection_display()
        
        # Clear search results
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()
        
        # Clear search box
        self.search_var.set('')

    def update_customer_selection_display(self):
        """Update the customer selection display"""
        if self.selected_customer:
            self.customer_info_label.config(
                text=f"✅ تم اختيار العميل: {self.selected_customer['name']}\nالرقم القومي: {self.selected_customer['national_id']}",
                bg='#d4edda',
                fg='#155724'
            )
            # Enable buttons - التأكد من وجود الأزرار
            try:
                self.save_btn.config(state='normal')
                self.add_selected_btn.config(state='normal')
            except AttributeError:
                # إذا لم يتم إنشاء الأزرار بعد، لا تفعل شيئاً
                pass
        else:
            self.customer_info_label.config(
                text="لم يتم اختيار عميل بعد",
                bg='#f8f9fa',
                fg='#6c757d'
            )
            # Disable buttons - التأكد من وجود الأزرار
            try:
                self.save_btn.config(state='disabled')
                self.add_selected_btn.config(state='disabled')
            except AttributeError:
                # إذا لم يتم إنشاء الأزرار بعد، لا تفعل شيئاً
                pass
        
        # التأكد من بقاء الأزرار مرئية
        try:
            self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
            self.button_frame.lift()  # رفع الأزرار للمقدمة
        except AttributeError:
            pass

    def create_new_customer(self):
        """Create new customer with manual input"""
        # Create dialog for new customer
        new_customer_dialog = tk.Toplevel(self.dialog)
        new_customer_dialog.title("إضافة عميل جديد")
        new_customer_dialog.geometry("450x250")
        new_customer_dialog.configure(bg='white')
        new_customer_dialog.grab_set()
        new_customer_dialog.transient(self.dialog)

        # Center dialog
        x = self.dialog.winfo_x() + 200
        y = self.dialog.winfo_y() + 150
        new_customer_dialog.geometry(f'+{x}+{y}')

        # Form
        form_frame = tk.Frame(new_customer_dialog, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

        # National ID
        tk.Label(form_frame, text="الرقم القومي:", font=(self.font[0], self.font[1], 'bold'), bg='white').pack(anchor='w')
        national_id_var = tk.StringVar()
        national_id_entry = tk.Entry(form_frame, textvariable=national_id_var, font=self.font, width=30)
        national_id_entry.pack(fill=tk.X, pady=(5, 15))
        national_id_entry.focus()

        # Name
        tk.Label(form_frame, text="اسم العميل:", font=(self.font[0], self.font[1], 'bold'), bg='white').pack(anchor='w')
        name_var = tk.StringVar()
        name_entry = tk.Entry(form_frame, textvariable=name_var, font=self.font, width=30)
        name_entry.pack(fill=tk.X, pady=(5, 15))

        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)

        def add_customer():
            national_id = national_id_var.get().strip()
            name = name_var.get().strip()

            if not national_id:
                messagebox.showerror("خطأ", "يرجى إدخال الرقم القومي")
                return

            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
                return

            if len(national_id) != 14 or not national_id.isdigit():
                messagebox.showerror("خطأ", "الرقم القومي يجب أن يكون 14 رقماً")
                return

            # Check if customer already exists
            try:
                existing = self.customer_manager.get_customer(national_id)
                if existing:
                    messagebox.showwarning("موجود مسبقاً", "هذا العميل موجود مسبقاً في النظام")
                    self.selected_customer = existing
                    self.update_customer_selection_display()
                    new_customer_dialog.destroy()
                    return
            except:
                pass

            try:
                # Add new customer
                self.customer_manager.add_customer(national_id, name)
                
                # Set as selected customer
                self.selected_customer = {
                    'national_id': national_id,
                    'name': name,
                    'notes': ''
                }
                
                self.update_customer_selection_display()
                messagebox.showinfo("نجح", "تم إضافة العميل الجديد بنجاح")
                new_customer_dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في إضافة العميل: {str(e)}")

        tk.Button(
            btn_frame,
            text="إضافة",
            command=add_customer,
            font=self.font,
            bg='#28a745',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="إلغاء",
            command=new_customer_dialog.destroy,
            font=self.font,
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

    def show_placeholder(self):
        """Show placeholder in results area"""
        placeholder = tk.Label(
            self.results_frame,
            text="📷 استخدم الأزرار أعلاه لاستخراج أرقام الهواتف من الصور\n\n💡 نصيحة: انسخ صورة إلى الحافظة واضغط Ctrl+V",
            font=self.font,
            bg='white',
            fg='#6c757d',
            justify=tk.CENTER
        )
        placeholder.pack(expand=True, pady=50)

    def setup_ocr_section(self, parent):
        """Setup OCR extraction section"""
        ocr_frame = tk.LabelFrame(
            parent,
            text="📷 استخراج الأرقام من الصور",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        ocr_frame.pack(fill=tk.X, pady=10)

        # OCR buttons
        ocr_buttons_frame = tk.Frame(ocr_frame, bg='white')
        ocr_buttons_frame.pack(fill=tk.X, padx=15, pady=15)

        clipboard_btn = tk.Button(
            ocr_buttons_frame,
            text="📋 استخراج من الحافظة",
            command=self.extract_from_clipboard,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#17a2b8',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2'
        )
        clipboard_btn.pack(side=tk.LEFT, padx=10)

        file_btn = tk.Button(
            ocr_buttons_frame,
            text="📁 استخراج من ملف",
            command=self.extract_from_file,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#6f42c1',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2'
        )
        file_btn.pack(side=tk.LEFT, padx=10)

        # Instructions
        instructions = tk.Label(
            ocr_frame,
            text="💡 نصيحة: انسخ صورة تحتوي على أرقام الهواتف إلى الحافظة واضغط Ctrl+V",
            font=(self.font[0], self.font[1]-1),
            bg='white',
            fg='#6c757d',
            wraplength=700
        )
        instructions.pack(padx=15, pady=(0, 15))

        # Bind Ctrl+V
        self.dialog.bind('<Control-v>', lambda e: self.extract_from_clipboard())
        self.dialog.focus_set()

    def setup_results_section(self, parent):
        """Setup results display section"""
        self.results_frame = tk.LabelFrame(
            parent,
            text="📱 الأرقام المستخرجة",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10, ipady=10)

        # Initially show placeholder
        self.show_placeholder()

    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        # إنشاء إطار الأزرار في الأسفل مع تثبيته
        self.button_frame = tk.Frame(parent, bg='white', height=80)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        self.button_frame.pack_propagate(False)  # منع تغيير الحجم

        # إطار داخلي للأزرار
        buttons_inner_frame = tk.Frame(self.button_frame, bg='white')
        buttons_inner_frame.pack(expand=True)

        self.save_btn = tk.Button(
            buttons_inner_frame,
            text="💾 حفظ الأرقام",
            command=self.save_phones,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2',
            state='disabled'
        )
        self.save_btn.pack(side=tk.LEFT, padx=10)

        # زرار إضافة الأرقام المحددة فقط
        self.add_selected_btn = tk.Button(
            buttons_inner_frame,
            text="➕ إضافة الأرقام المحددة",
            command=self.add_selected_phones,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#17a2b8',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2',
            state='disabled'
        )
        self.add_selected_btn.pack(side=tk.LEFT, padx=10)

        self.cancel_btn = tk.Button(
            buttons_inner_frame,
            text="❌ إلغاء",
            command=self.dialog.destroy,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=10)

    def add_selected_phones(self):
        """Add only the selected phone numbers without closing the dialog"""
        if not self.selected_customer or not self.extracted_phones:
            return

        selected_phones = []
        for phone_data in self.extracted_phones:
            if phone_data['selected_var'].get():
                selected_phones.append({
                    'phone_number': phone_data['phone_number'],
                    'carrier': phone_data['carrier'],
                    'has_wallet': phone_data['wallet_var'].get()
                })

        if not selected_phones:
            messagebox.showwarning("تحذير", "يرجى اختيار رقم واحد على الأقل")
            return

        success_count = 0
        errors = []

        for phone in selected_phones:
            try:
                self.customer_manager.add_phone_number(
                    self.selected_customer['national_id'],
                    phone['carrier'],
                    phone['phone_number'],
                    phone['has_wallet']
                )
                success_count += 1
            except Exception as e:
                errors.append(f"{phone['phone_number']}: {str(e)}")

        if success_count > 0:
            messagebox.showinfo("نجح", f"تمت إضافة {success_count} رقم بنجاح (بدون إغلاق النافذة)")

        if errors:
            error_msg = "\n".join(errors[:3])
            if len(errors) > 3:
                error_msg += f"\n... و {len(errors) - 3} أخطاء أخرى"
            messagebox.showerror("أخطاء", f"فشل في إضافة الأرقام التالية:\n{error_msg}")

    def extract_from_clipboard(self):
        """Extract phone numbers from clipboard"""
        if not self.selected_customer:
            messagebox.showwarning("تحذير", "يرجى اختيار العميل أولاً")
            return

        if not self.ocr_processor:
            messagebox.showerror("خطأ", "مكتبة OCR غير متوفرة. يرجى استخدام الإضافة اليدوية.")
            return

        try:
            # Show processing dialog
            processing = self.show_processing_dialog("جاري استخراج الأرقام من الحافظة...")

            # Extract from clipboard
            extracted_data = self.ocr_processor.extract_from_clipboard()

            processing.destroy()

            if extracted_data:
                self.display_extracted_phones(extracted_data)
            else:
                messagebox.showwarning("تحذير", "لم يتم العثور على صورة في الحافظة أو لم يتم استخراج أي أرقام")

        except Exception as e:
            try:
                if 'processing' in locals():
                    processing.destroy()
            except:
                pass
            messagebox.showerror("خطأ", f"فشل في استخراج الأرقام: {str(e)}")

    def extract_from_file(self):
        """Extract phone numbers from image file"""
        if not self.selected_customer:
            messagebox.showwarning("تحذير", "يرجى اختيار العميل أولاً")
            return

        if not self.ocr_processor:
            messagebox.showerror("خطأ", "مكتبة OCR غير متوفرة. يرجى استخدام الإضافة اليدوية.")
            return

        file_path = filedialog.askopenfilename(
            title="اختيار صورة",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                # Show processing dialog
                processing = self.show_processing_dialog("جاري استخراج الأرقام من الملف...")

                # Extract from file
                extracted_data = self.ocr_processor.extract_from_file(file_path)

                processing.destroy()

                if extracted_data:
                    self.display_extracted_phones(extracted_data)
                else:
                    messagebox.showwarning("تحذير", "لم يتم استخراج أي أرقام من الصورة")

            except Exception as e:
                try:
                    if 'processing' in locals():
                        processing.destroy()
                except:
                    pass
                messagebox.showerror("خطأ", f"فشل في استخراج الأرقام: {str(e)}")

    def show_processing_dialog(self, message):
        """Show processing dialog"""
        processing = tk.Toplevel(self.dialog)
        processing.title("جاري المعالجة...")
        processing.geometry("350x120")
        processing.configure(bg='white')
        processing.grab_set()
        processing.resizable(False, False)

        # Center on parent
        x = self.dialog.winfo_x() + (self.dialog.winfo_width() // 2) - 175
        y = self.dialog.winfo_y() + (self.dialog.winfo_height() // 2) - 60
        processing.geometry(f'+{x}+{y}')

        tk.Label(
            processing,
            text="🔄",
            font=('Arial', 24),
            bg='white',
            fg='#007bff'
        ).pack(pady=10)

        tk.Label(
            processing,
            text=message,
            font=self.font,
            bg='white',
            fg='#2c3e50'
        ).pack()

        processing.update()
        return processing

    def display_extracted_phones(self, extracted_data):
        """Display extracted phone numbers"""
        # Clear results frame
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        self.extracted_phones = extracted_data

        # Header
        header_frame = tk.Frame(self.results_frame, bg='white')
        header_frame.pack(fill=tk.X, padx=15, pady=15)

        tk.Label(
            header_frame,
            text=f"📱 تم استخراج {len(extracted_data)} رقم هاتف",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack()

        # Create a container for the scrollable area with fixed height
        scroll_container = tk.Frame(self.results_frame, bg='white')
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Scrollable area for phones with fixed height
        canvas = tk.Canvas(scroll_container, bg='white', height=300)  # Fixed height for better visibility
        scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create phone items
        for i, phone_data in enumerate(extracted_data):
            self.create_phone_item(scrollable_frame, phone_data, i)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable save button and ensure buttons are visible
        try:
            if self.selected_customer:
                self.save_btn.config(state='normal')
                self.add_selected_btn.config(state='normal')
            else:
                self.save_btn.config(state='disabled')
                self.add_selected_btn.config(state='disabled')
            
            # التأكد من بقاء الأزرار مرئية
            self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
            self.button_frame.lift()
        except AttributeError:
            pass

    def create_phone_item(self, parent, phone_data, index):
        """Create a phone number item in the results"""
        # Item frame
        item_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.RAISED, bd=1)
        item_frame.pack(fill=tk.X, padx=10, pady=5)

        # Selection checkbox
        phone_data['selected_var'] = tk.BooleanVar(value=True)
        checkbox = tk.Checkbutton(
            item_frame,
            variable=phone_data['selected_var'],
            bg='#f8f9fa'
        )
        checkbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Phone info
        info_frame = tk.Frame(item_frame, bg='#f8f9fa')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        # Phone number
        phone_label = tk.Label(
            info_frame,
            text=f"📱 {phone_data['phone_number']}",
            font=(self.font[0], self.font[1], 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        phone_label.pack(anchor='w')

        # Carrier with color
        carrier_colors = {
            'اورانج': '#FFC000',
            'فودافون': '#FF0000',
            'اتصالات': '#00B050',
            'وي': '#7030A0'
        }

        carrier_frame = tk.Frame(info_frame, bg='#f8f9fa')
        carrier_frame.pack(anchor='w', pady=(5, 0))

        carrier_label = tk.Label(
            carrier_frame,
            text=phone_data['carrier'],
            font=(self.font[0], self.font[1]-1, 'bold'),
            bg=carrier_colors.get(phone_data['carrier'], '#6c757d'),
            fg='white' if phone_data['carrier'] != 'اورانج' else 'black',
            padx=8,
            pady=2
        )
        carrier_label.pack(side=tk.LEFT)

        # Wallet checkbox
        phone_data['wallet_var'] = tk.BooleanVar(value=phone_data['has_wallet'])
        wallet_check = tk.Checkbutton(
            carrier_frame,
            text="💰 محفظة",
            variable=phone_data['wallet_var'],
            font=(self.font[0], self.font[1]-1),
            bg='#f8f9fa'
        )
        wallet_check.pack(side=tk.LEFT, padx=(10, 0))

    def save_phones(self):
        """Save selected phone numbers to customer"""
        if not self.selected_customer or not self.extracted_phones:
            return

        # Get selected phones
        selected_phones = []
        for phone_data in self.extracted_phones:
            if phone_data['selected_var'].get():
                selected_phones.append({
                    'phone_number': phone_data['phone_number'],
                    'carrier': phone_data['carrier'],
                    'has_wallet': phone_data['wallet_var'].get()
                })

        if not selected_phones:
            messagebox.showwarning("تحذير", "يرجى اختيار رقم واحد على الأقل")
            return

        # Add phones to customer
        success_count = 0
        errors = []

        for phone in selected_phones:
            try:
                self.customer_manager.add_phone_number(
                    self.selected_customer['national_id'],
                    phone['carrier'],
                    phone['phone_number'],
                    phone['has_wallet']
                )
                success_count += 1
            except Exception as e:
                errors.append(f"{phone['phone_number']}: {str(e)}")

        # Show results
        if success_count > 0:
            messagebox.showinfo("نجح", f"تم إضافة {success_count} رقم بنجاح!")

        if errors:
            error_msg = "\n".join(errors[:3])
            if len(errors) > 3:
                error_msg += f"\n... و {len(errors) - 3} أخطاء أخرى"
            messagebox.showerror("أخطاء", f"فشل في إضافة الأرقام التالية:\n{error_msg}")

        if success_count > 0:
            self.dialog.destroy()

class ModernCustomerDialog:
    def __init__(self, parent, title, font, customer_manager=None, customer=None, prefill_id=None):
        self.result = None
        self.font = font
        self.customer_manager = customer_manager
        self.extracted_phones = []

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.attributes("-fullscreen", True)
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        self.dialog.configure(bg='#f8f9fa')

        # Center the dialog
        self.dialog.transient(parent)
        self.center_window()

        # Setup the enhanced UI
        self.setup_enhanced_ui(title, customer, prefill_id)

        # Focus handling
        if not customer:
            self.national_id_entry.focus()
        else:
            self.name_entry.focus()

    def setup_enhanced_ui(self, title, customer, prefill_id):
        """Setup enhanced modern UI with OCR integration"""
        # Main container with proper layout
        main_container = tk.Frame(self.dialog, bg='#ffffff', relief=tk.RAISED, bd=2)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header section - fixed height
        header_frame = tk.Frame(main_container, bg='#4F81BD', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Title
        title_label = tk.Label(
            header_frame,
            text=title,
            font=(self.font[0], self.font[1]+6, 'bold'),
            bg='#4F81BD',
            fg='white',
            pady=25
        )
        title_label.pack()

        # Scrollable content area
        content_frame = tk.Frame(main_container, bg='#ffffff')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        # Create canvas and scrollbar for scrollable content
        canvas = tk.Canvas(content_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.scrollable_content = tk.Frame(canvas, bg='#ffffff')

        self.scrollable_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Form section inside scrollable content
        form_frame = tk.Frame(self.scrollable_content, bg='#ffffff')
        form_frame.pack(fill=tk.X, padx=40, pady=20)

        # National ID section
        self.create_form_field(
            form_frame, "الرقم القومي", "أدخل الرقم القومي (14 رقم)",
            customer['national_id'] if customer else (prefill_id or ''), 
            readonly=bool(customer), row=0
        )

        # Name section
        self.create_name_field(
            form_frame, "اسم العميل", "أدخل الاسم الكامل للعميل",
            customer['name'] if customer else '', row=1
        )

        # Notes section
        self.create_notes_field(
            form_frame, "ملاحظات", "أدخل أي ملاحظات إضافية هنا",
            customer['notes'] if customer else '', row=2
        )

        # OCR section for adding phones - inside scrollable content
        if not customer:  # Only show OCR for new customers
            self.setup_ocr_section(self.scrollable_content)

        # Phone numbers display - inside scrollable content
        self.setup_phones_display(self.scrollable_content)

        # Action buttons - OUTSIDE scrollable content, always visible at bottom
        self.create_action_buttons(main_container)

    def create_form_field(self, parent, label_text, placeholder, value, readonly=False, row=0):
        """Create a modern form field"""
        # Field container
        field_frame = tk.Frame(parent, bg='#ffffff')
        field_frame.pack(fill=tk.X, pady=15)

        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        )
        label.pack(anchor='w', pady=(0, 5))

        # Entry
        self.national_id_var = tk.StringVar(value=value)
        self.national_id_entry = tk.Entry(
            field_frame,
            textvariable=self.national_id_var,
            font=self.font,
            width=40,
            bd=2,
            relief=tk.GROOVE,
            bg='#f8f9fa' if readonly else '#ffffff',
            state='readonly' if readonly else 'normal'
        )
        self.national_id_entry.pack(fill=tk.X, pady=(0, 5))

        # Hint text
        hint_label = tk.Label(
            field_frame,
            text=placeholder,
            font=(self.font[0], self.font[1]-2),
            bg='#ffffff',
            fg='#6c757d'
        )
        hint_label.pack(anchor='w')

    def create_name_field(self, parent, label_text, placeholder, value, row=1):
        """Create name field"""
        # Field container
        field_frame = tk.Frame(parent, bg='#ffffff')
        field_frame.pack(fill=tk.X, pady=15)

        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        )
        label.pack(anchor='w', pady=(0, 5))

        # Entry
        self.name_var = tk.StringVar(value=value)
        self.name_entry = tk.Entry(
            field_frame,
            textvariable=self.name_var,
            font=self.font,
            width=40,
            bd=2,
            relief=tk.GROOVE
        )
        self.name_entry.pack(fill=tk.X, pady=(0, 5))

        # Hint text
        hint_label = tk.Label(
            field_frame,
            text=placeholder,
            font=(self.font[0], self.font[1]-2),
            bg='#ffffff',
            fg='#6c757d'
        )
        hint_label.pack(anchor='w')

    def create_notes_field(self, parent, label_text, placeholder, value, row=2):
        """Create notes field with text widget"""
        # Field container
        field_frame = tk.Frame(parent, bg='#ffffff')
        field_frame.pack(fill=tk.X, pady=15)

        # Label
        label = tk.Label(
            field_frame,
            text=label_text,
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='#ffffff',
            fg='#2c3e50'
        )
        label.pack(anchor='w', pady=(0, 5))

        # Text widget for notes
        self.notes_text = tk.Text(
            field_frame,
            height=4,
            width=40,
            font=self.font,
            bd=2,
            relief=tk.GROOVE,
            wrap=tk.WORD
        )
        self.notes_text.pack(fill=tk.X, pady=(0, 5))

        # Insert existing notes if any
        if value:
            self.notes_text.insert(tk.END, value)

        # Hint text
        hint_label = tk.Label(
            field_frame,
            text=placeholder,
            font=(self.font[0], self.font[1]-2),
            bg='#ffffff',
            fg='#6c757d'
        )
        hint_label.pack(anchor='w')

    def setup_ocr_section(self, parent):
        """Setup OCR section for adding phone numbers"""
        ocr_frame = tk.LabelFrame(
            parent,
            text="📱 إضافة أرقام الهواتف",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='#ffffff',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        ocr_frame.pack(fill=tk.X, padx=40, pady=20)

        # OCR buttons
        ocr_buttons_frame = tk.Frame(ocr_frame, bg='#ffffff')
        ocr_buttons_frame.pack(fill=tk.X, padx=15, pady=15)

        clipboard_btn = tk.Button(
            ocr_buttons_frame,
            text="📋 استخراج من الحافظة",
            command=self.extract_from_clipboard,
            font=(self.font[0], self.font[1]-1, 'bold'),
            bg='#17a2b8',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        clipboard_btn.pack(side=tk.LEFT, padx=5)

        file_btn = tk.Button(
            ocr_buttons_frame,
            text="📁 استخراج من ملف",
            command=self.extract_from_file,
            font=(self.font[0], self.font[1]-1, 'bold'),
            bg='#6f42c1',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        file_btn.pack(side=tk.LEFT, padx=5)

        manual_btn = tk.Button(
            ocr_buttons_frame,
            text="✏️ إضافة يدوية",
            command=self.add_manual_phone,
            font=(self.font[0], self.font[1]-1, 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        manual_btn.pack(side=tk.LEFT, padx=5)

        # Initialize OCR processor
        self.ocr_processor = EnhancedOCRProcessor()

        # Bind Ctrl+V
        self.dialog.bind('<Control-v>', lambda e: self.extract_from_clipboard())

    def setup_phones_display(self, parent):
        """Setup phone numbers display area"""
        self.phones_frame = tk.LabelFrame(
            parent,
            text="📞 أرقام الهواتف المضافة",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='#ffffff',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        self.phones_frame.pack(fill=tk.X, padx=40, pady=20)

        # Placeholder
        self.show_phones_placeholder()

    def show_phones_placeholder(self):
        """Show placeholder in phones area"""
        for widget in self.phones_frame.winfo_children():
            widget.destroy()

        placeholder = tk.Label(
            self.phones_frame,
            text="📱 لم يتم إضافة أي أرقام بعد\nاستخدم الأزرار أعلاه لإضافة أرقام الهواتف",
            font=self.font,
            bg='#ffffff',
            fg='#6c757d',
            justify=tk.CENTER
        )
        placeholder.pack(expand=True, pady=30)

    def extract_from_clipboard(self):
        """Extract phones from clipboard"""
        if not self.ocr_processor:
            messagebox.showerror("خطأ", "مكتبة OCR غير متوفرة")
            return
            
        try:
            extracted_data = self.ocr_processor.extract_from_clipboard()

            if extracted_data:
                self.add_extracted_phones(extracted_data)
                messagebox.showinfo("نجح", f"تم استخراج {len(extracted_data)} رقم من الحافظة!")
            else:
                messagebox.showwarning("تحذير", "لم يتم العثور على صورة في الحافظة أو لم يتم استخراج أي أرقام")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في استخراج الأرقام: {str(e)}")

    def extract_from_file(self):
        """Extract phones from image file"""
        if not self.ocr_processor:
            messagebox.showerror("خطأ", "مكتبة OCR غير متوفرة")
            return
            
        file_path = filedialog.askopenfilename(
            title="اختيار صورة",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                extracted_data = self.ocr_processor.extract_from_file(file_path)

                if extracted_data:
                    self.add_extracted_phones(extracted_data)
                    messagebox.showinfo("نجح", f"تم استخراج {len(extracted_data)} رقم من الملف!")
                else:
                    messagebox.showwarning("تحذير", "لم يتم استخراج أي أرقام من الصورة")

            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في استخراج الأرقام: {str(e)}")

    def add_manual_phone(self):
        """Add phone number manually"""
        # Create simple dialog for manual entry
        manual_dialog = tk.Toplevel(self.dialog)
        manual_dialog.title("إضافة رقم يدوياً")
        manual_dialog.geometry("400x300")
        manual_dialog.configure(bg='white')
        manual_dialog.grab_set()
        manual_dialog.transient(self.dialog)

        # Center dialog
        x = self.dialog.winfo_x() + 150
        y = self.dialog.winfo_y() + 200
        manual_dialog.geometry(f'+{x}+{y}')

        # Form
        form_frame = tk.Frame(manual_dialog, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Phone number
        tk.Label(form_frame, text="رقم الهاتف:", font=self.font, bg='white').pack(anchor='w')
        phone_var = tk.StringVar()
        phone_entry = tk.Entry(form_frame, textvariable=phone_var, font=self.font, width=30)
        phone_entry.pack(fill=tk.X, pady=(5, 15))
        phone_entry.focus()

        # Carrier
        tk.Label(form_frame, text="الشبكة:", font=self.font, bg='white').pack(anchor='w')
        carrier_var = tk.StringVar(value='اورانج')
        carrier_combo = ttk.Combobox(
            form_frame,
            textvariable=carrier_var,
            values=['اورانج', 'فودافون', 'اتصالات', 'وي'],
            state='readonly',
            font=self.font
        )
        carrier_combo.pack(fill=tk.X, pady=(5, 15))

        # Wallet
        wallet_var = tk.BooleanVar()
        wallet_check = tk.Checkbutton(
            form_frame,
            text="يحتوي على محفظة",
            variable=wallet_var,
            font=self.font,
            bg='white'
        )
        wallet_check.pack(anchor='w', pady=10)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)

        def add_phone():
            phone = phone_var.get().strip()
            if not phone:
                messagebox.showerror("خطأ", "يرجى إدخال رقم الهاتف")
                return

            # Simple validation for Egyptian phone numbers
            if not phone.isdigit() or len(phone) != 11:
                messagebox.showerror("خطأ", "رقم الهاتف يجب أن يكون 11 رقم")
                return
            
            # Check Egyptian mobile prefixes
            valid_prefixes = ['010', '011', '012', '015']
            if phone[:3] not in valid_prefixes:
                messagebox.showerror("خطأ", "رقم الهاتف يجب أن يبدأ بـ 010، 011، 012، أو 015")
                return

            # Add phone
            phone_data = {
                'phone_number': phone,
                'carrier': carrier_var.get(),
                'has_wallet': wallet_var.get()
            }

            self.add_extracted_phones([phone_data])
            manual_dialog.destroy()

        tk.Button(
            btn_frame,
            text="إضافة",
            command=add_phone,
            font=self.font,
            bg='#28a745',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="إلغاء",
            command=manual_dialog.destroy,
            font=self.font,
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

    def add_extracted_phones(self, extracted_data):
        """Add extracted phone numbers to the list"""
        self.extracted_phones.extend(extracted_data)
        self.display_phones()

    def display_phones(self):
        """Display added phone numbers"""
        # Clear phones frame
        for widget in self.phones_frame.winfo_children():
            widget.destroy()

        if not self.extracted_phones:
            self.show_phones_placeholder()
            return

        # Create phones display area with limited height
        phones_container = tk.Frame(self.phones_frame, bg='white')
        phones_container.pack(fill=tk.X, padx=15, pady=15)

        # Display each phone in a compact way
        for i, phone_data in enumerate(self.extracted_phones):
            self.create_phone_display_item(phones_container, phone_data, i)

        # Update the main dialog's scroll region
        self.dialog.update_idletasks()
        try:
            # Find the main canvas and update its scroll region
            for widget in self.dialog.winfo_children():
                if isinstance(widget, tk.Frame):
                    for subwidget in widget.winfo_children():
                        if isinstance(subwidget, tk.Frame):
                            for subsubwidget in subwidget.winfo_children():
                                if isinstance(subsubwidget, tk.Canvas):
                                    subsubwidget.configure(scrollregion=subsubwidget.bbox("all"))
                                    break
        except:
            pass

    def create_phone_display_item(self, parent, phone_data, index):
        """Create display item for phone number"""
        item_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.RAISED, bd=1)
        item_frame.pack(fill=tk.X, padx=5, pady=3)

        # Phone info
        info_frame = tk.Frame(item_frame, bg='#f8f9fa')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)

        # Phone number and carrier
        phone_label = tk.Label(
            info_frame,
            text=f"📱 {phone_data['phone_number']} ({phone_data['carrier']})",
            font=(self.font[0], self.font[1], 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        phone_label.pack(anchor='w')

        # Wallet status
        if phone_data['has_wallet']:
            wallet_label = tk.Label(
                info_frame,
                text="💰 يحتوي على محفظة",
                font=(self.font[0], self.font[1]-1),
                bg='#f8f9fa',
                fg='#28a745'
            )
            wallet_label.pack(anchor='w')

        # Remove button
        remove_btn = tk.Button(
            item_frame,
            text="❌",
            command=lambda idx=index: self.remove_phone(idx),
            font=(self.font[0], self.font[1]-2),
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=8,
            pady=4,
            cursor='hand2'
        )
        remove_btn.pack(side=tk.RIGHT, padx=10, pady=8)

    def remove_phone(self, index):
        """Remove phone number at index"""
        if 0 <= index < len(self.extracted_phones):
            del self.extracted_phones[index]
            self.display_phones()

    def create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = tk.Frame(parent, bg='#ffffff')
        button_frame.pack(fill=tk.X, padx=40, pady=20)

        save_btn = tk.Button(
            button_frame,
            text="💾 حفظ العميل والأرقام",
            command=self.save_customer,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        save_btn.pack(side=tk.LEFT, padx=10)

        cancel_btn = tk.Button(
            button_frame,
            text="❌ إلغاء",
            command=self.dialog.destroy,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        cancel_btn.pack(side=tk.LEFT, padx=10)

    def center_window(self):
        """Center the dialog window"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 350
        y = (self.dialog.winfo_screenheight() // 2) - 350
        self.dialog.geometry(f'+{x}+{y}')

    def save_customer(self):
        """Save customer with phone numbers"""
        national_id = self.national_id_var.get().strip()
        name = self.name_var.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not national_id:
            messagebox.showerror("خطأ", "يرجى إدخال الرقم القومي")
            return

        if not name:
            messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
            return

        if len(national_id) != 14 or not national_id.isdigit():
            messagebox.showerror("خطأ", "الرقم القومي يجب أن يكون 14 رقماً")
            return

        self.result = {
            'national_id': national_id,
            'name': name,
            'notes': notes,
            'phone_numbers': self.extracted_phones
        }

        self.dialog.destroy()

class PhoneManagementDialog:
    """Enhanced phone management with OCR support"""
    def __init__(self, parent, customer, customer_manager, font):
        self.customer = customer
        self.customer_manager = customer_manager
        self.font = font

        # Create dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"إدارة العميل: {customer['name']}")
        self.dialog.geometry("1000x800")
        self.dialog.resizable(True, True)
        self.dialog.configure(bg='white')
        self.dialog.grab_set()
        self.dialog.transient(parent)

        # Center dialog
        self.center_dialog(parent)

        # Setup UI
        self.setup_ui()

        # Load customer phones
        self.load_customer_phones()

        # Initialize OCR
        try:
            from ocr_processor import EnhancedOCRProcessor
            self.ocr_processor = EnhancedOCRProcessor()
        except:
            self.ocr_processor = None

    def center_dialog(self, parent):
        """Center dialog on parent"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 450
        y = (self.dialog.winfo_screenheight() // 2) - 400
        self.dialog.geometry(f'+{x}+{y}')

    def setup_ui(self):
        """Setup user interface"""
        # Main container
        main_frame = tk.Frame(self.dialog, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Header
        self.setup_header(main_frame)

        # Customer edit section
        self.setup_customer_edit_section(main_frame)

        # OCR section
        self.setup_ocr_section(main_frame)

        # Phone management section
        self.setup_phone_management(main_frame)

        # Action buttons
        self.setup_action_buttons(main_frame)

    def setup_header(self, parent):
        """Setup header section"""
        header_frame = tk.Frame(parent, bg='#4F81BD', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)

        # Customer info
        customer_label = tk.Label(
            header_frame,
            text=f"🧑‍💼 إدارة العميل: {self.customer['name']} - الرقم القومي: {self.customer['national_id']}",
            font=(self.font[0], self.font[1]+2, 'bold'),
            bg='#4F81BD',
            fg='white',
            pady=25
        )
        customer_label.pack()

    def setup_customer_edit_section(self, parent):
        """Setup customer information editing section"""
        edit_frame = tk.LabelFrame(
            parent,
            text="✏️ تعديل بيانات العميل",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        edit_frame.pack(fill=tk.X, pady=10)

        # Customer name
        name_frame = tk.Frame(edit_frame, bg='white')
        name_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(
            name_frame,
            text="اسم العميل:",
            font=(self.font[0], self.font[1], 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side=tk.RIGHT, padx=(10, 0))

        self.customer_name_var = tk.StringVar(value=self.customer['name'])
        self.customer_name_entry = tk.Entry(
            name_frame,
            textvariable=self.customer_name_var,
            font=self.font,
            width=30,
            bd=2,
            relief=tk.GROOVE
        )
        self.customer_name_entry.pack(side=tk.RIGHT, padx=(0, 10))

        # Customer notes
        notes_frame = tk.Frame(edit_frame, bg='white')
        notes_frame.pack(fill=tk.X, padx=15, pady=10)

        tk.Label(
            notes_frame,
            text="ملاحظات:",
            font=(self.font[0], self.font[1], 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(anchor='w')

        self.customer_notes_text = tk.Text(
            notes_frame,
            height=3,
            font=self.font,
            bd=2,
            relief=tk.GROOVE,
            wrap=tk.WORD
        )
        self.customer_notes_text.pack(fill=tk.X, pady=(5, 0))

        # Insert current notes
        if self.customer.get('notes'):
            self.customer_notes_text.insert(tk.END, self.customer['notes'])

        # Update button
        update_btn = tk.Button(
            edit_frame,
            text="💾 حفظ التعديلات",
            command=self.update_customer_info,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        update_btn.pack(padx=15, pady=(0, 15))

    def setup_ocr_section(self, parent):
        """Setup OCR section"""
        ocr_frame = tk.LabelFrame(
            parent,
            text="📱 إضافة أرقام جديدة",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        ocr_frame.pack(fill=tk.X, pady=10)

        # OCR buttons
        ocr_buttons_frame = tk.Frame(ocr_frame, bg='white')
        ocr_buttons_frame.pack(fill=tk.X, padx=15, pady=15)

        clipboard_btn = tk.Button(
            ocr_buttons_frame,
            text="📋 استخراج من الحافظة",
            command=self.extract_from_clipboard,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#17a2b8',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2'
        )
        clipboard_btn.pack(side=tk.LEFT, padx=10)

        file_btn = tk.Button(
            ocr_buttons_frame,
            text="📁 استخراج من ملف",
            command=self.extract_from_file,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#6f42c1',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2'
        )
        file_btn.pack(side=tk.LEFT, padx=10)

        manual_btn = tk.Button(
            ocr_buttons_frame,
            text="✏️ إضافة يدوية",
            command=self.add_manual_phone,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#28a745',
            fg='white',
            bd=0,
            padx=25,
            pady=10,
            cursor='hand2'
        )
        manual_btn.pack(side=tk.LEFT, padx=10)

        # Bind Ctrl+V
        self.dialog.bind('<Control-v>', lambda e: self.extract_from_clipboard())
        self.dialog.focus_set()

    def setup_phone_management(self, parent):
        """Setup phone management section"""
        self.phones_frame = tk.LabelFrame(
            parent,
            text="📞 أرقام الهواتف الحالية",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg='white',
            fg='#2c3e50',
            bd=2,
            relief=tk.GROOVE
        )
        self.phones_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def setup_action_buttons(self, parent):
        """Setup action buttons"""
        button_frame = tk.Frame(parent, bg='white')
        button_frame.pack(fill=tk.X, pady=20)

        close_btn = tk.Button(
            button_frame,
            text="✅ إغلاق",
            command=self.dialog.destroy,
            font=(self.font[0], self.font[1], 'bold'),
            bg='#007bff',
            fg='white',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        close_btn.pack(side=tk.RIGHT, padx=10)

    def load_customer_phones(self):
        """Load and display customer phone numbers"""
        try:
            phones = self.customer_manager.get_customer_phone_numbers(self.customer['national_id'])
            self.display_phones(phones)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحميل أرقام العميل: {str(e)}")

    def display_phones(self, phones):
        """Display phone numbers"""
        # Clear phones frame
        for widget in self.phones_frame.winfo_children():
            widget.destroy()

        if not phones:
            # Show placeholder
            placeholder = tk.Label(
                self.phones_frame,
                text="📱 لا توجد أرقام هواتف مسجلة لهذا العميل\nاستخدم الأزرار أعلاه لإضافة أرقام جديدة",
                font=self.font,
                bg='white',
                fg='#6c757d',
                justify=tk.CENTER
            )
            placeholder.pack(expand=False, pady=50)
            return

        # Create scrollable area
        canvas = tk.Canvas(self.phones_frame, bg='white')
        scrollbar = ttk.Scrollbar(self.phones_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display phones by carrier
        carriers = ['اورانج', 'فودافون', 'اتصالات', 'وي']
        carrier_colors = {
            'اورانج': '#FFC000',
            'فودافون': '#FF0000',
            'اتصالات': '#00B050',
            'وي': '#7030A0'
        }

        for carrier in carriers:
            carrier_phones = [p for p in phones if p['carrier'] == carrier]
            if carrier_phones:
                self.create_carrier_section(scrollable_frame, carrier, carrier_phones, carrier_colors[carrier])

        canvas.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=15)

    def create_carrier_section(self, parent, carrier, phones, color):
        """Create section for carrier phones"""
        # Carrier header
        carrier_frame = tk.Frame(parent, bg=color, height=40)
        carrier_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        carrier_frame.pack_propagate(False)

        carrier_label = tk.Label(
            carrier_frame,
            text=f"{carrier} ({len(phones)} رقم)",
            font=(self.font[0], self.font[1]+1, 'bold'),
            bg=color,
            fg='white' if carrier != 'اورانج' else 'black',
            pady=10
        )
        carrier_label.pack()

        # Phone numbers
        for phone in phones:
            self.create_phone_item(parent, phone, color)

    def create_phone_item(self, parent, phone, carrier_color):
        """Create phone number item"""
        item_frame = tk.Frame(parent, bg='#f8f9fa', relief=tk.RAISED, bd=1)
        item_frame.pack(fill=tk.X, padx=10, pady=2)

        # Phone info
        info_frame = tk.Frame(item_frame, bg='#f8f9fa')
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=15, pady=10)

        # Phone number
        phone_label = tk.Label(
            info_frame,
            text=f"📱 {phone['phone_number']}",
            font=(self.font[0], self.font[1], 'bold'),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        phone_label.pack(anchor='w')

        # Wallet status with toggle
        wallet_frame = tk.Frame(info_frame, bg='#f8f9fa')
        wallet_frame.pack(anchor='w', pady=(5, 0))

        wallet_var = tk.BooleanVar(value=phone['has_wallet'])
        wallet_check = tk.Checkbutton(
            wallet_frame,
            text="💰 محفظة",
            variable=wallet_var,
            font=(self.font[0], self.font[1]-1),
            bg='#f8f9fa',
            command=lambda p_id=phone['id'], var=wallet_var: self.toggle_wallet(p_id, var)
        )
        wallet_check.pack(side=tk.LEFT)

        # Delete button
        delete_btn = tk.Button(
            item_frame,
            text="🗑️ حذف",
            command=lambda p_id=phone['id']: self.delete_phone(p_id),
            font=(self.font[0], self.font[1]-1, 'bold'),
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        delete_btn.pack(side=tk.RIGHT, padx=15, pady=10)

    def toggle_wallet(self, phone_id, wallet_var):
        """Toggle wallet status for phone"""
        try:
            self.customer_manager.update_phone_wallet_status(phone_id, wallet_var.get())
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحديث حالة المحفظة: {str(e)}")
            # Revert the checkbox
            wallet_var.set(not wallet_var.get())

    def delete_phone(self, phone_id):
        """Delete phone number"""
        if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا الرقم؟"):
            try:
                self.customer_manager.delete_phone_number(phone_id)
                self.load_customer_phones()  # Refresh display
                messagebox.showinfo("نجح", "تم حذف الرقم بنجاح")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في حذف الرقم: {str(e)}")

    def extract_from_clipboard(self):
        """Extract phones from clipboard"""
        try:
            extracted_data = self.ocr_processor.extract_from_clipboard()

            if extracted_data:
                self.process_extracted_phones(extracted_data)
            else:
                messagebox.showwarning("تحذير", "لم يتم العثور على صورة في الحافظة أو لم يتم استخراج أي أرقام")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في استخراج الأرقام: {str(e)}")

    def extract_from_file(self):
        """Extract phones from image file"""
        file_path = filedialog.askopenfilename(
            title="اختيار صورة",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            try:
                extracted_data = self.ocr_processor.extract_from_file(file_path)

                if extracted_data:
                    self.process_extracted_phones(extracted_data)
                else:
                    messagebox.showwarning("تحذير", "لم يتم استخراج أي أرقام من الصورة")

            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في استخراج الأرقام: {str(e)}")

    def add_manual_phone(self):
        """Add phone manually"""
        # Similar to the one in ModernCustomerDialog
        manual_dialog = tk.Toplevel(self.dialog)
        manual_dialog.title("إضافة رقم يدوياً")
        manual_dialog.geometry("400x300")
        manual_dialog.configure(bg='white')
        manual_dialog.grab_set()
        manual_dialog.transient(self.dialog)

        # Center dialog
        x = self.dialog.winfo_x() + 250
        y = self.dialog.winfo_y() + 250
        manual_dialog.geometry(f'+{x}+{y}')

        # Form
        form_frame = tk.Frame(manual_dialog, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Phone number
        tk.Label(form_frame, text="رقم الهاتف:", font=self.font, bg='white').pack(anchor='w')
        phone_var = tk.StringVar()
        phone_entry = tk.Entry(form_frame, textvariable=phone_var, font=self.font, width=30)
        phone_entry.pack(fill=tk.X, pady=(5, 15))
        phone_entry.focus()

        # Carrier
        tk.Label(form_frame, text="الشبكة:", font=self.font, bg='white').pack(anchor='w')
        carrier_var = tk.StringVar(value='اورانج')
        carrier_combo = ttk.Combobox(
            form_frame,
            textvariable=carrier_var,
            values=['اورانج', 'فودafون', 'اتصالات', 'وي'],
            state='readonly',
            font=self.font
        )
        carrier_combo.pack(fill=tk.X, pady=(5, 15))

        # Wallet
        wallet_var = tk.BooleanVar()
        wallet_check = tk.Checkbutton(
            form_frame,
            text="يحتوي على محفظة",
            variable=wallet_var,
            font=self.font,
            bg='white'
        )
        wallet_check.pack(anchor='w', pady=10)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.pack(fill=tk.X, pady=20)

        def add_phone():
            phone = phone_var.get().strip()
            if not phone:
                messagebox.showerror("خطأ", "يرجى إدخال رقم الهاتف")
                return

            if not self.ocr_processor.validate_egyptian_phone(phone):
                messagebox.showerror("خطأ", "رقم الهاتف غير صحيح")
                return

            try:
                self.customer_manager.add_phone_number(
                    self.customer['national_id'],
                    carrier_var.get(),
                    phone,
                    wallet_var.get()
                )
                messagebox.showinfo("نجح", "تم إضافة الرقم بنجاح")
                manual_dialog.destroy()
                self.load_customer_phones()  # Refresh display
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في إضافة الرقم: {str(e)}")

        tk.Button(
            btn_frame,
            text="إضافة",
            command=add_phone,
            font=self.font,
            bg='#28a745',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="إلغاء",
            command=manual_dialog.destroy,
            font=self.font,
            bg='#dc3545',
            fg='white',
            bd=0,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=5)

    def update_customer_info(self):
        """Update customer information"""
        try:
            new_name = self.customer_name_var.get().strip()
            new_notes = self.customer_notes_text.get("1.0", tk.END).strip()

            if not new_name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم العميل")
                return

            # Update customer
            self.customer_manager.update_customer(
                self.customer['national_id'], 
                new_name, 
                new_notes
            )

            # Update local customer data
            self.customer['name'] = new_name
            self.customer['notes'] = new_notes

            messagebox.showinfo("نجح", "تم تحديث بيانات العميل بنجاح")

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحديث البيانات: {str(e)}")

    def process_extracted_phones(self, extracted_data):
        """Process and add extracted phone numbers"""
        if not extracted_data:
            return

        success_count = 0
        errors = []

        for phone_data in extracted_data:
            try:
                self.customer_manager.add_phone_number(
                    self.customer['national_id'],
                    phone_data['carrier'],
                    phone_data['phone_number'],
                    phone_data['has_wallet']
                )
                success_count += 1
            except Exception as e:
                errors.append(f"{phone_data['phone_number']}: {str(e)}")

        # Show results
        if success_count > 0:
            messagebox.showinfo("نجح", f"تم إضافة {success_count} رقم بنجاح!")
            self.load_customer_phones()  # Refresh display

        if errors:
            error_msg = "\n".join(errors[:3])
            if len(errors) > 3:
                error_msg += f"\n... و {len(errors) - 3} أخطاء أخرى"
            messagebox.showerror("أخطاء", f"فشل في إضافة الأرقام التالية:\n{error_msg}")

# Legacy compatibility classes
class EnhancedOCRDialog(SmartOCRDialog):
    """Legacy compatibility"""
    pass