#!/usr/bin/env python3
"""
🧾 Web Database Manager for Streamlit
Complete database implementation for web deployment
"""

import sqlite3
import json
from datetime import datetime, date
from pathlib import Path

class DatabaseManager:
    """Complete database manager for web deployment"""
    
    def __init__(self, db_path="invoice_web.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS shop_settings (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    gstin TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL,
                    gst_percent REAL DEFAULT 18,
                    stock_quantity INTEGER DEFAULT 0,
                    category TEXT,
                    barcode TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS invoices (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    invoice_number TEXT UNIQUE NOT NULL,
                    customer_id INTEGER,
                    items TEXT NOT NULL,
                    subtotal REAL NOT NULL,
                    gst_amount REAL NOT NULL,
                    sgst_amount REAL NOT NULL,
                    cgst_amount REAL NOT NULL,
                    total_amount REAL NOT NULL,
                    payment_method TEXT,
                    notes TEXT,
                    status TEXT DEFAULT 'pending',
                    payment_status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Add default shop settings
            self.add_default_settings()
            
        except Exception as e:
            print(f"Database initialization error: {e}")
    
    def add_default_settings(self):
        """Add default shop settings"""
        default_settings = {
            'shop_name': 'Your Shop Name',
            'address': 'Your Address',
            'phone': 'Your Phone',
            'email': 'your@email.com',
            'gstin': 'Your GSTIN',
            'upi_id': 'yourupi@upi',
            'invoice_prefix': 'INV',
            'default_gst': '18',
            'default_template': 'template1'
        }
        
        for key, value in default_settings.items():
            self.save_shop_setting(key, value)
    
    def save_shop_setting(self, key, value):
        """Save a shop setting"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO shop_settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving setting {key}: {e}")
    
    def get_shop_settings(self):
        """Get all shop settings"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT key, value FROM shop_settings')
            settings = dict(cursor.fetchall())
            
            conn.close()
            return settings
        except Exception as e:
            print(f"Error getting settings: {e}")
            return {}
    
    def save_shop_settings(self, settings_dict):
        """Save multiple shop settings"""
        for key, value in settings_dict.items():
            self.save_shop_setting(key, value)
    
    def add_customer(self, customer_data):
        """Add a new customer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO customers (name, phone, email, address, gstin)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                customer_data['name'],
                customer_data.get('phone', ''),
                customer_data.get('email', ''),
                customer_data.get('address', ''),
                customer_data.get('gstin', '')
            ))
            
            customer_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return customer_id
        except Exception as e:
            print(f"Error adding customer: {e}")
            return -1
    
    def get_customers(self, search_term=''):
        """Get all customers"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute('''
                    SELECT * FROM customers 
                    WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                    ORDER BY name
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                cursor.execute('SELECT * FROM customers ORDER BY name')
            
            customers = []
            for row in cursor.fetchall():
                customers.append({
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2],
                    'email': row[3],
                    'address': row[4],
                    'gstin': row[5],
                    'created_at': row[6],
                    'updated_at': row[7]
                })
            
            conn.close()
            return customers
        except Exception as e:
            print(f"Error getting customers: {e}")
            return []
    
    def get_customer(self, customer_id):
        """Get a specific customer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
            row = cursor.fetchone()
            
            if row:
                customer = {
                    'id': row[0],
                    'name': row[1],
                    'phone': row[2],
                    'email': row[3],
                    'address': row[4],
                    'gstin': row[5],
                    'created_at': row[6],
                    'updated_at': row[7]
                }
                conn.close()
                return customer
            else:
                conn.close()
                return None
        except Exception as e:
            print(f"Error getting customer: {e}")
            return None
    
    def add_product(self, product_data):
        """Add a new product"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO products (name, description, price, gst_percent, stock_quantity, category, barcode)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data['name'],
                product_data.get('description', ''),
                product_data['price'],
                product_data.get('gst_percent', 18),
                product_data.get('stock_quantity', 0),
                product_data.get('category', ''),
                product_data.get('barcode', '')
            ))
            
            product_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return product_id
        except Exception as e:
            print(f"Error adding product: {e}")
            return -1
    
    def get_products(self, search_term=''):
        """Get all products"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute('''
                    SELECT * FROM products 
                    WHERE name LIKE ? OR category LIKE ? OR barcode LIKE ?
                    ORDER BY name
                ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
            else:
                cursor.execute('SELECT * FROM products ORDER BY name')
            
            products = []
            for row in cursor.fetchall():
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'gst_percent': row[4],
                    'stock_quantity': row[5],
                    'category': row[6],
                    'barcode': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                })
            
            conn.close()
            return products
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def get_product(self, product_id):
        """Get a specific product"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            
            if row:
                product = {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'gst_percent': row[4],
                    'stock_quantity': row[5],
                    'category': row[6],
                    'barcode': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                }
                conn.close()
                return product
            else:
                conn.close()
                return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def create_invoice(self, invoice_data):
        """Create a new invoice"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO invoices (
                    invoice_number, customer_id, items, subtotal, gst_amount, 
                    sgst_amount, cgst_amount, total_amount, payment_method, notes, status, payment_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                invoice_data['invoice_number'],
                invoice_data.get('customer_id'),
                json.dumps(invoice_data['items']),
                invoice_data['subtotal'],
                invoice_data['gst_amount'],
                invoice_data['sgst_amount'],
                invoice_data['cgst_amount'],
                invoice_data['total_amount'],
                invoice_data.get('payment_method', ''),
                invoice_data.get('notes', ''),
                invoice_data.get('status', 'pending'),
                invoice_data.get('payment_status', 'pending')
            ))
            
            invoice_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return invoice_id
        except Exception as e:
            print(f"Error creating invoice: {e}")
            return -1
    
    def get_invoices(self, limit=None, customer_id=None):
        """Get invoices"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = '''
                SELECT i.*, c.name as customer_name 
                FROM invoices i 
                LEFT JOIN customers c ON i.customer_id = c.id
                ORDER BY i.created_at DESC
            '''
            params = []
            
            if customer_id:
                query += ' WHERE i.customer_id = ?'
                params.append(customer_id)
            
            if limit:
                query += ' LIMIT ?'
                params.append(limit)
            
            cursor.execute(query, params)
            
            invoices = []
            for row in cursor.fetchall():
                invoices.append({
                    'id': row[0],
                    'invoice_number': row[1],
                    'customer_id': row[2],
                    'items': json.loads(row[3]) if row[3] else [],
                    'subtotal': row[4],
                    'gst_amount': row[5],
                    'sgst_amount': row[6],
                    'cgst_amount': row[7],
                    'total_amount': row[8],
                    'payment_method': row[9],
                    'notes': row[10],
                    'status': row[11],
                    'payment_status': row[12],
                    'created_at': row[13],
                    'customer_name': row[14]
                })
            
            conn.close()
            return invoices
        except Exception as e:
            print(f"Error getting invoices: {e}")
            return []
    
    def generate_invoice_number(self):
        """Generate a unique invoice number"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current prefix
            settings = self.get_shop_settings()
            prefix = settings.get('invoice_prefix', 'INV')
            
            # Get last invoice number
            cursor.execute('''
                SELECT invoice_number FROM invoices 
                WHERE invoice_number LIKE ?
                ORDER BY created_at DESC 
                LIMIT 1
            ''', (f'{prefix}%',))
            
            result = cursor.fetchone()
            
            if result:
                last_number = result[0]
                # Extract numeric part
                try:
                    number_part = int(last_number.replace(prefix, ''))
                    new_number = number_part + 1
                except ValueError:
                    new_number = 1
            else:
                new_number = 1
            
            new_invoice_number = f"{prefix}{new_number:04d}"
            
            conn.close()
            return new_invoice_number
        except Exception as e:
            print(f"Error generating invoice number: {e}")
            return f"INV{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def get_sales_summary(self, start_date, end_date):
        """Get sales summary for date range"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_invoices,
                    COALESCE(SUM(total_amount), 0) as total_sales,
                    COALESCE(SUM(subtotal), 0) as total_subtotal,
                    COALESCE(SUM(gst_amount), 0) as total_gst
                FROM invoices 
                WHERE DATE(created_at) BETWEEN ? AND ?
                AND status = 'completed'
            ''', (start_date, end_date))
            
            result = cursor.fetchone()
            
            summary = {
                'total_invoices': result[0] or 0,
                'total_sales': result[1] or 0,
                'total_subtotal': result[2] or 0,
                'total_gst': result[3] or 0
            }
            
            conn.close()
            return summary
        except Exception as e:
            print(f"Error getting sales summary: {e}")
            return {
                'total_invoices': 0,
                'total_sales': 0,
                'total_subtotal': 0,
                'total_gst': 0
            }
    
    def get_low_stock_products(self):
        """Get products with low stock"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM products 
                WHERE stock_quantity <= 10 
                ORDER BY stock_quantity ASC
            ''')
            
            products = []
            for row in cursor.fetchall():
                products.append({
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                    'price': row[3],
                    'gst_percent': row[4],
                    'stock_quantity': row[5],
                    'category': row[6],
                    'barcode': row[7],
                    'created_at': row[8],
                    'updated_at': row[9]
                })
            
            conn.close()
            return products
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
