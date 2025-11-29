# 🧾 Invoice Maker - Professional Billing System

A comprehensive desktop-based billing solution for small and large shops with GST support, PDF generation, QR code payments, and complete customer management.

## ✨ Features

### 🏪 Shop Management
- **Shop Profile**: Complete shop details with logo, GSTIN, address, contact info
- **Settings Management**: Customizable invoice templates, GST rates, prefixes
- **Multi-User Support**: Admin and cashier roles (optional)

### 👥 Customer Management
- Add/edit customers with complete details
- Search customers by name, phone, or email
- GSTIN support for B2B customers
- Customer purchase history

### 📦 Product Management
- Add products with pricing, GST rates, categories
- Barcode support for quick scanning
- Stock management with low-stock alerts
- Auto-fill product details in invoices

### 📝 Invoice Creation
- **Dynamic Invoice Builder**: Add/remove items easily
- **Auto GST Calculations**: Support for 0%, 5%, 12%, 18%, 28% GST slabs
- **Discount Support**: Percentage discounts on items
- **Multiple Payment Methods**: Cash, Card, UPI, Net Banking, Cheque
- **Real-time Calculations**: Auto-calculate totals as you type

### 📄 PDF Generation
- **3 Professional Templates**: Clean, Modern, Minimalist
- **Complete Invoice Details**: Shop info, customer details, itemized billing
- **GST Breakup**: SGST/CGST calculations
- **QR Code Integration**: Payment QR codes on invoices

### 📊 Analytics & Reports
- **Sales Summary**: Daily, monthly, yearly sales
- **Top Products**: Best-selling items analysis
- **Top Customers**: Customer spending analysis
- **Export to Excel**: CSV/XLSX export support

### 🔧 Additional Features
- **Backup/Restore**: Database backup functionality
- **Low Stock Alerts**: Automatic notifications
- **Invoice History**: View, reprint, resend old invoices
- **Thermal Printer Support**: Generate receipt-style prints

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows/macOS/Linux

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd Invoice
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

### First Time Setup
1. Open the application
2. Go to **Settings** page
3. Fill in your shop details (name, address, GSTIN, phone, email)
4. Set your UPI ID for QR code payments
5. Upload your shop logo (optional)
6. Save settings

## 📱 Usage Guide

### Creating Your First Invoice
1. Click **"📝 New Invoice"** from the sidebar
2. Select a customer or choose "Walk-in Customer"
3. Click **"➕ Add Item"** to add products
4. Select products from dropdown or add new ones
5. Adjust quantities, discounts if needed
6. Review automatic GST calculations
7. Add notes if required
8. Click **"💾 Save Invoice"** to save
9. Click **"📄 Generate PDF"** to create invoice PDF

### Managing Customers
1. Go to **"👥 Customers"** page
2. Click **"➕ Add New Customer"** for new customers
3. Use search to find existing customers
4. Click **"Edit"** to modify customer details

### Managing Products
1. Go to **"📦 Products"** page
2. Click **"➕ Add New Product"** to add items
3. Set price, GST rate, stock quantity
4. Add barcode for scanning support
5. Monitor low-stock alerts on dashboard

### Viewing Reports
1. Go to **"📈 Reports"** page
2. Select date range for sales summary
3. View top products and customers
4. Export data to Excel if needed

## 🎯 GST Features

### Supported GST Slabs
- **0%**: Exempt goods
- **5%**: Essential goods
- **12%**: Standard rate
- **18%**: Standard rate  
- **28%**: Luxury/sin goods

### GST Calculations
- **Automatic SGST/CGST Split**: Equal division of total GST
- **Item-wise GST**: Different GST rates for different items
- **GST Breakup Display**: Clear GST breakdown in invoices
- **B2B Support**: GSTIN validation for business customers

## 🖨️ Printing Options

### PDF Templates
1. **Template 1 (Clean)**: Professional layout with all details
2. **Template 2 (Modern)**: Contemporary design with colored headers
3. **Template 3 (Minimalist)**: Simple, clean layout

### Thermal Printing
- Generate receipt-style PDFs for thermal printers
- 58mm/80mm paper support
- Compact format for quick receipts

## 💾 Data Management

### Database
- **SQLite**: Local, lightweight database
- **Auto-backup**: Manual backup functionality
- **Data Portability**: Easy export and migration

### Backup Process
1. Click **"💾 Backup Data"** from sidebar
2. Choose backup location
3. Database copied to selected location

## 🔧 Advanced Features

### Barcode Scanning (Optional)
```bash
# Install additional packages for barcode support
pip install pyzbar opencv-python
```

### WhatsApp Integration (Bonus)
```bash
# Install for WhatsApp invoice sending
pip install selenium webdriver-manager
```

### Multi-User Support
- **Admin**: Full access to all features
- **Cashier**: Limited to invoice creation
- User authentication and role management

## 📁 Project Structure

```
invoice_maker/
│
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── database/              # Database components
│   ├── db.py             # Database manager class
│   └── schema.sql        # Database schema
│
├── logic/                # Business logic
│   ├── gst_calculator.py # GST calculations
│   ├── pdf_generator.py  # PDF generation
│   └── qr_generator.py   # QR code generation
│
├── ui/                   # UI components (if using .ui files)
│   ├── dashboard.ui
│   ├── new_invoice.ui
│   ├── customer_form.ui
│   └── settings.ui
│
├── assets/               # Static assets
│   ├── logo.png         # Shop logos
│   └── qr_codes/        # Generated QR codes
│
└── dist/                # Build output (EXE files)
```

## 🎨 Customization

### Adding Your Own Templates
1. Create new template method in `logic/pdf_generator.py`
2. Follow the existing template structure
3. Update template combo box in settings

### Custom GST Rates
1. Modify `GST_RATES` list in `logic/gst_calculator.py`
2. Update UI combo boxes accordingly

### Branding
1. Replace logo in `assets/` folder
2. Modify colors in `main.py` stylesheet
3. Customize invoice templates

## 🐛 Troubleshooting

### Common Issues

**Application won't start**
- Check Python version (3.8+ required)
- Verify all dependencies installed: `pip install -r requirements.txt`

**PDF generation fails**
- Ensure ReportLab installed correctly
- Check file write permissions
- Verify logo image format (PNG/JPG)

**Database errors**
- Check write permissions in application directory
- Ensure schema.sql is accessible
- Try deleting database file to reset

**QR code issues**
- Verify qrcode package installed
- Check UPI ID format (username@upi)

### Getting Help
1. Check this README first
2. Review error messages carefully
3. Ensure all dependencies are current
4. Test with sample data first

## 📈 Performance Tips

- **Regular Backups**: Backup data weekly
- **Stock Management**: Update stock regularly
- **Database Cleanup**: Archive old invoices periodically
- **Logo Optimization**: Use compressed PNG files

## 🔒 Security Considerations

- **Local Database**: All data stored locally, secure by default
- **No Internet Required**: Works completely offline
- **Data Privacy**: No data shared with external services
- **Backup Security**: Encrypt sensitive backup files

## 🚀 Creating EXE File

### Build Process
```bash
# Install PyInstaller
pip install pyinstaller

# Build EXE
pyinstaller --onefile --windowed main.py

# Find EXE in dist/ folder
```

### Distribution
- EXE file in `dist/` folder
- No Python installation needed
- Includes all dependencies
- Ready for commercial distribution

## 📞 Support

### For Issues
1. Check error logs
2. Verify data integrity
3. Test with minimal setup
4. Contact support with details

### Feature Requests
- Email: support@example.com
- GitHub: Create issue in repository
- Include detailed requirements

## 📜 License

This project is open-source. Check LICENSE file for details.

## 🙏 Acknowledgments

- **GitHub Discussions**: Join our community discussions
- **Feature Updates**: Follow our repository for updates
- **Contributions**: Welcome pull requests and suggestions

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with ❤️ for small businesses in India**

*For support: ashwin2431333@gmail.com*

Perfect for:
🟢 Kirana stores  
🟡 Retail shops  
🔵 Wholesale businesses  
🟠 Service providers  
🟣 Small enterprises  

**Invoice Maker** - Making billing simple, professional, and GST-compliant!
