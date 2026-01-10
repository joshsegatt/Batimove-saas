"""
Quick Start Script for Batimove Backend
Run this script to start the development server locally
"""

import subprocess
import sys
import os


def check_python_version():
    """Check if Python version is 3.9+"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("⚠️  .env file not found")
        print("   Creating from .env.example...")
        if os.path.exists(".env.example"):
            with open(".env.example", "r") as src:
                with open(".env", "w") as dst:
                    dst.write(src.read())
            print("✅ .env file created with DEV_MODE=true (no Firebase needed)")
            return True
        else:
            print("❌ .env.example not found")
            return False
    
    # Check if in dev mode
    with open(".env", "r") as f:
        content = f.read()
        if "DEV_MODE=true" in content:
            print("✅ .env file exists (Development Mode - no Firebase needed)")
        else:
            print("✅ .env file exists (Production Mode - Firebase required)")
    return True


def main():
    """Main function"""
    print("=" * 50)
    print("🏗️  Batimove Backend - Quick Start")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Check .env file
    env_configured = check_env_file()
    
    if not env_configured:
        print("\n❌ Could not create .env file")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Start server
    start_server()


if __name__ == "__main__":
    main()
