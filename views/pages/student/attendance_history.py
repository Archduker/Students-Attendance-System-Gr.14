import customtkinter as ctk

class AttendanceHistoryPage(ctk.CTkFrame):
    def __init__(self, master, on_navigate=None):
        super().__init__(master, fg_color="#F3F4F6")
        self.pack(expand=True, fill="both")
        
        # Header
        self._create_header()
        
        # Table Section
        self._create_table_section()

    def _create_header(self):
        frm = ctk.CTkFrame(self, fg_color="transparent")
        frm.pack(fill="x", pady=(0, 30))
        
        ctk.CTkLabel(frm, text="Attendance History", font=("Inter", 24, "bold"), text_color="#1E293B").pack(anchor="w")
        ctk.CTkLabel(
            frm, 
            text="Review your past attendance records for Data Science modules.", 
            font=("Inter", 13), 
            text_color="#64748B"
        ).pack(anchor="w")
        
        # Toolbar
        tool_frm = ctk.CTkFrame(frm, fg_color="transparent")
        tool_frm.pack(fill="x", pady=(20, 0))
        
        # Filter btn
        ctk.CTkButton(
            tool_frm, 
            text="Filter", 
            fg_color="white", 
            text_color="#64748B", 
            width=80,
            hover_color="#F1F5F9"
        ).pack(side="right", padx=10)
        
        # Export btn
        ctk.CTkButton(
            tool_frm, 
            text="Export Data", 
            fg_color="#4F46E5", # Indigo
            width=100
        ).pack(side="right")

    def _create_table_section(self):
        # Card Container
        card = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        card.pack(fill="both", expand=True)
        
        # Search Bar inside card
        search_row = ctk.CTkFrame(card, fg_color="transparent")
        search_row.pack(fill="x", padx=20, pady=20)
        ctk.CTkEntry(search_row, placeholder_text="Search courses or dates...", width=300).pack(side="left")
        ctk.CTkLabel(search_row, text="📅 Semester 3, 2025", text_color="#64748B").pack(side="right")
        
        # Table Header
        h_frm = ctk.CTkFrame(card, fg_color="#F8FAFC", height=40)
        h_frm.pack(fill="x")
        
        cols = [
            ("COURSE NAME", 0.3),
            ("DATE", 0.15),
            ("TIME REGISTERED", 0.2),
            ("STATUS", 0.15),
            ("", 0.1) # Details link
        ]
        
        for name, weight in cols:
            lbl = ctk.CTkLabel(h_frm, text=name, font=("Inter", 11, "bold"), text_color="#94A3B8", anchor="w")
            # Ideally use grid for true columns, packing for quick mock
            lbl.pack(side="left", expand=True, fill="x", padx=10)

        # Rows
        data = [
            ("Machine Learning", "31 Dec 2025", "09:15 AM", "PRESENT", "#DCFCE7", "#166534"),
            ("Big Data Analytics", "30 Dec 2025", "10:02 AM", "PRESENT", "#DCFCE7", "#166534"),
            ("Data Science Ethics", "29 Dec 2025", "-", "ABSENT", "#FEE2E2", "#991B1B"),
            ("Business Intelligence", "28 Dec 2025", "02:30 PM", "LATE", "#FEF3C7", "#92400E"),
            ("Python for Data Science", "27 Dec 2025", "04:07 PM", "PRESENT", "#DCFCE7", "#166534"),
        ]
        
        for title, date, time, status, bg, fg in data:
            row = ctk.CTkFrame(card, fg_color="transparent", height=50)
            row.pack(fill="x", padx=0, pady=0)
            ctk.CTkFrame(card, height=1, fg_color="#F1F5F9").pack(fill="x") # Divider
            
            # Using pack side=left for simple columns
            ctk.CTkLabel(row, text=title, font=("Inter", 12, "bold"), text_color="#1E293B", anchor="w").pack(side="left", expand=True, fill="x", padx=10)
            ctk.CTkLabel(row, text=date, font=("Inter", 12), text_color="#64748B").pack(side="left", expand=True, fill="x", padx=10)
            ctk.CTkLabel(row, text=time, font=("Inter", 12), text_color="#64748B").pack(side="left", expand=True, fill="x", padx=10)
            
            # Status Badge Wrapper
            status_frm = ctk.CTkFrame(row, fg_color="transparent")
            status_frm.pack(side="left", expand=True, fill="x")
            ctk.CTkLabel(status_frm, text=status, font=("Inter", 9, "bold"), fg_color=bg, text_color=fg, corner_radius=10, width=80).pack()
            
            ctk.CTkButton(row, text="Details", font=("Inter", 11), text_color="#4F46E5", fg_color="transparent", hover=False, width=50).pack(side="left", padx=20)
            
            
        # Paginator
        foot = ctk.CTkFrame(card, fg_color="transparent")
        foot.pack(fill="x", pady=20, padx=20)
        ctk.CTkLabel(foot, text="Showing 5 of 42 records", font=("Inter", 11), text_color="#94A3B8").pack(side="left")
        
        ctk.CTkButton(foot, text="Next", width=60, fg_color="white", border_width=1, border_color="#E2E8F0", text_color="black").pack(side="right")
        ctk.CTkButton(foot, text="Previous", width=60, fg_color="white", border_width=1, border_color="#E2E8F0", text_color="black").pack(side="right", padx=10)
