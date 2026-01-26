import customtkinter as ctk
from views.styles.theme import COLORS, FONTS
from views.pages.student.qr_scan_modal import QRScanModal
from views.pages.student.secret_code_modal import SecretCodeModal
from tkinter import messagebox

class SubmitAttendancePage(ctk.CTkFrame):
    def __init__(self, master, on_navigate=None, user=None, student_service=None, student_controller=None):
        super().__init__(master, fg_color="#F3F4F6") # Light gray bg like layout
        self.pack(expand=True, fill="both")
        
        self.on_navigate = on_navigate
        self.user = user
        self.controller = student_controller
        
        self.student_code = getattr(user, 'student_code', "UNKNOWN") if user else "UNKNOWN"
        if user and not hasattr(user, 'student_code') and hasattr(user, 'username'):
             self.student_code = user.username
        
        self._init_ui()

    def _init_ui(self):
        # 1. Header
        header_frm = ctk.CTkFrame(self, fg_color="transparent")
        header_frm.pack(fill="x", padx=40, pady=(40, 20))
        
        ctk.CTkLabel(
            header_frm, 
            text="Submit Attendance", 
            font=("Inter", 24, "bold"), 
            text_color=COLORS["text_primary"]
        ).pack(anchor="center")
        
        ctk.CTkLabel(
            header_frm, 
            text="Choose a method to verify your presence in class.", 
            font=("Inter", 14), 
            text_color=COLORS["text_secondary"]
        ).pack(anchor="center", pady=(5, 0))
        
        # 2. Cards Container
        cards_container = ctk.CTkFrame(self, fg_color="transparent")
        cards_container.pack(expand=True, fill="both", padx=40, pady=20)
        
        # Center the cards
        center_frame = ctk.CTkFrame(cards_container, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.4, anchor="center")
        
        # Scan QR Card
        self._create_card(
            center_frame,
            title="Scan QR code",
            desc="Scan the QR code displayed by your\nteacher on the board.",
            icon="📷", # Fallback icon
            icon_color="#3B82F6",
            bg_icon="#DBEAFE",
            command=self._open_qr_modal
        ).pack(side="left", padx=20)
        
        # Enter Code Card
        self._create_card(
            center_frame,
            title="Enter Secret Code",
            desc="Enter the unique session code provided\nby your teacher.",
            icon="T",
            icon_color=COLORS["text_secondary"],
            bg_icon="#F3F4F6", # Light gray
            command=self._open_code_modal
        ).pack(side="left", padx=20)
        
        # Status Label
        self.status_label = ctk.CTkLabel(self, text="", font=("Inter", 14))
        self.status_label.pack(pady=20)

    def _create_card(self, parent, title, desc, icon, icon_color, bg_icon, command):
        card = ctk.CTkButton(
            parent,
            text="",
            fg_color="white",
            hover_color="#F8FAFC",
            width=300,
            height=250,
            corner_radius=20,
            command=command,
            border_width=1,
            border_color="#E2E8F0"
        )
        # We need a frame inside the button, but CTkButton content is limited.
        # So we use a Frame and make it clickable or bind events if possible. 
        # But CTkButton is eager. Let's use Frame and bind click to it and children.
        
        card.destroy() # Revert to Frame
        
        frame = ctk.CTkFrame(
            parent,
            fg_color="white",
            width=300,
            height=220,
            corner_radius=20,
            border_width=1,
            border_color="#E2E8F0"
        )
        frame.pack_propagate(False)
        frame.bind("<Button-1>", lambda e: command())
        frame.bind("<Enter>", lambda e: frame.configure(border_color=COLORS["primary"]))
        frame.bind("<Leave>", lambda e: frame.configure(border_color="#E2E8F0"))
        
        # Icon
        icon_frame = ctk.CTkFrame(frame, width=60, height=60, fg_color=bg_icon, corner_radius=12)
        icon_frame.pack(pady=(40, 20))
        icon_frame.bind("<Button-1>", lambda e: command())
        
        ctk.CTkLabel(
            icon_frame, 
            text=icon, 
            font=("Inter", 24), 
            text_color=icon_color
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        t = ctk.CTkLabel(frame, text=title, font=("Inter", 16, "bold"), text_color=COLORS["text_primary"])
        t.pack()
        t.bind("<Button-1>", lambda e: command())
        
        # Desc
        d = ctk.CTkLabel(frame, text=desc, font=("Inter", 12), text_color=COLORS["text_secondary"], justify="center")
        d.pack(pady=(5, 0))
        d.bind("<Button-1>", lambda e: command())
        
        return frame

    def _open_qr_modal(self):
        QRScanModal(self.winfo_toplevel(), self._handle_qr_scan_success)

    def _open_code_modal(self):
        # Fetch sessions first
        if not self.controller:
            messagebox.showerror("Error", "Controller not connected.")
            return

        result = self.controller.handle_get_todays_sessions(self.student_code)
        if result["success"]:
            sessions = result["data"]
            # Filter only OPEN sessions for manual entry? 
            # Or assume user can pick any. Let's filter active/open if possible, or show all valid for today.
            # The service returns status. We probably only want OPEN ones.
            active_sessions = [s for s in sessions if s.get("status") == "OPEN"]
            
            if not active_sessions:
                 messagebox.showinfo("Info", "No active sessions found for today.")
                 return

            SecretCodeModal(self.winfo_toplevel(), active_sessions, self._handle_code_submit)
        else:
             messagebox.showerror("Error", f"Failed to fetch sessions: {result.get('error')}")

    def _handle_qr_scan_success(self, qr_data):
        # QR Data format expected: session_id|token|timestamp
        # We need to extract session_id from it to pass to submit_attendance
        # Or let controller handle parsing?
        # Controller handle_submit_attendance takes (student_code, session_id, verification_data)
        
        # Let's try to parse session_id here or pass data and let backend parse.
        # But handle_submit_attendance requires session_id as explicit arg.
        
        try:
            parts = qr_data.split("|")
            if len(parts) >= 1:
                session_id = parts[0]
                self._submit(session_id, qr_data)
            else:
                 messagebox.showerror("Error", "Invalid QR Data format.")
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing QR: {e}")

    def _handle_code_submit(self, session_id, code):
        self._submit(session_id, code)

    def _submit(self, session_id, verification_data):
        if not self.controller:
             return
             
        result = self.controller.handle_submit_attendance(
            self.student_code,
            session_id,
            verification_data
        )
        
        if result["success"]:
            messagebox.showinfo("Success", result["message"])
            self.status_label.configure(text=f"✅ {result['message']}", text_color=COLORS["success"])
        else:
            messagebox.showerror("Failed", result["message"])
            self.status_label.configure(text=f"❌ {result['message']}", text_color=COLORS["error"])
