from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import black, blue, gray, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.platypus import PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime
from typing import Dict, List, Optional
from .gst_calculator import GSTCalculator

class PDFGenerator:
    """Generate professional PDF invoices"""
    
    def __init__(self):
        self.page_size = A4
        self.margin = 0.5 * inch
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='InvoiceTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=blue
        ))
        
        # Header style
        self.styles.add(ParagraphStyle(
            name='HeaderStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=gray
        ))
        
        # Bold style
        self.styles.add(ParagraphStyle(
            name='BoldStyle',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='FooterStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            alignment=TA_CENTER,
            textColor=gray
        ))
    
    def generate_invoice_pdf(self, invoice_data: Dict, shop_data: Dict, 
                           customer_data: Dict, template: str = "template1",
                           qr_code_path: Optional[str] = None,
                           logo_path: Optional[str] = None,
                           save_path: Optional[str] = None) -> str:
        """
        Generate invoice PDF
        
        Args:
            invoice_data: Invoice information
            shop_data: Shop information
            customer_data: Customer information
            template: Template style to use
            qr_code_path: Path to QR code image
            logo_path: Path to shop logo
            save_path: Path to save PDF
            
        Returns:
            Path to generated PDF
        """
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"invoice_{invoice_data['invoice_number']}_{timestamp}.pdf"
        
        # Create PDF document
        doc = SimpleDocTemplate(
            save_path,
            pagesize=self.page_size,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Build story (content)
        story = []
        
        if template == "template1":
            story = self._build_template1(invoice_data, shop_data, customer_data, qr_code_path, logo_path)
        elif template == "template2":
            story = self._build_template2(invoice_data, shop_data, customer_data, qr_code_path, logo_path)
        else:
            story = self._build_template3(invoice_data, shop_data, customer_data, qr_code_path, logo_path)
        
        # Build PDF
        doc.build(story)
        return save_path
    
    def _build_template1(self, invoice_data: Dict, shop_data: Dict, 
                         customer_data: Dict, qr_code_path: Optional[str], 
                         logo_path: Optional[str]) -> List:
        """Build Template 1 - Clean and professional"""
        story = []
        
        # Header with logo and shop info
        header_table_data = []
        
        # Left side - Shop info
        shop_info = []
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=2*inch, height=1*inch)
                shop_info.append(logo)
            except:
                pass
        
        shop_info.append(Paragraph(f"<b>{shop_data.get('shop_name', 'Shop Name')}</b>", self.styles['BoldStyle']))
        shop_info.append(Paragraph(shop_data.get('address', ''), self.styles['Normal']))
        shop_info.append(Paragraph(f"Phone: {shop_data.get('phone', '')}", self.styles['Normal']))
        shop_info.append(Paragraph(f"Email: {shop_data.get('email', '')}", self.styles['Normal']))
        if shop_data.get('gstin'):
            shop_info.append(Paragraph(f"GSTIN: {shop_data['gstin']}", self.styles['Normal']))
        
        # Right side - Invoice info
        invoice_info = [
            Paragraph(f"<b>INVOICE</b>", self.styles['InvoiceTitle']),
            Paragraph(f"<b>Invoice No:</b> {invoice_data['invoice_number']}", self.styles['Normal']),
            Paragraph(f"<b>Date:</b> {invoice_data.get('created_at', datetime.now().strftime('%Y-%m-%d'))}", self.styles['Normal']),
            Paragraph("", self.styles['Normal'])  # Spacer
        ]
        
        if qr_code_path and os.path.exists(qr_code_path):
            try:
                qr_img = Image(qr_code_path, width=1.5*inch, height=1.5*inch)
                invoice_info.append(qr_img)
            except:
                pass
        
        header_table_data.append([shop_info, invoice_info])
        
        header_table = Table(header_table_data, colWidths=[4*inch, 3*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 20))
        
        # Customer information
        if customer_data:
            customer_table_data = [
                [Paragraph("<b>BILL TO:</b>", self.styles['BoldStyle']), 
                 Paragraph("", self.styles['Normal'])],
                [Paragraph(customer_data.get('name', ''), self.styles['Normal']), 
                 Paragraph("", self.styles['Normal'])],
                [Paragraph(customer_data.get('address', ''), self.styles['Normal']), 
                 Paragraph("", self.styles['Normal'])],
                [Paragraph(f"Phone: {customer_data.get('phone', '')}", self.styles['Normal']), 
                 Paragraph("", self.styles['Normal'])],
            ]
            
            if customer_data.get('gstin'):
                customer_table_data.append([Paragraph(f"GSTIN: {customer_data['gstin']}", self.styles['Normal']), 
                                          Paragraph("", self.styles['Normal'])])
            
            customer_table = Table(customer_table_data, colWidths=[4*inch, 3*inch])
            customer_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            
            story.append(customer_table)
            story.append(Spacer(1, 20))
        
        # Items table
        items_data = [["ITEM", "QTY", "RATE", "GST%", "AMOUNT"]]
        
        for item in invoice_data.get('items', []):
            items_data.append([
                item.get('name', ''),
                str(item.get('quantity', 0)),
                f"₹{item.get('price', 0):.2f}",
                f"{item.get('gst_percent', 18):.0f}%",
                f"₹{item.get('total', 0):.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[3*inch, 0.8*inch, 1*inch, 0.8*inch, 1.2*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 20))
        
        # Totals
        totals_data = [
            ["", "", "", "Subtotal:", f"₹{invoice_data.get('subtotal', 0):.2f}"],
            ["", "", "", "GST:", f"₹{invoice_data.get('gst_amount', 0):.2f}"],
            ["", "", "", "SGST:", f"₹{invoice_data.get('sgst_amount', 0):.2f}"],
            ["", "", "", "CGST:", f"₹{invoice_data.get('cgst_amount', 0):.2f}"],
            ["", "", "", "Total:", f"₹{invoice_data.get('total_amount', 0):.2f}"],
        ]
        
        totals_table = Table(totals_data, colWidths=[3*inch, 0.8*inch, 1*inch, 1.2*inch, 1.2*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (3, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (3, 4), (4, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (3, 4), (4, 4), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 30))
        
        # Footer
        footer_text = "Thank you for your business!"
        if invoice_data.get('notes'):
            footer_text += f"\n\nNotes: {invoice_data['notes']}"
        
        story.append(Paragraph(footer_text, self.styles['FooterStyle']))
        
        return story
    
    def _build_template2(self, invoice_data: Dict, shop_data: Dict, 
                         customer_data: Dict, qr_code_path: Optional[str], 
                         logo_path: Optional[str]) -> List:
        """Build Template 2 - Modern design"""
        story = []
        
        # Modern header with background
        story.append(Spacer(1, 20))
        
        # Shop info centered
        story.append(Paragraph(f"<b>{shop_data.get('shop_name', 'Shop Name')}</b>", self.styles['InvoiceTitle']))
        story.append(Paragraph(shop_data.get('address', ''), self.styles['Normal']))
        story.append(Paragraph(f"Phone: {shop_data.get('phone', '')} | Email: {shop_data.get('email', '')}", self.styles['Normal']))
        if shop_data.get('gstin'):
            story.append(Paragraph(f"GSTIN: {shop_data['gstin']}", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Invoice details in a box
        invoice_details = [
            ["Invoice Number:", invoice_data['invoice_number']],
            ["Date:", invoice_data.get('created_at', datetime.now().strftime('%Y-%m-%d'))],
            ["Status:", invoice_data.get('status', 'Completed').upper()],
        ]
        
        if customer_data.get('name'):
            invoice_details.append(["Customer:", customer_data['name']])
        
        details_table = Table(invoice_details, colWidths=[2*inch, 3*inch])
        details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), (0.95, 0.95, 0.95)),
            ('GRID', (0, 0), (-1, -1), 1, gray),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(details_table)
        story.append(Spacer(1, 20))
        
        # QR Code on the right if available
        if qr_code_path and os.path.exists(qr_code_path):
            try:
                qr_img = Image(qr_code_path, width=1.2*inch, height=1.2*inch)
                qr_table = Table([[qr_img]], colWidths=[1.2*inch])
                qr_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
                ]))
                story.append(qr_table)
                story.append(Spacer(1, 10))
            except:
                pass
        
        # Items table with alternating colors
        items_data = [["ITEM DESCRIPTION", "QTY", "RATE", "GST%", "TOTAL"]]
        
        for i, item in enumerate(invoice_data.get('items', [])):
            bg_color = (0.98, 0.98, 0.98) if i % 2 == 0 else white
            items_data.append([
                item.get('name', ''),
                str(item.get('quantity', 0)),
                f"₹{item.get('price', 0):.2f}",
                f"{item.get('gst_percent', 18):.0f}%",
                f"₹{item.get('total', 0):.2f}"
            ])
        
        items_table = Table(items_data, colWidths=[3.5*inch, 0.7*inch, 0.8*inch, 0.7*inch, 1.3*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), blue),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), white),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Left align item names
        ]))
        
        story.append(items_table)
        story.append(Spacer(1, 20))
        
        # GST Breakdown
        gst_breakdown = GSTCalculator.generate_gst_breakdown_text(invoice_data.get('items', []))
        if gst_breakdown:
            story.append(Paragraph("<b>GST Breakdown:</b>", self.styles['BoldStyle']))
            story.append(Paragraph(gst_breakdown, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Totals section
        totals_data = [
            ["Subtotal", f"₹{invoice_data.get('subtotal', 0):.2f}"],
            ["GST Amount", f"₹{invoice_data.get('gst_amount', 0):.2f}"],
            ["SGST", f"₹{invoice_data.get('sgst_amount', 0):.2f}"],
            ["CGST", f"₹{invoice_data.get('cgst_amount', 0):.2f}"],
            ["<b>GRAND TOTAL</b>", f"<b>₹{invoice_data.get('total_amount', 0):.2f}</b>"],
        ]
        
        totals_table = Table(totals_data, colWidths=[3*inch, 2*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 4), (1, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 4), (1, 4), 12),
            ('TEXTCOLOR', (0, 4), (1, 4), blue),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 4), (1, 4), 12),
            ('LINEBELOW', (0, 3), (1, 3), 1, gray),
        ]))
        
        story.append(totals_table)
        story.append(Spacer(1, 30))
        
        # Footer with terms
        terms = [
            "Terms & Conditions:",
            "1. Goods once sold will not be taken back.",
            "2. Payment due within 30 days.",
            "3. Subject to [City] jurisdiction."
        ]
        
        for term in terms:
            story.append(Paragraph(term, self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("Thank you for shopping with us!", self.styles['FooterStyle']))
        
        return story
    
    def _build_template3(self, invoice_data: Dict, shop_data: Dict, 
                         customer_data: Dict, qr_code_path: Optional[str], 
                         logo_path: Optional[str]) -> List:
        """Build Template 3 - Minimalist design"""
        story = []
        
        # Minimal header
        story.append(Paragraph(f"<b>{shop_data.get('shop_name', 'Shop Name')}</b>", self.styles['Heading2']))
        story.append(Paragraph(shop_data.get('address', ''), self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Simple invoice info
        story.append(Paragraph(f"Invoice #{invoice_data['invoice_number']}", self.styles['Heading3']))
        story.append(Paragraph(f"Date: {invoice_data.get('created_at', datetime.now().strftime('%Y-%m-%d'))}", self.styles['Normal']))
        
        if customer_data:
            story.append(Paragraph(f"Bill to: {customer_data.get('name', '')}", self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Simple items list
        for item in invoice_data.get('items', []):
            item_text = f"{item.get('name', '')} - {item.get('quantity', 0)} x ₹{item.get('price', 0):.2f} = ₹{item.get('total', 0):.2f}"
            story.append(Paragraph(item_text, self.styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Simple totals
        story.append(Paragraph(f"Subtotal: ₹{invoice_data.get('subtotal', 0):.2f}", self.styles['Normal']))
        story.append(Paragraph(f"GST: ₹{invoice_data.get('gst_amount', 0):.2f}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Total: ₹{invoice_data.get('total_amount', 0):.2f}</b>", self.styles['BoldStyle']))
        
        if qr_code_path and os.path.exists(qr_code_path):
            story.append(Spacer(1, 20))
            try:
                qr_img = Image(qr_code_path, width=1*inch, height=1*inch)
                story.append(qr_img)
            except:
                pass
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("Thank you!", self.styles['FooterStyle']))
        
        return story
    
    def generate_receipt_pdf(self, receipt_data: Dict, shop_data: Dict, 
                           save_path: Optional[str] = None) -> str:
        """Generate thermal printer style receipt"""
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"receipt_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(
            save_path,
            pagesize=(4*inch, 8*inch),  # Thermal paper size
            leftMargin=0.2*inch,
            rightMargin=0.2*inch,
            topMargin=0.2*inch,
            bottomMargin=0.2*inch
        )
        
        story = []
        
        # Centered shop name
        story.append(Paragraph(f"<b>{shop_data.get('shop_name', 'Shop Name')}</b>", self.styles['Heading2']))
        story.append(Paragraph(shop_data.get('address', ''), self.styles['Normal']))
        story.append(Paragraph(f"Phone: {shop_data.get('phone', '')}", self.styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Receipt info
        story.append(Paragraph("=" * 30, self.styles['Normal']))
        story.append(Paragraph(f"Receipt: {receipt_data.get('receipt_number', '')}", self.styles['Normal']))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['Normal']))
        story.append(Paragraph("=" * 30, self.styles['Normal']))
        story.append(Spacer(1, 8))
        
        # Items
        for item in receipt_data.get('items', []):
            item_line = f"{item.get('name', '')[:20]}"
            price_line = f"{item.get('quantity', 0)} x {item.get('price', 0):.2f}"
            total_line = f"{item.get('total', 0):.2f}"
            
            story.append(Paragraph(item_line, self.styles['Normal']))
            story.append(Paragraph(f"{price_line}    {total_line}", self.styles['Normal']))
        
        story.append(Spacer(1, 8))
        story.append(Paragraph("-" * 30, self.styles['Normal']))
        
        # Totals
        story.append(Paragraph(f"Subtotal: {receipt_data.get('subtotal', 0):.2f}", self.styles['Normal']))
        story.append(Paragraph(f"GST: {receipt_data.get('gst_amount', 0):.2f}", self.styles['Normal']))
        story.append(Paragraph(f"Total: {receipt_data.get('total_amount', 0):.2f}", self.styles['BoldStyle']))
        
        story.append(Spacer(1, 12))
        story.append(Paragraph("Thank you!", self.styles['Normal']))
        
        doc.build(story)
        return save_path
