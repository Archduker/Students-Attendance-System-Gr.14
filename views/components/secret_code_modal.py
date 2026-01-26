"""
Secret Code Modal - Session Code Entry Dialog
=============================================

Modal dialog cho phép sinh viên điểm danh bằng cách nhập mã bí mật (secret code).

Author: Group 14
"""

import customtkinter as ctk
from typing import Optional, Callable


class SecretCodeModal(ctk.CTkToplevel):
    """
    Modal dialog để nhập secret code cho điểm danh.
    
    Features:
        - Input field cho secret code
        - Validation
        - Submit và callback khi thành công
        
    Example:
        >>> def on_code_submit(code):
        ...     return True, "Success"
        >>> modal = SecretCodeModal(parent, on_submit=on_code_submit)
    """
    
    def __init__(
        self,
        master,
        student_code: str,
        on_code_submit: Optional[Callable[[str], tuple[bool, str]]] = None
    ):
        """
        Khởi tạo Secret Code Modal.
        
        Args:
            master: Parent widget
            student_code: Mã sinh viên
            on_code_submit: Callback (code) -> (success, message)
        """
        super().__init__(master)
        
        self.student_code = student_code
        self.on_code_submit = on_code_submit
        
        # Configure modal
        self.title("Enter Secret Code")
        self.geometry("450x350")
        self.resizable(False, False)
        
        # Center modal
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (350 // 2)
        self.geometry(f"450x350+{x}+{y}")
        
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
        
        # Icon
        icon_frame = ctk.CTkFrame(
            container,
            width=70,
            height=70,
            fg_color="#F3F4F6",
            corner_radius=35
        )
        icon_frame.pack(pady=(10, 20))
        
        icon_label = ctk.CTkLabel(
            icon_frame,
            text="🔑",
            font=("Arial", 32)
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_label = ctk.CTkLabel(
            container,
            text="Enter Secret Code",
            font=("Inter", 22, "bold"),
            text_color="#1E293B"
        )
        title_label.pack(pady=(0, 8))
        
        # Description
        desc_label = ctk.CTkLabel(
            container,
            text="Enter the unique session code provided\nby your teacher",
            font=("Inter", 13),
            text_color="#64748B"
        )
        desc_label.pack(pady=(0, 25))
        
        # Code input
        self.code_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter session code...",
            font=("Inter", 15),
            width=390,
            height=50,
            border_width=2,
            corner_radius=10
        )
        self.code_entry.pack(pady=(0, 15))
        
        # Focus on entry
        self.code_entry.focus()
        
        # Bind Enter key
        self.code_entry.bind("<Return>", lambda e: self._on_submit())
        
        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=("Inter", 12),
            text_color="#3B82F6"
        )
        self.status_label.pack(pady=(0, 20))
        
        # Buttons container
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x")
        
        # Cancel button
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancel",
            font=("Inter", 13),
            fg_color="gray40",
            hover_color="gray30",
            text_color="white",
            corner_radius=10,
            width=180,
            height=45,
            command=self._on_close
        )
        cancel_btn.pack(side="left")
        
        # Submit button
        self.submit_btn = ctk.CTkButton(
            btn_frame,
            text="Submit",
            font=("Inter", 13, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            corner_radius=10,
            width=180,
            height=45,
            command=self._on_submit
        )
        self.submit_btn.pack(side="right")
    
    def _on_submit(self):
        """Handle submit button."""
        code = self.code_entry.get().strip()
        
        # Validate input
        if not code:
            self._update_status("❌ Please enter a code", "#EF4444")
            return
        
        if len(code) < 3:
            self._update_status("❌ Code is too short", "#EF4444")
            return
        
        # Disable button to prevent double submit
        self.submit_btn.configure(state="disabled", text="Submitting...")
        self._update_status("⏳ Verifying code...", "#3B82F6")
        
        # Call callback
        if self.on_code_submit:
            try:
                success, message = self.on_code_submit(code)
                
                if success:
                    self._update_status(f"✅ {message}", "#10B981")
                    # Auto close after 1.5 seconds
                    self.after(1500, self._on_close)
                else:
                    self._update_status(f"❌ {message}", "#EF4444")
                    # Re-enable button
                    self.submit_btn.configure(state="normal", text="Submit")
                    # Clear input
                    self.code_entry.delete(0, "end")
                    self.code_entry.focus()
            except Exception as e:
                self._update_status(f"❌ Error: {str(e)}", "#EF4444")
                self.submit_btn.configure(state="normal", text="Submit")
    
    def _update_status(self, text: str, color: str):
        """Update status label."""
        self.status_label.configure(text=text, text_color=color)
    
    def _on_close(self):
        """Handle modal close."""
        self.destroy()
