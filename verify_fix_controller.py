
import sys
import os
from unittest.mock import MagicMock

# Add project root to path
sys.path.append("/home/billtran/Archduker/UTH/SUBJECT/Students-Attendance-System-Gr.14")

try:
    from controllers.student_controller import StudentController
    print("Successfully imported StudentController")
except ImportError as e:
    print(f"Failed to import StudentController: {e}")
    sys.exit(1)

def test_methods_exist():
    service_mock = MagicMock()
    controller = StudentController(service_mock)

    # Test handle_get_todays_sessions existence
    if hasattr(controller, 'handle_get_todays_sessions'):
        print("✅ handle_get_todays_sessions exists")
        
        # Test basic call
        service_mock.get_todays_sessions.return_value = [{"session_id": "1", "name": "Test Session"}]
        result = controller.handle_get_todays_sessions("SV001")
        if result["success"] and result["data"][0]["name"] == "Test Session":
            print("✅ handle_get_todays_sessions returns success")
        else:
             print(f"❌ handle_get_todays_sessions failed: {result}")
    else:
        print("❌ handle_get_todays_sessions MISSING")

    # Test handle_submit_attendance existence
    if hasattr(controller, 'handle_submit_attendance'):
        print("✅ handle_submit_attendance exists")
        
        # Test basic call
        service_mock.submit_attendance.return_value = (True, "Success")
        result = controller.handle_submit_attendance("SV001", "S1", "T1")
        if result["success"]:
            print("✅ handle_submit_attendance returns success")
        else:
            print(f"❌ handle_submit_attendance failed: {result}")
    else:
        print("❌ handle_submit_attendance MISSING")

if __name__ == "__main__":
    test_methods_exist()
