"""
Attendance Method Enum - Phương thức điểm danh
===============================================

Định nghĩa các phương thức điểm danh:
- QR: Quét mã QR
- LINK_TOKEN: Nhập mã token/link
- MANUAL: Giáo viên điểm danh thủ công
- AUTO: Tự động điểm danh
"""

from enum import Enum


class AttendanceMethod(Enum):
    """
    Enum định nghĩa các phương thức điểm danh trong hệ thống.
    
    Attributes:
        QR: Quét mã QR - mã tự động đổi mỗi 30 giây
        LINK_TOKEN: Nhập mã token - mã có hiệu lực trong thời gian quy định
        MANUAL: Thủ công - giáo viên điểm danh trực tiếp
        AUTO: Tự động - hệ thống tự động điểm danh
        
    Example:
        >>> from core.enums import AttendanceMethod
        >>> method = AttendanceMethod.QR
        >>> print(method.description)
        Quét mã QR để điểm danh
    """
    
    QR = "QR"
    LINK_TOKEN = "LINK_TOKEN"
    MANUAL = "MANUAL"
    AUTO = "AUTO"
    
    @property
    def description(self) -> str:
        """Mô tả phương thức điểm danh."""
        descriptions = {
            AttendanceMethod.QR: "Quét mã QR để điểm danh",
            AttendanceMethod.LINK_TOKEN: "Nhập mã token để điểm danh",
            AttendanceMethod.MANUAL: "Giáo viên điểm danh thủ công",
            AttendanceMethod.AUTO: "Hệ thống tự động điểm danh",
        }
        return descriptions.get(self, "")
    
    @classmethod
    def from_string(cls, method_str: str) -> "AttendanceMethod":
        """
        Chuyển đổi string thành AttendanceMethod enum.
        
        Args:
            method_str: Chuỗi phương thức (case-insensitive)
            
        Returns:
            AttendanceMethod enum tương ứng
            
        Raises:
            ValueError: Nếu method_str không hợp lệ
        """
        try:
            return cls(method_str.upper())
        except ValueError:
            valid_methods = [m.value for m in cls]
            raise ValueError(
                f"Invalid method: '{method_str}'. "
                f"Valid methods: {valid_methods}"
            )
    
    def requires_student_action(self) -> bool:
        """Kiểm tra phương thức có yêu cầu sinh viên thao tác không."""
        return self in [AttendanceMethod.QR, AttendanceMethod.LINK_TOKEN]
    
    def __str__(self) -> str:
        return self.value
