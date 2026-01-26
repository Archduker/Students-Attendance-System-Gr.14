import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import threading
from views.styles.theme import COLORS
from utils.qr_decoder import QRDecoder

class QRScanModal(ctk.CTkToplevel):
    def __init__(self, parent, on_scan_success):
        super().__init__(parent)
        self.title("Scan QR Code")
        self.geometry("600x500")
        
        # Make modal
        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        
        self.on_scan_success = on_scan_success
        self.scanning = False
        self.cap = None
        
        self.configure(fg_color=COLORS["bg_primary"])
        
        self._create_widgets()
        self._center_window()
        
        # Handle close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _create_widgets(self):
        # Header
        title = ctk.CTkLabel(
            self, 
            text="Scan QR Code", 
            font=("Inter", 18, "bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack(pady=(20, 5))
        
        sub = ctk.CTkLabel(
            self, 
            text="Scan the QR code displayed by your teacher.", 
            font=("Inter", 12),
            text_color=COLORS["text_secondary"]
        )
        sub.pack(pady=(0, 20))
        
        # Camera Preview Area
        self.preview_frame = ctk.CTkFrame(
            self, 
            width=400, 
            height=300, 
            fg_color="#000000"
        )
        self.preview_frame.pack(pady=10)
        self.preview_frame.pack_propagate(False)
        
        self.camera_label = ctk.CTkLabel(self.preview_frame, text="Camera Off", text_color="white")
        self.camera_label.pack(expand=True, fill="both")
        
        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20, fill="x", padx=50)
        
        self.upload_btn = ctk.CTkButton(
            btn_frame,
            text="Upload Image",
            command=self._handle_upload,
            fg_color=COLORS["secondary"],
            hover_color=COLORS["secondary_hover"],
            width=140
        )
        self.upload_btn.pack(side="left", padx=10, expand=True)
        
        self.camera_btn = ctk.CTkButton(
            btn_frame,
            text="Start Camera",
            command=self._toggle_camera,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            width=140
        )
        self.camera_btn.pack(side="right", padx=10, expand=True)
        
        self.status_lbl = ctk.CTkLabel(self, text="", text_color=COLORS["error"])
        self.status_lbl.pack(pady=5)

    def _handle_upload(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            self.status_lbl.configure(text="Processing...", text_color=COLORS["info"])
            # Run in thread to not freeze UI
            threading.Thread(target=self._process_image_file, args=(file_path,), daemon=True).start()

    def _process_image_file(self, path):
        data = QRDecoder.decode_image(path)
        if data:
            self.after(0, lambda: self._success(data))
        else:
            self.after(0, lambda: self.status_lbl.configure(text="No QR code found in image.", text_color=COLORS["error"]))

    def _toggle_camera(self):
        if self.scanning:
            self._stop_camera()
        else:
            self._start_camera()

    def _start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.status_lbl.configure(text="Could not open camera.", text_color=COLORS["error"])
            return
            
        self.scanning = True
        self.camera_btn.configure(text="Stop Camera", fg_color=COLORS["error"], hover_color="#DC2626")
        self._update_camera()

    def _stop_camera(self):
        self.scanning = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.camera_btn.configure(text="Start Camera", fg_color=COLORS["primary"], hover_color=COLORS["primary_hover"])
        self.camera_label.configure(image=None, text="Camera Off")

    def _update_camera(self):
        if not self.scanning or not self.cap:
            return
            
        ret, frame = self.cap.read()
        if ret:
            # Decode frame
            data = QRDecoder.decode_frame(frame)
            if data:
                self._stop_camera()
                self._success(data)
                return

            # Convert to CTkImage
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            # Resize
            img = img.resize((400, 300), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 300))
            
            self.camera_label.configure(text="", image=ctk_img)
            self.camera_label.image = ctk_img # Keep ref
            
        self.after(10, self._update_camera)

    def _success(self, data):
        self.status_lbl.configure(text="QR Code Scanned!", text_color=COLORS["success"])
        self.on_scan_success(data)
        self.destroy()

    def _on_close(self):
        self._stop_camera()
        self.destroy()

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
