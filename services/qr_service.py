"""
QR Service - QR Code Generation
===============================

Service tạo và validate QR code cho điểm danh.
"""

import io
from typing import Optional, Tuple
from datetime import datetime

try:
    import qrcode
    from PIL import Image
    HAS_QR = True
except ImportError:
    HAS_QR = False
    # Dummy class for type hinting if PIL is missing
    class Image:
        class Image: pass

from .security_service import SecurityService


class QRService:
    """
    Service tạo và quản lý QR code cho điểm danh.
    
    Example:
        >>> qr_service = QRService(security_service)
        >>> qr_image, token = qr_service.generate_attendance_qr("SS001")
    """
    
    def __init__(self, security_service: SecurityService):
        """
        Khởi tạo QRService.
        
        Args:
            security_service: SecurityService instance
        """
        self.security = security_service
        
        if not HAS_QR:
            print("⚠️ Warning: qrcode library not installed. QR features disabled.")
    
    def generate_attendance_qr(
        self, 
        session_id: str,
        validity_seconds: int = 30
    ) -> Tuple[Optional[Image.Image], str]:
        """
        Tạo QR code cho phiên điểm danh.
        
        Args:
            session_id: Mã phiên điểm danh
            validity_seconds: Thời gian hiệu lực (giây)
            
        Returns:
            Tuple (PIL Image, token string)
            
        Example:
            >>> qr_image, token = qr_service.generate_attendance_qr("SS001")
            >>> qr_image.save("qr_code.png")
        """
        if not HAS_QR:
            token = self.security.generate_token(16)
            return None, token
        
        # Generate unique token
        token = self.security.generate_token(16)
        timestamp = int(datetime.now().timestamp())
        
        # QR data format: session_id|token|timestamp
        qr_data = f"{session_id}|{token}|{timestamp}"
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create image
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        return qr_image, token
    
    def validate_qr_data(
        self, 
        qr_data: str, 
        expected_session_id: str,
        validity_seconds: int = 30
    ) -> Tuple[bool, str]:
        """
        Validate QR code data.
        
        Args:
            qr_data: Data đọc từ QR code
            expected_session_id: Session ID mong đợi
            validity_seconds: Thời gian hiệu lực
            
        Returns:
            Tuple (is_valid, message)
        """
        try:
            parts = qr_data.split("|")
            if len(parts) != 3:
                return False, "QR code không hợp lệ"
            
            session_id, token, timestamp_str = parts
            
            # Check session ID
            if session_id != expected_session_id:
                return False, "QR code không thuộc phiên điểm danh này"
            
            # Check expiration
            timestamp = int(timestamp_str)
            current_time = int(datetime.now().timestamp())
            
            if current_time - timestamp > validity_seconds:
                return False, "QR code đã hết hạn"
            
            return True, "QR code hợp lệ"
            
        except Exception as e:
            return False, f"Lỗi khi validate QR: {str(e)}"
    
    def get_qr_as_bytes(self, qr_image) -> bytes:
        """
        Chuyển QR image thành bytes (để hiển thị trong UI).
        
        Args:
            qr_image: PIL Image object
            
        Returns:
            Image bytes
        """
        if qr_image is None:
            return b""
        
        buffer = io.BytesIO()
        qr_image.save(buffer, format="PNG")
        return buffer.getvalue()
