#!/usr/bin/env python3
"""
Invoice Maker - Build Script
Creates distributable EXE file with all dependencies
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def create_icon():
    """Create a simple icon file if not exists"""
    icon_path = "assets/icon.ico"
    if not os.path.exists(icon_path):
        print("Creating default icon...")
        os.makedirs("assets", exist_ok=True)
        
        # Create a simple text-based icon placeholder
        # In production, use a real .ico file
        with open(icon_path, "w") as f:
            f.write("icon_placeholder")
        print(f"Icon placeholder created at {icon_path}")

def build_exe():
    """Build the EXE file using PyInstaller"""
    print("🚀 Building Invoice Maker EXE...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Create icon
    create_icon()
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single EXE
        "--windowed",                    # No console window
        "--name=InvoiceMaker",          # EXE name
        "--distpath=dist",              # Output directory
        "--workpath=build",             # Build directory
        "--specpath=build",             # Spec file location
        "--clean",                      # Clean build
        "main.py"                       # Main script
    ]
    
    try:
        print("🔨 Running PyInstaller...")
        subprocess.check_call(cmd)
        print("✅ Build completed successfully!")
        
        # Check if EXE was created
        exe_path = "dist/InvoiceMaker.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📦 EXE created: {exe_path} ({size_mb:.1f} MB)")
        else:
            print("❌ EXE not found!")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def create_portable_package():
    """Create portable ZIP package"""
    print("📦 Creating portable package...")
    
    package_dir = "InvoiceMaker_Portable"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    # Create package directory
    os.makedirs(package_dir)
    
    # Copy EXE
    if os.path.exists("dist/InvoiceMaker.exe"):
        shutil.copy("dist/InvoiceMaker.exe", package_dir)
    
    # Copy essential files
    essential_files = [
        "README.md",
        "requirements.txt"
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy(file, package_dir)
    
    # Create portable launcher script
    with open(f"{package_dir}/Run Invoice Maker.bat", "w") as f:
        f.write("""@echo off
title Invoice Maker
echo Starting Invoice Maker...
InvoiceMaker.exe
pause
""")
    
    # Create README for portable version
    with open(f"{package_dir}/README_PORTABLE.txt", "w") as f:
        f.write("""🧾 Invoice Maker - Portable Version

📋 How to Use:
1. Double-click "Run Invoice Maker.bat"
2. Or double-click "InvoiceMaker.exe"
3. No installation required!

📁 What's Included:
- InvoiceMaker.exe (Main application)
- Run Invoice Maker.bat (Easy launcher)
- README_PORTABLE.txt (This file)

💡 Features:
- Create professional invoices
- GST calculations
- PDF generation
- QR code payments
- Customer management
- Product management
- Sales reports

🔧 System Requirements:
- Windows 7/8/10/11 (64-bit)
- 4GB RAM minimum
- 100MB free space

📞 Support:
For help, contact: support@invoicemaker.com

🎉 Enjoy using Invoice Maker!
""")
    
    print(f"✅ Portable package created: {package_dir}")
    
    # Create ZIP
    zip_name = "InvoiceMaker_Portable_v1.0.zip"
    shutil.make_archive(zip_name.replace('.zip', ''), 'zip', package_dir)
    print(f"✅ ZIP created: {zip_name}")

def create_installer_script():
    """Create Inno Setup installer script"""
    print("📝 Creating installer script...")
    
    script_content = """[Setup]
AppName=Invoice Maker
AppVersion=1.0
DefaultDirName={pf}\\Invoice Maker
DefaultGroupName=Invoice Maker
OutputDir=installer
OutputBaseFileName=InvoiceMaker_Setup
SetupIconFile=assets\\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\InvoiceMaker.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{app}\\assets"; Flags: ignoreversion recursedirs

[Icons]
Name: "{group}\\Invoice Maker"; Filename: "{app}\\InvoiceMaker.exe"
Name: "{group}\\{cm:UninstallProgram,Invoice Maker}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\\Invoice Maker"; Filename: "{app}\\InvoiceMaker.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\InvoiceMaker.exe"; Description: "{cm:LaunchProgram,Invoice Maker}"; Flags: nowait postinstall skipifsilent
"""
    
    with open("installer_script.iss", "w") as f:
        f.write(script_content)
    
    print("✅ Installer script created: installer_script.iss")
    print("💡 To create installer:")
    print("   1. Download Inno Setup from: https://jrsoftware.org/isinfo.php")
    print("   2. Open installer_script.iss in Inno Setup")
    print("   3. Compile to create installer")

def main():
    """Main build process"""
    print("🧾 Invoice Maker - Build System")
    print("=" * 50)
    
    # Change to project directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Build EXE
    if build_exe():
        print("\n🎉 Build successful!")
        
        # Create portable package
        create_portable_package()
        
        # Create installer script
        create_installer_script()
        
        print("\n📋 Build Summary:")
        print("✅ EXE file: dist/InvoiceMaker.exe")
        print("✅ Portable ZIP: InvoiceMaker_Portable_v1.0.zip")
        print("✅ Installer script: installer_script.iss")
        
        print("\n🚀 Distribution Options:")
        print("1. Share the ZIP file directly")
        print("2. Upload to Google Drive/Dropbox")
        print("3. Create installer with Inno Setup")
        print("4. Upload to GitHub Releases")
        
        print("\n💡 Next Steps:")
        print("1. Test the EXE file")
        print("2. Create professional icon")
        print("3. Set up distribution platform")
        print("4. Create user documentation")
        
    else:
        print("\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
