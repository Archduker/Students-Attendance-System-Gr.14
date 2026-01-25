"""
Submit Attendance Page - Student Attendance Submission
======================================================

Trang cho phép sinh viên submit điểm danh qua:
1. Scan QR Code (camera hoặc upload ảnh)
2. Enter Secret Code (mã bí mật)

Author: Group 14
"""

import customtkinter as ctk
from views.components import QRScanModal, SecretCodeModal


class SubmitAttendancePage(ctk.CTkFrame):
    """
    Trang Submit Attendance cho sinh viên
    
    Features:
        - 2 method cards: QR Code và Secret Code
        - Mở modal tương ứng khi click
        - Integrate với student controller
        
    Example:
        >>> page = SubmitAttendancePage(
        ...     master=content_area,
        ...     user=student_user,
        ...     student_controller=controller
        ... )
    """
    
    def __init__(
        self, 
        master, 
        on_navigate=None,
        user=None,
        student_controller=None
    ):
        """
        Khởi tạo Submit Attendance Page.
        
        Args:
            master: Parent widget
            on_navigate: Navigation callback
            user: Current user object (Student)
            student_controller: StudentController instance
        """
        super().__init__(master, fg_color="#F3F4F6")
        self.pack(expand=True, fill="both")
        
        self.on_navigate = on_navigate
        self.user = user
        self.student_controller = student_controller
        
        # Get student code
        self.student_code = user.student_code if user and hasattr(user, 'student_code') else None
        
        self._init_ui()
    
    def _init_ui(self):
        """Khởi tạo giao diện."""
        # Main container - centered content
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.85)
        
        # Header section
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(pady=(0, 50))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Submit Attendance",
            font=("Inter", 36, "bold"),
            text_color="#1E293B"
        )
        title_label.pack(pady=(0, 12))
        
        # Description
        desc_label = ctk.CTkLabel(
            header_frame,
            text="Choose a method to verify your presence in class.",
            font=("Inter", 15),
            text_color="#64748B"
        )
        desc_label.pack()
        
        # Cards container
        cards_container = ctk.CTkFrame(main_container, fg_color="transparent")
        cards_container.pack()
        
        # Configure grid for cards
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=0)  # Spacer
        cards_container.grid_columnconfigure(2, weight=1)
        
        # Card 1: Scan QR Code
        self._create_qr_card(cards_container)
        
        # Spacer between cards
        spacer = ctk.CTkFrame(cards_container, fg_color="transparent", width=50)
        spacer.grid(row=0, column=1, padx=20)
        
        # Card 2: Enter Secret Code
        self._create_code_card(cards_container)
    
    def _create_qr_card(self, parent):
        """Tạo card cho Scan QR Code."""
        # Card frame
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            width=340,
            height=280,
            corner_radius=20
        )
        card.grid(row=0, column=0, sticky="nsew")
        card.grid_propagate(False)
        
        # Content container
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon container
        icon_container = ctk.CTkFrame(
            content,
            width=80,
            height=80,
            fg_color="#EFF6FF",  # Light blue
            corner_radius=15
        )
        icon_container.pack(pady=(0, 25))
        icon_container.pack_propagate(False)
        
        # QR Icon (using Unicode symbol)
        icon_label = ctk.CTkLabel(
            icon_container,
            text="⬚",  # QR-like symbol
            font=("Arial", 40),
            text_color="#3B82F6"  # Blue
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Scan QR code",
            font=("Inter", 20, "bold"),
            text_color="#1E293B"
        )
        title.pack(pady=(0, 12))
        
        # Description
        desc = ctk.CTkLabel(
            content,
            text="Scan the QR code displayed by your\nteacher on the board.",
            font=("Inter", 14),
            text_color="#94A3B8",
            justify="center"
        )
        desc.pack()
        
        # Hover effect + click handler
        card.bind("<Enter>", lambda e: card.configure(fg_color="#F8FAFC"))
        card.bind("<Leave>", lambda e: card.configure(fg_color="white"))
        card.bind("<Button-1>", lambda e: self._on_qr_card_click())
        
        # Make all children clickable
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e: self._on_qr_card_click())
            for sub_child in child.winfo_children():
                sub_child.bind("<Button-1>", lambda e: self._on_qr_card_click())
    
    def _create_code_card(self, parent):
        """Tạo card cho Enter Secret Code."""
        # Card frame
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            width=340,
            height=280,
            corner_radius=20
        )
        card.grid(row=0, column=2, sticky="nsew")
        card.grid_propagate(False)
        
        # Content container
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icon container
        icon_container = ctk.CTkFrame(
            content,
            width=80,
            height=80,
            fg_color="#F3F4F6",  # Light gray
            corner_radius=15
        )
        icon_container.pack(pady=(0, 25))
        icon_container.pack_propagate(False)
        
        # Text Icon
        icon_label = ctk.CTkLabel(
            icon_container,
            text="T",
            font=("Inter", 36, "bold"),
            text_color="#64748B"  # Gray
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="Enter Secret Code",
            font=("Inter", 20, "bold"),
            text_color="#1E293B"
        )
        title.pack(pady=(0, 12))
        
        # Description
        desc = ctk.CTkLabel(
            content,
            text="Enter the unique session code provided\nby your teacher.",
            font=("Inter", 14),
            text_color="#94A3B8",
            justify="center"
        )
        desc.pack()
        
        # Hover effect + click handler
        card.bind("<Enter>", lambda e: card.configure(fg_color="#F8FAFC"))
        card.bind("<Leave>", lambda e: card.configure(fg_color="white"))
        card.bind("<Button-1>", lambda e: self._on_code_card_click())
        
        # Make all children clickable
        for child in card.winfo_children():
            child.bind("<Button-1>", lambda e: self._on_code_card_click())
            for sub_child in child.winfo_children():
                sub_child.bind("<Button-1>", lambda e: self._on_code_card_click())
    
    def _on_qr_card_click(self):
        """Handle click trên QR card - mở QR Scan Modal."""
        if not self.student_code:
            from tkinter import messagebox
            messagebox.showerror(
                "Lỗi",
                "Không tìm thấy mã sinh viên. Vui lòng đăng nhập lại."
            )
            return
        
        # Open QR Scan Modal
        modal = QRScanModal(
            self,
            student_code=self.student_code,
            on_qr_scanned=self._handle_qr_scanned
        )
        self.wait_window(modal)
    
    def _on_code_card_click(self):
        """Handle click trên Code card - mở Secret Code Modal."""
        if not self.student_code:
            from tkinter import messagebox
            messagebox.showerror(
                "Lỗi",
                "Không tìm thấy mã sinh viên. Vui lòng đăng nhập lại."
            )
            return
        
        # Open Secret Code Modal
        modal = SecretCodeModal(
            self,
            student_code=self.student_code,
            on_code_submit=self._handle_code_submitted
        )
        self.wait_window(modal)
    
    def _handle_qr_scanned(self, qr_data: str) -> tuple[bool, str]:
        """
        Callback khi QR được quét.
        
        Args:
            qr_data: QR code data string
            
        Returns:
            Tuple (success, message)
        """
        if not self.student_controller:
            return False, "Không có student controller"
        
        # Submit attendance via controller
        result = self.student_controller.handle_qr_attendance(
            self.student_code,
            qr_data
        )
        
        return result.get("success", False), result.get("message", "Lỗi không xác định")
    
    def _handle_code_submitted(self, secret_code: str) -> tuple[bool, str]:
        """
        Callback khi code được submit.
        
        Args:
            secret_code: Secret code string
            
        Returns:
            Tuple (success, message)
        """
        if not self.student_controller:
            return False, "Không có student controller"
        
        # Submit attendance via controller
        result = self.student_controller.handle_code_attendance(
            self.student_code,
            secret_code
        )
        
        return result.get("success", False), result.get("message", "Lỗi không xác định")
