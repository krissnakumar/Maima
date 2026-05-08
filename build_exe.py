
import os
import subprocess
import sys

def build():
    print("🚀 Starting Maima Windows Build Process...")
    
    # 1. Install requirements
    print("📦 Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 2. Run PyInstaller
    print("🛠️  Bundling into EXE (this may take a minute)...")
    try:
        subprocess.check_call(["pyinstaller", "--noconfirm", "maima.spec"])
        print("\n✅ Build Successful!")
        print("📁 Your executable is located in the 'dist' folder as 'Maima.exe'")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build Failed: {e}")
    except FileNotFoundError:
        print("\n❌ Error: PyInstaller not found. Please ensure it's installed via pip.")

if __name__ == "__main__":
    if os.name != 'nt':
        print("⚠️  Warning: You are running this on a non-Windows system.")
        print("To create a Windows EXE, please run this script on a Windows machine.")
    build()
