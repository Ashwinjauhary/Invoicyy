import qrcode
import os
from typing import Optional
from datetime import datetime

class QRCodeGenerator:
    """Generate QR codes for invoices and payments"""
    
    @staticmethod
    def generate_upi_payment_qr(upi_id: str, amount: float, shop_name: str, 
                               note: str = "", save_path: Optional[str] = None) -> str:
        """
        Generate UPI payment QR code
        
        Args:
            upi_id: UPI ID (e.g., shop@upi)
            amount: Payment amount
            shop_name: Shop name for display
            note: Payment note
            save_path: Path to save QR code image
            
        Returns:
            Path to generated QR code image
        """
        # Create UPI payment URL
        upi_url = f"upi://pay?pa={upi_id}&pn={shop_name}&am={amount:.2f}&cu=INR"
        
        if note:
            upi_url += f"&tn={note}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"qr_payment_{timestamp}.png"
        
        img.save(save_path)
        return save_path
    
    @staticmethod
    def generate_invoice_qr(invoice_number: str, customer_phone: str, 
                          shop_name: str, total_amount: float,
                          verification_url: str = "", save_path: Optional[str] = None) -> str:
        """
        Generate invoice verification QR code
        
        Args:
            invoice_number: Invoice number
            customer_phone: Customer phone number
            shop_name: Shop name
            total_amount: Total invoice amount
            verification_url: URL for invoice verification
            save_path: Path to save QR code image
            
        Returns:
            Path to generated QR code image
        """
        # Create invoice data
        invoice_data = {
            'invoice_number': invoice_number,
            'shop_name': shop_name,
            'customer_phone': customer_phone,
            'total_amount': total_amount,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'verification_url': verification_url
        }
        
        # Convert to string (you can customize the format)
        data_string = f"INV:{invoice_number}|SHOP:{shop_name}|PHONE:{customer_phone}|AMT:{total_amount}|DATE:{invoice_data['date']}"
        
        if verification_url:
            data_string += f"|URL:{verification_url}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data_string)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"qr_invoice_{timestamp}.png"
        
        img.save(save_path)
        return save_path
    
    @staticmethod
    def generate_business_card_qr(shop_name: str, phone: str, email: str, 
                                 address: str, gstin: str = "", save_path: Optional[str] = None) -> str:
        """
        Generate business card QR code with shop details
        
        Args:
            shop_name: Shop name
            phone: Shop phone number
            email: Shop email
            address: Shop address
            gstin: Shop GSTIN
            save_path: Path to save QR code image
            
        Returns:
            Path to generated QR code image
        """
        # Create vCard-like data
        card_data = f"""BEGIN:VCARD
VERSION:3.0
FN:{shop_name}
TEL:{phone}
EMAIL:{email}
ADR:{address}
{'ORG:' + shop_name}
{'NOTE:GSTIN: ' + gstin if gstin else ''}
END:VCARD"""
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(card_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"qr_business_{timestamp}.png"
        
        img.save(save_path)
        return save_path
    
    @staticmethod
    def generate_custom_qr(data: str, save_path: Optional[str] = None, 
                          box_size: int = 10, border: int = 4) -> str:
        """
        Generate custom QR code with any data
        
        Args:
            data: Data to encode in QR code
            save_path: Path to save QR code image
            box_size: Size of each box in pixels
            border: Border size in boxes
            
        Returns:
            Path to generated QR code image
        """
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save image
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"qr_custom_{timestamp}.png"
        
        img.save(save_path)
        return save_path
    
    @staticmethod
    def generate_qr_with_logo(data: str, logo_path: str, save_path: Optional[str] = None) -> str:
        """
        Generate QR code with logo in center
        
        Args:
            data: Data to encode
            logo_path: Path to logo image
            save_path: Path to save QR code image
            
        Returns:
            Path to generated QR code image
        """
        from PIL import Image
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create QR image
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Add logo if provided
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                
                # Calculate logo size (about 20% of QR code size)
                qr_width, qr_height = img.size
                logo_size = min(qr_width, qr_height) // 5
                
                # Resize logo
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                # Calculate position to center logo
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                
                # Paste logo
                img.paste(logo, pos)
            except Exception as e:
                print(f"Error adding logo to QR code: {e}")
        
        # Save image
        if save_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"qr_logo_{timestamp}.png"
        
        img.save(save_path)
        return save_path
    
    @staticmethod
    def create_qr_directory(base_path: str = "assets/qr_codes") -> str:
        """
        Create directory for QR codes if it doesn't exist
        
        Args:
            base_path: Base path for QR codes directory
            
        Returns:
            Path to QR codes directory
        """
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        return base_path
    
    @staticmethod
    def cleanup_old_qr_files(directory: str, days_old: int = 30):
        """
        Clean up old QR code files
        
        Args:
            directory: Directory containing QR codes
            days_old: Remove files older than this many days
        """
        import time
        
        if not os.path.exists(directory):
            return
        
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"Removed old QR file: {filename}")
                    except Exception as e:
                        print(f"Error removing {filename}: {e}")
