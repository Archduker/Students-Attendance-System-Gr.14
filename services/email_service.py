"""
Email Service - Email Sending
=============================

Service gửi email cho password reset, notifications.

⚠️ LƯU Ý: Cần cấu hình SMTP credentials trong config/email.py
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from config.email import get_email_config, is_email_configured, EMAIL_SUBJECTS


class EmailService:
    """
    Service gửi email.
    
    Example:
        >>> email_service = EmailService()
        >>> email_service.send_password_reset_email("user@email.com", "newpassword123")
    """
    
    def __init__(self):
        """Khởi tạo EmailService."""
        self.config = get_email_config()
        self._is_configured = is_email_configured()
        
        if not self._is_configured:
            print("⚠️ Warning: Email not configured. Set SENDER_EMAIL and SENDER_PASSWORD.")
    
    def _create_smtp_connection(self) -> smtplib.SMTP:
        """Tạo SMTP connection."""
        server = smtplib.SMTP(self.config["server"], self.config["port"])
        
        if self.config.get("use_tls"):
            server.starttls()
        
        server.login(self.config["sender_email"], self.config["sender_password"])
        return server
    
    def send_email(
        self, 
        to_email: str, 
        subject: str, 
        body: str,
        is_html: bool = False
    ) -> bool:
        """
        Gửi email.
        
        Args:
            to_email: Email người nhận
            subject: Tiêu đề email
            body: Nội dung email
            is_html: True nếu body là HTML
            
        Returns:
            True nếu gửi thành công
            
        Example:
            >>> email_service.send_email(
            ...     "user@email.com",
            ...     "Test Subject",
            ...     "Hello World!"
            ... )
        """
        if not self._is_configured:
            print(f"📧 [Mock] Email to {to_email}: {subject}")
            return True
        
        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.config["sender_email"]
            msg["To"] = to_email
            
            # Attach body
            mime_type = "html" if is_html else "plain"
            msg.attach(MIMEText(body, mime_type))
            
            # Send email
            with self._create_smtp_connection() as server:
                server.sendmail(
                    self.config["sender_email"],
                    to_email,
                    msg.as_string()
                )
            
            return True
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def send_password_reset_email(self, to_email: str, new_password: str) -> bool:
        """
        Gửi email reset password.
        
        Args:
            to_email: Email người nhận
            new_password: Mật khẩu mới
            
        Returns:
            True nếu gửi thành công
        """
        subject = EMAIL_SUBJECTS.get("password_reset", "Password Reset")
        
        body = f"""
        <html>
        <body>
            <h2>🔐 Khôi phục mật khẩu</h2>
            <p>Xin chào,</p>
            <p>Mật khẩu mới của bạn là: <strong>{new_password}</strong></p>
            <p>Vui lòng đăng nhập và đổi mật khẩu ngay sau khi nhận được email này.</p>
            <br>
            <p>Trân trọng,<br>Student Attendance System</p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, is_html=True)
    
    def send_welcome_email(self, to_email: str, full_name: str, username: str) -> bool:
        """
        Gửi email chào mừng user mới.
        
        Args:
            to_email: Email người nhận
            full_name: Tên đầy đủ
            username: Tên đăng nhập
            
        Returns:
            True nếu gửi thành công
        """
        subject = EMAIL_SUBJECTS.get("welcome", "Welcome")
        
        body = f"""
        <html>
        <body>
            <h2>👋 Chào mừng {full_name}!</h2>
            <p>Tài khoản của bạn đã được tạo thành công.</p>
            <p><strong>Tên đăng nhập:</strong> {username}</p>
            <p>Vui lòng liên hệ Admin để nhận mật khẩu.</p>
            <br>
            <p>Trân trọng,<br>Student Attendance System</p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, is_html=True)
