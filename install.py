#!/usr/bin/env python3
"""
🧾 Invoice Maker - One-Click Installer
Automated installation script for Windows/Mac/Linux
"""

import os
import sys
import subprocess
import platform
import webbrowser
from pathlib import Path
import json

class InvoiceMakerInstaller:
    """One-click installer for Invoice Maker"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.install_dir = self.get_install_directory()
        self.desktop_dir = self.get_desktop_directory()
        self.start_menu_dir = self.get_start_menu_directory()
        
    def get_install_directory(self):
        """Get appropriate installation directory"""
        if self.system == "windows":
            return Path(os.environ.get("PROGRAMFILES", "C:\\Program Files")) / "InvoiceMaker"
        elif self.system == "darwin":  # macOS
            return Path.home() / "Applications" / "InvoiceMaker"
        else:  # Linux
            return Path.home() / ".local" / "share" / "InvoiceMaker"
    
    def get_desktop_directory(self):
        """Get desktop directory"""
        if self.system == "windows":
            return Path(os.environ.get("USERPROFILE", "")) / "Desktop"
        else:
            return Path.home() / "Desktop"
    
    def get_start_menu_directory(self):
        """Get start menu/applications directory"""
        if self.system == "windows":
            return Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"
        elif self.system == "darwin":
            return Path.home() / "Applications"
        else:
            return Path.home() / ".local" / "share" / "applications"
    
    def print_header(self):
        """Print installer header"""
        print("=" * 60)
        print("🧾 Invoice Maker - One-Click Installer")
        print("=" * 60)
        print(f"🖥️  System: {platform.system()} {platform.release()}")
        print(f"📁 Install Directory: {self.install_dir}")
        print(f"🏠 Desktop: {self.desktop_dir}")
        print("=" * 60)
    
    def check_python_version(self):
        """Check Python version compatibility"""
        print("🐍 Checking Python version...")
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            print("❌ Python 3.8+ required. Please install Python 3.8 or higher.")
            print("📥 Download from: https://www.python.org/downloads/")
            return False
        
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    
    def install_dependencies(self):
        """Install required Python packages"""
        print("📦 Installing dependencies...")
        
        packages = [
            "streamlit>=1.29.0",
            "pandas>=2.1.0", 
            "plotly>=5.17.0",
            "reportlab>=4.0.0",
            "Pillow>=10.0.0",
            "qrcode[pil]>=7.4.0",
            "requests>=2.31.0",
            "pyinstaller>=6.0.0"
        ]
        
        for package in packages:
            print(f"  📥 Installing {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"  ✅ {package} installed")
            except subprocess.CalledProcessError:
                print(f"  ❌ Failed to install {package}")
                return False
        
        print("✅ All dependencies installed successfully")
        return True
    
    def create_install_directory(self):
        """Create installation directory"""
        print(f"📁 Creating install directory: {self.install_dir}")
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            print("✅ Install directory created")
            return True
        except Exception as e:
            print(f"❌ Failed to create install directory: {e}")
            return False
    
    def copy_application_files(self):
        """Copy application files to install directory"""
        print("📋 Copying application files...")
        
        # Get current directory (where install.py is located)
        current_dir = Path(__file__).parent
        
        # Files to copy
        files_to_copy = [
            "web_app.py",
            "db_web.py", 
            "gst_calculator_simple.py",
            "requirements.txt",
            "README.md"
        ]
        
        for file_name in files_to_copy:
            source_file = current_dir / file_name
            target_file = self.install_dir / file_name
            
            if source_file.exists():
                try:
                    import shutil
                    shutil.copy2(source_file, target_file)
                    print(f"  ✅ Copied {file_name}")
                except Exception as e:
                    print(f"  ❌ Failed to copy {file_name}: {e}")
                    return False
            else:
                print(f"  ⚠️  {file_name} not found, skipping")
        
        print("✅ Application files copied")
        return True
    
    def create_launcher_scripts(self):
        """Create launcher scripts for desktop and start menu"""
        print("🚀 Creating launcher scripts...")
        
        if self.system == "windows":
            return self.create_windows_launchers()
        elif self.system == "darwin":
            return self.create_mac_launchers()
        else:
            return self.create_linux_launchers()
    
    def create_windows_launchers(self):
        """Create Windows batch files and shortcuts"""
        try:
            # Create desktop shortcut
            desktop_shortcut = self.desktop_dir / "Invoice Maker.lnk"
            self.create_windows_shortcut(
                str(desktop_shortcut),
                "Invoice Maker",
                f'"{sys.executable}" "{self.install_dir / "web_app.py"}"',
                str(self.install_dir)
            )
            print("  ✅ Desktop shortcut created")
            
            # Create start menu shortcut
            start_menu_shortcut = self.start_menu_dir / "Invoice Maker.lnk"
            self.create_windows_shortcut(
                str(start_menu_shortcut),
                "Invoice Maker", 
                f'"{sys.executable}" "{self.install_dir / "web_app.py"}"',
                str(self.install_dir)
            )
            print("  ✅ Start menu shortcut created")
            
            # Create batch file for command line
            batch_file = self.install_dir / "run_invoice_maker.bat"
            with open(batch_file, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'echo 🧾 Starting Invoice Maker...\n')
                f.write(f'cd /d "{self.install_dir}"\n')
                f.write(f'"{sys.executable}" "{self.install_dir / "web_app.py"}"\n')
                f.write(f'pause\n')
            print("  ✅ Batch file created")
            
            return True
        except Exception as e:
            print(f"  ❌ Failed to create Windows launchers: {e}")
            return False
    
    def create_windows_shortcut(self, shortcut_path, description, target, working_dir):
        """Create Windows shortcut using PowerShell"""
        import tempfile
        
        powershell_script = f'''
        $WshShell = New-Object -comObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{target}"
        $Shortcut.WorkingDirectory = "{working_dir}"
        $Shortcut.Description = "{description}"
        $Shortcut.Save()
        '''
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
            f.write(powershell_script)
            ps_file = f.name
        
        try:
            subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file], 
                         check=True, capture_output=True)
        finally:
            os.unlink(ps_file)
    
    def create_mac_launchers(self):
        """Create macOS app bundle and launcher"""
        try:
            # Create app bundle structure
            app_dir = Path.home() / "Applications" / "Invoice Maker.app"
            contents_dir = app_dir / "Contents"
            macos_dir = contents_dir / "MacOS"
            
            for dir_path in [app_dir, contents_dir, macos_dir]:
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create Info.plist
            info_plist = contents_dir / "Info.plist"
            with open(info_plist, 'w') as f:
                f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
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
</plist>''')
            
            # Create executable script
            executable = macos_dir / "run_invoice_maker"
            with open(executable, 'w') as f:
                f.write(f'''#!/bin/bash
echo "🧾 Starting Invoice Maker..."
cd "{self.install_dir}"
"{sys.executable}" "{self.install_dir / "web_app.py"}"
''')
            
            # Make executable
            executable.chmod(0o755)
            
            print("  ✅ macOS app bundle created")
            return True
        except Exception as e:
            print(f"  ❌ Failed to create macOS launchers: {e}")
            return False
    
    def create_linux_launchers(self):
        """Create Linux desktop entry and launcher"""
        try:
            # Create desktop entry
            desktop_entry = self.start_menu_dir / "invoicemaker.desktop"
            with open(desktop_entry, 'w') as f:
                f.write(f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Invoice Maker
Comment=Professional Billing System
Exec={sys.executable} {self.install_dir / "web_app.py"}
Icon={self.install_dir / "icon.png"}
Terminal=false
Categories=Office;Finance;
Keywords=invoice;billing;gst;accounting;
''')
            
            # Make executable
            desktop_entry.chmod(0o755)
            
            # Create launcher script
            launcher = self.install_dir / "run_invoice_maker.sh"
            with open(launcher, 'w') as f:
                f.write(f'''#!/bin/bash
echo "🧾 Starting Invoice Maker..."
cd "{self.install_dir}"
"{sys.executable}" "{self.install_dir / "web_app.py"}"
''')
            
            launcher.chmod(0o755)
            
            print("  ✅ Linux desktop entry created")
            return True
        except Exception as e:
            print(f"  ❌ Failed to create Linux launchers: {e}")
            return False
    
    def create_uninstaller(self):
        """Create uninstaller script"""
        print("🗑️  Creating uninstaller...")
        
        if self.system == "windows":
            uninstaller = self.install_dir / "uninstall.bat"
            install_dir_str = str(self.install_dir)
            desktop_dir_str = str(self.desktop_dir)
            start_menu_dir_str = str(self.start_menu_dir)
            
            with open(uninstaller, 'w') as f:
                f.write(f'''@echo off
echo 🗑️  Uninstalling Invoice Maker...
echo.
echo This will remove Invoice Maker from your system.
echo.
pause
rmdir /s /q "{install_dir_str}"
del "{desktop_dir_str}\\Invoice Maker.lnk"
del "{start_menu_dir_str}\\Invoice Maker.lnk"
echo.
echo ✅ Invoice Maker uninstalled successfully!
pause
''')
        else:
            uninstaller = self.install_dir / "uninstall.sh"
            install_dir_str = str(self.install_dir)
            desktop_dir_str = str(self.desktop_dir)
            start_menu_dir_str = str(self.start_menu_dir)
            
            with open(uninstaller, 'w') as f:
                f.write(f'''#!/bin/bash
echo "🗑️  Uninstalling Invoice Maker..."
echo
echo "This will remove Invoice Maker from your system."
echo
read -p "Press Enter to continue..."
rm -rf "{install_dir_str}"
rm -f "{desktop_dir_str}/Invoice Maker.lnk" 2>/dev/null || true
rm -f "{start_menu_dir_str}/invoicemaker.desktop" 2>/dev/null || true
echo
echo "✅ Invoice Maker uninstalled successfully!"
''')
            uninstaller.chmod(0o755)
        
        print("✅ Uninstaller created")
    
    def test_installation(self):
        """Test the installation"""
        print("🧪 Testing installation...")
        
        try:
            # Test if web_app.py exists and is readable
            web_app_path = self.install_dir / "web_app.py"
            if not web_app_path.exists():
                print("❌ web_app.py not found")
                return False
            
            # Test if we can import the main modules
            sys.path.insert(0, str(self.install_dir))
            
            # Test database import
            try:
                import db_web
                print("✅ Database module imports successfully")
            except ImportError as e:
                print(f"❌ Database import failed: {e}")
                return False
            
            print("✅ Installation test passed")
            return True
            
        except Exception as e:
            print(f"❌ Installation test failed: {e}")
            return False
    
    def create_desktop_icon(self):
        """Create desktop icon"""
        print("🎨 Creating desktop icon...")
        
        # Create a simple icon using text (placeholder)
        icon_path = self.install_dir / "icon.png"
        
        try:
            # Create a simple icon using PIL
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a 256x256 icon
            img = Image.new('RGBA', (256, 256), (102, 126, 234, 255))
            draw = ImageDraw.Draw(img)
            
            # Draw invoice icon
            draw.rectangle([20, 20, 236, 236], fill=(255, 255, 255, 200), outline=(76, 75, 162, 255), width=3)
            draw.rectangle([40, 40, 216, 80], fill=(76, 75, 162, 255))
            
            # Draw lines to represent invoice
            for i in range(5):
                y = 100 + i * 20
                draw.rectangle([50, y, 180, y + 10], fill=(200, 200, 200, 255))
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            draw.text((128, 200), "🧾", fill=(255, 255, 255, 255), font=font, anchor="mm")
            
            img.save(icon_path)
            print("✅ Desktop icon created")
            
        except Exception as e:
            print(f"⚠️  Could not create icon: {e}")
    
    def run_application(self):
        """Run the application after installation"""
        print("🚀 Starting Invoice Maker...")
        
        try:
            webbrowser.open("http://localhost:8501")
            subprocess.Popen([sys.executable, str(self.install_dir / "web_app.py")])
            print("✅ Invoice Maker started in your browser!")
            return True
        except Exception as e:
            print(f"❌ Failed to start application: {e}")
            return False
    
    def install(self):
        """Main installation process"""
        self.print_header()
        
        # Installation steps
        steps = [
            ("Python Version Check", self.check_python_version),
            ("Install Dependencies", self.install_dependencies),
            ("Create Install Directory", self.create_install_directory),
            ("Copy Application Files", self.copy_application_files),
            ("Create Launcher Scripts", self.create_launcher_scripts),
            ("Create Desktop Icon", self.create_desktop_icon),
            ("Create Uninstaller", self.create_uninstaller),
            ("Test Installation", self.test_installation)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ Installation failed at: {step_name}")
                return False
            print(f"✅ {step_name} completed")
        
        print("\n" + "=" * 60)
        print("🎉 Invoice Maker installed successfully!")
        print("=" * 60)
        print(f"📁 Installation Directory: {self.install_dir}")
        print(f"🖥️  Desktop Shortcut: Available")
        print(f"📱 Start Menu: Available")
        print(f"🗑️  Uninstaller: {self.install_dir}/uninstall.{'bat' if self.system == 'windows' else 'sh'}")
        print("=" * 60)
        
        # Ask if user wants to run the app
        try:
            response = input("\n🚀 Start Invoice Maker now? (y/n): ").lower().strip()
            if response in ['y', 'yes', '']:
                self.run_application()
        except KeyboardInterrupt:
            print("\n👋 Installation complete. Run Invoice Maker from your desktop or start menu!")
        
        return True

def main():
    """Main installer function"""
    installer = InvoiceMakerInstaller()
    
    try:
        success = installer.install()
        if success:
            print("\n🎯 Installation completed successfully!")
            print("📱 You can now run Invoice Maker from:")
            print("   • Desktop shortcut")
            print("   • Start menu")
            print("   • Command line: Navigate to install directory and run web_app.py")
        else:
            print("\n❌ Installation failed. Please check the error messages above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Installation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
