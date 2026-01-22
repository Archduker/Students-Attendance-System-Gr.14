"""
Create Session Dialog - Dialog tạo phiên điểm danh
==================================================

Dialog cho phép giáo viên tạo phiên điểm danh mới.
"""

import customtkinter as ctk
from typing import Optional, Callable
from datetime import datetime, timedelta

from core.models import Teacher
from core.enums import AttendanceMethod
from controllers.teacher_controller import TeacherController


class CreateSessionDialog(ctk.CTkToplevel):
    """
    Dialog tạo phiên điểm danh mới.
    
    Chức năng:
    - Chọn lớp học
    - Chọn thời gian bắt đầu/kết thúc
    - Chọn phương thức điểm danh
    - Cấu hình các tham số
    """
    
    def __init__(
        self,
        parent,
        teacher: Teacher,
        controller: TeacherController,
        on_success: Optional[Callable] = None
    ):
        """
        Khởi tạo Create Session Dialog.
        
        Args:
            parent: Parent window
            teacher: Teacher object
            controller: TeacherController instance
            on_success: Callback khi tạo session thành công
        """
        super().__init__(parent)
        
        self.teacher = teacher
        self.controller = controller
        self.on_success_callback = on_success
        
        # Dialog settings
        self.title("Tạo phiên điểm danh mới")
        self.geometry("500x600")
        self.resizable(False, False)
        
        # Center dialog
        self.transient(parent)
        self.grab_set()
        
        self._setup_ui()
        self._load_classes()
    
    def _setup_ui(self):
        """Setup giao diện."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Tạo phiên điểm danh mới",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header.grid(row=0, column=0, padx=20, pady=20)
        
        # Form Frame
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        form_frame.grid_columnconfigure(1, weight=1)
        
        current_row = 0
        
        # Class selection
        ctk.CTkLabel(form_frame, text="Lớp học:", anchor="w").grid(
            row=current_row, column=0, padx=15, pady=10, sticky="w"
        )
        self.class_combo = ctk.CTkComboBox(form_frame, values=["Loading..."], width=250)
        self.class_combo.grid(row=current_row, column=1, padx=15, pady=10, sticky="ew")
        current_row += 1
        
        # Start time
        ctk.CTkLabel(form_frame, text="Thời gian bắt đầu:", anchor="w").grid(
            row=current_row, column=0, padx=15, pady=10, sticky="w"
        )
        start_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        start_frame.grid(row=current_row, column=1, padx=15, pady=10, sticky="ew")
        
        self.start_date = ctk.CTkEntry(start_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.start_date.pack(side="left", padx=(0, 10))
        self.start_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.start_time = ctk.CTkEntry(start_frame, placeholder_text="HH:MM", width=100)
        self.start_time.pack(side="left")
        self.start_time.insert(0, datetime.now().strftime("%H:%M"))
        
        current_row += 1
        
        # End time
        ctk.CTkLabel(form_frame, text="Thời gian kết thúc:", anchor="w").grid(
            row=current_row, column=0, padx=15, pady=10, sticky="w"
        )
        end_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        end_frame.grid(row=current_row, column=1, padx=15, pady=10, sticky="ew")
        
        self.end_date = ctk.CTkEntry(end_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.end_date.pack(side="left", padx=(0, 10))
        self.end_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        self.end_time = ctk.CTkEntry(end_frame, placeholder_text="HH:MM", width=100)
        self.end_time.pack(side="left")
        end_time_default = (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
        self.end_time.insert(0, end_time_default)
        
        current_row += 1
        
        # Attendance method
        ctk.CTkLabel(form_frame, text="Phương thức:", anchor="w").grid(
            row=current_row, column=0, padx=15, pady=10, sticky="w"
        )
        self.method_combo = ctk.CTkComboBox(
            form_frame,
            values=["QR", "LINK_TOKEN", "MANUAL", "AUTO"],
            width=250
        )
        self.method_combo.grid(row=current_row, column=1, padx=15, pady=10, sticky="ew")
        self.method_combo.set("QR")
        current_row += 1
        
        # QR window (minutes)
        ctk.CTkLabel(form_frame, text="QR hiệu lực (phút):", anchor="w").grid(
            row=current_row, column=0, padx=15, pady=10, sticky="w"
        )
        self.qr_window = ctk.CTkEntry(form_frame, width=250)
        self.qr_window.grid(row=current_row, column=1, padx=15, pady=10, sticky="ew")
        self.qr_window.insert(0, "1")
        current_row += 1
        
        # Late window (minutes)
        ctk.CTkLabel(form_frame, text="Cho phép trễ (phút):", anchor="w").grid(
            row=current_row, column=0, padx=15, pady=10, sticky="w"
        )
        self.late_window = ctk.CTkEntry(form_frame, width=250)
        self.late_window.grid(row=current_row, column=1, padx=15, pady=10, sticky="ew")
        self.late_window.insert(0, "15")
        current_row += 1
        
        # Error label
        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="#F44336",
            font=ctk.CTkFont(size=12)
        )
        self.error_label.grid(row=2, column=0, padx=20, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=3, column=0, padx=20, pady=20)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Hủy",
            command=self.on_cancel,
            width=120,
            fg_color="#757575"
        )
        cancel_btn.pack(side="left", padx=10)
        
        create_btn = ctk.CTkButton(
            button_frame,
            text="Tạo phiên",
            command=self.on_create,
            width=120,
            fg_color="#4CAF50"
        )
        create_btn.pack(side="left", padx=10)
    
    def _load_classes(self):
        """Load danh sách lớp học của giáo viên."""
        try:
            classes = self.controller.get_class_list(self.teacher)
            
            if not classes:
                self.class_combo.configure(values=["Không có lớp nào"])
                self.class_combo.set("Không có lớp nào")
            else:
                class_ids = [c.class_id for c in classes]
                self.class_combo.configure(values=class_ids)
                self.class_combo.set(class_ids[0])
        
        except Exception as e:
            print(f"Error loading classes: {e}")
            self.class_combo.configure(values=["Error loading"])
    
    def validate_form(self) -> tuple[bool, str]:
        """
        Validate form inputs.
        
        Returns:
            Tuple (is_valid, error_message)
        """
        # Validate class selection
        class_id = self.class_combo.get()
        if not class_id or class_id in ["Loading...", "Không có lớp nào", "Error loading"]:
            return False, "Vui lòng chọn lớp học"
        
        # Validate times
        try:
            start_datetime = datetime.strptime(
                f"{self.start_date.get()} {self.start_time.get()}",
                "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{self.end_date.get()} {self.end_time.get()}",
                "%Y-%m-%d %H:%M"
            )
            
            if end_datetime <= start_datetime:
                return False, "Thời gian kết thúc phải sau thời gian bắt đầu"
        
        except ValueError:
            return False, "Định dạng thời gian không hợp lệ (YYYY-MM-DD HH:MM)"
        
        # Validate QR window
        try:
            qr_window = int(self.qr_window.get())
            if qr_window <= 0:
                return False, "QR window phải > 0"
        except ValueError:
            return False, "QR window phải là số"
        
        # Validate late window
        try:
            late_window = int(self.late_window.get())
            if late_window < 0:
                return False, "Late window phải >= 0"
        except ValueError:
            return False, "Late window phải là số"
        
        return True, ""
    
    def on_create(self):
        """Handler khi click nút Tạo phiên."""
        # Clear error
        self.error_label.configure(text="")
        
        # Validate
        is_valid, error_msg = self.validate_form()
        if not is_valid:
            self.error_label.configure(text=error_msg)
            return
        
        # Get form data
        class_id = self.class_combo.get()
        start_datetime = datetime.strptime(
            f"{self.start_date.get()} {self.start_time.get()}",
            "%Y-%m-%d %H:%M"
        )
        end_datetime = datetime.strptime(
            f"{self.end_date.get()} {self.end_time.get()}",
            "%Y-%m-%d %H:%M"
        )
        method = AttendanceMethod.from_string(self.method_combo.get())
        qr_window = int(self.qr_window.get())
        late_window = int(self.late_window.get())
        
        # Create session
        try:
            success, message, session = self.controller.create_new_session(
                self.teacher,
                class_id,
                start_datetime,
                end_datetime,
                method,
                qr_window,
                late_window
            )
            
            if success:
                print(f"Session created: {session.session_id}")
                
                # Call success callback
                if self.on_success_callback:
                    self.on_success_callback()
                
                # Close dialog
                self.destroy()
            else:
                self.error_label.configure(text=message)
        
        except Exception as e:
            self.error_label.configure(text=f"Lỗi: {str(e)}")
            print(f"Error creating session: {e}")
    
    def on_cancel(self):
        """Handler khi click nút Hủy."""
        self.destroy()
