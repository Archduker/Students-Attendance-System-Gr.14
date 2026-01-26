"""
Session Detail View - Chi tiết phiên điểm danh & Điểm danh thủ công
===================================================================

Page quản lý chi tiết một phiên điểm danh, danh sách sinh viên.
Match UI from Image 3.
"""

import customtkinter as ctk
from typing import Optional, List
from datetime import datetime
import threading
import time
import qrcode
import secrets
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox

class SessionDetailPage(ctk.CTkFrame):
    """
    Page chi tiết session / manual entry.
    Matches Image 3 UI.
    """
    
    def __init__(self, parent, session_id=None):
        super().__init__(parent, fg_color="transparent")
        self.session_id = session_id
        
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # State
        self.is_session_active = False
        self.qr_image_ref = None
        self.timer_thread = None
        self.qr_thread = None
        self.stop_event = threading.Event()
        self.duration_minutes = 1
        
        self._setup_ui()
        # self.load_data()

    def _setup_ui(self):
        # 1. Header Area
        self._create_header(self)
        
        # 2. Main Card
        self._create_roster_card(self)

    def _create_header(self, parent):
        header_frm = ctk.CTkFrame(parent, fg_color="transparent")
        header_frm.grid(row=0, column=0, sticky="ew", pady=(0, 20), padx=20)
        
        # Title
        title_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        title_area.pack(side="left")
        
        ctk.CTkLabel(title_area, text="Attendance Management", font=("Inter", 24, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(title_area, text="Review lab sessions or manually update student status for cohorts (~60 students)", font=("Inter", 12), text_color="#94A3B8").pack(anchor="w")

        # Buttons
        btn_area = ctk.CTkFrame(header_frm, fg_color="transparent")
        btn_area.pack(side="right")
        
        # HISTORY (Outline)
        ctk.CTkButton(
            btn_area, text="HISTORY", fg_color="transparent", border_width=1, border_color="#E2E8F0",
            text_color="#64748B", font=("Inter", 11, "bold"), width=80, height=32, corner_radius=16, hover_color="#F1F5F9"
        ).pack(side="left", padx=(0, 10))
        
        # MANUAL ENTRY (Dark/Active) - as per image 3
        # Controls Frame
        ctrl_frame = ctk.CTkFrame(btn_area, fg_color="transparent")
        ctrl_frame.pack(side="left")

        # Duration Selector
        self.duration_var = ctk.StringVar(value="2 min")
        self.duration_combo = ctk.CTkOptionMenu(
            ctrl_frame,
            values=[f"{i} min" for i in range(1, 6)],
            variable=self.duration_var,
            width=80,
            height=32,
            fg_color="#F1F5F9",
            text_color="#0F172A",
            button_color="#CBD5E1",
            button_hover_color="#94A3B8"
        )
        self.duration_combo.pack(side="left", padx=(0, 10))

        # START / STOP Button
        self.action_btn = ctk.CTkButton(
            ctrl_frame, 
            text="START SESSION", 
            fg_color="#0F172A", 
            text_color="white",
            font=("Inter", 11, "bold"), 
            width=120, 
            height=32, 
            corner_radius=16, 
            hover_color="#1E293B",
            command=self.toggle_session
        )
        self.action_btn.pack(side="left")
        
        # Cut QR Button (Hidden by default)
        self.cut_qr_btn = ctk.CTkButton(
            ctrl_frame,
            text="CUT QR",
            fg_color="#E2E8F0",
            text_color="#0F172A",
            font=("Inter", 11, "bold"),
            width=80,
            height=32,
            corner_radius=16,
            hover_color="#CBD5E1",
            command=self.cut_qr_image
        )


    def _create_roster_card(self, parent):
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, border_width=1, border_color="#E2E8F0")
        card.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        # Card Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=25)
        
        info = ctk.CTkFrame(header, fg_color="transparent")
        info.pack(side="left")
        
        ctk.CTkLabel(info, text="Data Science Roster", font=("Inter", 18, "bold"), text_color="#0F172A").pack(anchor="w")
        self.subtitle_label = ctk.CTkLabel(info, text="Machine Learning - Cohort Average: 60 Scholars", font=("Inter", 12), text_color="#94A3B8")
        self.subtitle_label.pack(anchor="w")
        
        # QR Code Display Area (Initially Hidden)
        self.qr_frame = ctk.CTkFrame(card, fg_color="#F8FAFC", corner_radius=10)
        
        self.qr_label = ctk.CTkLabel(self.qr_frame, text="")
        self.qr_label.pack(pady=20)
        
        self.timer_label = ctk.CTkLabel(self.qr_frame, text="00:00", font=("Inter", 24, "bold"), text_color="#EF4444")
        self.timer_label.pack(pady=(0, 20))

        # Controls (Search + Button)
        controls = ctk.CTkFrame(header, fg_color="transparent")
        controls.pack(side="right")
        
        search_frm = ctk.CTkFrame(controls, fg_color="transparent", border_width=1, border_color="#E2E8F0", corner_radius=20, width=200, height=35)
        search_frm.pack(side="left", padx=(0, 10))
        search_frm.pack_propagate(False)
        ctk.CTkLabel(search_frm, text="🔍", font=("Arial", 12), text_color="#94A3B8").pack(side="left", padx=(10, 5))
        ctk.CTkEntry(search_frm, placeholder_text="Search scholar...", border_width=0, fg_color="transparent", height=30, font=("Inter", 12)).pack(fill="x")
        
        ctk.CTkButton(
            controls, text="SET 100% PRESENT", fg_color="#0F172A", text_color="white",
            font=("Inter", 11, "bold"), width=150, height=35, corner_radius=8, hover_color="#1E293B"
        ).pack(side="left")

        # Student List
        self.list_frame = ctk.CTkScrollableFrame(card, fg_color="transparent")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Mock Students
        students = [
            ("Phan Nhat Tai", "S01", "09:12 AM", "present"),
            ("Hoang Thuy Linh", "S02", "09:13 AM", "present"),
            ("Dam Vinh Hung", "S03", "-", "absent"),
            ("Tran Thi Bich Phuong", "S04", "09:12 AM", "late"),
            ("Ho Ngoc Ha", "S05", "09:20 AM", "present"),
        ]
        
        for name, sid, ping, status in students:
            self._add_student_row(self.list_frame, name, sid, ping, status)

    def _add_student_row(self, parent, name, student_id, last_ping, initial_status):
        row = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        row.pack(fill="x", pady=5)
        
        # 1. Avatar + Info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", padx=10)
        
        # Avatar placeholder
        avatar = ctk.CTkLabel(
            info_frame, text="PT", width=40, height=40, corner_radius=20,
            fg_color="#F1F5F9", text_color="#64748B", font=("Inter", 12, "bold")
        )
        avatar.pack(side="left", padx=(0, 15))
        
        # Text
        text_f = ctk.CTkFrame(info_frame, fg_color="transparent")
        text_f.pack(side="left")
        
        ctk.CTkLabel(text_f, text=name, font=("Inter", 13, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(text_f, text=f"ID: {student_id} LAST PING: {last_ping}", font=("Inter", 10, "bold"), text_color="#94A3B8").pack(anchor="w")

        # 2. Status Buttons
        status_frame = ctk.CTkFrame(row, fg_color="transparent")
        status_frame.pack(side="right", padx=10)
        
        # Determine colors based on status
        present_fg = "#DCFCE7" if initial_status == "present" else "transparent"
        present_icon_c = "#22C55E" if initial_status == "present" else "#CBD5E1"
        
        late_fg = "#FEF3C7" if initial_status == "late" else "transparent"
        late_icon_c = "#D97706" if initial_status == "late" else "#CBD5E1"

        absent_fg = "#FEE2E2" if initial_status == "absent" else "transparent"
        absent_icon_c = "#EF4444" if initial_status == "absent" else "#CBD5E1"

        # Buttons (Circular Icon style)
        self._create_status_btn(status_frame, "✔️", present_fg, present_icon_c) # Present
        self._create_status_btn(status_frame, "📋", late_fg, late_icon_c)    # Late (Clipboard icon)
        self._create_status_btn(status_frame, "✖️", absent_fg, absent_icon_c)  # Absent
        
        # Separator
        ctk.CTkFrame(parent, height=1, fg_color="#F1F5F9").pack(fill="x", padx=10)

    def _create_status_btn(self, parent, icon, fg_color, text_color):
        btn = ctk.CTkButton(
            parent,
            text=icon,
            width=36,
            height=36,
            corner_radius=18,
            fg_color=fg_color,
            text_color=text_color,
            font=("Arial", 16),
            hover_color="#F1F5F9",
             # No command for UI demo
        )
        btn.pack(side="left", padx=5)

    def toggle_session(self):
        if not self.is_session_active:
            self.start_session()
        else:
            self.stop_session()

    def start_session(self):
        try:
            minutes = int(self.duration_var.get().split()[0])
            self.duration_seconds = minutes * 60
        except:
            self.duration_seconds = 60
            
        self.is_session_active = True
        self.stop_event.clear()
        
        # Update UI
        self.action_btn.configure(text="STOP SESSION", fg_color="#EF4444", hover_color="#DC2626")
        self.cut_qr_btn.pack(side="left", padx=(10, 0))
        self.duration_combo.configure(state="disabled")
        
        # Show QR Frame
        self.list_frame.pack_forget()
        self.qr_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Start Threads
        self.qr_thread = threading.Thread(target=self._qr_loop, daemon=True)
        self.timer_thread = threading.Thread(target=self._timer_loop, daemon=True)
        
        self.qr_thread.start()
        self.timer_thread.start()

    def stop_session(self):
        self.is_session_active = False
        self.stop_event.set()
        
        # Update UI
        self.action_btn.configure(text="START SESSION", fg_color="#0F172A", hover_color="#1E293B")
        self.cut_qr_btn.pack_forget()
        self.duration_combo.configure(state="normal")
        self.timer_label.configure(text="00:00")
        
        # Hide QR, Show List
        self.qr_frame.pack_forget()
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def _qr_loop(self):
        """Regenerate QR every 30 seconds"""
        while not self.stop_event.is_set():
            # Generate QR Data
            timestamp = int(datetime.now().timestamp())
            token = secrets.token_hex(8)
            # Format: session_id|token|timestamp
            data = f"{self.session_id or 'TEST'}|{token}|{timestamp}"
            
            # Create QR Image
            qr = qrcode.QRCode(box_size=10, border=2)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Update UI on main thread
            self.after(0, lambda i=img: self._update_qr_image(i))
            
            # Wait 30s or stop
            for _ in range(30):
                if self.stop_event.is_set(): break
                time.sleep(1)

    def _update_qr_image(self, pil_image):
        self.current_qr_image = pil_image # Save ref for cut/save
        ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(300, 300))
        self.qr_label.configure(image=ctk_img)

    def _timer_loop(self):
        remaining = self.duration_seconds
        while remaining > 0 and not self.stop_event.is_set():
            mins, secs = divmod(remaining, 60)
            time_str = f"{mins:02d}:{secs:02d}"
            self.after(0, lambda t=time_str: self.timer_label.configure(text=t))
            
            time.sleep(1)
            remaining -= 1
            
        if remaining <= 0 and not self.stop_event.is_set():
            self.after(0, self.stop_session)
            self.after(0, lambda: tk.messagebox.showinfo("Session Ended", "Attendance session finished."))

    def cut_qr_image(self):
        """Save QR Code to file (Cut/Export)"""
        if hasattr(self, 'current_qr_image') and self.current_qr_image:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                title="Save QR Code"
            )
            if filename:
                self.current_qr_image.save(filename)
                tk.messagebox.showinfo("Saved", f"QR Code saved to {filename}")

