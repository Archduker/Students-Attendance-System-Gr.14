"""
Admin - System Reports Page
===========================

Reports & Insights page for Admin.
Matching UI from Image 3.
"""

import customtkinter as ctk
from typing import Optional

class SystemReportsPage(ctk.CTkFrame):
    """
    System Reports page showing analytics and downloadable reports.
    Matches Image 3 design.
    """
    
    def __init__(self, parent, admin_user=None, controller=None):
        super().__init__(parent, fg_color="transparent")
        
        self.admin_user = admin_user
        self.controller = controller
        
        self._setup_ui()
    
    def _setup_ui(self):
        # Header
        self._create_header(self)
        
        # Stats Cards
        self._create_stats_cards(self)
        
        # Reports List
        self._create_reports_list(self)
    
    def _create_header(self, parent):
        """Header with title and Generate button."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 25))
        
        # Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        ctk.CTkLabel(
            title_frame,
            text="Reports & Insights",
            font=("Inter", 26, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_frame,
            text="Global analytics for the Data Science & AI Department (~60 scholars/class).",
            font=("Inter", 12),
            text_color="#64748B"
        ).pack(anchor="w")
        
        # Generate button
        ctk.CTkButton(
            header,
            text="📄 Generate New Report",
            fg_color="#3B82F6",
            text_color="white",
            font=("Inter", 11, "bold"),
            width=180,
            height=36,
            corner_radius=8,
            hover_color="#2563EB",
            command=self._handle_generate_report  # Added command handler
        ).pack(side="right")
    
    def _create_stats_cards(self, parent):
        """3 stats cards."""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", pady=(0, 30))
        
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)
        
        # Stats
        stats = [
            ("📊 DEPARTMENTAL RATE", "95.4%", "+1.2% vs baseline", "#22C55E"),
            ("👥 ACTIVE DS SCHOLARS", "1,250", "Verified Identity", "#3B82F6"),
            ("📚 ACTIVE MODULES", "22", "Across all DS Labs", "#A855F7"),
        ]
        
        for i, (label, value, subtitle, color) in enumerate(stats):
            self._create_stat_card(cards_frame, label, value, subtitle, color, i)
    
    def _create_stat_card(self, parent, label, value, subtitle, color, col):
        """Single stat card."""
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.grid(row=0, column=col, sticky="ew", padx=10)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", padx=25, pady=25)
        
        # Label
        ctk.CTkLabel(
            content,
            text=label,
            font=("Inter", 10, "bold"),
            text_color="#64748B"
        ).pack(anchor="w")
        
        # Value
        ctk.CTkLabel(
            content,
            text=value,
            font=("Inter", 28, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w", pady=(8, 5))
        
        # Subtitle
        ctk.CTkLabel(
            content,
            text=subtitle,
            font=("Inter", 11),
            text_color=color
        ).pack(anchor="w")
    
    def _create_reports_list(self, parent):
        """Available Reports list."""
        card = ctk.CTkFrame(
            parent,
            fg_color="white",
            corner_radius=15,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.pack(fill="both", expand=True)
        
        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(
            header,
            text="Available Reports",
            font=("Inter", 14, "bold"),
            text_color="#0F172A"
        ).pack(side="left")
        
        # Search + Filter
        search_area = ctk.CTkFrame(header, fg_color="transparent")
        search_area.pack(side="right")
        
        # Search
        search_frame = ctk.CTkFrame(search_area, fg_color="#F1F5F9", corner_radius=8, height=35, width=250)
        search_frame.pack(side="left", padx=(0, 10))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(search_frame, text="🔍", font=("Arial", 12)).pack(side="left", padx=(10, 5))
        ctk.CTkEntry(search_frame, placeholder_text="Search reports...", border_width=0, fg_color="transparent", font=("Inter", 11)).pack(fill="both", expand=True, padx=(0, 10))
        
        # Filter icon
        ctk.CTkButton(search_area, text="⚙", width=35, height=35, fg_color="#F1F5F9", text_color="#64748B", hover_color="#E2E8F0", corner_radius=8).pack(side="left")
        
        # Reports
        reports_area = ctk.CTkScrollableFrame(card, fg_color="transparent")
        reports_area.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        
        reports = [
            ("Monthly Attendance Summary", "system", "Updated Dec 2025", ["PDF", "XLSX"]),
            ("Faculty Performance Review", "performance", "Updated Q1 2025", ["PDF"]),
            ("Student Retention Analysis", "students", "Updated Formation 3", ["CSV"]),
            ("Security & Access Audit", "security", "Updated Weekly", ["PDF"]),
        ]
        
        for title, category, updated, formats in reports:
            self._add_report_item(reports_area, title, category, updated, formats)
    
    def _add_report_item(self, parent, title, category, updated, formats):
        """Single report item."""
        item = ctk.CTkFrame(parent, fg_color="transparent")
        item.pack(fill="x", pady=8)
        
        # Icon
        icon = ctk.CTkLabel(
            item,
            text="📄",
            font=("Arial", 24),
            width=40,
            height=40,
            fg_color="#F1F5F9",
            corner_radius=8
        )
        icon.pack(side="left", padx=(0, 15))
        
        # Info
        info = ctk.CTkFrame(item, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(info, text=title, font=("Inter", 13, "bold"), text_color="#0F172A").pack(anchor="w")
        ctk.CTkLabel(info, text=f"{category} • {updated}", font=("Inter", 10), text_color="#94A3B8").pack(anchor="w")
        
        # Formats + Download
        actions = ctk.CTkFrame(item, fg_color="transparent")
        actions.pack(side="right")
        
        # Format badges
        for fmt in formats:
            ctk.CTkLabel(
                actions,
                text=fmt,
                font=("Inter", 9, "bold"),
                text_color="#64748B",
                fg_color="#F1F5F9",
                corner_radius=5,
                padx=8,
                pady=4
            ).pack(side="left", padx=3)
        
        # Download button
        ctk.CTkButton(
            actions,
            text="⬇",
            width=32,
            height=32,
            fg_color="#3B82F6",
            text_color="white",
            hover_color="#2563EB",
            corner_radius=6,
            command=lambda: self._handle_download_report(title, formats[0] if formats else "PDF")  # Download first available format
        ).pack(side="left", padx=(10, 0))
        
        # Separator
        ctk.CTkFrame(parent, height=1, fg_color="#F1F5F9").pack(fill="x", pady=5)
    
    def _handle_generate_report(self):
        """Handle Generate New Report button click."""
        from tkinter import messagebox
        
        # Show dialog asking for report type
        messagebox.showinfo(
            "Generate Report",
            "Report generation feature coming soon!\n\nYou can select:\n" +
            "• Monthly Attendance Summary\n" +
            "• Faculty Performance Review\n" +
            "• Student Retention Analysis\n" +
            "• Custom Report"
        )
    
    def _handle_download_report(self, report_title, format_type):
        """Handle report download."""
        from tkinter import filedialog, messagebox
        import os
        
        # File extension based on format
        ext_map = {
            "PDF": ".pdf",
            "XLSX": ".xlsx",
            "CSV": ".csv"
        }
        ext = ext_map.get(format_type, ".pdf")
        
        # Generate filename from title
        filename = report_title.replace(" ", "_").lower() + ext
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            title=f"Save {report_title}",
            defaultextension=ext,
            initialfile=filename,
            filetypes=[(f"{format_type} files", f"*{ext}"), ("All files", "*.*")]
        )
        
        if save_path:
            try:
                # Create placeholder file (in a real app, generate actual report)
                with open(save_path, 'w') as f:
                    f.write(f"# {report_title}\n\n")
                    f.write(f"Report Type: {format_type}\n")
                    f.write(f"Generated: {os.path.basename(save_path)}\n\n")
                    f.write("[This is a placeholder. Actual report generation coming soon.]\n")
                
                messagebox.showinfo(
                    "Download Complete",
                    f"Report saved successfully!\n\nLocation: {save_path}"
                )
            except Exception as e:
                messagebox.showerror(
                    "Download Failed",
                    f"Failed to save report:\n{str(e)}"
                )
