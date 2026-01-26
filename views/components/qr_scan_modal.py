"""
QR Scan Modal - QR Code Scanning Dialog
========================================

Modal dialog cho phép sinh viên điểm danh bằng cách:
1. Upload ảnh QR code từ máy tính
2. Quét QR code qua camera (real-time)

Author: Group 14
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, Callable
import cv2
from PIL import Image, ImageTk
import threading
import time


class QRScanModal(ctk.CTkToplevel):
    """
    Modal dialog để quét QR code cho điểm danh.
    
    Features:
        - Upload QR image từ file
        - Scan QR qua camera (real-time)
        - Tự động detect và process QR code
        - Callback khi quét thành công
        
    Example:
        >>> def on_qr_detected(qr_data):
        ...     print(f"QR Data: {qr_data}")
        >>> modal = QRScanModal(parent, on_qr_scanned=on_qr_detected)
    """
    
    def __init__(
        self,
        master,
        student_code: str,
        on_qr_scanned: Optional[Callable[[str], tuple[bool, str]]] = None
    ):
        """
        Khởi tạo QR Scan Modal.
        
        Args:
            master: Parent widget
            student_code: Mã sinh viên
            on_qr_scanned: Callback (qr_data) -> (success, message)
        """
        super().__init__(master)
        
        self.student_code = student_code
        self.on_qr_scanned = on_qr_scanned
        
        # Camera state
        self.camera = None
        self.camera_running = False
        self.camera_thread = None
        
        # Configure modal
        self.title("Scan QR Code")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Center modal
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"600x700+{x}+{y}")
        
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
            text="Scan QR Code",
            font=("Inter", 24, "bold"),
            text_color="#1E293B"
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            container,
            text="Upload an image or use your camera to scan the QR code",
            font=("Inter", 13),
            text_color="#64748B"
        )
        desc_label.pack(pady=(0, 20))
        
        # Preview area
        self.preview_frame = ctk.CTkFrame(
            container,
            width=540,
            height=400,
            fg_color="#F3F4F6",
            corner_radius=15
        )
        self.preview_frame.pack(pady=(0, 20))
        self.preview_frame.pack_propagate(False)
        
        # Placeholder cho preview
        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="📷\n\nNo image or camera feed yet",
            font=("Inter", 16),
            text_color="#94A3B8"
        )
        self.preview_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            container,
            text="",
            font=("Inter", 12),
            text_color="#3B82F6"
        )
        self.status_label.pack(pady=(0, 15))
        
        # Buttons container
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(0, 10))
        
        # Upload Image button
        upload_btn = ctk.CTkButton(
            btn_frame,
            text="📁  Upload Image",
            font=("Inter", 14, "bold"),
            fg_color="#3B82F6",
            hover_color="#2563EB",
            text_color="white",
            corner_radius=10,
            width=250,
            height=45,
            command=self._on_upload_image
        )
        upload_btn.pack(side="left", padx=(0, 10))
        
        # Scan via Camera button
        camera_btn = ctk.CTkButton(
            btn_frame,
            text="📷  Scan via Camera",
            font=("Inter", 14, "bold"),
            fg_color="#10B981",
            hover_color="#059669",
            text_color="white",
            corner_radius=10,
            width=250,
            height=45,
            command=self._on_start_camera
        )
        camera_btn.pack(side="right")
        
        # Stop Camera button (hidden initially)
        self.stop_camera_btn = ctk.CTkButton(
            container,
            text="⏹  Stop Camera",
            font=("Inter", 13, "bold"),
            fg_color="#EF4444",
            hover_color="#DC2626",
            text_color="white",
            corner_radius=10,
            width=520,
            height=40,
            command=self._on_stop_camera
        )
        # Don't pack initially
        
        # Close button
        close_btn = ctk.CTkButton(
            container,
            text="Close",
            font=("Inter", 13),
            fg_color="gray40",
            hover_color="gray30",
            text_color="white",
            corner_radius=10,
            width=520,
            height=40,
            command=self._on_close
        )
        close_btn.pack(side="bottom")
    
    def _on_upload_image(self):
        """Handle upload image button."""
        # Open file dialog
        file_path = filedialog.askopenfilename(
            title="Select QR Code Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if not file_path:
            return
        
        self._update_status("Processing image...", "#3B82F6")
        
        try:
            # Read and decode QR from image
            image = cv2.imread(file_path)
            if image is None:
                self._update_status("❌ Invalid image file", "#EF4444")
                return
            
            # Display image in preview
            self._display_image(image)
            
            # Decode QR using OpenCV
            qr_detector = cv2.QRCodeDetector()
            qr_data, bbox, _ = qr_detector.detectAndDecode(image)
            
            if not qr_data:
                self._update_status("❌ No QR code found in image", "#EF4444")
                return
            
            self._update_status("✅ QR code detected! Processing...", "#10B981")
            
            # Process QR code
            self._process_qr_data(qr_data)
            
        except Exception as e:
            self._update_status(f"❌ Error: {str(e)}", "#EF4444")
    
    def _on_start_camera(self):
        """Start camera for real-time QR scanning."""
        if self.camera_running:
            return
        
        try:
            # Try to open camera
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                self._update_status("❌ Cannot access camera", "#EF4444")
                return
            
            self.camera_running = True
            self._update_status("📷 Camera active - scanning...", "#10B981")
            
            # Show stop button
            self.stop_camera_btn.pack(pady=(0, 10))
            
            # Start camera thread
            self.camera_thread = threading.Thread(target=self._camera_loop, daemon=True)
            self.camera_thread.start()
            
        except Exception as e:
            self._update_status(f"❌ Camera error: {str(e)}", "#EF4444")
    
    def _camera_loop(self):
        """Camera loop để quét QR real-time."""
        qr_detector = cv2.QRCodeDetector()
        
        while self.camera_running:
            ret, frame = self.camera.read()
            if not ret:
                break
            
            # Display frame
            self.after(0, self._display_image, frame)
            
            # Try to decode QR using OpenCV
            qr_data, bbox, _ = qr_detector.detectAndDecode(frame)
            
            if qr_data:
                # QR code found!
                # Stop camera
                self.camera_running = False
                
                # Process QR
                self.after(0, self._process_qr_data, qr_data)
                break
            
            time.sleep(0.1)  # 10 FPS
    
    def _on_stop_camera(self):
        """Stop camera."""
        self.camera_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
        
        # Hide stop button
        self.stop_camera_btn.pack_forget()
        
        # Reset preview
        self.preview_label.configure(
            text="📷\n\nCamera stopped",
            image=None
        )
        self._update_status("Camera stopped", "#64748B")
    
    def _display_image(self, cv_image):
        """Display image in preview area."""
        try:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            
            # Resize to fit preview (540x400)
            h, w = rgb_image.shape[:2]
            aspect_ratio = w / h
            
            if aspect_ratio > 540 / 400:
                # Width is limiting
                new_w = 540
                new_h = int(540 / aspect_ratio)
            else:
                # Height is limiting
                new_h = 400
                new_w = int(400 * aspect_ratio)
            
            resized = cv2.resize(rgb_image, (new_w, new_h))
            
            # Convert to PIL and then to CTkImage
            pil_image = Image.fromarray(resized)
            ctk_image = ImageTk.PhotoImage(pil_image)
            
            # Update preview
            self.preview_label.configure(
                image=ctk_image,
                text=""
            )
            self.preview_label.image = ctk_image  # Keep reference
            
        except Exception as e:
            print(f"Display error: {e}")
    
    def _process_qr_data(self, qr_data: str):
        """Process scanned QR data."""
        self._update_status("✅ QR detected! Submitting attendance...", "#10B981")
        
        # Call callback
        if self.on_qr_scanned:
            try:
                success, message = self.on_qr_scanned(qr_data)
                
                if success:
                    self._update_status(f"✅ {message}", "#10B981")
                    # Auto close after 2 seconds
                    self.after(2000, self._on_close)
                else:
                    self._update_status(f"❌ {message}", "#EF4444")
            except Exception as e:
                self._update_status(f"❌ Error: {str(e)}", "#EF4444")
    
    def _update_status(self, text: str, color: str):
        """Update status label."""
        self.status_label.configure(text=text, text_color=color)
    
    def _on_close(self):
        """Handle modal close."""
        # Stop camera if running
        if self.camera_running:
            self._on_stop_camera()
        
        self.destroy()
