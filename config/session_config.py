import json
from pathlib import Path
import os

# Create config directory if not exists
CONFIG_DIR = Path.home() / ".attendance_system"
CONFIG_DIR.mkdir(exist_ok=True)

SESSION_FILE = CONFIG_DIR / "session.json"

def save_session(email, remember=False):
    """
    Lưu session info (email và trạng thái remember).
    Mật khẩu không được lưu vì lý do bảo mật.
    """
    try:
        data = {
            "last_email": email,
            "remember": remember
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(f"Failed to save session: {e}")
        return False

def load_session():
    """
    Load session info đã lưu.
    Returns dict or None.
    """
    if not SESSION_FILE.exists():
        return None
    
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load session: {e}")
        return None

def clear_session():
    """
    Xóa session file (hoặc reset data).
    Nếu user chọn remember me, ta có thể chỉ xóa token nhưng giữ email.
    Ở đây ta xóa hết để đơn giản, hoặc chỉ giữ lại last_email nếu muốn.
    """
    try:
        if SESSION_FILE.exists():
            # Check if we should keep email (mock implementation logic)
            # For strict security, delete file
            SESSION_FILE.unlink()
        return True
    except Exception as e:
        print(f"Failed to clear session: {e}")
        return False
