#!/bin/bash

echo "🧾 Invoice Maker - Quick Installer for Linux/macOS"
echo "=============================================="
echo

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found! Please install Python first."
    echo "📥 Download from: https://www.python.org/downloads/"
    echo
    exit 1
fi

echo "✅ Python3 detected"
echo

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 not found! Please install pip first."
    echo "📥 Run: sudo apt-get install python3-pip (Ubuntu/Debian)"
    echo "📥 Run: brew install python3 (macOS)"
    echo
    exit 1
fi

echo "✅ pip3 detected"
echo

# Install dependencies
echo "📦 Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install streamlit pandas plotly reportlab pillow "qrcode[pil]" requests

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Create launcher script
echo "🚀 Creating launcher script..."
LAUNCHER="$SCRIPT_DIR/run_invoice_maker.sh"

cat > "$LAUNCHER" << EOF
#!/bin/bash
echo "🧾 Starting Invoice Maker..."
cd "$SCRIPT_DIR"
python3 web_app.py
EOF

chmod +x "$LAUNCHER"

echo "✅ Launcher script created: $LAUNCHER"
echo

# Create desktop entry (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📱 Creating desktop entry..."
    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"
    
    cat > "$DESKTOP_DIR/invoicemaker.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Invoice Maker
Comment=Professional Billing System
Exec=$LAUNCHER
Icon=$SCRIPT_DIR/icon.png
Terminal=false
Categories=Office;Finance;
Keywords=invoice;billing;gst;accounting;
EOF
    
    chmod +x "$DESKTOP_DIR/invoicemaker.desktop"
    echo "✅ Desktop entry created"
fi

# Create macOS app bundle (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Creating macOS app bundle..."
    APP_DIR="$HOME/Applications/Invoice Maker.app"
    CONTENTS_DIR="$APP_DIR/Contents"
    MACOS_DIR="$CONTENTS_DIR/MacOS"
    
    mkdir -p "$MACOS_DIR"
    
    # Create Info.plist
    cat > "$CONTENTS_DIR/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>run_invoice_maker</string>
    <key>CFBundleIdentifier</key>
    <string>com.invoicemaker.app</string>
    <key>CFBundleName</key>
    <string>Invoice Maker</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
    
    # Create executable
    cat > "$MACOS_DIR/run_invoice_maker" << EOF
#!/bin/bash
echo "🧾 Starting Invoice Maker..."
cd "$SCRIPT_DIR"
python3 web_app.py
EOF
    
    chmod +x "$MACOS_DIR/run_invoice_maker"
    echo "✅ macOS app bundle created"
fi

echo
echo "🎉 Installation completed successfully!"
echo "===================================="
echo "📁 Installation Directory: $SCRIPT_DIR"
echo "🚀 Launch Invoice Maker:"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "   • Applications menu > Office > Invoice Maker"
    echo "   • Run: $LAUNCHER"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "   • Launchpad > Invoice Maker"
    echo "   • Run: open '$APP_DIR'"
fi
echo "   • Command line: cd $SCRIPT_DIR && python3 web_app.py"
echo
echo "📱 Invoice Maker will open in your browser!"
echo

# Ask to launch
read -p "🚀 Launch Invoice Maker now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 Starting Invoice Maker..."
    sleep 2
    open "http://localhost:8501" 2>/dev/null || xdg-open "http://localhost:8501" 2>/dev/null || echo "Please open http://localhost:8501 in your browser"
    cd "$SCRIPT_DIR"
    python3 web_app.py
else
    echo "👋 Installation complete! Launch Invoice Maker from Applications menu."
fi
