"""
Student Controller - Student Request Handler
============================================

Controller xử lý các request liên quan đến Student:
- Dashboard views
- Attendance submission
- History retrieval
- Profile updates
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from core.models import Student
from core.exceptions import ValidationError, NotFoundError, AuthenticationError
from services import StudentService


class StudentController:
    """
    Controller xử lý student requests.
    
    Example:
        >>> controller = StudentController(student_service)
        >>> result = controller.handle_submit_attendance("SV001", "SESSION123", "TOKEN")
        >>> if result["success"]:
        ...     print("Điểm danh thành công!")
    """
    
    def __init__(self, student_service: StudentService):
        """
        Khởi tạo StudentController.
        
        Args:
            student_service: StudentService instance
        """
        self.student_service = student_service
    
    def handle_get_dashboard(self, student_code: str) -> Dict[str, Any]:
        """
        Xử lý request lấy dashboard data.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            Dict với keys: success, data/error
            
        Example:
            >>> result = controller.handle_get_dashboard("SV001")
            >>> print(f"Tỷ lệ: {result['data']['attendance_rate']}%")
        """
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "error": "Mã sinh viên không hợp lệ"
            }
        
        try:
            stats = self.student_service.get_dashboard_stats(student_code.strip())
            schedule = self.student_service.get_class_schedule(student_code.strip())
            student_info = self.student_service.get_student_info(student_code.strip())
            
            return {
                "success": True,
                "data": {
                    "student_info": student_info,
                    "statistics": stats,
                    "schedule": schedule
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Lỗi khi tải dashboard: {str(e)}"
            }

    def handle_get_todays_sessions(self, student_code: str) -> Dict[str, Any]:
        """
        Xử lý request lấy danh sách session hôm nay.
        """
        if not student_code or not student_code.strip():
            return {"success": False, "error": "Mã sinh viên không hợp lệ"}
        
        try:
            sessions = self.student_service.get_todays_sessions(student_code.strip())
            return {"success": True, "data": sessions}
        except Exception as e:
            return {"success": False, "error": f"Lỗi khi tải phiên học: {str(e)}"}
    
    def handle_submit_attendance(
        self,
        student_code: str,
        session_id: str,
        verification_data: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Xử lý request điểm danh.
        
        Args:
            student_code: Mã sinh viên
            session_id: ID của session
            verification_data: Token hoặc QR data
            
        Returns:
            Dict với keys: success, message
            
        Example:
            >>> result = controller.handle_submit_attendance("SV001", "SESSION123", "TOKEN")
        """
        # Validate inputs
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "message": "Mã sinh viên không hợp lệ"
            }
        
        if not session_id or not session_id.strip():
            return {
                "success": False,
                "message": "Session ID không hợp lệ"
            }
        
        try:
            success, message = self.student_service.submit_attendance(
                student_code.strip(),
                session_id.strip(),
                verification_data
            )
            
            return {
                "success": success,
                "message": message
            }
        except NotFoundError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except ValidationError as e:
            return {
                "success": False,
                "message": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi hệ thống: {str(e)}"
            }
    
    def handle_get_attendance_history(
        self,
        student_code: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Xử lý request lấy lịch sử điểm danh.
        
        Args:
            student_code: Mã sinh viên
            filters: Dict chứa các filter options:
                - search_query: str (optional)
                - start_date: str (YYYY-MM-DD)
                - end_date: str (YYYY-MM-DD)
                - class_id: str
                - status: str
                - sort_by: str ('date' or 'class_name')
                - sort_order: str ('asc' or 'desc')
                
        Returns:
            Dict với keys: success, data/error
            
        Example:
            >>> filters = {"start_date": "2024-01-01", "class_id": "CS101"}
            >>> result = controller.handle_get_attendance_history("SV001", filters)
        """
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "error": "Mã sinh viên không hợp lệ"
            }
        
        try:
            # Parse filters
            search_query = None
            start_date = None
            end_date = None
            class_id = None
            status = None
            sort_by = 'date'
            sort_order = 'desc'
            
            if filters:
                if 'search_query' in filters:
                    search_query = filters['search_query']

                if 'start_date' in filters and filters['start_date']:
                    try:
                        start_date = datetime.strptime(filters['start_date'], "%Y-%m-%d")
                    except ValueError:
                        return {
                            "success": False,
                            "error": "Định dạng ngày bắt đầu không hợp lệ (YYYY-MM-DD)"
                        }
                
                if 'end_date' in filters and filters['end_date']:
                    try:
                        end_date = datetime.strptime(filters['end_date'], "%Y-%m-%d")
                    except ValueError:
                        return {
                            "success": False,
                            "error": "Định dạng ngày kết thúc không hợp lệ (YYYY-MM-DD)"
                        }
                
                if 'class_id' in filters:
                    class_id = filters['class_id']
                
                if 'status' in filters:
                    status = filters['status']
                    
                if 'sort_by' in filters:
                    sort_by = filters['sort_by']
                    
                if 'sort_order' in filters:
                    sort_order = filters['sort_order']
            
            # Get history
            history = self.student_service.get_attendance_history(
                student_code.strip(),
                search_query=search_query,
                start_date=start_date,
                end_date=end_date,
                class_id=class_id,
                status=status,
                sort_by=sort_by,
                sort_order=sort_order
            )
            
            return {
                "success": True,
                "data": {
                    "records": history,
                    "total_count": len(history)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Lỗi khi tải lịch sử: {str(e)}"
            }
    
    def handle_update_profile(
        self,
        student_code: str,
        profile_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Xử lý request cập nhật profile.
        
        Args:
            student_code: Mã sinh viên
            profile_data: Dict chứa thông tin cần update:
                - full_name: str (optional)
                - email: str (optional)
                - class_name: str (optional)
                
        Returns:
            Dict với keys: success, message
            
        Example:
            >>> data = {"full_name": "Nguyễn Văn A", "email": "nva@email.com"}
            >>> result = controller.handle_update_profile("SV001", data)
        """
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "message": "Mã sinh viên không hợp lệ"
            }
        
        if not profile_data:
            return {
                "success": False,
                "message": "Không có dữ liệu để cập nhật"
            }
        
        # Validate data
        full_name = profile_data.get('full_name', '').strip() if profile_data.get('full_name') else None
        email = profile_data.get('email', '').strip() if profile_data.get('email') else None
        class_name = profile_data.get('class_name', '').strip() if profile_data.get('class_name') else None
        
        if not any([full_name, email, class_name]):
            return {
                "success": False,
                "message": "Không có dữ liệu hợp lệ để cập nhật"
            }
        
        try:
            success, message = self.student_service.update_profile(
                student_code.strip(),
                full_name=full_name,
                email=email,
                class_name=class_name
            )
            
            return {
                "success": success,
                "message": message
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi hệ thống: {str(e)}"
            }
    
    def handle_get_student_info(self, student_code: str) -> Dict[str, Any]:
        """
        Xử lý request lấy thông tin sinh viên.
        
        Args:
            student_code: Mã sinh viên
            
        Returns:
            Dict với keys: success, data/error
        """
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "error": "Mã sinh viên không hợp lệ"
            }
        
        try:
            student_info = self.student_service.get_student_info(student_code.strip())
            
            if not student_info:
                return {
                    "success": False,
                    "error": "Không tìm thấy sinh viên"
                }
            
            return {
                "success": True,
                "data": student_info
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Lỗi khi tải thông tin: {str(e)}"
            }
    
    def validate_student_code(self, student_code: str) -> bool:
        """
        Validate format của student code.
        
        Args:
            student_code: Mã sinh viên cần validate
            
        Returns:
            True nếu hợp lệ
        """
        if not student_code or not student_code.strip():
            return False
        
        # Implement validation logic
        # VD: Mã sinh viên phải có độ dài 5-15 ký tự
        code = student_code.strip()
        return 5 <= len(code) <= 15
    
    def handle_qr_attendance(
        self,
        student_code: str,
        qr_data: str
    ) -> Dict[str, Any]:
        """
        Xử lý điểm danh qua QR code.
        
        Args:
            student_code: Mã sinh viên
            qr_data: Dữ liệu từ QR code (format: session_id|token|timestamp)
            
        Returns:
            Dict với keys: success, message
            
        Example:
            >>> qr_data = "SESSION123|TOKEN456|1640000000"
            >>> result = controller.handle_qr_attendance("SV001", qr_data)
        """
        # Validate student code
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "message": "Mã sinh viên không hợp lệ"
            }
        
        # Parse QR data
        try:
            parts = qr_data.split("|")
            if len(parts) != 3:
                return {
                    "success": False,
                    "message": "QR code không đúng định dạng"
                }
            
            session_id, token, timestamp_str = parts
            
            # Validate timestamp (QR không quá cũ - max 60 giây)
            try:
                from datetime import datetime
                qr_timestamp = int(timestamp_str)
                current_timestamp = int(datetime.now().timestamp())
                
                if current_timestamp - qr_timestamp > 60:
                    return {
                        "success": False,
                        "message": "QR code đã hết hạn (quá 60 giây)"
                    }
            except ValueError:
                return {
                    "success": False,
                    "message": "QR code có timestamp không hợp lệ"
                }
            
            # Submit attendance with QR verification
            return self.handle_submit_attendance(
                student_code.strip(),
                session_id.strip(),
                verification_data=token
            )
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi khi xử lý QR code: {str(e)}"
            }
    
    def handle_code_attendance(
        self,
        student_code: str,
        secret_code: str
    ) -> Dict[str, Any]:
        """
        Xử lý điểm danh qua secret code.
        
        Args:
            student_code: Mã sinh viên
            secret_code: Mã bí mật từ giáo viên
            
        Returns:
            Dict với keys: success, message
            
        Example:
            >>> result = controller.handle_code_attendance("SV001", "ABC123")
        """
        # Validate inputs
        if not student_code or not student_code.strip():
            return {
                "success": False,
                "message": "Mã sinh viên không hợp lệ"
            }
        
        if not secret_code or not secret_code.strip():
            return {
                "success": False,
                "message": "Mã bí mật không được để trống"
            }
        
        try:
            # Tìm session với token matching
            # (Cần access session repository để find by token)
            # Tạm thời giả sử token = verification_data
            
            # Note: Đoạn này cần session repository để tìm session_id từ token
            # Hiện tại sẽ trả về lỗi nếu không tìm thấy
            
            # Workaround: Try to submit với assumption rằng secret_code có thể là session_id hoặc token
            # Real implementation cần query database
            
            # For now, return generic message
            return {
                "success": False,
                "message": "Chức năng secret code cần được tích hợp với session repository. "
                          "Vui lòng sử dụng QR code hoặc liên hệ giáo viên."
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Lỗi hệ thống: {str(e)}"
            }
    
    def find_active_session_by_token(self, token: str) -> Optional[str]:
        """
        Tìm session_id từ token (cần session repository).
        
        Note: Method này cần được implement khi có session repository.
        
        Args:
            token: Token/secret code
            
        Returns:
            session_id nếu tìm thấy, None nếu không
        """
        # TODO: Implement with session repository
        # session_repo.find_by_token(token)
        return None

