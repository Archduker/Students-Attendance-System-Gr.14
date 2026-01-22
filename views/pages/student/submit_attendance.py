"""
Submit Attendance Page - Page for students to submit attendance
===============================================================

Hỗ trợ các phương thức điểm danh:
- QR Code scanning
- Link/Token input
- Manual (teacher marks)
"""

import customtkinter as ctk
from typing import Optional
from datetime import datetime

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS
from controllers import StudentController
from core.enums import AttendanceMethod


class SubmitAttendancePage(ctk.CTkFrame):
    """
    Page để sinh viên submit attendance.
    
    Features:
    - Nhập session ID hoặc scan QR
    - Nhập token (nếu cần)
    - Submit và nhận feedback
    """
    
    def __init__(
        self,
        parent,
        controller: StudentController,
        student_code: str,
        qr_scanner=None,  # QRScanner component (optional)
        **kwargs
    ):
        """
        Khởi tạo Submit Attendance Page.
        
        Args:
            parent: Parent widget
            controller: StudentController instance
            student_code: Mã sinh viên
            qr_scanner: QRScanner component (optional)
        """
        super().__init__(parent, **kwargs)
        
        self.controller = controller
        self.student_code = student_code
        self.qr_scanner = qr_scanner
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Thiết lập UI components."""
        self.configure(fg_color=COLORS["bg_secondary"])
        
        # Main container
        main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Header
        self._create_header(main_container)
        
        # Content area - centered
        content = ctk.CTkFrame(
            main_container,
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["lg"]
        )
        content.pack(fill="both", expand=True, pady=(SPACING["md"], 0))
        
        # Center form
        form_container = ctk.CTkFrame(content, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ctk.CTkLabel(
            form_container,
            text="✅ Điểm danh",
            font=(FONTS["family"], FONTS["size_3xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(pady=(0, SPACING["xl"]))
        
        # Method selection
        self._create_method_selection(form_container)
        
        # QR Scanner section
        self.qr_section = ctk.CTkFrame(form_container, fg_color="transparent")
        self.qr_section.pack(fill="x", pady=SPACING["md"])
        
        # Manual input section
        self.manual_section = ctk.CTkFrame(form_container, fg_color="transparent")
        
        # Session ID input
        session_label = ctk.CTkLabel(
            self.manual_section,
            text="Mã phiên điểm danh (Session ID):",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_primary"]
        )
        session_label.pack(anchor="w", pady=(0, SPACING["sm"]))
        
        self.session_entry = ctk.CTkEntry(
            self.manual_section,
            width=400,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập mã phiên điểm danh..."
        )
        self.session_entry.pack(fill="x", pady=(0, SPACING["md"]))
        
        # Token input
        token_label = ctk.CTkLabel(
            self.manual_section,
            text="Token điểm danh (nếu có):",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_primary"]
        )
        token_label.pack(anchor="w", pady=(0, SPACING["sm"]))
        
        self.token_entry = ctk.CTkEntry(
            self.manual_section,
            width=400,
            height=40,
            corner_radius=RADIUS["md"],
            placeholder_text="Nhập token (tùy chọn)..."
        )
        self.token_entry.pack(fill="x", pady=(0, SPACING["lg"]))
        
        self.manual_section.pack(fill="x", pady=SPACING["md"])
        
        # Submit button
        self.submit_btn = ctk.CTkButton(
            form_container,
            text="📝 Xác nhận điểm danh",
            width=400,
            height=45,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["success"],
            hover_color=COLORS["success"],
            font=(FONTS["family"], FONTS["size_lg"], FONTS["weight_bold"]),
            command=self._handle_submit
        )
        self.submit_btn.pack(pady=(SPACING["lg"], 0))
        
        # Message label
        self.message_label = ctk.CTkLabel(
            form_container,
            text="",
            font=(FONTS["family"], FONTS["size_base"]),
            wraplength=380
        )
        self.message_label.pack(pady=(SPACING["md"], 0))
    
    def _create_header(self, parent):
        """Tạo header section."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, SPACING["lg"]))
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="📋 Điểm danh",
            font=(FONTS["family"], FONTS["size_3xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left")
        
        # Info
        info = ctk.CTkLabel(
            header,
            text=f"Sinh viên: {self.student_code}",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"]
        )
        info.pack(side="right")
    
    def _create_method_selection(self, parent):
        """Tạo phần chọn phương thức điểm danh."""
        method_frame = ctk.CTkFrame(parent, fg_color="transparent")
        method_frame.pack(fill="x", pady=(0, SPACING["lg"]))
        
        label = ctk.CTkLabel(
            method_frame,
            text="Chọn phương thức điểm danh:",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_primary"]
        )
        label.pack(anchor="w", pady=(0, SPACING["sm"]))
        
        # Method buttons
        btn_frame = ctk.CTkFrame(method_frame, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        # QR button
        qr_btn = ctk.CTkButton(
            btn_frame,
            text="📷 Quét QR Code",
            width=195,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            command=self._show_qr_scanner
        )
        qr_btn.pack(side="left", padx=(0, SPACING["sm"]))
        
        # Manual button
        manual_btn = ctk.CTkButton(
            btn_frame,
            text="⌨️ Nhập thủ công",
            width=195,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            command=self._show_manual_input
        )
        manual_btn.pack(side="left")
    
    def _show_qr_scanner(self):
        """Hiển thị QR scanner."""
        self.manual_section.pack_forget()
        
        if self.qr_scanner:
            # Clear QR section
            for widget in self.qr_section.winfo_children():
                widget.destroy()
            
            # Show QR scanner
            scanner_label = ctk.CTkLabel(
                self.qr_section,
                text="📷 Quét mã QR từ màn hình giáo viên",
                font=(FONTS["family"], FONTS["size_lg"]),
                text_color=COLORS["text_primary"]
            )
            scanner_label.pack(pady=SPACING["md"])
            
            # Scan button
            scan_btn = ctk.CTkButton(
                self.qr_section,
                text="🎥 Mở camera",
                width=200,
                height=40,
                corner_radius=RADIUS["md"],
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                command=self._start_qr_scan
            )
            scan_btn.pack(pady=SPACING["sm"])
        else:
            self._show_message("QR Scanner chưa được cấu hình", "error")
    
    def _show_manual_input(self):
        """Hiển thị form nhập thủ công."""
        # Clear QR section
        for widget in self.qr_section.winfo_children():
            widget.destroy()
        
        self.manual_section.pack(fill="x", pady=SPACING["md"])
    
    def _start_qr_scan(self):
        """Bắt đầu scan QR code."""
        if self.qr_scanner:
            try:
                # Open QR scanner
                qr_data = self.qr_scanner.scan()
                
                if qr_data:
                    # Parse QR data (format: "SESSION_ID|TOKEN")
                    parts = qr_data.split("|")
                    session_id = parts[0] if len(parts) > 0 else ""
                    token = parts[1] if len(parts) > 1 else ""
                    
                    # Submit attendance
                    self._submit_attendance(session_id, token)
                else:
                    self._show_message("Không quét được mã QR", "error")
            except Exception as e:
                self._show_message(f"Lỗi khi quét QR: {str(e)}", "error")
    
    def _handle_submit(self):
        """Xử lý submit attendance."""
        session_id = self.session_entry.get().strip()
        token = self.token_entry.get().strip() if self.token_entry.get() else None
        
        if not session_id:
            self._show_message("Vui lòng nhập mã phiên điểm danh", "error")
            return
        
        self._submit_attendance(session_id, token)
    
    def _submit_attendance(self, session_id: str, token: Optional[str] = None):
        """
        Submit attendance.
        
        Args:
            session_id: Session ID
            token: Token hoặc QR data
        """
        # Disable button
        self.submit_btn.configure(state="disabled", text="⏳ Đang xử lý...")
        
        # Submit
        result = self.controller.handle_submit_attendance(
            self.student_code,
            session_id,
            token
        )
        
        # Re-enable button
        self.submit_btn.configure(state="normal", text="📝 Xác nhận điểm danh")
        
        # Show message
        if result["success"]:
            self._show_message(result["message"], "success")
            # Clear inputs
            self.session_entry.delete(0, "end")
            self.token_entry.delete(0, "end")
        else:
            self._show_message(result["message"], "error")
    
    def _show_message(self, message: str, msg_type: str = "info"):
        """
        Hiển thị message.
        
        Args:
            message: Message text
            msg_type: "success", "error", or "info"
        """
        if msg_type == "success":
            color = COLORS["success"]
            icon = "✅"
        elif msg_type == "error":
            color = COLORS["error"]
            icon = "❌"
        else:
            color = COLORS["info"]
            icon = "ℹ️"
        
        self.message_label.configure(
            text=f"{icon} {message}",
            text_color=color
        )
