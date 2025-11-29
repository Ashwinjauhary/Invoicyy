import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

class DatabaseManager:
    def __init__(self, db_path: str = "invoice_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with schema"""
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_script = f.read()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.executescript(schema_script)
            conn.commit()
            conn.close()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # Shop Settings Methods
    def get_shop_settings(self) -> Dict:
        """Get shop settings"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shop_settings WHERE id = 1")
        settings = cursor.fetchone()
        conn.close()
        return dict(settings) if settings else {}
    
    def update_shop_settings(self, settings: Dict) -> bool:
        """Update shop settings"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            fields = ['shop_name', 'address', 'phone', 'email', 'gstin', 'logo_path', 
                     'invoice_prefix', 'default_gst', 'default_template', 'upi_id']
            
            update_fields = []
            values = []
            for field in fields:
                if field in settings:
                    update_fields.append(f"{field} = ?")
                    values.append(settings[field])
            
            if update_fields:
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                values.append(1)
                
                query = f"UPDATE shop_settings SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, values)
                conn.commit()
            
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating shop settings: {e}")
            return False
    
    # Customer Methods
    def add_customer(self, customer: Dict) -> int:
        """Add new customer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO customers (name, phone, address, email, gstin)
            VALUES (?, ?, ?, ?, ?)
        """, (customer['name'], customer.get('phone'), customer.get('address'),
              customer.get('email'), customer.get('gstin')))
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id
    
    def get_customers(self, search: str = "") -> List[Dict]:
        """Get all customers or search customers"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if search:
            cursor.execute("""
                SELECT * FROM customers 
                WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                ORDER BY name
            """, (f"%{search}%", f"%{search}%", f"%{search}%"))
        else:
            cursor.execute("SELECT * FROM customers ORDER BY name")
        
        customers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return customers
    
    def get_customer(self, customer_id: int) -> Optional[Dict]:
        """Get customer by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers WHERE id = ?", (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return dict(customer) if customer else None
    
    def update_customer(self, customer_id: int, customer: Dict) -> bool:
        """Update customer details"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers 
                SET name = ?, phone = ?, address = ?, email = ?, gstin = ?, 
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (customer['name'], customer.get('phone'), customer.get('address'),
                  customer.get('email'), customer.get('gstin'), customer_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating customer: {e}")
            return False
    
    # Product Methods
    def add_product(self, product: Dict) -> int:
        """Add new product"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO products (name, description, price, gst_percent, barcode, 
                                category, stock_quantity, min_stock_alert)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (product['name'], product.get('description'), product['price'],
              product.get('gst_percent', 18.0), product.get('barcode'),
              product.get('category'), product.get('stock_quantity', 0),
              product.get('min_stock_alert', 5)))
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id
    
    def get_products(self, search: str = "", category: str = "") -> List[Dict]:
        """Get all products or search products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM products"
        params = []
        
        conditions = []
        if search:
            conditions.append("(name LIKE ? OR barcode LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])
        
        if category:
            conditions.append("category = ?")
            params.append(category)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY name"
        
        cursor.execute(query, params)
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """Get product by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        return dict(product) if product else None
    
    def update_product(self, product_id: int, product: Dict) -> bool:
        """Update product details"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products 
                SET name = ?, description = ?, price = ?, gst_percent = ?, 
                    barcode = ?, category = ?, stock_quantity = ?, min_stock_alert = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (product['name'], product.get('description'), product['price'],
                  product.get('gst_percent', 18.0), product.get('barcode'),
                  product.get('category'), product.get('stock_quantity'),
                  product.get('min_stock_alert', 5), product_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def update_stock(self, product_id: int, quantity_change: int, transaction_type: str, 
                    reference_id: Optional[int] = None, notes: str = "") -> bool:
        """Update product stock"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Update product stock
            cursor.execute("""
                UPDATE products 
                SET stock_quantity = stock_quantity + ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (quantity_change, product_id))
            
            # Add stock transaction record
            cursor.execute("""
                INSERT INTO stock_transactions (product_id, transaction_type, quantity, 
                                             reference_id, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, transaction_type, quantity_change, reference_id, notes))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating stock: {e}")
            return False
    
    def get_low_stock_products(self) -> List[Dict]:
        """Get products with low stock"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM products 
            WHERE stock_quantity <= min_stock_alert 
            ORDER BY stock_quantity ASC
        """)
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products
    
    # Invoice Methods
    def create_invoice(self, invoice: Dict) -> int:
        """Create new invoice"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO invoices (invoice_number, customer_id, subtotal, 
                                    discount_amount, gst_amount, sgst_amount, cgst_amount, 
                                    total_amount, items_json, pdf_path, status, 
                                    payment_method, payment_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (invoice['invoice_number'], invoice.get('customer_id'),
                  invoice['subtotal'], invoice.get('discount_amount', 0),
                  invoice['gst_amount'], invoice.get('sgst_amount', 0),
                  invoice.get('cgst_amount', 0), invoice['total_amount'],
                  json.dumps(invoice['items']), invoice.get('pdf_path'),
                  invoice.get('status', 'completed'), invoice.get('payment_method'),
                  invoice.get('payment_status', 'pending'), invoice.get('notes')))
            
            invoice_id = cursor.lastrowid
            
            # Add individual invoice items
            for item in invoice['items']:
                cursor.execute("""
                    INSERT INTO invoice_items (invoice_id, product_id, product_name, 
                                             quantity, unit_price, discount_percent, 
                                             gst_percent, total_price)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (invoice_id, item.get('product_id'), item['name'],
                      item['quantity'], item['price'], item.get('discount_percent', 0),
                      item.get('gst_percent', 18.0), item['total']))
                
                # Update stock
                if item.get('product_id'):
                    self.update_stock(item['product_id'], -int(item['quantity']), 'sale', 
                                    invoice_id, f"Invoice {invoice['invoice_number']}")
            
            conn.commit()
            conn.close()
            return invoice_id
            
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Error creating invoice: {e}")
            return 0
    
    def get_invoices(self, limit: int = 100, customer_id: Optional[int] = None) -> List[Dict]:
        """Get invoices with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT i.*, c.name as customer_name, c.phone as customer_phone
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
        """
        params = []
        
        if customer_id:
            query += " WHERE i.customer_id = ?"
            params.append(customer_id)
        
        query += " ORDER BY i.created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        invoices = []
        for row in cursor.fetchall():
            invoice = dict(row)
            invoice['items'] = json.loads(invoice.get('items', '[]')) if invoice.get('items') else []
            invoices.append(invoice)
        
        conn.close()
        return invoices
    
    def get_invoice(self, invoice_id: int) -> Optional[Dict]:
        """Get invoice by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.*, c.name as customer_name, c.phone as customer_phone, 
                   c.address as customer_address, c.email as customer_email, c.gstin as customer_gstin
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
            WHERE i.id = ?
        """, (invoice_id,))
        invoice = cursor.fetchone()
        conn.close()
        
        if invoice:
            invoice_dict = dict(invoice)
            invoice_dict['items'] = json.loads(invoice_dict['items']) if invoice_dict['items'] else []
            return invoice_dict
        return None
    
    def get_invoice_by_number(self, invoice_number: str) -> Optional[Dict]:
        """Get invoice by invoice number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.*, c.name as customer_name, c.phone as customer_phone, 
                   c.address as customer_address, c.email as customer_email, c.gstin as customer_gstin
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
            WHERE i.invoice_number = ?
        """, (invoice_number,))
        invoice = cursor.fetchone()
        conn.close()
        
        if invoice:
            invoice_dict = dict(invoice)
            invoice_dict['items'] = json.loads(invoice_dict['items']) if invoice_dict['items'] else []
            return invoice_dict
        return None
    
    def update_invoice(self, invoice_id: int, invoice: Dict) -> bool:
        """Update invoice details"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE invoices 
                SET customer_id = ?, subtotal = ?, discount_amount = ?, 
                    gst_amount = ?, sgst_amount = ?, cgst_amount = ?, 
                    total_amount = ?, items_json = ?, pdf_path = ?, 
                    status = ?, payment_method = ?, payment_status = ?, 
                    notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (invoice.get('customer_id'), invoice['subtotal'],
                  invoice.get('discount_amount', 0), invoice['gst_amount'],
                  invoice.get('sgst_amount', 0), invoice.get('cgst_amount', 0),
                  invoice['total_amount'], json.dumps(invoice['items']),
                  invoice.get('pdf_path'), invoice.get('status', 'completed'),
                  invoice.get('payment_method'), invoice.get('payment_status', 'pending'),
                  invoice.get('notes'), invoice_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating invoice: {e}")
            return False
    
    def delete_invoice(self, invoice_id: int) -> bool:
        """Delete invoice (and restore stock)"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get invoice items to restore stock
            cursor.execute("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
            items = cursor.fetchall()
            
            # Restore stock for each item
            for item in items:
                if item['product_id']:
                    self.update_stock(item['product_id'], int(item['quantity']), 
                                    'adjustment', invoice_id, f"Deleted invoice {invoice_id}")
            
            # Delete invoice (cascade will delete invoice_items)
            cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting invoice: {e}")
            return False
    
    def generate_invoice_number(self) -> str:
        """Generate next invoice number"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get shop settings for prefix
        cursor.execute("SELECT invoice_prefix FROM shop_settings WHERE id = 1")
        result = cursor.fetchone()
        prefix = result['invoice_prefix'] if result else 'INV'
        
        # Get last invoice number
        cursor.execute("""
            SELECT invoice_number FROM invoices 
            WHERE invoice_number LIKE ?
            ORDER BY created_at DESC LIMIT 1
        """, (f"{prefix}%",))
        result = cursor.fetchone()
        
        if result:
            last_number = result['invoice_number']
            # Extract numeric part
            numeric_part = last_number[len(prefix):]
            try:
                next_num = int(numeric_part) + 1
            except ValueError:
                next_num = 1
        else:
            next_num = 1
        
        conn.close()
        return f"{prefix}{next_num:06d}"
    
    # Analytics Methods
    def get_sales_summary(self, start_date: str = None, end_date: str = None) -> Dict:
        """Get sales summary for date range"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) as total_invoices, SUM(total_amount) as total_sales FROM invoices"
        params = []
        
        if start_date or end_date:
            conditions = []
            if start_date:
                conditions.append("DATE(created_at) >= ?")
                params.append(start_date)
            if end_date:
                conditions.append("DATE(created_at) <= ?")
                params.append(end_date)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_invoices': result['total_invoices'] or 0,
            'total_sales': result['total_sales'] or 0.0
        }
    
    def get_top_products(self, limit: int = 10, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get top selling products"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT ii.product_name, SUM(ii.quantity) as total_quantity, 
                   SUM(ii.total_price) as total_revenue
            FROM invoice_items ii
            JOIN invoices i ON ii.invoice_id = i.id
        """
        params = []
        
        if start_date or end_date:
            conditions = []
            if start_date:
                conditions.append("DATE(i.created_at) >= ?")
                params.append(start_date)
            if end_date:
                conditions.append("DATE(i.created_at) <= ?")
                params.append(end_date)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += """
            GROUP BY ii.product_name
            ORDER BY total_quantity DESC
            LIMIT ?
        """
        params.append(limit)
        
        cursor.execute(query, params)
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return products
    
    def get_top_customers(self, limit: int = 10, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get top customers by sales"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT c.name, c.phone, COUNT(i.id) as invoice_count, SUM(i.total_amount) as total_spent
            FROM customers c
            JOIN invoices i ON c.id = i.customer_id
        """
        params = []
        
        if start_date or end_date:
            conditions = []
            if start_date:
                conditions.append("DATE(i.created_at) >= ?")
                params.append(start_date)
            if end_date:
                conditions.append("DATE(i.created_at) <= ?")
                params.append(end_date)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
        
        query += """
            GROUP BY c.id
            ORDER BY total_spent DESC
            LIMIT ?
        """
        params.append(limit)
        
        cursor.execute(query, params)
        customers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return customers
