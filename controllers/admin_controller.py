"""
Admin Controller - Admin Request Controller
===========================================

Controller xử lý các request liên quan đến admin operations.
"""

from typing import Dict, Any, Optional

from services import AdminService


class AdminController:
    """
    Controller xử lý admin requests.
    
    Example:
        >>> admin_controller = AdminController(admin_service)
        >>> result = admin_controller.get_all_users()
        >>> if result["success"]:
        ...     users = result["users"]
    """
    
    def __init__(self, admin_service: AdminService):
        """
        Khởi tạo AdminController.
        
        Args:
            admin_service: AdminService instance
        """
        self.admin_service = admin_service
    
    # ==================== Dashboard ====================
    
    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Lấy dashboard statistics.
        
        Returns:
            Dict với keys: success, data/error
        """
        try:
            stats = self.admin_service.get_dashboard_stats()
            return {
                "success": True,
                "data": stats
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get dashboard stats: {str(e)}"
            }
    
    # ==================== User Management ====================
    
    def get_all_users(self, role_filter: Optional[str] = None) -> Dict[str, Any]:
        """
        Lấy danh sách users.
        
        Args:
            role_filter: Filter theo role (optional)
            
        Returns:
            Dict với keys: success, users/error
        """
        try:
            # Parse role filter if provided
            from core.enums import UserRole
            role = None
            if role_filter:
                try:
                    role = UserRole.from_string(role_filter)
                except ValueError:
                    return {
                        "success": False,
                        "error": f"Invalid role: {role_filter}"
                    }
            
            users = self.admin_service.get_all_users(role)
            return {
                "success": True,
                "users": users
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get users: {str(e)}"
            }
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Lấy thông tin một user.
        
        Args:
            user_id: ID của user
            
        Returns:
            Dict với keys: success, user/error
        """
        try:
            user = self.admin_service.get_user(user_id)
            
            if user:
                return {
                    "success": True,
                    "user": user
                }
            else:
                return {
                    "success": False,
                    "error": "User not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get user: {str(e)}"
            }
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tạo user mới.
        
        Args:
            user_data: Dict chứa thông tin user
            
        Returns:
            Dict với keys: success, password/error, message
        """
        try:
            success, message, password = self.admin_service.create_user(user_data)
            
            result = {
                "success": success,
                "message": message
            }
            
            if success and password:
                result["password"] = password
            
            if not success:
                result["error"] = message
            
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create user: {str(e)}"
            }
    
    def update_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cập nhật user.
        
        Args:
            user_data: Dict chứa thông tin cần update
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.update_user(user_data)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update user: {str(e)}"
            }
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """
        Xóa user.
        
        Args:
            user_id: ID của user
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.delete_user(user_id)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete user: {str(e)}"
            }
    
    def get_teachers(self) -> Dict[str, Any]:
        """
        Lấy danh sách teachers.
        
        Returns:
            Dict với keys: success, teachers/error
        """
        try:
            teachers = self.admin_service.get_teachers()
            return {
                "success": True,
                "teachers": teachers
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get teachers: {str(e)}"
            }
    
    # ==================== Class Management ====================
    
    def get_all_classes(self) -> Dict[str, Any]:
        """
        Lấy danh sách classes.
        
        Returns:
            Dict với keys: success, classes/error
        """
        try:
            classes = self.admin_service.get_all_classes()
            return {
                "success": True,
                "classes": classes
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get classes: {str(e)}"
            }
    
    def get_class(self, class_id: str) -> Dict[str, Any]:
        """
        Lấy thông tin một class.
        
        Args:
            class_id: ID của class
            
        Returns:
            Dict với keys: success, class/error
        """
        try:
            class_data = self.admin_service.get_class(class_id)
            
            if class_data:
                return {
                    "success": True,
                    "class": class_data
                }
            else:
                return {
                    "success": False,
                    "error": "Class not found"
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to get class: {str(e)}"
            }
    
    def create_class(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tạo class mới.
        
        Args:
            class_data: Dict chứa thông tin class
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.create_class(class_data)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to create class: {str(e)}"
            }
    
    def update_class(self, class_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cập nhật class.
        
        Args:
            class_data: Dict chứa thông tin cần update
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.update_class(class_data)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to update class: {str(e)}"
            }
    
    def delete_class(self, class_id: str) -> Dict[str, Any]:
        """
        Xóa class.
        
        Args:
            class_id: ID của class
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.delete_class(class_id)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to delete class: {str(e)}"
            }
    
    def add_student_to_class(self, class_id: str, student_code: str) -> Dict[str, Any]:
        """
        Thêm student vào class.
        
        Args:
            class_id: ID của class
            student_code: Mã sinh viên
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.add_student_to_class(class_id, student_code)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to add student to class: {str(e)}"
            }
    
    def remove_student_from_class(self, class_id: str, student_code: str) -> Dict[str, Any]:
        """
        Xóa student khỏi class.
        
        Args:
            class_id: ID của class
            student_code: Mã sinh viên
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            success, message = self.admin_service.remove_student_from_class(class_id, student_code)
            
            return {
                "success": success,
                "message": message,
                "error": None if success else message
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to remove student from class: {str(e)}"
            }
    
    # ==================== Reports ====================
    
    def generate_report(self, report_type: str, date_range: str, **kwargs) -> Dict[str, Any]:
        """
        Generate system report.
        
        Args:
            report_type: Loại báo cáo
            date_range: Khoảng thời gian
            **kwargs: Additional filters
            
        Returns:
            Dict với keys: success, data/error
        """
        try:
            # TODO: Implement report generation
            # This is a placeholder implementation
            
            data = {
                "summary": {
                    "Total Records": 100,
                    "Present": 85,
                    "Absent": 15,
                    "Attendance Rate": "85%"
                },
                "details": [
                    "Record 1: Student SV001 - Present",
                    "Record 2: Student SV002 - Present",
                    "Record 3: Student SV003 - Absent",
                ]
            }
            
            return {
                "success": True,
                "data": data
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to generate report: {str(e)}"
            }
    
    def export_report(
        self,
        report_data: Dict[str, Any],
        filename: str,
        format_type: str
    ) -> Dict[str, Any]:
        """
        Export report to file.
        
        Args:
            report_data: Data cần export
            filename: Tên file
            format_type: Format ("pdf", "excel", "csv")
            
        Returns:
            Dict với keys: success, message/error
        """
        try:
            # TODO: Implement actual export using ReportService
            # This is a placeholder
            
            return {
                "success": True,
                "message": f"Report exported to {filename}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to export report: {str(e)}"
            }
