import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QGridLayout, QSplitter, QStackedWidget,
                            QLabel, QPushButton, QLineEdit, QTextEdit, QTableWidget,
                            QTableWidgetItem, QComboBox, QSpinBox, QDoubleSpinBox,
                            QCheckBox, QGroupBox, QTabWidget, QScrollArea,
                            QFrame, QSizePolicy, QMessageBox, QFileDialog,
                            QProgressBar, QStatusBar, QMenuBar, QToolBar, QAction, QDialog)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db import DatabaseManager
from logic.gst_calculator import GSTCalculator
from logic.pdf_generator import PDFGenerator
from logic.qr_generator import QRCodeGenerator

class InvoiceMakerApp(QMainWindow):
    """Main Application Window"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.pdf_generator = PDFGenerator()
        self.qr_generator = QRCodeGenerator()
        self.current_invoice_items = []
        self.current_customer_id = None
        
        self.init_ui()
        self.load_initial_data()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("🧾 Invoice Maker - Professional Billing System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set application style - Clean Modern Design
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
                color: #2c3e50;
            }
            QGroupBox {
                font-weight: 600;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background: #ffffff;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                background: #ffffff;
                color: #3498db;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 6px;
                font-weight: 600;
                font-size: 12px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton[class="primary"] {
                background-color: #27ae60;
            }
            QPushButton[class="primary"]:hover {
                background-color: #229954;
            }
            QPushButton[class="danger"] {
                background-color: #e74c3c;
            }
            QPushButton[class="danger"]:hover {
                background-color: #c0392b;
            }
            QTableWidget {
                gridline-color: #ecf0f1;
                background-color: #ffffff;
                alternate-background-color: #f8f9fa;
                border: 1px solid #e1e8ed;
                border-radius: 6px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTableWidget::header {
                background-color: #f8f9fa;
                border: none;
                border-bottom: 2px solid #3498db;
                font-weight: 600;
                color: #2c3e50;
                padding: 10px;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 8px;
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                background: white;
                color: #2c3e50;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
            QTabWidget::pane {
                border: 1px solid #e1e8ed;
                background: white;
                border-radius: 6px;
                top: -1px;
            }
            QTabBar::tab {
                background-color: #f8f9fa;
                padding: 10px 16px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: 600;
                color: #7f8c8d;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
                font-weight: 500;
            }
            QTextEdit {
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                background: white;
                padding: 8px;
                font-size: 12px;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
            QStatusBar {
                background-color: #f8f9fa;
                border-top: 1px solid #e1e8ed;
                color: #7f8c8d;
                font-weight: 500;
            }
            QMenuBar {
                background: white;
                border-bottom: 1px solid #e1e8ed;
                color: #2c3e50;
            }
            QMenuBar::item {
                padding: 8px 16px;
                background: transparent;
            }
            QMenuBar::item:selected {
                background: #3498db;
                color: white;
            }
            QMenuBar::item:pressed {
                background: #2980b9;
            }
            QProgressBar {
                border: 2px solid #e1e8ed;
                border-radius: 6px;
                text-align: center;
                font-weight: 600;
                color: white;
            }
            QProgressBar::chunk {
                background: #27ae60;
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background: #f8f9fa;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #bdc3c7;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #95a5a6;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar, 1)
        
        # Create content area
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 4)
        
        # Create pages
        self.create_dashboard_page()
        self.create_invoice_page()
        self.create_customers_page()
        self.create_products_page()
        self.create_reports_page()
        self.create_settings_page()
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_sidebar(self):
        """Create navigation sidebar"""
        sidebar = QFrame()
        sidebar.setFixedWidth(260)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-right: 1px solid #2c3e50;
            }
            QPushButton {
                background-color: transparent;
                color: #ecf0f1;
                border: none;
                padding: 12px 18px;
                text-align: left;
                font-size: 13px;
                font-weight: 500;
                border-radius: 4px;
                margin: 2px 8px;
            }
            QPushButton:hover {
                background-color: #4a5f7a;
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: #2c3e50;
                color: #ffffff;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        
        # App title
        title = QLabel("🧾 Invoice Maker")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            padding: 20px;
            color: #ffffff;
            background-color: #2c3e50;
            border-radius: 6px;
            margin: 10px;
        """)
        layout.addWidget(title)
        
        # Navigation buttons
        nav_buttons = [
            ("📊 Dashboard", 0),
            ("📝 New Invoice", 1),
            ("👥 Customers", 2),
            ("📦 Products", 3),
            ("📈 Reports", 4),
            ("⚙️ Settings", 5)
        ]
        
        for text, index in nav_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, idx=index: self.content_stack.setCurrentIndex(idx))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Quick actions section
        quick_actions = QLabel("Quick Actions")
        quick_actions.setStyleSheet("""
            font-weight: bold; 
            padding: 12px;
            color: #3498db;
            font-size: 14px;
            background-color: rgba(52, 152, 219, 0.1);
            border-radius: 4px;
            margin: 8px;
        """)
        layout.addWidget(quick_actions)
        
        quick_invoice_btn = QPushButton("⚡ Quick Invoice")
        quick_invoice_btn.clicked.connect(self.quick_invoice)
        quick_invoice_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            font-weight: bold;
        """)
        layout.addWidget(quick_invoice_btn)
        
        backup_btn = QPushButton("💾 Backup Data")
        backup_btn.clicked.connect(self.backup_data)
        backup_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            font-weight: bold;
        """)
        layout.addWidget(backup_btn)
        
        return sidebar
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_invoice_action = QAction('New Invoice', self)
        new_invoice_action.setShortcut('Ctrl+N')
        new_invoice_action.triggered.connect(lambda: self.content_stack.setCurrentIndex(1))
        file_menu.addAction(new_invoice_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_dashboard_page(self):
        """Create dashboard page"""
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        
        # Welcome section
        welcome_label = QLabel("Welcome to Invoice Maker")
        welcome_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: bold; 
            color: #2c3e50;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 20px;
        """)
        layout.addWidget(welcome_label)
        
        # Stats grid
        stats_layout = QGridLayout()
        
        # Today's sales
        today_sales_group = QGroupBox("Today's Sales")
        today_sales_layout = QVBoxLayout()
        self.today_sales_label = QLabel("₹0.00")
        self.today_sales_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #27ae60;
        """)
        self.today_invoices_label = QLabel("0 Invoices")
        self.today_invoices_label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        today_sales_layout.addWidget(self.today_sales_label)
        today_sales_layout.addWidget(self.today_invoices_label)
        today_sales_group.setLayout(today_sales_layout)
        stats_layout.addWidget(today_sales_group, 0, 0)
        
        # Total customers
        customers_group = QGroupBox("Total Customers")
        customers_layout = QVBoxLayout()
        self.total_customers_label = QLabel("0")
        self.total_customers_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #3498db;
        """)
        customers_layout.addWidget(self.total_customers_label)
        customers_group.setLayout(customers_layout)
        stats_layout.addWidget(customers_group, 0, 1)
        
        # Total products
        products_group = QGroupBox("Total Products")
        products_layout = QVBoxLayout()
        self.total_products_label = QLabel("0")
        self.total_products_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #e74c3c;
        """)
        products_layout.addWidget(self.total_products_label)
        products_group.setLayout(products_layout)
        stats_layout.addWidget(products_group, 0, 2)
        
        # Low stock alert
        low_stock_group = QGroupBox("Low Stock Alert")
        low_stock_layout = QVBoxLayout()
        self.low_stock_label = QLabel("0 Items")
        self.low_stock_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #f39c12;
        """)
        low_stock_layout.addWidget(self.low_stock_label)
        low_stock_group.setLayout(low_stock_layout)
        stats_layout.addWidget(low_stock_group, 1, 0)
        
        # Recent invoices
        recent_group = QGroupBox("Recent Invoices")
        recent_layout = QVBoxLayout()
        self.recent_invoices_table = QTableWidget()
        self.recent_invoices_table.setColumnCount(4)
        self.recent_invoices_table.setHorizontalHeaderLabels(["Invoice No", "Customer", "Amount", "Date"])
        self.recent_invoices_table.setMaximumHeight(200)
        recent_layout.addWidget(self.recent_invoices_table)
        recent_group.setLayout(recent_layout)
        stats_layout.addWidget(recent_group, 1, 1, 1, 2)
        
        layout.addLayout(stats_layout)
        
        self.content_stack.addWidget(dashboard)
    
    def create_invoice_page(self):
        """Create invoice creation page"""
        invoice_page = QWidget()
        layout = QVBoxLayout(invoice_page)
        
        # Invoice form
        form_layout = QHBoxLayout()
        
        # Left side - Customer and items
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Customer selection
        customer_group = QGroupBox("Customer Details")
        customer_layout = QGridLayout()
        
        customer_layout.addWidget(QLabel("Customer:"), 0, 0)
        self.customer_combo = QComboBox()
        self.customer_combo.setEditable(True)
        self.customer_combo.currentTextChanged.connect(self.on_customer_changed)
        customer_layout.addWidget(self.customer_combo, 0, 1)
        
        self.add_customer_btn = QPushButton("+ Add New")
        self.add_customer_btn.clicked.connect(self.add_customer_dialog)
        customer_layout.addWidget(self.add_customer_btn, 0, 2)
        
        customer_layout.addWidget(QLabel("Phone:"), 1, 0)
        self.customer_phone_label = QLabel("-")
        customer_layout.addWidget(self.customer_phone_label, 1, 1)
        
        customer_layout.addWidget(QLabel("Address:"), 2, 0)
        self.customer_address_label = QLabel("-")
        customer_layout.addWidget(self.customer_address_label, 1, 1, 2, 2)
        
        customer_group.setLayout(customer_layout)
        left_layout.addWidget(customer_group)
        
        # Items table
        items_group = QGroupBox("Invoice Items")
        items_layout = QVBoxLayout()
        
        # Items table
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(7)
        self.items_table.setHorizontalHeaderLabels(["Product", "Qty", "Rate", "GST%", "Discount%", "Amount", "Actions"])
        # self.items_table.cellChanged.connect(self.on_item_changed)  # Removed as we use widget-based approach
        items_layout.addWidget(self.items_table)
        
        # Add item buttons
        item_buttons_layout = QHBoxLayout()
        
        self.add_item_btn = QPushButton("➕ Add Item")
        self.add_item_btn.clicked.connect(self.add_item_row)
        item_buttons_layout.addWidget(self.add_item_btn)
        
        self.clear_items_btn = QPushButton("🗑️ Clear All")
        self.clear_items_btn.clicked.connect(self.clear_items)
        item_buttons_layout.addWidget(self.clear_items_btn)
        
        item_buttons_layout.addStretch()
        items_layout.addLayout(item_buttons_layout)
        
        items_group.setLayout(items_layout)
        left_layout.addWidget(items_group)
        
        form_layout.addWidget(left_panel, 2)
        
        # Right side - Totals and actions
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Invoice details
        details_group = QGroupBox("Invoice Details")
        details_layout = QGridLayout()
        
        details_layout.addWidget(QLabel("Invoice No:"), 0, 0)
        self.invoice_number_label = QLabel("AUTO")
        details_layout.addWidget(self.invoice_number_label, 0, 1)
        
        details_layout.addWidget(QLabel("Date:"), 1, 0)
        self.invoice_date_label = QLabel("")
        details_layout.addWidget(self.invoice_date_label, 1, 1)
        
        details_layout.addWidget(QLabel("Payment Method:"), 2, 0)
        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems(["Cash", "Card", "UPI", "Net Banking", "Cheque"])
        details_layout.addWidget(self.payment_method_combo, 2, 1)
        
        details_group.setLayout(details_layout)
        right_layout.addWidget(details_group)
        
        # Totals
        totals_group = QGroupBox("Invoice Totals")
        totals_layout = QGridLayout()
        
        totals_layout.addWidget(QLabel("Subtotal:"), 0, 0)
        self.subtotal_label = QLabel("₹0.00")
        self.subtotal_label.setStyleSheet("font-weight: bold;")
        totals_layout.addWidget(self.subtotal_label, 0, 1)
        
        totals_layout.addWidget(QLabel("GST Amount:"), 1, 0)
        self.gst_amount_label = QLabel("₹0.00")
        totals_layout.addWidget(self.gst_amount_label, 1, 1)
        
        totals_layout.addWidget(QLabel("SGST:"), 2, 0)
        self.sgst_amount_label = QLabel("₹0.00")
        totals_layout.addWidget(self.sgst_amount_label, 2, 1)
        
        totals_layout.addWidget(QLabel("CGST:"), 3, 0)
        self.cgst_amount_label = QLabel("₹0.00")
        totals_layout.addWidget(self.cgst_amount_label, 3, 1)
        
        totals_layout.addWidget(QLabel("Grand Total:"), 4, 0)
        self.grand_total_label = QLabel("₹0.00")
        self.grand_total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
        totals_layout.addWidget(self.grand_total_label, 4, 1)
        
        totals_group.setLayout(totals_layout)
        right_layout.addWidget(totals_group)
        
        # Notes
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout()
        self.notes_text = QTextEdit()
        self.notes_text.setMaximumHeight(80)
        self.notes_text.setPlaceholderText("Add invoice notes here...")
        notes_layout.addWidget(self.notes_text)
        notes_group.setLayout(notes_layout)
        right_layout.addWidget(notes_group)
        
        # Action buttons
        actions_layout = QVBoxLayout()
        
        self.save_invoice_btn = QPushButton("💾 Save Invoice")
        self.save_invoice_btn.clicked.connect(self.save_invoice)
        actions_layout.addWidget(self.save_invoice_btn)
        
        self.generate_pdf_btn = QPushButton("📄 Generate PDF")
        self.generate_pdf_btn.clicked.connect(self.generate_invoice_pdf)
        actions_layout.addWidget(self.generate_pdf_btn)
        
        self.print_invoice_btn = QPushButton("🖨️ Print Invoice")
        self.print_invoice_btn.clicked.connect(self.print_invoice)
        actions_layout.addWidget(self.print_invoice_btn)
        
        right_layout.addLayout(actions_layout)
        right_layout.addStretch()
        
        form_layout.addWidget(right_panel, 1)
        
        layout.addLayout(form_layout)
        
        self.content_stack.addWidget(invoice_page)
    
    def create_customers_page(self):
        """Create customers management page"""
        customers_page = QWidget()
        layout = QVBoxLayout(customers_page)
        
        # Header with search
        header_layout = QHBoxLayout()
        
        search_label = QLabel("Search:")
        self.customer_search = QLineEdit()
        self.customer_search.setPlaceholderText("Search by name, phone, or email...")
        self.customer_search.textChanged.connect(self.load_customers)
        
        self.add_new_customer_btn = QPushButton("➕ Add New Customer")
        self.add_new_customer_btn.clicked.connect(self.add_customer_dialog)
        
        header_layout.addWidget(search_label)
        header_layout.addWidget(self.customer_search)
        header_layout.addWidget(self.add_new_customer_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Customers table
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(6)
        self.customers_table.setHorizontalHeaderLabels(["Name", "Phone", "Email", "GSTIN", "Address", "Actions"])
        layout.addWidget(self.customers_table)
        
        self.content_stack.addWidget(customers_page)
    
    def create_products_page(self):
        """Create products management page"""
        products_page = QWidget()
        layout = QVBoxLayout(products_page)
        
        # Header with search and add
        header_layout = QHBoxLayout()
        
        search_label = QLabel("Search:")
        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText("Search by name, barcode, or category...")
        self.product_search.textChanged.connect(self.load_products)
        
        category_filter = QComboBox()
        category_filter.addItems(["All Categories", "Electronics", "Groceries", "Clothing", "Other"])
        category_filter.currentTextChanged.connect(self.load_products)
        
        self.add_new_product_btn = QPushButton("➕ Add New Product")
        self.add_new_product_btn.clicked.connect(self.add_product_dialog)
        
        header_layout.addWidget(search_label)
        header_layout.addWidget(self.product_search)
        header_layout.addWidget(category_filter)
        header_layout.addWidget(self.add_new_product_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels(["Name", "Price", "GST%", "Stock", "Category", "Barcode", "Description", "Actions"])
        layout.addWidget(self.products_table)
        
        self.content_stack.addWidget(products_page)
    
    def create_reports_page(self):
        """Create reports and analytics page"""
        reports_page = QWidget()
        layout = QVBoxLayout(reports_page)
        
        # Report tabs
        reports_tabs = QTabWidget()
        
        # Sales summary tab
        sales_tab = QWidget()
        sales_layout = QVBoxLayout(sales_tab)
        
        # Date range
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("From:"))
        self.report_from_date = QLineEdit()
        self.report_from_date.setPlaceholderText("YYYY-MM-DD")
        date_layout.addWidget(self.report_from_date)
        
        date_layout.addWidget(QLabel("To:"))
        self.report_to_date = QLineEdit()
        self.report_to_date.setPlaceholderText("YYYY-MM-DD")
        date_layout.addWidget(self.report_to_date)
        
        self.generate_report_btn = QPushButton("Generate Report")
        self.generate_report_btn.clicked.connect(self.generate_sales_report)
        date_layout.addWidget(self.generate_report_btn)
        
        date_layout.addStretch()
        sales_layout.addLayout(date_layout)
        
        # Sales summary
        self.sales_summary_text = QTextEdit()
        self.sales_summary_text.setReadOnly(True)
        sales_layout.addWidget(self.sales_summary_text)
        
        reports_tabs.addTab(sales_tab, "Sales Summary")
        
        # Top products tab
        top_products_tab = QWidget()
        top_products_layout = QVBoxLayout(top_products_tab)
        
        self.top_products_table = QTableWidget()
        self.top_products_table.setColumnCount(3)
        self.top_products_table.setHorizontalHeaderLabels(["Product", "Quantity Sold", "Revenue"])
        top_products_layout.addWidget(self.top_products_table)
        
        reports_tabs.addTab(top_products_tab, "Top Products")
        
        # Top customers tab
        top_customers_tab = QWidget()
        top_customers_layout = QVBoxLayout(top_customers_tab)
        
        self.top_customers_table = QTableWidget()
        self.top_customers_table.setColumnCount(4)
        self.top_customers_table.setHorizontalHeaderLabels(["Customer", "Phone", "Invoices", "Total Spent"])
        top_customers_layout.addWidget(self.top_customers_table)
        
        reports_tabs.addTab(top_customers_tab, "Top Customers")
        
        layout.addWidget(reports_tabs)
        
        self.content_stack.addWidget(reports_page)
    
    def create_settings_page(self):
        """Create settings page"""
        settings_page = QWidget()
        layout = QVBoxLayout(settings_page)
        
        # Shop settings
        shop_group = QGroupBox("Shop Information")
        shop_layout = QGridLayout()
        
        shop_layout.addWidget(QLabel("Shop Name:"), 0, 0)
        self.shop_name_edit = QLineEdit()
        shop_layout.addWidget(self.shop_name_edit, 0, 1)
        
        shop_layout.addWidget(QLabel("Address:"), 1, 0)
        self.shop_address_edit = QLineEdit()
        shop_layout.addWidget(self.shop_address_edit, 1, 1)
        
        shop_layout.addWidget(QLabel("Phone:"), 2, 0)
        self.shop_phone_edit = QLineEdit()
        shop_layout.addWidget(self.shop_phone_edit, 2, 1)
        
        shop_layout.addWidget(QLabel("Email:"), 3, 0)
        self.shop_email_edit = QLineEdit()
        shop_layout.addWidget(self.shop_email_edit, 3, 1)
        
        shop_layout.addWidget(QLabel("GSTIN:"), 4, 0)
        self.shop_gstin_edit = QLineEdit()
        shop_layout.addWidget(self.shop_gstin_edit, 4, 1)
        
        shop_layout.addWidget(QLabel("UPI ID:"), 5, 0)
        self.shop_upi_edit = QLineEdit()
        self.shop_upi_edit.setPlaceholderText("shop@upi")
        shop_layout.addWidget(self.shop_upi_edit, 5, 1)
        
        shop_group.setLayout(shop_layout)
        layout.addWidget(shop_group)
        
        # Invoice settings
        invoice_group = QGroupBox("Invoice Settings")
        invoice_layout = QGridLayout()
        
        invoice_layout.addWidget(QLabel("Invoice Prefix:"), 0, 0)
        self.invoice_prefix_edit = QLineEdit()
        self.invoice_prefix_edit.setText("INV")
        invoice_layout.addWidget(self.invoice_prefix_edit, 0, 1)
        
        invoice_layout.addWidget(QLabel("Default GST (%):"), 1, 0)
        self.default_gst_spin = QSpinBox()
        self.default_gst_spin.setRange(0, 28)
        self.default_gst_spin.setValue(18)
        invoice_layout.addWidget(self.default_gst_spin, 1, 1)
        
        invoice_layout.addWidget(QLabel("Default Template:"), 2, 0)
        self.template_combo = QComboBox()
        self.template_combo.addItems(["template1 - Clean", "template2 - Modern", "template3 - Minimalist"])
        invoice_layout.addWidget(self.template_combo, 2, 1)
        
        invoice_group.setLayout(invoice_layout)
        layout.addWidget(invoice_group)
        
        # Logo upload
        logo_group = QGroupBox("Shop Logo")
        logo_layout = QHBoxLayout()
        
        self.logo_path_label = QLabel("No logo selected")
        self.select_logo_btn = QPushButton("Select Logo")
        self.select_logo_btn.clicked.connect(self.select_logo)
        
        logo_layout.addWidget(self.logo_path_label)
        logo_layout.addWidget(self.select_logo_btn)
        logo_layout.addStretch()
        
        logo_group.setLayout(logo_layout)
        layout.addWidget(logo_group)
        
        # Save button
        self.save_settings_btn = QPushButton("💾 Save Settings")
        self.save_settings_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_settings_btn)
        
        layout.addStretch()
        
        self.content_stack.addWidget(settings_page)
    
    def load_initial_data(self):
        """Load initial data into the application"""
        self.load_customers()
        self.load_products()
        self.load_dashboard_stats()
        self.load_shop_settings()
        self.update_invoice_number()
        
        # Set current date
        from datetime import datetime
        self.invoice_date_label.setText(datetime.now().strftime("%Y-%m-%d"))
    
    def load_dashboard_stats(self):
        """Load dashboard statistics"""
        # Today's sales
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        today_summary = self.db.get_sales_summary(today, today)
        
        self.today_sales_label.setText(f"₹{today_summary['total_sales']:.2f}")
        self.today_invoices_label.setText(f"{today_summary['total_invoices']} Invoices")
        
        # Total customers
        customers = self.db.get_customers()
        self.total_customers_label.setText(str(len(customers)))
        
        # Total products
        products = self.db.get_products()
        self.total_products_label.setText(str(len(products)))
        
        # Low stock items
        low_stock = self.db.get_low_stock_products()
        self.low_stock_label.setText(f"{len(low_stock)} Items")
        
        # Recent invoices
        recent_invoices = self.db.get_invoices(limit=10)
        self.recent_invoices_table.setRowCount(len(recent_invoices))
        
        for i, invoice in enumerate(recent_invoices):
            self.recent_invoices_table.setItem(i, 0, QTableWidgetItem(invoice['invoice_number']))
            self.recent_invoices_table.setItem(i, 1, QTableWidgetItem(invoice.get('customer_name', 'Walk-in')))
            self.recent_invoices_table.setItem(i, 2, QTableWidgetItem(f"₹{invoice['total_amount']:.2f}"))
            self.recent_invoices_table.setItem(i, 3, QTableWidgetItem(invoice['created_at'][:10]))
    
    def load_customers(self):
        """Load customers into table"""
        search_text = self.customer_search.text() if hasattr(self, 'customer_search') else ""
        customers = self.db.get_customers(search_text)
        
        self.customers_table.setRowCount(len(customers))
        
        for i, customer in enumerate(customers):
            self.customers_table.setItem(i, 0, QTableWidgetItem(customer['name']))
            self.customers_table.setItem(i, 1, QTableWidgetItem(customer.get('phone', '')))
            self.customers_table.setItem(i, 2, QTableWidgetItem(customer.get('email', '')))
            self.customers_table.setItem(i, 3, QTableWidgetItem(customer.get('gstin', '')))
            self.customers_table.setItem(i, 4, QTableWidgetItem(customer.get('address', '')))
            
            # Actions button
            actions_btn = QPushButton("Edit")
            actions_btn.clicked.connect(lambda checked, cid=customer['id']: self.edit_customer(cid))
            self.customers_table.setCellWidget(i, 5, actions_btn)
        
        # Update customer combo in invoice page
        if hasattr(self, 'customer_combo'):
            self.customer_combo.clear()
            self.customer_combo.addItem("Walk-in Customer")
            for customer in customers:
                self.customer_combo.addItem(customer['name'], customer['id'])
    
    def load_products(self):
        """Load products into table"""
        search_text = self.product_search.text() if hasattr(self, 'product_search') else ""
        products = self.db.get_products(search_text)
        
        self.products_table.setRowCount(len(products))
        
        for i, product in enumerate(products):
            self.products_table.setItem(i, 0, QTableWidgetItem(product['name']))
            self.products_table.setItem(i, 1, QTableWidgetItem(f"₹{product['price']:.2f}"))
            self.products_table.setItem(i, 2, QTableWidgetItem(f"{product['gst_percent']:.0f}%"))
            self.products_table.setItem(i, 3, QTableWidgetItem(str(product['stock_quantity'])))
            self.products_table.setItem(i, 4, QTableWidgetItem(product.get('category', '')))
            self.products_table.setItem(i, 5, QTableWidgetItem(product.get('barcode', '')))
            self.products_table.setItem(i, 6, QTableWidgetItem(product.get('description', '')))
            
            # Actions button
            actions_btn = QPushButton("Edit")
            actions_btn.clicked.connect(lambda checked, pid=product['id']: self.edit_product(pid))
            self.products_table.setCellWidget(i, 7, actions_btn)
    
    def load_shop_settings(self):
        """Load shop settings"""
        settings = self.db.get_shop_settings()
        
        if settings:
            self.shop_name_edit.setText(settings.get('shop_name', ''))
            self.shop_address_edit.setText(settings.get('address', ''))
            self.shop_phone_edit.setText(settings.get('phone', ''))
            self.shop_email_edit.setText(settings.get('email', ''))
            self.shop_gstin_edit.setText(settings.get('gstin', ''))
            self.shop_upi_edit.setText(settings.get('upi_id', ''))
            self.invoice_prefix_edit.setText(settings.get('invoice_prefix', 'INV'))
            self.default_gst_spin.setValue(int(settings.get('default_gst', 18)))
            
            template_name = settings.get('default_template', 'template1')
            template_index = 0
            if template_name == 'template2':
                template_index = 1
            elif template_name == 'template3':
                template_index = 2
            self.template_combo.setCurrentIndex(template_index)
            
            if settings.get('logo_path'):
                self.logo_path_label.setText(settings['logo_path'])
    
    def update_invoice_number(self):
        """Update invoice number"""
        invoice_number = self.db.generate_invoice_number()
        self.invoice_number_label.setText(invoice_number)
    
    def on_customer_changed(self, text):
        """Handle customer selection change"""
        current_data = self.customer_combo.currentData()
        if current_data:
            customer = self.db.get_customer(current_data)
            if customer:
                self.current_customer_id = customer['id']
                self.customer_phone_label.setText(customer.get('phone', ''))
                self.customer_address_label.setText(customer.get('address', ''))
        else:
            self.current_customer_id = None
            self.customer_phone_label.setText("")
            self.customer_address_label.setText("")
    
    def add_item_row(self):
        """Add new item row to invoice table"""
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)
        
        # Product combo
        product_combo = QComboBox()
        products = self.db.get_products()
        product_combo.addItem("Select Product", None)
        for product in products:
            display_text = f"{product['name']} - ₹{product['price']:.2f}"
            product_combo.addItem(display_text, product['id'])
        
        self.items_table.setCellWidget(row, 0, product_combo)
        
        # Quantity
        qty_spin = QSpinBox()
        qty_spin.setMinimum(1)
        qty_spin.setValue(1)
        qty_spin.valueChanged.connect(lambda value: self.calculate_item_total(row))
        self.items_table.setCellWidget(row, 1, qty_spin)
        
        # Rate (read-only, auto-filled)
        rate_edit = QLineEdit("0.00")
        rate_edit.setReadOnly(True)
        self.items_table.setCellWidget(row, 2, rate_edit)
        
        # GST %
        gst_combo = QComboBox()
        gst_combo.addItems(["0%", "5%", "12%", "18%", "28%"])
        gst_combo.setCurrentText("18%")
        gst_combo.currentTextChanged.connect(lambda text: self.calculate_item_total(row))
        self.items_table.setCellWidget(row, 3, gst_combo)
        
        # Discount %
        discount_spin = QSpinBox()
        discount_spin.setMaximum(100)
        discount_spin.setValue(0)
        discount_spin.valueChanged.connect(lambda value: self.calculate_item_total(row))
        self.items_table.setCellWidget(row, 4, discount_spin)
        
        # Amount (read-only, calculated)
        amount_edit = QLineEdit("0.00")
        amount_edit.setReadOnly(True)
        self.items_table.setCellWidget(row, 5, amount_edit)
        
        # Actions
        remove_btn = QPushButton("🗑️")
        remove_btn.clicked.connect(lambda checked, r=row: self.remove_item_row(r))
        self.items_table.setCellWidget(row, 6, remove_btn)
        
        # Connect signals for auto-calculation
        product_combo.currentIndexChanged.connect(lambda: self.calculate_item_total(row))
        qty_spin.valueChanged.connect(lambda: self.calculate_item_total(row))
        gst_combo.currentIndexChanged.connect(lambda: self.calculate_item_total(row))
        discount_spin.valueChanged.connect(lambda: self.calculate_item_total(row))
    
    def remove_item_row(self, row):
        """Remove item row from invoice table"""
        self.items_table.removeRow(row)
        self.calculate_invoice_totals()
    
    def clear_items(self):
        """Clear all items from invoice table"""
        self.items_table.setRowCount(0)
        self.calculate_invoice_totals()
    
    def calculate_item_total(self, row):
        """Calculate total for a specific item row"""
        try:
            # Get product
            product_combo = self.items_table.cellWidget(row, 0)
            if not product_combo:
                return
                
            product_id = product_combo.currentData()
            
            print(f"Row {row}: Product ID = {product_id}")  # Debug line
            
            if product_id:
                product = self.db.get_product(product_id)
                if product:
                    print(f"Product found: {product['name']}, Price: {product['price']}")  # Debug line
                    
                    # Update rate
                    rate_edit = self.items_table.cellWidget(row, 2)
                    if rate_edit:
                        rate_edit.setText(f"{product['price']:.2f}")
                    
                    # Update GST
                    gst_combo = self.items_table.cellWidget(row, 3)
                    if gst_combo:
                        gst_combo.setCurrentText(f"{product['gst_percent']:.0f}%")
            
            # Get values
            qty_spin = self.items_table.cellWidget(row, 1)
            rate_edit = self.items_table.cellWidget(row, 2)
            gst_combo = self.items_table.cellWidget(row, 3)
            discount_spin = self.items_table.cellWidget(row, 4)
            amount_edit = self.items_table.cellWidget(row, 5)
            
            if not all([qty_spin, rate_edit, gst_combo, discount_spin, amount_edit]):
                return
            
            quantity = qty_spin.value()
            rate_text = rate_edit.text()
            if not rate_text:
                rate_text = "0.00"
            rate = float(rate_text)
            gst_percent = float(gst_combo.currentText().replace('%', ''))
            discount_percent = discount_spin.value()
            
            print(f"Calculating: Qty={quantity}, Rate={rate}, GST={gst_percent}%, Discount={discount_percent}%")  # Debug line
            
            # Calculate
            calc_result = GSTCalculator.calculate_item_total(quantity, rate, discount_percent, gst_percent)
            
            amount_edit.setText(f"{calc_result['total_amount']:.2f}")
            
            print(f"Amount calculated: {calc_result['total_amount']:.2f}")  # Debug line
            
            # Update invoice totals
            self.calculate_invoice_totals()
            
        except Exception as e:
            print(f"Error calculating item total: {e}")
    
    def calculate_invoice_totals(self):
        """Calculate entire invoice totals"""
        try:
            items = []
            
            for row in range(self.items_table.rowCount()):
                product_combo = self.items_table.cellWidget(row, 0)
                if not product_combo:
                    continue
                    
                product_id = product_combo.currentData()
                
                if product_id:
                    product = self.db.get_product(product_id)
                    if product:
                        qty_spin = self.items_table.cellWidget(row, 1)
                        rate_edit = self.items_table.cellWidget(row, 2)
                        gst_combo = self.items_table.cellWidget(row, 3)
                        discount_spin = self.items_table.cellWidget(row, 4)
                        amount_edit = self.items_table.cellWidget(row, 5)
                        
                        if not all([qty_spin, rate_edit, gst_combo, discount_spin, amount_edit]):
                            continue
                        
                        quantity = qty_spin.value()
                        rate_text = rate_edit.text()
                        if not rate_text:
                            rate_text = "0.00"
                        rate = float(rate_text)
                        gst_percent = float(gst_combo.currentText().replace('%', ''))
                        discount_percent = discount_spin.value()
                        
                        calc_result = GSTCalculator.calculate_item_total(quantity, rate, discount_percent, gst_percent)
                        
                        item_data = {
                            'product_id': product_id,
                            'name': product['name'],
                            'quantity': quantity,
                            'price': rate,
                            'gst_percent': gst_percent,
                            'discount_percent': discount_percent,
                            'total': calc_result['total_amount'],
                            **calc_result
                        }
                        items.append(item_data)
            
            # Calculate totals
            totals = GSTCalculator.calculate_invoice_totals(items)
            
            # Update labels with error checking
            if hasattr(self, 'subtotal_label'):
                self.subtotal_label.setText(f"₹{totals['subtotal']:.2f}")
            if hasattr(self, 'gst_amount_label'):
                self.gst_amount_label.setText(f"₹{totals['total_gst']:.2f}")
            if hasattr(self, 'sgst_amount_label'):
                self.sgst_amount_label.setText(f"₹{totals['total_sgst']:.2f}")
            if hasattr(self, 'cgst_amount_label'):
                self.cgst_amount_label.setText(f"₹{totals['total_cgst']:.2f}")
            if hasattr(self, 'grand_total_label'):
                self.grand_total_label.setText(f"₹{totals['grand_total']:.2f}")
            
            # Store current items
            self.current_invoice_items = items
            
        except Exception as e:
            print(f"Error calculating invoice totals: {e}")
    
    def save_invoice(self):
        """Save invoice to database"""
        try:
            if not hasattr(self, 'current_invoice_items') or not self.current_invoice_items:
                QMessageBox.warning(self, "Warning", "Please add items to invoice")
                return
            
            # Get values with error checking
            invoice_number = getattr(self, 'invoice_number_label', None)
            if not invoice_number:
                QMessageBox.critical(self, "Error", "Invoice number not available")
                return
            
            subtotal_label = getattr(self, 'subtotal_label', None)
            gst_amount_label = getattr(self, 'gst_amount_label', None)
            sgst_amount_label = getattr(self, 'sgst_amount_label', None)
            cgst_amount_label = getattr(self, 'cgst_amount_label', None)
            grand_total_label = getattr(self, 'grand_total_label', None)
            payment_method_combo = getattr(self, 'payment_method_combo', None)
            notes_text = getattr(self, 'notes_text', None)
            
            if not all([subtotal_label, gst_amount_label, sgst_amount_label, cgst_amount_label, grand_total_label, payment_method_combo, notes_text]):
                QMessageBox.critical(self, "Error", "Invoice form not properly initialized")
                return
            
            invoice_data = {
                'invoice_number': invoice_number.text(),
                'customer_id': self.current_customer_id,
                'items': self.current_invoice_items,
                'subtotal': float(subtotal_label.text().replace('₹', '')),
                'gst_amount': float(gst_amount_label.text().replace('₹', '')),
                'sgst_amount': float(sgst_amount_label.text().replace('₹', '')),
                'cgst_amount': float(cgst_amount_label.text().replace('₹', '')),
                'total_amount': float(grand_total_label.text().replace('₹', '')),
                'payment_method': payment_method_combo.currentText(),
                'notes': notes_text.toPlainText(),
                'status': 'completed',
                'payment_status': 'pending'
            }
            
            invoice_id = self.db.create_invoice(invoice_data)
            
            if invoice_id > 0:
                QMessageBox.information(self, "Success", f"Invoice saved successfully!\nInvoice ID: {invoice_id}")
                self.clear_invoice_form()
                self.load_dashboard_stats()
            else:
                QMessageBox.critical(self, "Error", "Failed to save invoice")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving invoice: {str(e)}")
    
    def generate_invoice_pdf(self):
        """Generate PDF for current invoice"""
        try:
            if not hasattr(self, 'current_invoice_items') or not self.current_invoice_items:
                QMessageBox.warning(self, "Warning", "Please add items to invoice")
                return
            
            # Get shop settings
            shop_settings = self.db.get_shop_settings()
            
            # Get customer data
            customer_data = {}
            if self.current_customer_id:
                customer_data = self.db.get_customer(self.current_customer_id)
            
            # Get values with error checking
            invoice_number_label = getattr(self, 'invoice_number_label', None)
            invoice_date_label = getattr(self, 'invoice_date_label', None)
            subtotal_label = getattr(self, 'subtotal_label', None)
            gst_amount_label = getattr(self, 'gst_amount_label', None)
            sgst_amount_label = getattr(self, 'sgst_amount_label', None)
            cgst_amount_label = getattr(self, 'cgst_amount_label', None)
            grand_total_label = getattr(self, 'grand_total_label', None)
            notes_text = getattr(self, 'notes_text', None)
            
            if not all([invoice_number_label, invoice_date_label, subtotal_label, gst_amount_label, 
                       sgst_amount_label, cgst_amount_label, grand_total_label, notes_text]):
                QMessageBox.critical(self, "Error", "Invoice form not properly initialized")
                return
            
            # Prepare invoice data
            invoice_data = {
                'invoice_number': invoice_number_label.text(),
                'created_at': invoice_date_label.text(),
                'items': self.current_invoice_items,
                'subtotal': float(subtotal_label.text().replace('₹', '')),
                'gst_amount': float(gst_amount_label.text().replace('₹', '')),
                'sgst_amount': float(sgst_amount_label.text().replace('₹', '')),
                'cgst_amount': float(cgst_amount_label.text().replace('₹', '')),
                'total_amount': float(grand_total_label.text().replace('₹', '')),
                'notes': notes_text.toPlainText()
            }
            
            # Generate QR code
            qr_path = None
            if shop_settings.get('upi_id'):
                qr_path = self.qr_generator.generate_upi_payment_qr(
                    shop_settings['upi_id'],
                    invoice_data['total_amount'],
                    shop_settings.get('shop_name', 'Shop'),
                    f"Payment for {invoice_data['invoice_number']}"
                )
            
            # Generate PDF
            template = shop_settings.get('default_template', 'template1')
            logo_path = shop_settings.get('logo_path')
            
            pdf_path = self.pdf_generator.generate_invoice_pdf(
                invoice_data, shop_settings, customer_data, 
                template, qr_path, logo_path
            )
            
            QMessageBox.information(self, "Success", f"PDF generated successfully!\nSaved to: {pdf_path}")
            
            # Open PDF file
            import os
            if os.path.exists(pdf_path):
                os.startfile(pdf_path)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating PDF: {str(e)}")
    
    def print_invoice(self):
        """Print invoice"""
        # First generate PDF, then print
        self.generate_invoice_pdf()
    
    def clear_invoice_form(self):
        """Clear invoice form for new invoice"""
        self.clear_items()
        
        # Clear customer selection with error checking
        customer_combo = getattr(self, 'customer_combo', None)
        if customer_combo:
            customer_combo.setCurrentIndex(0)
        
        # Clear payment method with error checking
        payment_method_combo = getattr(self, 'payment_method_combo', None)
        if payment_method_combo:
            payment_method_combo.setCurrentIndex(0)
        
        # Clear notes with error checking
        notes_text = getattr(self, 'notes_text', None)
        if notes_text:
            notes_text.clear()
        
        # Update invoice number
        self.update_invoice_number()
        
        # Reset date
        from datetime import datetime
        invoice_date_label = getattr(self, 'invoice_date_label', None)
        if invoice_date_label:
            invoice_date_label.setText(datetime.now().strftime("%Y-%m-%d"))
    
    def quick_invoice(self):
        """Quick invoice shortcut"""
        self.content_stack.setCurrentIndex(1)
        self.clear_invoice_form()
    
    def backup_data(self):
        """Backup database"""
        try:
            from datetime import datetime
            backup_path, _ = QFileDialog.getSaveFileName(
                self, "Save Backup", f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db",
                "Database Files (*.db)"
            )
            
            if backup_path:
                import shutil
                shutil.copy2(self.db.db_path, backup_path)
                QMessageBox.information(self, "Success", f"Backup saved to: {backup_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error creating backup: {str(e)}")
    
    def add_customer_dialog(self):
        """Show add customer dialog"""
        dialog = CustomerDialog(self.db, self)
        if dialog.exec_():
            self.load_customers()
    
    def edit_customer(self, customer_id):
        """Edit customer dialog"""
        customer = self.db.get_customer(customer_id)
        if customer:
            dialog = CustomerDialog(self.db, self, customer)
            if dialog.exec_():
                self.load_customers()
    
    def add_product_dialog(self):
        """Show add product dialog"""
        dialog = ProductDialog(self.db, self)
        if dialog.exec_():
            self.load_products()
    
    def edit_product(self, product_id):
        """Edit product dialog"""
        product = self.db.get_product(product_id)
        if product:
            dialog = ProductDialog(self.db, self, product)
            if dialog.exec_():
                self.load_products()
    
    def generate_sales_report(self):
        """Generate sales report"""
        try:
            from_date = self.report_from_date.text()
            to_date = self.report_to_date.text()
            
            summary = self.db.get_sales_summary(from_date, to_date)
            top_products = self.db.get_top_products(10, from_date, to_date)
            top_customers = self.db.get_top_customers(10, from_date, to_date)
            
            report_text = f"""
SALES SUMMARY REPORT
==================
Period: {from_date or 'All time'} to {to_date or 'Today'}

Total Invoices: {summary['total_invoices']}
Total Sales: ₹{summary['total_sales']:.2f}
Average Invoice Value: ₹{summary['total_sales']/max(summary['total_invoices'], 1):.2f}

TOP PRODUCTS
============
"""
            
            for i, product in enumerate(top_products, 1):
                report_text += f"{i}. {product['product_name']}\n"
                report_text += f"   Quantity: {product['total_quantity']}\n"
                report_text += f"   Revenue: ₹{product['total_revenue']:.2f}\n\n"
            
            report_text += "\nTOP CUSTOMERS\n============\n"
            
            for i, customer in enumerate(top_customers, 1):
                report_text += f"{i}. {customer['name']}\n"
                report_text += f"   Phone: {customer['phone']}\n"
                report_text += f"   Invoices: {customer['invoice_count']}\n"
                report_text += f"   Total Spent: ₹{customer['total_spent']:.2f}\n\n"
            
            self.sales_summary_text.setText(report_text)
            
            # Update tables
            self.top_products_table.setRowCount(len(top_products))
            for i, product in enumerate(top_products):
                self.top_products_table.setItem(i, 0, QTableWidgetItem(product['product_name']))
                self.top_products_table.setItem(i, 1, QTableWidgetItem(str(product['total_quantity'])))
                self.top_products_table.setItem(i, 2, QTableWidgetItem(f"₹{product['total_revenue']:.2f}"))
            
            self.top_customers_table.setRowCount(len(top_customers))
            for i, customer in enumerate(top_customers):
                self.top_customers_table.setItem(i, 0, QTableWidgetItem(customer['name']))
                self.top_customers_table.setItem(i, 1, QTableWidgetItem(customer['phone']))
                self.top_customers_table.setItem(i, 2, QTableWidgetItem(str(customer['invoice_count'])))
                self.top_customers_table.setItem(i, 3, QTableWidgetItem(f"₹{customer['total_spent']:.2f}"))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error generating report: {str(e)}")
    
    def select_logo(self):
        """Select shop logo"""
        logo_path, _ = QFileDialog.getOpenFileName(
            self, "Select Logo", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        
        if logo_path:
            self.logo_path_label.setText(logo_path)
    
    def save_settings(self):
        """Save shop settings"""
        try:
            settings = {
                'shop_name': self.shop_name_edit.text(),
                'address': self.shop_address_edit.text(),
                'phone': self.shop_phone_edit.text(),
                'email': self.shop_email_edit.text(),
                'gstin': self.shop_gstin_edit.text(),
                'upi_id': self.shop_upi_edit.text(),
                'invoice_prefix': self.invoice_prefix_edit.text(),
                'default_gst': self.default_gst_spin.value(),
                'default_template': self.template_combo.currentText().split(' - ')[0],
                'logo_path': self.logo_path_label.text() if self.logo_path_label.text() != "No logo selected" else ""
            }
            
            if self.db.update_shop_settings(settings):
                QMessageBox.information(self, "Success", "Settings saved successfully!")
                self.load_shop_settings()
            else:
                QMessageBox.critical(self, "Error", "Failed to save settings")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving settings: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Invoice Maker", 
                         "🧾 Invoice Maker v1.0\n\n"
                         "Professional Billing System for Small & Big Shops\n\n"
                         "Features:\n"
                         "• GST Support\n"
                         "• PDF Generation\n"
                         "• QR Code Payments\n"
                         "• Customer Management\n"
                         "• Product Management\n"
                         "• Analytics & Reports\n\n"
                         "Created with PyQt5")

class CustomerDialog(QDialog):
    """Customer add/edit dialog"""
    
    def __init__(self, db, parent, customer=None):
        super().__init__(parent)
        self.db = db
        self.customer = customer
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Add/Edit Customer")
        self.setModal(True)
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Form
        form_layout = QGridLayout()
        
        form_layout.addWidget(QLabel("Name*:"), 0, 0)
        self.name_edit = QLineEdit()
        form_layout.addWidget(self.name_edit, 0, 1)
        
        form_layout.addWidget(QLabel("Phone:"), 1, 0)
        self.phone_edit = QLineEdit()
        form_layout.addWidget(self.phone_edit, 1, 1)
        
        form_layout.addWidget(QLabel("Email:"), 2, 0)
        self.email_edit = QLineEdit()
        form_layout.addWidget(self.email_edit, 2, 1)
        
        form_layout.addWidget(QLabel("Address:"), 3, 0)
        self.address_edit = QLineEdit()
        form_layout.addWidget(self.address_edit, 3, 1)
        
        form_layout.addWidget(QLabel("GSTIN:"), 4, 0)
        self.gstin_edit = QLineEdit()
        form_layout.addWidget(self.gstin_edit, 4, 1)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_customer)
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # Load customer data if editing
        if self.customer:
            self.name_edit.setText(self.customer['name'])
            self.phone_edit.setText(self.customer.get('phone', ''))
            self.email_edit.setText(self.customer.get('email', ''))
            self.address_edit.setText(self.customer.get('address', ''))
            self.gstin_edit.setText(self.customer.get('gstin', ''))
    
    def save_customer(self):
        """Save customer"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Customer name is required")
            return
        
        customer_data = {
            'name': name,
            'phone': self.phone_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'address': self.address_edit.text().strip(),
            'gstin': self.gstin_edit.text().strip()
        }
        
        try:
            if self.customer:
                # Update existing customer
                if self.db.update_customer(self.customer['id'], customer_data):
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update customer")
            else:
                # Add new customer
                customer_id = self.db.add_customer(customer_data)
                if customer_id > 0:
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to add customer")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving customer: {str(e)}")

class ProductDialog(QDialog):
    """Product add/edit dialog"""
    
    def __init__(self, db, parent, product=None):
        super().__init__(parent)
        self.db = db
        self.product = product
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Add/Edit Product")
        self.setModal(True)
        self.setFixedSize(450, 400)
        
        layout = QVBoxLayout()
        
        # Form
        form_layout = QGridLayout()
        
        form_layout.addWidget(QLabel("Name*:"), 0, 0)
        self.name_edit = QLineEdit()
        form_layout.addWidget(self.name_edit, 0, 1)
        
        form_layout.addWidget(QLabel("Price*:"), 1, 0)
        self.price_edit = QLineEdit()
        form_layout.addWidget(self.price_edit, 1, 1)
        
        form_layout.addWidget(QLabel("GST %:"), 2, 0)
        self.gst_spin = QSpinBox()
        self.gst_spin.setRange(0, 28)
        self.gst_spin.setValue(18)
        form_layout.addWidget(self.gst_spin, 2, 1)
        
        form_layout.addWidget(QLabel("Stock Quantity:"), 3, 0)
        self.stock_spin = QSpinBox()
        self.stock_spin.setMinimum(0)
        form_layout.addWidget(self.stock_spin, 3, 1)
        
        form_layout.addWidget(QLabel("Category:"), 4, 0)
        self.category_edit = QLineEdit()
        form_layout.addWidget(self.category_edit, 4, 1)
        
        form_layout.addWidget(QLabel("Barcode:"), 5, 0)
        self.barcode_edit = QLineEdit()
        form_layout.addWidget(self.barcode_edit, 5, 1)
        
        form_layout.addWidget(QLabel("Description:"), 6, 0)
        self.description_edit = QLineEdit()
        form_layout.addWidget(self.description_edit, 6, 1)
        
        form_layout.addWidget(QLabel("Min Stock Alert:"), 7, 0)
        self.min_stock_spin = QSpinBox()
        self.min_stock_spin.setMinimum(0)
        self.min_stock_spin.setValue(5)
        form_layout.addWidget(self.min_stock_spin, 7, 1)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_product)
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # Load product data if editing
        if self.product:
            self.name_edit.setText(self.product['name'])
            self.price_edit.setText(str(self.product['price']))
            self.gst_spin.setValue(int(self.product['gst_percent']))
            self.stock_spin.setValue(self.product['stock_quantity'])
            self.category_edit.setText(self.product.get('category', ''))
            self.barcode_edit.setText(self.product.get('barcode', ''))
            self.description_edit.setText(self.product.get('description', ''))
            self.min_stock_spin.setValue(self.product['min_stock_alert'])
    
    def save_product(self):
        """Save product"""
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Product name is required")
            return
        
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Invalid price format")
            return
        
        product_data = {
            'name': name,
            'price': price,
            'gst_percent': self.gst_spin.value(),
            'stock_quantity': self.stock_spin.value(),
            'category': self.category_edit.text().strip(),
            'barcode': self.barcode_edit.text().strip(),
            'description': self.description_edit.text().strip(),
            'min_stock_alert': self.min_stock_spin.value()
        }
        
        try:
            if self.product:
                # Update existing product
                if self.db.update_product(self.product['id'], product_data):
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update product")
            else:
                # Add new product
                product_id = self.db.add_product(product_data)
                if product_id > 0:
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to add product")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error saving product: {str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Invoice Maker")
    
    # Set application icon (if available)
    # app.setWindowIcon(QIcon("assets/icon.png"))
    
    window = InvoiceMakerApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
