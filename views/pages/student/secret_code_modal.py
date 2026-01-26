import customtkinter as ctk
from views.styles.theme import COLORS, FONTS

class SecretCodeModal(ctk.CTkToplevel):
    def __init__(self, parent, session_options: list, on_submit):
        super().__init__(parent)
        self.title("Enter Secret Code")
        self.geometry("400x350")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.wait_visibility()
        self.grab_set()
        
        self.session_options = session_options
        self.on_submit = on_submit
        
        self.configure(fg_color=COLORS["bg_primary"])
        
        self._create_widgets()
        self._center_window()

    def _create_widgets(self):
        # Header
        icon_lbl = ctk.CTkLabel(
            self, 
            text="T", 
            font=("Inter", 40), 
            text_color=COLORS["primary"],
            fg_color="#F3F4F6",
            width=80,
            height=80,
            corner_radius=10
        )
        icon_lbl.pack(pady=(30, 15))
        
        title = ctk.CTkLabel(
            self, 
            text="Enter Secret Code", 
            font=("Inter", 18, "bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack()
        
        sub = ctk.CTkLabel(
            self, 
            text="Enter the unique session code provided\nby your teacher.", 
            font=("Inter", 12),
            text_color=COLORS["text_secondary"]
        )
        sub.pack(pady=(5, 20))
        
        # Form
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.pack(fill="x", padx=40)
        
        # Subject Dropdown
        # Mapping display string to session object/id
        self.session_map = {f"{s['class_name']} ({s['subject_code']})": s for s in self.session_options}
        values = list(self.session_map.keys())
        
        self.subject_var = ctk.StringVar(value=values[0] if values else "No Active Sessions")
        
        self.subject_menu = ctk.CTkOptionMenu(
            self.form_frame,
            variable=self.subject_var,
            values=values if values else ["No Active Sessions"],
            fg_color=COLORS["bg_secondary"],
            text_color=COLORS["text_primary"],
            button_color=COLORS["secondary"],
            button_hover_color=COLORS["secondary_hover"],
            height=35
        )
        self.subject_menu.pack(fill="x", pady=(0, 10))
        
        # Code Input
        self.code_entry = ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Enter Code...",
            height=35,
            border_color=COLORS["border"],
            font=("Inter", 14)
        )
        self.code_entry.pack(fill="x", pady=(0, 20))
        
        # Submit Button
        self.submit_btn = ctk.CTkButton(
            self.form_frame,
            text="Submit Attendance",
            height=40,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=("Inter", 13, "bold"),
            command=self._handle_submit
        )
        self.submit_btn.pack(fill="x")
        
        if not values:
            self.code_entry.configure(state="disabled")
            self.submit_btn.configure(state="disabled")

    def _handle_submit(self):
        selection = self.subject_var.get()
        code = self.code_entry.get().strip()
        
        if not code:
            return # Could show error
            
        if selection in self.session_map:
            session = self.session_map[selection]
            # Call callback with session_id and code
            self.on_submit(session["session_id"], code)
            self.destroy()

    def _center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'+{x}+{y}')
