import customtkinter as ctk

class SubmitAttendancePage(ctk.CTkFrame):
    def __init__(self, master, on_navigate=None):
        super().__init__(master, fg_color="#F3F4F6")
        self.pack(expand=True, fill="both")
        
        # Center Content
        self.center_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.center_frame.place(relx=0.5, rely=0.4, anchor="center", relwidth=0.8)

        # Header
        ctk.CTkLabel(
            self.center_frame,
            text="Submit Attendance",
            font=("Inter", 32, "bold"),
            text_color="#1E293B"
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            self.center_frame,
            text="Choose a method to verify your presence in class.",
            font=("Inter", 14),
            text_color="#64748B"
        ).pack(pady=(0, 60))

        # Cards Container
        self.cards_frame = ctk.CTkFrame(self.center_frame, fg_color="transparent")
        self.cards_frame.pack()

        # Method 1: QR
        self._create_card(
            self.cards_frame, 
            icon="📷", # Replace with scan icon
            title="Scan QR code",
            desc="Scan the QR code displayed by your\nteacher on the board."
        )

        # Spacer
        ctk.CTkFrame(self.cards_frame, fg_color="transparent", width=40).pack(side="left")

        # Method 2: Code
        self._create_card(
            self.cards_frame, 
            icon="T", # Replace with text input icon
            title="Enter Secret Code",
            desc="Enter the unique session code provided\nby your teacher."
        )

    def _create_card(self, parent, icon, title, desc):
        card = ctk.CTkButton(
            parent,
            text="",
            fg_color="white",
            hover_color="#F8FAFC",
            width=300,
            height=220,
            corner_radius=20,
            border_width=0, # Shadow effect simulated via color or custom draw if needed
        )
        card.pack(side="left")
        
        # Since button text layout is limited, we pack a frame INSIDE or ON TOP?
        # CTkButton doesn't support easy complex content. 
        # Better to make a frame and bind click.
        
        card_frm = ctk.CTkFrame(parent, fg_color="white", width=300, height=220, corner_radius=20)
        card_frm.pack(side="left", padx=0)
        card_frm.pack_propagate(False)
        
        # Mock Icon Box
        icon_box = ctk.CTkFrame(card_frm, width=60, height=60, fg_color="#EFF6FF", corner_radius=10)
        icon_box.pack(pady=(40, 20))
        ctk.CTkLabel(icon_box, text=icon, font=("Arial", 24), text_color="#3B82F6").place(relx=0.5, rely=0.5, anchor="center")
        
        # Text
        ctk.CTkLabel(card_frm, text=title, font=("Inter", 16, "bold"), text_color="#1E293B").pack(pady=(0, 10))
        ctk.CTkLabel(card_frm, text=desc, font=("Inter", 12), text_color="#94A3B8").pack()
        
        # Hover effect logic would go here
