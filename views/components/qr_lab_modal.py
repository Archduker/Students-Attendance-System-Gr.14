"""
QR Lab Modal - QR Code Display for Attendance
==============================================

Modal hiển thị QR code và secret code cho students điểm danh.
CHỈ dành cho Teacher - GENERATE QR code, không scan.

Author: Group 14
"""

import customtkinter as ctk
from typing import Optional, Callable
from PIL import Image, ImageTk
from datetime import datetime
import io


class QRLabModal(ctk.CTkToplevel):
    """
    Modal để hiển thị QR code và secret code cho attendance.
    
    Features:
        - Hiển thị QR code image (300x300px)
        - Secret code với nút copy
        - Session information (status, times)
        - Refresh QR button
        
    Example:
        >>> modal = QRLabModal(
        ...     master=parent,
        ...     session_data={...},
        ...     qr_image=pil_image,
        ...     on_refresh=refresh_callback
        ... )
    """
    
    def __init__(
        self,
        master,
        session_data: dict,
        qr_image: Image.Image,
        on_refresh: Optional[Callable] = None,
        on_close: Optional[Callable] = None
    ):
        """
        Khởi tạo QR Lab Modal.
        
        Args:
            master: Parent widget
            session_data: Dict containing session info:
                - session_id: str
                - secret_code: str
                - status: str (ACTIVE/CLOSED)
                - start_time: datetime
                - end_time: datetime
                - class_name: str
            qr_image: PIL Image object của QR code
            on_refresh: Callback để refresh QR code
            on_close: Callback khi đóng modal
        """
        super().__init__(master)
        
        self.session_data = session_data
        self.qr_image = qr_image
        self.on_refresh = on_refresh
        self.on_close_callback = on_close
        
        # Configure modal
        self.title("Attendance QR Code")
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Center modal
        self.update_idletasks()  
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (750 // 2)
        self.geometry(f"600x750+{x}+{y}")
        
        # Make modal
        self.transient(master)
        self.grab_set()
        
        # Handle close
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        self._init_ui()
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Main container
        container = ctk.CTkFrame(self, fg_color="white")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Attendance QR Code",
            font=("Inter", 24, "bold"),
            text_color="#1E293B"
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            container,
            text="Students can scan this QR code or enter the secret code\n(provided via Remote Link) to submit attendance.",
            font=("Inter", 13),
            text_color="#64748B",
            justify="center"
        )
        desc_label.pack(pady=(0, 25))
        
        # QR Code Display
        self._create_qr_display(container)
        
        # Divider
        self._create_divider(container)
        
        # Secret Code Section
        self._create_secret_code_section(container)
        
        # Divider
        self._create_divider(container)
        
        # Session Info
        self._create_session_info(container)
        
        # Divider
        self._create_divider(container)
        
        # Action Buttons
        self._create_action_buttons(container)
    
    def _create_qr_display(self, parent):
        """Tạo khu vực hiển thị QR code."""
        qr_container = ctk.CTkFrame(parent, fg_color="#F3F4F6", corner_radius=15)
        qr_container.pack(pady=(0, 20))
        
        # Convert PIL to CTkImage
        if self.qr_image:
            # Resize if needed
            qr_size = 300
            qr_resized = self.qr_image.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo_image = ImageTk.PhotoImage(qr_resized)
            
            # Display
            qr_label = ctk.CTkLabel(qr_container, image=photo_image, text="")
            qr_label.image = photo_image  # Keep reference
            qr_label.pack(padx=20, pady=20)
        else:
            # Placeholder if no image
            placeholder = ctk.CTkLabel(
                qr_container,
                text="QR Code\n300 x 300",
                font=("Inter", 16),
                text_color="#94A3B8",
                width=300,
                height=300
            )
            placeholder.pack(padx=20, pady=20)
    
    def _create_secret_code_section(self, parent):
        """Tạo section hiển thị secret code."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Secret Code:",
            font=("Inter", 14, "bold"),
            text_color="#1E293B"
        )
        label.pack(anchor="w", pady=(0, 10))
        
        # Code display + Copy button
        code_frame = ctk.CTkFrame(parent, fg_color="#F3F4F6", corner_radius=10)
        code_frame.pack(fill="x", pady=(0, 10))
        
        # Secret code text
        secret_code = self.session_data.get("secret_code", "N/A")
        code_label = ctk.CTkLabel(
            code_frame,
            text=secret_code,
            font=("Inter", 28, "bold"),
            text_color="#1E293B"
        )
        code_label.pack(side="left", padx=20, pady=15)
        
        # Copy button
        self.copy_btn = ctk.CTkButton(
            code_frame,
            text="Copy",
            font=("Inter", 13, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            corner_radius=8,
            width=80,
            height=35,
            command=self._copy_secret_code
        )
        self.copy_btn.pack(side="right", padx=20)
        
        # Note
        note_label = ctk.CTkLabel(
            parent,
            text="📝 This code can be shared with remote students",
            font=("Inter", 11),
            text_color="#64748B"
        )
        note_label.pack(anchor="w")
    
    def _create_session_info(self, parent):
        """Tạo session information section."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Session Information:",
            font=("Inter", 14, "bold"),
            text_color="#1E293B"
        )
        label.pack(anchor="w", pady=(0, 12))
        
        # Info frame
        info_frame = ctk.CTkFrame(parent, fg_color="transparent")
        info_frame.pack(fill="x")
        
        # Status
        status = self.session_data.get("status", "UNKNOWN")
        status_color = "#10B981" if status == "ACTIVE" else "#94A3B8"
        status_bg_color = "#D1FAE5" if status == "ACTIVE" else "#F1F5F9"  # Solid colors instead of alpha
        
        status_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        status_row.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            status_row,
            text="Status:",
            font=("Inter", 12),
            text_color="#64748B",
            width=80,
            anchor="w"
        ).pack(side="left")
        
        status_badge = ctk.CTkLabel(
            status_row,
            text=status,
            font=("Inter", 11, "bold"),
            text_color=status_color,
            fg_color=status_bg_color,  # Use solid color
            corner_radius=6,
            padx=12,
            pady=4
        )
        status_badge.pack(side="left")
        
        # Start time
        start_time = self.session_data.get("start_time")
        if start_time:
            start_str = start_time.strftime("%Y-%m-%d %H:%M") if isinstance(start_time, datetime) else str(start_time)
            
            start_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            start_row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                start_row,
                text="Start:",
                font=("Inter", 12),
                text_color="#64748B",
                width=80,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                start_row,
                text=start_str,
                font=("Inter", 12, "bold"),
                text_color="#1E293B"
            ).pack(side="left")
        
        # End time
        end_time = self.session_data.get("end_time")
        if end_time:
            end_str = end_time.strftime("%Y-%m-%d %H:%M") if isinstance(end_time, datetime) else str(end_time)
            
            end_row = ctk.CTkFrame(info_frame, fg_color="transparent")
            end_row.pack(fill="x", pady=3)
            
            ctk.CTkLabel(
                end_row,
                text="Expires:",
                font=("Inter", 12),
                text_color="#64748B",
                width=80,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                end_row,
                text=end_str,
                font=("Inter", 12, "bold"),
                text_color="#1E293B"
            ).pack(side="left")
        
        # Class name
        class_name = self.session_data.get("class_name", "N/A")
        
        class_row = ctk.CTkFrame(info_frame, fg_color="transparent")
        class_row.pack(fill="x", pady=3)
        
        ctk.CTkLabel(
            class_row,
            text="Class:",
            font=("Inter", 12),
            text_color="#64748B",
            width=80,
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            class_row,
            text=class_name,
            font=("Inter", 12, "bold"),
            text_color="#1E293B"
        ).pack(side="left")
    
    def _create_action_buttons(self, parent):
        """Tạo action buttons."""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(10, 0))
        
        # Refresh QR button (nếu có callback)
        if self.on_refresh:
            refresh_btn = ctk.CTkButton(
                btn_frame,
                text="🔄  Refresh QR",
                font=("Inter", 13, "bold"),
                fg_color="#10B981",
                hover_color="#059669",
                text_color="white",
                corner_radius=10,
                width=200,
                height=40,
                command=self._handle_refresh
            )
            refresh_btn.pack(side="left")
        
        # Close button
        close_btn = ctk.CTkButton(
            btn_frame,
            text="Close",
            font=("Inter", 13),
            fg_color="gray40",
            hover_color="gray30",
            text_color="white",
            corner_radius=10,
            width=150,
            height=40,
            command=self._on_close
        )
        close_btn.pack(side="right")
    
    def _create_divider(self, parent):
        """Tạo divider line."""
        divider = ctk.CTkFrame(parent, height=1, fg_color="#E5E7EB")
        divider.pack(fill="x", pady=15)
    
    def _copy_secret_code(self):
        """Copy secret code to clipboard."""
        secret_code = self.session_data.get("secret_code", "")
        if secret_code:
            # Copy to clipboard
            self.clipboard_clear()
            self.clipboard_append(secret_code)
            
            # Visual feedback
            self.copy_btn.configure(text="Copied!", fg_color="#10B981")
            
            # Reset sau 2 giây
            self.after(2000, lambda: self.copy_btn.configure(text="Copy", fg_color="#3B82F6"))
    
    def _handle_refresh(self):
        """Handle refresh QR button."""
        if self.on_refresh:
            # Call refresh callback
            new_qr_image = self.on_refresh()
            
            if new_qr_image:
                # Update QR image
                self.qr_image = new_qr_image
                # Rebuild UI to show new QR
                for widget in self.winfo_children():
                    widget.destroy()
                self._init_ui()
    
    def _on_close(self):
        """Handle modal close."""
        if self.on_close_callback:
            self.on_close_callback()
        self.destroy()
