"""
History Attendance Page
=======================

Displays attendance history with filtering, sorting, and export options.
Matches the premium design requirements.
"""

import customtkinter as ctk
from datetime import datetime
from typing import Optional, List, Dict, Any
import tkinter as tk

from views.styles.theme import COLORS, FONTS, SPACING, RADIUS
from services import StudentService
from controllers.student_controller import StudentController

class HistoryPage(ctk.CTkFrame):
    """
    History page with table view of attendance records.
    """
    
    def __init__(self, master, on_navigate=None, user=None, student_service=None):
        super().__init__(master, fg_color=COLORS["bg_secondary"]) # Light gray bg
        self.pack(expand=True, fill="both")
        
        self.on_navigate = on_navigate
        self.user = user
        # Ensure student service is available
        self.student_service = student_service 
        if not self.student_service:
             # Fallback if not injected (though main.py should inject it)
             # This is just a safety net for standalone testing
             pass

        self.student_code = user.student_code if hasattr(user, 'student_code') else (user.username if user else "UNKNOWN")
        
        # State
        self.current_filters = {
            "search_query": "",
            "status": None,
            "sort_by": "date",
            "sort_order": "desc"
        }
        self.current_page = 1
        self.items_per_page = 10
        self.total_records = 0
        
        # Layout
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        self._init_ui()
        self.refresh_data()

    def _init_ui(self):
        # 1. Header Section
        self._create_header()
        
        # 2. Filter & Actions Toolbar
        self._create_toolbar()
        
        # 3. Table Section
        self._create_table_area()
        
        # 4. Pagination
        self._create_pagination()

    def _create_header(self):
        head = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        head.pack(fill="x", pady=(0, 20))
        
        # Title
        ctk.CTkLabel(
            head, 
            text="Attendance History", 
            font=("Inter", 24, "bold"), 
            text_color=COLORS["text_primary"]
        ).pack(anchor="w")
        
        # Subtitle
        ctk.CTkLabel(
            head, 
            text="Review your past attendance records for Data Science modules.", 
            font=("Inter", 14), 
            text_color=COLORS["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))

    def _create_toolbar(self):
        toolbar = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        toolbar.pack(fill="x", pady=(0, 20))
        
        # Search Box
        search_frm = ctk.CTkFrame(toolbar, fg_color="white", corner_radius=8, border_width=1, border_color=COLORS["border"], height=44)
        search_frm.pack(side="left", fill="x", expand=True, padx=(0, 20))
        search_frm.pack_propagate(False)
        
        ctk.CTkLabel(search_frm, text="🔍", text_color="#94A3B8", font=("Inter", 16)).pack(side="left", padx=(15, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frm, 
            placeholder_text="Search courses or dates...", 
            border_width=0, 
            fg_color="transparent",
            font=("Inter", 13),
            text_color=COLORS["text_primary"]
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<Return>", lambda e: self._on_search())
        
        # Search Button (Optional, but good UX)
        # Hidden implies Enter key usage, but let's keep it clean as per design

        # Filter Button (Dropdown logic can be added here)
        self.filter_btn = self._create_action_btn(
            toolbar, "Filter", "Y", "white", COLORS["text_secondary"], COLORS["border"],
            command=self._show_filter_dialog
        )
        
        # Export Button
        self.export_btn = self._create_action_btn(
            toolbar, "Export Data", "📥", COLORS["primary"], "white", COLORS["primary"],
            command=self._export_data
        )

    def _create_action_btn(self, parent, text, icon, bg, fg, border, command=None):
        btn = ctk.CTkButton(
            parent,
            text=f" {icon}  {text}",
            fg_color=bg,
            text_color=fg,
            border_width=1,
            border_color=border,
            font=("Inter", 13, "bold"),
            hover_color=bg, # Should darken slightly in real impl
            height=44,
            corner_radius=8,
            width=120,
            command=command
        )
        btn.pack(side="right", padx=(10, 0))
        return btn

    def _create_table_area(self):
        # Table Container (White Card)
        self.table_card = ctk.CTkFrame(
            self.content_frame, 
            fg_color="white", 
            corner_radius=12,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.table_card.pack(fill="both", expand=True)
        
        # Header Row
        self._create_table_header()
        
        # Rows Container (Scrollable)
        self.rows_frame = ctk.CTkScrollableFrame(self.table_card, fg_color="transparent")
        self.rows_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _create_table_header(self):
        header = ctk.CTkFrame(self.table_card, fg_color=COLORS["table_header_bg"], height=50, corner_radius=0)
        header.pack(fill="x", padx=1, pady=1)
        
        # Grid layout for header
        header.grid_columnconfigure(0, weight=4) # Course
        header.grid_columnconfigure(1, weight=2) # Date
        header.grid_columnconfigure(2, weight=2) # Time
        header.grid_columnconfigure(3, weight=2) # Status
        header.grid_columnconfigure(4, weight=1) # Action
        
        # Header configurations
        headers = [
            ("COURSE NAME", "class_name", 0),
            ("DATE", "date", 1),
            ("TIME REGISTERED", None, 2),
            ("STATUS", "status", 3),
            ("DETAILS", None, 4)
        ]
        
        for text, sort_key, col_idx in headers:
            # Container for alignment
            wrapper = ctk.CTkFrame(header, fg_color="transparent")
            wrapper.grid(row=0, column=col_idx, sticky="ew", padx=20, pady=12)
            
            if sort_key:
                # Clickable label for sorting
                lbl = ctk.CTkLabel(
                    wrapper, 
                    text=text + " ⇅", # Sort indicator
                    font=("Inter", 11, "bold"), 
                    text_color="#64748B", 
                    anchor="w",
                    cursor="hand2"
                )
                lbl.pack(anchor="w")
                lbl.bind("<Button-1>", lambda e, k=sort_key: self._on_sort(k))
            else:
                ctk.CTkLabel(
                    wrapper, 
                    text=text, 
                    font=("Inter", 11, "bold"), 
                    text_color="#64748B", 
                    anchor="w"
                ).pack(anchor="w")

    def _create_pagination(self):
        # Footer
        self.footer = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.footer.pack(fill="x", pady=(20, 0))
        
        self.record_count_label = ctk.CTkLabel(
            self.footer, 
            text="Showing 0 of 0 records", 
            font=("Inter", 12), 
            text_color="#64748B"
        )
        self.record_count_label.pack(side="left")
        
        # Pagination Buttons
        nav = ctk.CTkFrame(self.footer, fg_color="transparent")
        nav.pack(side="right")
        
        self.prev_btn = ctk.CTkButton(
            nav, text="Previous", fg_color="white", text_color="#64748B", 
            border_width=1, border_color="#E2E8F0", width=80, height=32, corner_radius=6,
            command=self._prev_page,
            state="disabled"
        )
        self.prev_btn.pack(side="left", padx=5)
        
        self.next_btn = ctk.CTkButton(
            nav, text="Next", fg_color="white", text_color="#64748B", 
            border_width=1, border_color="#E2E8F0", width=80, height=32, corner_radius=6,
            command=self._next_page,
            state="disabled"
        )
        self.next_btn.pack(side="left", padx=5)

    def _on_search(self):
        query = self.search_entry.get()
        self.current_filters["search_query"] = query
        self.current_page = 1 # Reset to first page
        self.refresh_data()

    def _on_sort(self, sort_key):
        # Toggle order if same key, else set to asc
        if self.current_filters["sort_by"] == sort_key:
            current_order = self.current_filters["sort_order"]
            new_order = "asc" if current_order == "desc" else "desc"
            self.current_filters["sort_order"] = new_order
        else:
            self.current_filters["sort_by"] = sort_key
            self.current_filters["sort_order"] = "asc" # Default for new sort
            
        self.refresh_data()

    def _show_filter_dialog(self):
        # Simple implementation: toggle status filter cyclically for demo
        # Real implementation would use a Toplevel or Menu
        current = self.current_filters["status"]
        options = [None, "PRESENT", "ABSENT", "LATE"]
        
        try:
            curr_idx = options.index(current)
            next_idx = (curr_idx + 1) % len(options)
        except ValueError:
            next_idx = 0
            
        new_status = options[next_idx]
        self.current_filters["status"] = new_status
        
        # Update button text to reflect filter
        btn_text = f"Filter: {new_status}" if new_status else "Filter"
        self.filter_btn.configure(text=f" Y  {btn_text}")
        
        self.refresh_data()

    def _export_data(self):
        # Placeholder for export functionality
        print("Exporting data...")
        # Could show a success toast here

    def refresh_data(self):
        # Reset UI
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
            
        if not self.student_service:
            return

        try:
            # Fetch data using controller implementation directly calling service here for simplicity
            # In pure MVC, controller should be calling this update, or via observer
            # We will use the service directly as passed in init
           
            history = self.student_service.get_attendance_history(
                student_code=self.student_code,
                search_query=self.current_filters["search_query"],
                status=self.current_filters["status"],
                sort_by=self.current_filters["sort_by"],
                sort_order=self.current_filters["sort_order"]
            )
            
            self.total_records = len(history)
            
            # Pagination Logic
            start_idx = (self.current_page - 1) * self.items_per_page
            end_idx = start_idx + self.items_per_page
            page_data = history[start_idx:end_idx]
            
            # Update Footer
            self.record_count_label.configure(
                text=f"Showing {min(end_idx, self.total_records)} of {self.total_records} records"
            )
            
            # Enable/Disable buttons
            self.prev_btn.configure(state="normal" if self.current_page > 1 else "disabled")
            self.next_btn.configure(state="normal" if end_idx < self.total_records else "disabled")

            # Render Rows
            if not page_data:
                self._show_empty_state()
            else:
                for row_data in page_data:
                    self._add_row(row_data)
                    
        except Exception as e:
            print(f"Error loading history: {e}")
            ctk.CTkLabel(self.rows_frame, text=f"Error loading data: {e}").pack(pady=20)

    def _show_empty_state(self):
        ctk.CTkLabel(
            self.rows_frame, 
            text="No attendance records found.", 
            font=("Inter", 14), 
            text_color="gray"
        ).pack(pady=40)

    def _add_row(self, data):
        row = ctk.CTkFrame(self.rows_frame, fg_color="transparent", height=60)
        row.pack(fill="x")
        
        # Grid configuration for row content
        row.grid_columnconfigure(0, weight=4)
        row.grid_columnconfigure(1, weight=2)
        row.grid_columnconfigure(2, weight=2)
        row.grid_columnconfigure(3, weight=2)
        row.grid_columnconfigure(4, weight=1)
        
        # Styling
        text_col = COLORS["text_primary"]
        font = ("Inter", 13, "bold")
        
        # 1. Course
        course_name = data.get("class_name") or "Unknown Class"
        ctk.CTkLabel(row, text=course_name, text_color=text_col, font=font, anchor="w").grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        # 2. Date
        date_str = data.get("date") or ""
        ctk.CTkLabel(row, text=date_str, text_color="#64748B", font=("Inter", 13), anchor="w").grid(row=0, column=1, sticky="ew", padx=20)
        
        # 3. Time
        time_str = data.get("time") or "-"
        ctk.CTkLabel(row, text=time_str, text_color="#64748B", font=("Inter", 13), anchor="w").grid(row=0, column=2, sticky="ew", padx=20)
        
        # 4. Status Badge
        status = data.get("status", "UNKNOWN")
        status_colors = {
            "PRESENT": ("#DCFCE7", "#166534"), # Green
            "ABSENT": ("#FEE2E2", "#991B1B"),  # Red
            "LATE": ("#FEF3C7", "#92400E")     # Yellow
        }
        bg, fg = status_colors.get(status, ("#F1F5F9", "#64748B"))
        
        status_frm = ctk.CTkFrame(row, fg_color="transparent")
        status_frm.grid(row=0, column=3, sticky="w", padx=20)
        
        ctk.CTkLabel(
            status_frm, 
            text=status, 
            fg_color=bg, 
            text_color=fg, 
            font=("Inter", 11, "bold"), 
            corner_radius=6,
            width=80,
            height=28
        ).pack()

        # 5. Details
        ctk.CTkButton(
            row, 
            text="Details", 
            text_color=COLORS["primary"], 
            fg_color="transparent", 
            font=("Inter", 12, "bold"), 
            hover=False,
            width=60,
            anchor="e"
        ).grid(row=0, column=4, sticky="e", padx=20)
        
        # Separator line
        sep = ctk.CTkFrame(row, height=1, fg_color="#F1F5F9")
        sep.place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.refresh_data()

    def _next_page(self):
        start_idx = self.current_page * self.items_per_page
        if start_idx < self.total_records:
            self.current_page += 1
            self.refresh_data()
