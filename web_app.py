#!/usr/bin/env python3
"""
🧾 Invoice Maker - Web Version (Mobile Responsive)
Built with Streamlit for cross-platform compatibility
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sqlite3
import json
import os
from pathlib import Path
import base64
from io import BytesIO
import plotly.express as px
import plotly.graph_objects as go

# Database imports
try:
    from database.db import DatabaseManager
    from logic.gst_calculator import GSTCalculator
    from logic.pdf_generator import PDFGenerator
    from logic.qr_generator import QRCodeGenerator
except ImportError:
    # Fallback to simple implementations for Streamlit Cloud
    from db_simple import DatabaseManager
    from gst_calculator_simple import GSTCalculator
    
    # Simple PDF and QR generators (placeholders)
    class PDFGenerator:
        def generate_invoice_pdf(self, invoice_data, shop_settings, customer_data, template, qr_path, logo_path):
            # Generate a simple text-based invoice for now
            invoice_text = f"""
            INVOICE - {invoice_data['invoice_number']}
            Date: {invoice_data['created_at']}
            
            Shop: {shop_settings.get('shop_name', 'Your Shop')}
            Address: {shop_settings.get('address', 'Your Address')}
            Phone: {shop_settings.get('phone', 'Your Phone')}
            
            Customer: {customer_data.get('name', 'Walk-in')}
            
            Items:
            """
            
            for item in invoice_data['items']:
                invoice_text += f"- {item['name']} x {item['quantity']} = ₹{item['total']:.2f}\n"
            
            invoice_text += f"""
            
            Subtotal: ₹{invoice_data['subtotal']:.2f}
            GST: ₹{invoice_data['gst_amount']:.2f}
            Total: ₹{invoice_data['total_amount']:.2f}
            
            Thank you for your business!
            """
            
            # Save as text file (temporary solution)
            filename = f"invoice_{invoice_data['invoice_number']}.txt"
            with open(filename, 'w') as f:
                f.write(invoice_text)
            
            return filename
    
    class QRCodeGenerator:
        def generate_upi_payment_qr(self, upi_id, amount, shop_name, note):
            # Return None for now (QR generation requires additional setup)
            return None

# Page configuration
st.set_page_config(
    page_title="Invoice Maker",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile responsiveness
st.markdown("""
<style>
/* Mobile Responsive Styles */
@media (max-width: 768px) {
    .stSelectbox > div > div {
        font-size: 16px !important;
    }
    .stTextInput > div > div > input {
        font-size: 16px !important;
    }
    .stNumberInput > div > div > input {
        font-size: 16px !important;
    }
    .stButton > button {
        font-size: 16px !important;
        padding: 12px 24px !important;
        margin: 4px 2px !important;
    }
    .dataframe {
        font-size: 12px !important;
    }
    
    /* Mobile layout adjustments */
    .element-container {
        margin-bottom: 1rem !important;
    }
    
    /* Mobile navigation */
    .css-1d391kg {
        padding: 0.5rem !important;
    }
    
    .css-1lcbmhc {
        padding: 0.5rem !important;
    }
    
    /* Mobile columns */
    .css-1wrcr25 {
        flex-direction: column !important;
    }
    
    /* Mobile tables */
    .dataframe {
        overflow-x: auto !important;
        display: block !important;
    }
    
    /* Mobile forms */
    .stForm {
        padding: 1rem !important;
    }
    
    /* Mobile expander */
    .streamlit-expanderHeader {
        font-size: 16px !important;
        padding: 1rem !important;
    }
}

@media (max-width: 480px) {
    /* Small mobile phones */
    .stButton > button {
        font-size: 14px !important;
        padding: 10px 16px !important;
        width: 100% !important;
        margin: 2px 0 !important;
    }
    
    .stSelectbox, .stTextInput, .stNumberInput {
        width: 100% !important;
    }
    
    .dataframe {
        font-size: 10px !important;
    }
    
    /* Mobile metrics */
    .css-1v0mbdj {
        flex-direction: column !important;
    }
    
    /* Mobile sidebar */
    .css-1lcbmhc {
        width: 100% !important;
        max-width: 100% !important;
    }
}

/* Tablet Styles */
@media (min-width: 769px) and (max-width: 1024px) {
    .stButton > button {
        font-size: 14px !important;
        padding: 10px 20px !important;
    }
    
    .dataframe {
        font-size: 11px !important;
    }
}

/* General Styles */
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}

.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 4px solid #667eea;
    margin: 0.5rem 0;
}

.invoice-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
    border-left: 4px solid #28a745;
}

.sidebar-section {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

/* Button Styles */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    transition: all 0.3s ease;
    width: auto;
    margin: 4px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

/* Primary button variant */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}

/* Secondary button variant */
.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
}

/* Table Styles */
.dataframe {
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.dataframe th {
    background: #667eea;
    color: white;
    font-weight: 600;
    padding: 12px 8px;
    text-align: left;
}

.dataframe td {
    padding: 10px 8px;
    border-bottom: 1px solid #e9ecef;
}

.dataframe tr:hover {
    background-color: #f8f9fa;
}

/* Form Styles */
.stForm {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

/* Success/Error Messages */
.stSuccess {
    background: #d4edda;
    border: 1px solid #c3e6cb;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: #155724;
}

.stError {
    background: #f8d7da;
    border: 1px solid #f5c6cb;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: #721c24;
}

.stInfo {
    background: #d1ecf1;
    border: 1px solid #bee5eb;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: #0c5460;
}

.stWarning {
    background: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    color: #856404;
}

/* Expander Styles */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 8px;
    font-weight: 600;
    border: 1px solid #dee2e6;
}

/* Metric Styles */
.css-1v0mbdj {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
    margin: 0.5rem;
}

/* Input Styles */
.stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
    border-radius: 8px;
    border: 2px solid #e9ecef;
    transition: border-color 0.3s ease;
}

.stSelectbox > div > div:focus, .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

/* Mobile Navigation */
.mobile-nav {
    display: flex;
    justify-content: space-around;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 10px;
    margin-bottom: 2rem;
    position: sticky;
    top: 0;
    z-index: 1000;
}

.mobile-nav .stButton > button {
    flex: 1;
    margin: 0 2px;
    font-size: 12px;
    padding: 8px 4px;
}

@media (max-width: 768px) {
    .mobile-nav .stButton > button {
        font-size: 10px;
        padding: 6px 2px;
    }
}

/* Responsive grid */
.responsive-grid {
    display: grid;
    gap: 1rem;
}

@media (min-width: 769px) {
    .responsive-grid {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1025px) {
    .responsive-grid {
        grid-template-columns: repeat(3, 1fr);
    }
}

/* Mobile-friendly tables */
.mobile-table {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}

.mobile-table table {
    min-width: 600px;
}

/* Loading spinner */
.stSpinner {
    text-align: center;
    padding: 2rem;
}

/* Footer */
.mobile-footer {
    text-align: center;
    padding: 2rem 1rem;
    background: #f8f9fa;
    border-radius: 10px;
    margin-top: 2rem;
}

/* Hide streamlit branding */
.stDeployButton {
    display: none;
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #667eea;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #5a6fd8;
}
</style>
""", unsafe_allow_html=True)

# Initialize database
@st.cache_resource
def init_db():
    return DatabaseManager()

# Initialize classes
db = init_db()
gst_calc = GSTCalculator()
pdf_gen = PDFGenerator()
qr_gen = QRCodeGenerator()

# Session state initialization
if 'current_customer_id' not in st.session_state:
    st.session_state.current_customer_id = None
if 'invoice_items' not in st.session_state:
    st.session_state.invoice_items = []
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Helper functions
def format_currency(amount):
    """Format amount as Indian Rupee"""
    return f"₹{amount:,.2f}"

def get_base64_image(image_path):
    """Convert image to base64 for embedding"""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return ""

# Mobile-friendly navigation
def mobile_navigation():
    """Mobile-responsive navigation with icons"""
    st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
    
    cols = st.columns([1, 1, 1, 1, 1])
    
    with cols[0]:
        if st.button("📊\nDashboard", key="nav_dashboard", use_container_width=True, help="Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with cols[1]:
        if st.button("📝\nInvoice", key="nav_invoice", use_container_width=True, help="New Invoice"):
            st.session_state.page = 'invoice'
            st.rerun()
    
    with cols[2]:
        if st.button("👥\nCustomers", key="nav_customers", use_container_width=True, help="Customers"):
            st.session_state.page = 'customers'
            st.rerun()
    
    with cols[3]:
        if st.button("📦\nProducts", key="nav_products", use_container_width=True, help="Products"):
            st.session_state.page = 'products'
            st.rerun()
    
    with cols[4]:
        if st.button("⚙️\nSettings", key="nav_settings", use_container_width=True, help="Settings"):
            st.session_state.page = 'settings'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Dashboard Page
def dashboard_page():
    """Mobile-responsive dashboard"""
    st.markdown('<div class="main-header"><h1>🧾 Invoice Maker</h1><p>Professional Billing System</p></div>', unsafe_allow_html=True)
    
    # Stats Cards - Responsive Grid
    st.markdown('<div class="responsive-grid">', unsafe_allow_html=True)
    
    # Today's Sales
    today = date.today().strftime("%Y-%m-%d")
    today_summary = db.get_sales_summary(today, today)
    st.markdown(f'''
    <div class="metric-card">
        <h3 style="color: #28a745; margin: 0;">{format_currency(today_summary['total_sales'])}</h3>
        <p style="margin: 0; color: #6c757d;">Today's Sales</p>
        <small>{today_summary['total_invoices']} invoices</small>
    </div>
    ''', unsafe_allow_html=True)
    
    # Total Customers
    customers = db.get_customers()
    st.markdown(f'''
    <div class="metric-card">
        <h3 style="color: #007bff; margin: 0;">{len(customers)}</h3>
        <p style="margin: 0; color: #6c757d;">Total Customers</p>
        <small>Active customers</small>
    </div>
    ''', unsafe_allow_html=True)
    
    # Total Products
    products = db.get_products()
    st.markdown(f'''
    <div class="metric-card">
        <h3 style="color: #dc3545; margin: 0;">{len(products)}</h3>
        <p style="margin: 0; color: #6c757d;">Total Products</p>
        <small>In inventory</small>
    </div>
    ''', unsafe_allow_html=True)
    
    # Low Stock
    low_stock = db.get_low_stock_products()
    st.markdown(f'''
    <div class="metric-card">
        <h3 style="color: #ffc107; margin: 0;">{len(low_stock)}</h3>
        <p style="margin: 0; color: #6c757d;">Low Stock Alert</p>
        <small>Need restocking</small>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Invoices
    st.subheader("📋 Recent Invoices")
    recent_invoices = db.get_invoices(limit=10)
    
    if recent_invoices:
        # Create mobile-friendly table
        df_data = []
        for invoice in recent_invoices:
            df_data.append({
                'Invoice #': invoice['invoice_number'],
                'Customer': invoice.get('customer_name', 'Walk-in'),
                'Amount': format_currency(invoice['total_amount']),
                'Date': invoice['created_at'][:10]
            })
        
        df = pd.DataFrame(df_data)
        st.markdown('<div class="mobile-table">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No invoices found. Create your first invoice!")
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Create Invoice", use_container_width=True):
            st.session_state.page = 'invoice'
            st.rerun()
    
    with col2:
        if st.button("💾 Backup Data", use_container_width=True):
            backup_data()

# Invoice Page
def invoice_page():
    """Mobile-responsive invoice creation"""
    st.markdown('<div class="main-header"><h1>📝 Create Invoice</h1></div>', unsafe_allow_html=True)
    
    # Customer Selection
    st.subheader("👥 Customer Information")
    customers = db.get_customers()
    customer_options = {"Walk-in Customer": None}
    
    for customer in customers:
        customer_options[f"{customer['name']} - {customer.get('phone', '')}"] = customer['id']
    
    selected_customer = st.selectbox("Select Customer", list(customer_options.keys()))
    
    if selected_customer != "Walk-in Customer":
        st.session_state.current_customer_id = customer_options[selected_customer]
        customer = db.get_customer(st.session_state.current_customer_id)
        
        if customer:
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Phone", customer.get('phone', ''), disabled=True)
            with col2:
                st.text_input("Email", customer.get('email', ''), disabled=True)
            
            st.text_area("Address", customer.get('address', ''), disabled=True)
    else:
        st.session_state.current_customer_id = None
    
    # Invoice Details
    st.subheader("🧾 Invoice Details")
    col1, col2 = st.columns(2)
    
    with col1:
        invoice_number = db.generate_invoice_number()
        st.text_input("Invoice Number", invoice_number, disabled=True)
    
    with col2:
        st.date_input("Invoice Date", datetime.now().date())
    
    # Items Section
    st.subheader("📦 Items")
    
    # Add new item
    with st.expander("➕ Add Item", expanded=True):
        products = db.get_products()
        product_options = {"Select Product": None}
        
        for product in products:
            product_options[f"{product['name']} - ₹{product['price']:.2f}"] = product['id']
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_product = st.selectbox("Product", list(product_options.keys()))
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, value=1)
        
        if selected_product != "Select Product" and st.button("Add to Invoice"):
            product_id = product_options[selected_product]
            product = db.get_product(product_id)
            
            if product:
                # Calculate item total
                calc_result = gst_calc.calculate_item_total(
                    quantity, 
                    product['price'], 
                    0,  # discount
                    product['gst_percent']
                )
                
                item_data = {
                    'product_id': product_id,
                    'name': product['name'],
                    'quantity': quantity,
                    'price': product['price'],
                    'gst_percent': product['gst_percent'],
                    'discount_percent': 0,
                    'total': calc_result['total_amount'],
                    **calc_result
                }
                
                st.session_state.invoice_items.append(item_data)
                st.success(f"Added {quantity} x {product['name']}")
                st.rerun()
    
    # Display Items
    if st.session_state.invoice_items:
        st.subheader("📋 Invoice Items")
        
        for i, item in enumerate(st.session_state.invoice_items):
            with st.expander(f"📦 {item['name']} - {format_currency(item['total'])}"):
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.text(f"Product: {item['name']}")
                
                with col2:
                    st.text(f"Qty: {item['quantity']}")
                
                with col3:
                    st.text(f"Rate: {format_currency(item['price'])}")
                
                with col4:
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.invoice_items.pop(i)
                        st.rerun()
                
                st.text(f"GST: {item['gst_percent']}% | Discount: {item['discount_percent']}%")
                st.text(f"Total: {format_currency(item['total'])}")
    
    # Calculate Totals
    if st.session_state.invoice_items:
        totals = gst_calc.calculate_invoice_totals(st.session_state.invoice_items)
        
        st.subheader("💰 Invoice Summary")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Subtotal", format_currency(totals['subtotal']))
            st.metric("GST Amount", format_currency(totals['total_gst']))
        
        with col2:
            st.metric("SGST", format_currency(totals['total_sgst']))
            st.metric("CGST", format_currency(totals['total_cgst']))
        
        st.metric("Grand Total", format_currency(totals['grand_total']))
        
        # Payment Method
        payment_method = st.selectbox("Payment Method", ["Cash", "Card", "UPI", "Net Banking", "Cheque"])
        
        # Notes
        notes = st.text_area("Notes (Optional)")
        
        # Action Buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Invoice", use_container_width=True):
                save_invoice(totals, payment_method, notes)
        
        with col2:
            if st.button("📄 Generate PDF", use_container_width=True):
                generate_pdf_invoice(totals, payment_method, notes)
        
        with col3:
            if st.button("🗑️ Clear All", use_container_width=True):
                st.session_state.invoice_items = []
                st.rerun()
    else:
        st.info("No items added. Add items to create invoice.")

# Customers Page
def customers_page():
    """Mobile-responsive customer management"""
    st.markdown('<div class="main-header"><h1>👥 Customer Management</h1></div>', unsafe_allow_html=True)
    
    # Add Customer Form
    with st.expander("➕ Add New Customer", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Customer Name *")
            phone = st.text_input("Phone Number *")
        
        with col2:
            email = st.text_input("Email")
            gstin = st.text_input("GSTIN")
        
        address = st.text_area("Address")
        
        if st.button("💾 Add Customer", use_container_width=True):
            if name and phone:
                customer_data = {
                    'name': name,
                    'phone': phone,
                    'email': email,
                    'gstin': gstin,
                    'address': address
                }
                
                try:
                    customer_id = db.add_customer(customer_data)
                    if customer_id > 0:
                        st.success(f"Customer added successfully! ID: {customer_id}")
                        st.rerun()
                    else:
                        st.error("Failed to add customer")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Name and Phone are required!")
    
    # Search Customers
    search_term = st.text_input("🔍 Search Customers", placeholder="Search by name, phone, or email...")
    
    # Display Customers
    customers = db.get_customers(search_term)
    
    if customers:
        st.subheader(f"📋 Customers ({len(customers)} found)")
        
        for customer in customers:
            with st.expander(f"👤 {customer['name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text(f"📱 Phone: {customer.get('phone', 'N/A')}")
                    st.text(f"📧 Email: {customer.get('email', 'N/A')}")
                
                with col2:
                    st.text(f"🆔 GSTIN: {customer.get('gstin', 'N/A')}")
                    st.text(f"📍 Address: {customer.get('address', 'N/A')}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", key=f"edit_{customer['id']}"):
                        st.info("Edit functionality coming soon!")
                
                with col2:
                    if st.button("🧾 View Invoices", key=f"invoices_{customer['id']}"):
                        st.info("Invoice history coming soon!")
    else:
        st.info("No customers found. Add your first customer!")

# Products Page
def products_page():
    """Mobile-responsive product management"""
    st.markdown('<div class="main-header"><h1>📦 Product Management</h1></div>', unsafe_allow_html=True)
    
    # Add Product Form
    with st.expander("➕ Add New Product", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Product Name *")
            price = st.number_input("Price (₹) *", min_value=0.0, value=0.0, step=0.01)
            gst_percent = st.selectbox("GST %", [0, 5, 12, 18, 28], index=3)
        
        with col2:
            stock_quantity = st.number_input("Stock Quantity", min_value=0, value=0)
            category = st.text_input("Category")
            barcode = st.text_input("Barcode")
        
        description = st.text_area("Description")
        
        if st.button("💾 Add Product", use_container_width=True):
            if name and price > 0:
                product_data = {
                    'name': name,
                    'description': description,
                    'price': price,
                    'gst_percent': gst_percent,
                    'stock_quantity': stock_quantity,
                    'category': category,
                    'barcode': barcode
                }
                
                try:
                    product_id = db.add_product(product_data)
                    if product_id > 0:
                        st.success(f"Product added successfully! ID: {product_id}")
                        st.rerun()
                    else:
                        st.error("Failed to add product")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            else:
                st.error("Product Name and Price are required!")
    
    # Search Products
    search_term = st.text_input("🔍 Search Products", placeholder="Search by name, category, or barcode...")
    
    # Display Products
    products = db.get_products(search_term)
    
    if products:
        st.subheader(f"📦 Products ({len(products)} found)")
        
        for product in products:
            stock_status = "🟢 In Stock" if product['stock_quantity'] > 10 else "🟡 Low Stock" if product['stock_quantity'] > 0 else "🔴 Out of Stock"
            
            with st.expander(f"📦 {product['name']} - {format_currency(product['price'])} {stock_status}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text(f"💰 Price: {format_currency(product['price'])}")
                    st.text(f"📊 GST: {product['gst_percent']}%")
                    st.text(f"📦 Stock: {product['stock_quantity']} units")
                
                with col2:
                    st.text(f"📂 Category: {product.get('category', 'N/A')}")
                    st.text(f"🏷️ Barcode: {product.get('barcode', 'N/A')}")
                
                if product.get('description'):
                    st.text(f"📝 Description: {product['description']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("✏️ Edit", key=f"edit_{product['id']}"):
                        st.info("Edit functionality coming soon!")
                
                with col2:
                    if st.button("📦 Update Stock", key=f"stock_{product['id']}"):
                        st.info("Stock update coming soon!")
    else:
        st.info("No products found. Add your first product!")

# Settings Page
def settings_page():
    """Mobile-responsive settings"""
    st.markdown('<div class="main-header"><h1>⚙️ Settings</h1></div>', unsafe_allow_html=True)
    
    # Shop Settings
    st.subheader("🏪 Shop Information")
    
    shop_settings = db.get_shop_settings()
    
    col1, col2 = st.columns(2)
    
    with col1:
        shop_name = st.text_input("Shop Name", shop_settings.get('shop_name', ''))
        shop_phone = st.text_input("Phone", shop_settings.get('phone', ''))
        shop_gstin = st.text_input("GSTIN", shop_settings.get('gstin', ''))
    
    with col2:
        shop_address = st.text_input("Address", shop_settings.get('address', ''))
        shop_email = st.text_input("Email", shop_settings.get('email', ''))
        shop_upi = st.text_input("UPI ID", shop_settings.get('upi_id', ''))
    
    # Invoice Settings
    st.subheader("🧾 Invoice Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        invoice_prefix = st.text_input("Invoice Prefix", shop_settings.get('invoice_prefix', 'INV'))
        default_gst = st.selectbox("Default GST %", [0, 5, 12, 18, 28], 
                                  index=[0, 5, 12, 18, 28].index(int(shop_settings.get('default_gst', 18))))
    
    with col2:
        template = st.selectbox("Invoice Template", 
                               ["template1 - Clean", "template2 - Modern", "template3 - Minimalist"],
                               index=0 if shop_settings.get('default_template') == 'template1' else 
                                      1 if shop_settings.get('default_template') == 'template2' else 2)
    
    if st.button("💾 Save Settings", use_container_width=True):
        settings_data = {
            'shop_name': shop_name,
            'address': shop_address,
            'phone': shop_phone,
            'email': shop_email,
            'gstin': shop_gstin,
            'upi_id': shop_upi,
            'invoice_prefix': invoice_prefix,
            'default_gst': default_gst,
            'default_template': template.split(' - ')[0]
        }
        
        try:
            db.save_shop_settings(settings_data)
            st.success("Settings saved successfully!")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # Data Management
    st.subheader("💾 Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Backup Data", use_container_width=True):
            backup_data()
    
    with col2:
        if st.button("📊 Export Reports", use_container_width=True):
            st.info("Export functionality coming soon!")
    
    # About
    st.subheader("ℹ️ About")
    st.markdown("""
    **🧾 Invoice Maker - Web Version**
    
    Version: 1.0.0
    Platform: Web (Mobile Responsive)
    
    Features:
    - 📱 Mobile & Desktop compatible
    - 🌐 Works in any browser
    - 💾 Cloud sync (coming soon)
    - 📧 Email invoices (coming soon)
    - 📊 Advanced analytics (coming soon)
    
    Support: support@invoicemaker.com
    """)

# Helper Functions
def save_invoice(totals, payment_method, notes):
    """Save invoice to database"""
    try:
        invoice_data = {
            'invoice_number': db.generate_invoice_number(),
            'customer_id': st.session_state.current_customer_id,
            'items': st.session_state.invoice_items,
            'subtotal': totals['subtotal'],
            'gst_amount': totals['total_gst'],
            'sgst_amount': totals['total_sgst'],
            'cgst_amount': totals['total_cgst'],
            'total_amount': totals['grand_total'],
            'payment_method': payment_method,
            'notes': notes,
            'status': 'completed',
            'payment_status': 'pending'
        }
        
        invoice_id = db.create_invoice(invoice_data)
        
        if invoice_id > 0:
            st.success(f"Invoice saved successfully! ID: {invoice_id}")
            st.session_state.invoice_items = []
            st.session_state.page = 'dashboard'
            st.rerun()
        else:
            st.error("Failed to save invoice")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")

def generate_pdf_invoice(totals, payment_method, notes):
    """Generate PDF invoice"""
    try:
        # Get shop settings
        shop_settings = db.get_shop_settings()
        
        # Get customer data
        customer_data = {}
        if st.session_state.current_customer_id:
            customer_data = db.get_customer(st.session_state.current_customer_id)
        
        # Prepare invoice data
        invoice_data = {
            'invoice_number': db.generate_invoice_number(),
            'created_at': datetime.now().strftime("%Y-%m-%d"),
            'items': st.session_state.invoice_items,
            'subtotal': totals['subtotal'],
            'gst_amount': totals['total_gst'],
            'sgst_amount': totals['total_sgst'],
            'cgst_amount': totals['total_cgst'],
            'total_amount': totals['grand_total'],
            'notes': notes
        }
        
        # Generate QR code
        qr_path = None
        if shop_settings.get('upi_id'):
            qr_path = qr_gen.generate_upi_payment_qr(
                shop_settings['upi_id'],
                invoice_data['total_amount'],
                shop_settings.get('shop_name', 'Shop'),
                f"Payment for {invoice_data['invoice_number']}"
            )
        
        # Generate PDF
        template = shop_settings.get('default_template', 'template1')
        logo_path = shop_settings.get('logo_path')
        
        pdf_path = pdf_gen.generate_invoice_pdf(
            invoice_data, shop_settings, customer_data, 
            template, qr_path, logo_path
        )
        
        # Provide download link
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="📄 Download PDF Invoice",
                data=file.read(),
                file_name=f"Invoice_{invoice_data['invoice_number']}.pdf",
                mime="application/pdf"
            )
        
        st.success("PDF generated successfully!")
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")

def backup_data():
    """Backup database"""
    try:
        from datetime import datetime
        import shutil
        
        backup_path = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(db.db_path, backup_path)
        
        # Provide download link
        with open(backup_path, "rb") as file:
            st.download_button(
                label="💾 Download Backup",
                data=file.read(),
                file_name=backup_path,
                mime="application/octet-stream"
            )
        
        st.success("Backup created successfully!")
        
    except Exception as e:
        st.error(f"Error creating backup: {str(e)}")

# Main App
def main():
    """Main application logic"""
    # Mobile Navigation
    mobile_navigation()
    
    # Page routing
    if st.session_state.page == 'dashboard':
        dashboard_page()
    elif st.session_state.page == 'invoice':
        invoice_page()
    elif st.session_state.page == 'customers':
        customers_page()
    elif st.session_state.page == 'products':
        products_page()
    elif st.session_state.page == 'settings':
        settings_page()
    else:
        dashboard_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="mobile-footer">
        <h3>📞 Need Help?</h3>
        <p>Get support for Invoice Maker</p>
        <p><strong>Email:</strong> <a href="mailto:ashwin2431333@gmail.com">ashwin2431333@gmail.com</a></p>
        <p><strong>GitHub:</strong> <a href="https://github.com/Ashwinjauhary/Invoicyy">Report Issues</a></p>
        <p><strong>Live Demo:</strong> <a href="https://invoicyy.streamlit.app">Web App</a></p>
        <hr style="margin: 1rem 0; border: 1px solid #e9ecef;">
        <p style="font-size: 0.9rem; color: #6c757d;">
            🧾 Invoice Maker - Professional Billing System<br>
            Made with ❤️ for small businesses in India
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
