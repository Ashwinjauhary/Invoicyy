#!/usr/bin/env python3
"""
🧾 Simple GST Calculator for Web Version
Fallback implementation for Streamlit deployment
"""

class GSTCalculator:
    """Simple GST calculation class"""
    
    @staticmethod
    def calculate_item_total(quantity, price, discount_percent, gst_percent):
        """Calculate total amount for an item with GST"""
        # Calculate basic amount
        basic_amount = quantity * price
        
        # Apply discount
        discount_amount = basic_amount * (discount_percent / 100)
        after_discount = basic_amount - discount_amount
        
        # Calculate GST
        gst_amount = after_discount * (gst_percent / 100)
        
        # Split GST (for Indian tax system)
        sgst_amount = gst_amount / 2
        cgst_amount = gst_amount / 2
        
        # Total amount
        total_amount = after_discount + gst_amount
        
        return {
            'basic_amount': basic_amount,
            'discount_amount': discount_amount,
            'after_discount': after_discount,
            'gst_amount': gst_amount,
            'sgst_amount': sgst_amount,
            'cgst_amount': cgst_amount,
            'total_amount': total_amount
        }
    
    @staticmethod
    def calculate_invoice_totals(items):
        """Calculate totals for all items in invoice"""
        subtotal = 0
        total_gst = 0
        total_sgst = 0
        total_cgst = 0
        
        for item in items:
            subtotal += item.get('basic_amount', 0)
            total_gst += item.get('gst_amount', 0)
            total_sgst += item.get('sgst_amount', 0)
            total_cgst += item.get('cgst_amount', 0)
        
        grand_total = subtotal + total_gst
        
        return {
            'subtotal': subtotal,
            'total_gst': total_gst,
            'total_sgst': total_sgst,
            'total_cgst': total_cgst,
            'grand_total': grand_total
        }
