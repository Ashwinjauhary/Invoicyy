#!/usr/bin/env python3
"""
🧾 Invoice Maker - Web Launcher
Quick start script for mobile-responsive web version
"""

import subprocess
import sys
import os
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'plotly',
        'reportlab',
        'Pillow',
        'qrcode'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'Pillow':
                import PIL
            elif package == 'qrcode':
                import qrcode
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install"
            ] + missing_packages)
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please run:")
            print("pip install -r requirements_web.txt")
            return False
    
    return True

def start_web_app():
    """Start the Streamlit web application"""
    print("🚀 Starting Invoice Maker Web App...")
    print("📱 Mobile Responsive | Works on all devices")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Change to project directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Streamlit configuration
    config_options = [
        "--server.port", "8501",
        "--server.address", "0.0.0.0",  # Allow network access
        "--server.headless", "false",    # Show in browser
        "--browser.gatherUsageStats", "false",
        "--global.developmentMode", "false",
        "--logger.level", "info",
        "--runner.fastReruns", "true",
        "--server.fileWatcherType", "none",
        "--server.maxUploadSize", "200",  # 200MB max upload
    ]
    
    try:
        # Start Streamlit
        print("🌐 Starting web server...")
        print("🔗 Local: http://localhost:8501")
        print("🔗 Network: http://YOUR_IP:8501")
        print("📱 Mobile: Access from phone using network URL")
        print("=" * 50)
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "web_app.py"
        ] + config_options)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if port 8501 is available")
        print("2. Install required packages: pip install -r requirements_web.txt")
        print("3. Check Python version (3.8+ recommended)")

def show_info():
    """Show application information"""
    print("""
🧾 Invoice Maker - Web Version
================================

📱 Mobile Responsive Features:
• Works on Desktop, Tablet & Mobile
• Touch-friendly interface
• Adaptive layouts
• Fast loading
• No installation required

🌐 Access Methods:
• Local: http://localhost:8501
• Network: http://YOUR_IP:8501
• Mobile: Use network URL on phone

🚀 Quick Start:
1. Run: python run_web.py
2. Open browser to localhost:8501
3. Start creating invoices!

📦 Requirements:
• Python 3.8+
• Modern web browser
• Internet connection (for mobile access)

💡 Features:
• Create invoices on-the-go
• Customer management
• Product management
• GST calculations
• PDF generation
• Mobile-optimized UI

🔧 Configuration:
• Port: 8501 (default)
• Network access: Enabled
• File uploads: Up to 200MB
• Auto-reload: Enabled

📞 Support:
• Email: support@invoicemaker.com
• Web: www.invoicemaker.com
""")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Invoice Maker Web Launcher")
    parser.add_argument("--info", action="store_true", help="Show application information")
    parser.add_argument("--port", type=int, default=8501, help="Port number (default: 8501)")
    parser.add_argument("--host", default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    
    args = parser.parse_args()
    
    if args.info:
        show_info()
    else:
        # Override port and host if provided
        if args.port != 8501 or args.host != "0.0.0.0":
            print(f"🔧 Custom settings: Port={args.port}, Host={args.host}")
        
        start_web_app()
