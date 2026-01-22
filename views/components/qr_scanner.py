"""
QR Scanner Component - QR code scanning for attendance
======================================================

Component để scan QR code sử dụng camera.
Tích hợp với OpenCV và pyzbar.
"""

import cv2
import customtkinter as ctk
from typing import Optional, Callable
from pyzbar import pyzbar
from PIL import Image, ImageTk
import threading

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS


class QRScanner(ctk.CTkFrame):
    """
    QR Scanner component sử dụng camera.
    
    Features:
    - Mở camera
    - Scan QR code real-time
    - Callback khi scan thành công
    """
    
    def __init__(
        self,
        parent,
        on_scan_success: Optional[Callable[[str], None]] = None,
        camera_index: int = 0,
        **kwargs
    ):
        """
        Khởi tạo QR Scanner.
        
        Args:
            parent: Parent widget
            on_scan_success: Callback function khi scan thành công
            camera_index: Index của camera (default: 0)
        """
        super().__init__(parent, **kwargs)
        
        self.on_scan_success = on_scan_success
        self.camera_index = camera_index
        self.camera = None
        self.is_scanning = False
        self.scan_thread = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Thiết lập UI components."""
        self.configure(
            fg_color=COLORS["bg_primary"],
            corner_radius=RADIUS["lg"]
        )
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=SPACING["lg"], pady=SPACING["lg"])
        
        # Title
        title = ctk.CTkLabel(
            content,
            text="📷 QR Code Scanner",
            font=(FONTS["family"], FONTS["size_xl"], FONTS["weight_bold"]),
            text_color=COLORS["text_primary"]
        )
        title.pack(pady=(0, SPACING["md"]))
        
        # Camera display area
        self.camera_label = ctk.CTkLabel(
            content,
            text="📷\n\nNhấn 'Bắt đầu quét' để mở camera",
            font=(FONTS["family"], FONTS["size_base"]),
            text_color=COLORS["text_secondary"],
            width=480,
            height=360,
            fg_color=COLORS["bg_secondary"],
            corner_radius=RADIUS["md"]
        )
        self.camera_label.pack(pady=(0, SPACING["md"]))
        
        # Control buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack()
        
        self.start_btn = ctk.CTkButton(
            btn_frame,
            text="▶️ Bắt đầu quét",
            width=150,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["success"],
            hover_color=COLORS["success"],
            command=self.start_scanning
        )
        self.start_btn.pack(side="left", padx=SPACING["sm"])
        
        self.stop_btn = ctk.CTkButton(
            btn_frame,
            text="⏹️ Dừng",
            width=150,
            height=40,
            corner_radius=RADIUS["md"],
            fg_color=COLORS["error"],
            hover_color=COLORS["error"],
            command=self.stop_scanning,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=SPACING["sm"])
        
        # Status label
        self.status_label = ctk.CTkLabel(
            content,
            text="",
            font=(FONTS["family"], FONTS["size_sm"]),
            text_color=COLORS["text_secondary"]
        )
        self.status_label.pack(pady=(SPACING["md"], 0))
    
    def start_scanning(self):
        """Bắt đầu quét QR code."""
        if self.is_scanning:
            return
        
        try:
            # Mở camera
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if not self.camera.isOpened():
                self._show_error("Không thể mở camera")
                return
            
            self.is_scanning = True
            
            # Update UI
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
            self._update_status("🔍 Đang quét QR code...", COLORS["info"])
            
            # Start scan thread
            self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
            self.scan_thread.start()
            
        except Exception as e:
            self._show_error(f"Lỗi: {str(e)}")
    
    def stop_scanning(self):
        """Dừng quét QR code."""
        self.is_scanning = False
        
        if self.camera:
            self.camera.release()
            self.camera = None
        
        # Update UI
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.camera_label.configure(
            text="📷\n\nNhấn 'Bắt đầu quét' để mở camera",
            image=None
        )
        self._update_status("Camera đã tắt", COLORS["text_secondary"])
    
    def _scan_loop(self):
        """Main scanning loop (chạy trong thread riêng)."""
        while self.is_scanning:
            if not self.camera or not self.camera.isOpened():
                break
            
            try:
                # Đọc frame từ camera
                ret, frame = self.camera.read()
                
                if not ret:
                    continue
                
                # Scan QR codes trong frame
                qr_codes = pyzbar.decode(frame)
                
                if qr_codes:
                    # Tìm thấy QR code
                    qr_data = qr_codes[0].data.decode('utf-8')
                    
                    # Stop scanning
                    self.is_scanning = False
                    
                    # Update UI (phải chạy trong main thread)
                    self.after(0, lambda: self._on_qr_found(qr_data))
                    break
                
                # Hiển thị frame lên UI (chạy trong main thread)
                self.after(0, lambda f=frame: self._update_camera_display(f))
                
            except Exception as e:
                print(f"Error in scan loop: {e}")
                break
        
        # Cleanup
        if self.camera:
            self.camera.release()
    
    def _update_camera_display(self, frame):
        """Cập nhật hiển thị camera."""
        try:
            # Resize frame
            frame = cv2.resize(frame, (480, 360))
            
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            image = Image.fromarray(frame_rgb)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image=image)
            
            # Update label
            self.camera_label.configure(image=photo, text="")
            self.camera_label.image = photo  # Keep reference
            
        except Exception as e:
            print(f"Error updating display: {e}")
    
    def _on_qr_found(self, qr_data: str):
        """Xử lý khi tìm thấy QR code."""
        # Stop scanning
        self.stop_scanning()
        
        # Update status
        self._update_status(f"✅ Đã quét: {qr_data[:20]}...", COLORS["success"])
        
        # Call callback
        if self.on_scan_success:
            self.on_scan_success(qr_data)
    
    def _update_status(self, message: str, color: str):
        """Cập nhật status message."""
        self.status_label.configure(text=message, text_color=color)
    
    def _show_error(self, message: str):
        """Hiển thị error message."""
        self._update_status(f"❌ {message}", COLORS["error"])
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
    
    def scan(self) -> Optional[str]:
        """
        Scan QR code một lần (blocking).
        
        Returns:
            QR code data hoặc None
            
        Note:
            Method này là blocking, nên cân nhắc sử dụng
            start_scanning() với callback thay vì.
        """
        try:
            camera = cv2.VideoCapture(self.camera_index)
            
            if not camera.isOpened():
                return None
            
            # Scan trong 10 giây
            timeout = 10
            start_time = cv2.getTickCount()
            
            while True:
                ret, frame = camera.read()
                
                if not ret:
                    continue
                
                # Decode QR
                qr_codes = pyzbar.decode(frame)
                
                if qr_codes:
                    qr_data = qr_codes[0].data.decode('utf-8')
                    camera.release()
                    return qr_data
                
                # Check timeout
                elapsed = (cv2.getTickCount() - start_time) / cv2.getTickFrequency()
                if elapsed > timeout:
                    break
            
            camera.release()
            return None
            
        except Exception as e:
            print(f"Error scanning QR: {e}")
            return None
    
    def __del__(self):
        """Cleanup khi destroy."""
        if self.camera:
            self.camera.release()


# Utility function để tạo QR Scanner dialog
def show_qr_scanner_dialog(
    parent,
    on_scan_success: Callable[[str], None],
    camera_index: int = 0
):
    """
    Hiển thị QR Scanner trong một dialog window.
    
    Args:
        parent: Parent window
        on_scan_success: Callback khi scan thành công
        camera_index: Index của camera
    """
    dialog = ctk.CTkToplevel(parent)
    dialog.title("QR Code Scanner")
    dialog.geometry("600x550")
    dialog.transient(parent)
    dialog.grab_set()
    
    scanner = QRScanner(
        dialog,
        on_scan_success=lambda data: (on_scan_success(data), dialog.destroy()),
        camera_index=camera_index
    )
    scanner.pack(fill="both", expand=True, padx=20, pady=20)
    
    return dialog
