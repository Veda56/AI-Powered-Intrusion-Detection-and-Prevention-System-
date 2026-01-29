import os
import sys
import time
import subprocess
from pathlib import Path

def get_project_root():
    """Get the absolute path to the project root"""
    return Path(__file__).parent

def start_aatis_service():
    """Run AATIS as a continuous service"""
    project_root = get_project_root()
    app_path = project_root / "app.py"
    venv_python = project_root / "venv" / "Scripts" / "python.exe"
    
    print("=" * 60)
    print("🛡️  AATIS Security System - Background Service")
    print("=" * 60)
    print(f"Project: {project_root}")
    print(f"Python: {venv_python}")
    print(f"App: {app_path}")
    print("Service started. AATIS will auto-restart if it crashes.")
    print("=" * 60)
    
    # Use system Python if venv doesn't exist
    if not venv_python.exists():
        venv_python = sys.executable
        print("⚠️  Using system Python (venv not found)")
    
    while True:
        try:
            print(f"\n🕒 {time.strftime('%Y-%m-%d %H:%M:%S')} - Starting AATIS...")
            
            # Run the main app
            process = subprocess.Popen(
                [str(venv_python), str(app_path)], 
                cwd=str(project_root),
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Monitor the process
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print(output.strip())
            
            # Check exit code
            return_code = process.poll()
            if return_code == 0:
                print("✅ AATIS stopped normally.")
                break
            else:
                print(f"❌ AATIS crashed (Code: {return_code}). Restarting in 10 seconds...")
                time.sleep(10)
                
        except KeyboardInterrupt:
            print("\n🛑 Service stopped by user")
            break
        except Exception as e:
            print(f"❌ Service error: {e}")
            print("🔄 Restarting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    start_aatis_service()