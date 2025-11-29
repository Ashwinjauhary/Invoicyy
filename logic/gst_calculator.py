from typing import Dict, List, Tuple

class GSTCalculator:
    """GST calculation utilities for Indian tax system"""
    
    # GST rates in India
    GST_RATES = [0, 5, 12, 18, 28]
    
    @staticmethod
    def calculate_gst(amount: float, gst_percent: float) -> Tuple[float, float, float]:
        """
        Calculate GST, SGST, and CGST from amount
        
        Args:
            amount: Base amount (before GST)
            gst_percent: GST percentage (0, 5, 12, 18, 28)
            
        Returns:
            Tuple of (total_gst, sgst_amount, cgst_amount)
        """
        total_gst = amount * (gst_percent / 100)
        sgst_amount = total_gst / 2
        cgst_amount = total_gst / 2
        
        return round(total_gst, 2), round(sgst_amount, 2), round(cgst_amount, 2)
    
    @staticmethod
    def calculate_total_with_gst(base_amount: float, gst_percent: float) -> float:
        """
        Calculate total amount including GST
        
        Args:
            base_amount: Base amount before GST
            gst_percent: GST percentage
            
        Returns:
            Total amount including GST
        """
        total_gst, _, _ = GSTCalculator.calculate_gst(base_amount, gst_percent)
        return round(base_amount + total_gst, 2)
    
    @staticmethod
    def extract_gst_from_total(total_amount: float, gst_percent: float) -> Tuple[float, float, float]:
        """
        Extract base amount and GST from total amount
        
        Args:
            total_amount: Total amount including GST
            gst_percent: GST percentage
            
        Returns:
            Tuple of (base_amount, total_gst, sgst_amount, cgst_amount)
        """
        # Base amount = Total / (1 + GST%/100)
        base_amount = total_amount / (1 + gst_percent / 100)
        total_gst, sgst_amount, cgst_amount = GSTCalculator.calculate_gst(base_amount, gst_percent)
        
        return round(base_amount, 2), round(total_gst, 2), round(sgst_amount, 2), round(cgst_amount, 2)
    
    @staticmethod
    def calculate_item_total(quantity: float, unit_price: float, discount_percent: float = 0, gst_percent: float = 18) -> Dict:
        """
        Calculate total for a single item including discount and GST
        
        Args:
            quantity: Quantity of items
            unit_price: Price per unit
            discount_percent: Discount percentage (0-100)
            gst_percent: GST percentage
            
        Returns:
            Dictionary with all calculation details
        """
        # Calculate base amount
        base_amount = quantity * unit_price
        
        # Apply discount
        discount_amount = base_amount * (discount_percent / 100)
        amount_after_discount = base_amount - discount_amount
        
        # Calculate GST on discounted amount
        total_gst, sgst_amount, cgst_amount = GSTCalculator.calculate_gst(amount_after_discount, gst_percent)
        
        # Final total
        total_amount = amount_after_discount + total_gst
        
        return {
            'base_amount': round(base_amount, 2),
            'discount_amount': round(discount_amount, 2),
            'amount_after_discount': round(amount_after_discount, 2),
            'gst_percent': gst_percent,
            'total_gst': round(total_gst, 2),
            'sgst_amount': round(sgst_amount, 2),
            'cgst_amount': round(cgst_amount, 2),
            'total_amount': round(total_amount, 2)
        }
    
    @staticmethod
    def calculate_invoice_totals(items: List[Dict]) -> Dict:
        """
        Calculate totals for entire invoice
        
        Args:
            items: List of item dictionaries with calculation details
            
        Returns:
            Dictionary with invoice totals
        """
        subtotal = 0
        total_discount = 0
        total_gst = 0
        total_sgst = 0
        total_cgst = 0
        grand_total = 0
        
        for item in items:
            subtotal += item.get('amount_after_discount', 0)
            total_discount += item.get('discount_amount', 0)
            total_gst += item.get('total_gst', 0)
            total_sgst += item.get('sgst_amount', 0)
            total_cgst += item.get('cgst_amount', 0)
            grand_total += item.get('total_amount', 0)
        
        return {
            'subtotal': round(subtotal, 2),
            'total_discount': round(total_discount, 2),
            'total_gst': round(total_gst, 2),
            'total_sgst': round(total_sgst, 2),
            'total_cgst': round(total_cgst, 2),
            'grand_total': round(grand_total, 2)
        }
    
    @staticmethod
    def validate_gst_rate(gst_percent: float) -> bool:
        """
        Validate if GST rate is valid
        
        Args:
            gst_percent: GST percentage to validate
            
        Returns:
            True if valid, False otherwise
        """
        return gst_percent in GSTCalculator.GST_RATES
    
    @staticmethod
    def get_gst_slab_description(gst_percent: float) -> str:
        """
        Get description for GST slab
        
        Args:
            gst_percent: GST percentage
            
        Returns:
            Description string
        """
        descriptions = {
            0: "Exempt",
            5: "Essential Goods",
            12: "Standard Rate",
            18: "Standard Rate", 
            28: "Luxury/Sin Goods"
        }
        return descriptions.get(gst_percent, "Unknown Rate")
    
    @staticmethod
    def format_gst_amount(amount: float) -> str:
        """
        Format GST amount for display
        
        Args:
            amount: GST amount
            
        Returns:
            Formatted string
        """
        return f"₹{amount:.2f}"
    
    @staticmethod
    def generate_gst_breakdown_text(items: List[Dict]) -> str:
        """
        Generate GST breakdown text for invoice
        
        Args:
            items: List of item dictionaries
            
        Returns:
            Formatted GST breakdown text
        """
        # Group items by GST rate
        gst_groups = {}
        for item in items:
            gst_rate = item.get('gst_percent', 18)
            if gst_rate not in gst_groups:
                gst_groups[gst_rate] = {
                    'taxable_amount': 0,
                    'gst_amount': 0,
                    'sgst_amount': 0,
                    'cgst_amount': 0
                }
            
            gst_groups[gst_rate]['taxable_amount'] += item.get('amount_after_discount', 0)
            gst_groups[gst_rate]['gst_amount'] += item.get('total_gst', 0)
            gst_groups[gst_rate]['sgst_amount'] += item.get('sgst_amount', 0)
            gst_groups[gst_rate]['cgst_amount'] += item.get('cgst_amount', 0)
        
        # Generate breakdown text
        breakdown_lines = []
        for rate in sorted(gst_groups.keys()):
            group = gst_groups[rate]
            if rate == 0:
                breakdown_lines.append(f"Exempt: ₹{group['taxable_amount']:.2f}")
            else:
                breakdown_lines.append(
                    f"GST @ {rate}%: ₹{group['taxable_amount']:.2f} | "
                    f"SGST: ₹{group['sgst_amount']:.2f} | "
                    f"CGST: ₹{group['cgst_amount']:.2f}"
                )
        
        return "\n".join(breakdown_lines) if breakdown_lines else "No GST applicable"
