"""
Email Service - Email Sending
=============================

Service for sending emails for password reset, notifications.

⚠️ NOTE: Configure SMTP credentials in config/email.py
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from config.email import get_email_config, is_email_configured, EMAIL_SUBJECTS


class EmailService:
    """
    Service for sending emails.
    
    Example:
        >>> email_service = EmailService()
        >>> email_service.send_password_reset_email("user@email.com", "newpassword123")
    """
    
    def __init__(self):
        """Initialize EmailService."""
        self.config = get_email_config()
        self._is_configured = is_email_configured()
        
        if not self._is_configured:
            print("⚠️ Warning: Email not configured. Set SENDER_EMAIL and SENDER_PASSWORD.")
    
    def _create_smtp_connection(self) -> smtplib.SMTP:
        """Create SMTP connection."""
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
        Send email.
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            is_html: True if body is HTML
            
        Returns:
            True if sent successfully
            
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
        Send password reset email.
        
        Args:
            to_email: Recipient email address
            new_password: New password
            
        Returns:
            True if sent successfully
        """
        subject = EMAIL_SUBJECTS.get("password_reset", "Password Reset")
        
        body = f"""
        <html>
        <body>
            <h2>🔐 Password Recovery</h2>
            <p>Hello,</p>
            <p>Your new password is: <strong>{new_password}</strong></p>
            <p>Please login and change your password immediately after receiving this email.</p>
            <br>
            <p>Best regards,<br>Student Attendance System</p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, is_html=True)
    
    def send_welcome_email(self, to_email: str, full_name: str, username: str) -> bool:
        """
        Send welcome email to new user.
        
        Args:
            to_email: Recipient email address
            full_name: Full name
            username: Username
            
        Returns:
            True if sent successfully
        """
        subject = EMAIL_SUBJECTS.get("welcome", "Welcome")
        
        body = f"""
        <html>
        <body>
            <h2>👋 Welcome {full_name}!</h2>
            <p>Your account has been created successfully.</p>
            <p><strong>Username:</strong> {username}</p>
            <p>Please contact Admin to receive your password.</p>
            <br>
            <p>Best regards,<br>Student Attendance System</p>
        </body>
        </html>
        """
        
        return self.send_email(to_email, subject, body, is_html=True)
