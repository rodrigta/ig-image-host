"""
Helper script to automatically commit and push code changes.
This is used by the AI assistant to automatically push code updates.
"""

import subprocess
import sys
from datetime import datetime

def auto_push(message=None):
    """Automatically commit and push code changes."""
    if not message:
        message = f"Auto-update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    try:
        # Add all changes
        subprocess.run(["git", "add", "."], check=True, capture_output=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", message], check=True, capture_output=True)
        
        # Push
        result = subprocess.run(["git", "push", "origin", "main"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[SUCCESS] Code pushed successfully: {message}")
            return True
        else:
            print(f"[ERROR] Push failed: {result.stderr}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    message = sys.argv[1] if len(sys.argv) > 1 else None
    auto_push(message)

