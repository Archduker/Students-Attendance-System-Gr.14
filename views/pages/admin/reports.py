"""
System Reports Page - Báo cáo hệ thống
======================================

Page tạo và export báo cáo:
- Báo cáo điểm danh toàn hệ thống
- Filter theo thời gian, lớp, user
- Export PDF/Excel/CSV
"""

import customtkinter as ctk
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from tkinter import messagebox, filedialog


class SystemReportsPage(ctk.CTkFrame):
    """
    System Reports Page - Báo cáo hệ thống.
    
    Features:
        - Filter reports by date range, class, user
        - View attendance statistics
        - Export to PDF/Excel/CSV
        - Generate custom reports
        
    Example:
        >>> page = SystemReportsPage(parent, admin_controller)
        >>> page.pack(fill="both", expand=True)
    """
    
    def __init__(
        self, 
        parent, 
        admin_controller,
        **kwargs
    ):
        """
        Khởi tạo System Reports Page.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
        """
        super().__init__(parent, **kwargs)
        
        self.admin_controller = admin_controller
        self.report_data: Dict[str, Any] = {}
        
        self._init_ui()
    
    def _init_ui(self):
        """Khởi tạo UI components."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self._create_header()
        
        # Main content
        self._create_content()
    
    def _create_header(self):
        """Tạo header."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 System Reports",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
    
    def _create_content(self):
        """Tạo main content."""
        content_frame = ctk.CTkScrollableFrame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Filter section
        self._create_filter_section(content_frame)
        
        # Report preview section
        self._create_preview_section(content_frame)
        
        # Export section
        self._create_export_section(content_frame)
    
    def _create_filter_section(self, parent):
        """Tạo filter section."""
        filter_frame = ctk.CTkFrame(parent, corner_radius=10)
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        filter_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            filter_frame,
            text="🔍 Report Filters",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))
        
        # Report type
        label = ctk.CTkLabel(
            filter_frame,
            text="Report Type:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=1, column=0, sticky="w", padx=15, pady=(10, 5))
        
        self.report_type_var = ctk.StringVar(value="Overall Attendance")
        report_type_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=[
                "Overall Attendance",
                "Class Attendance",
                "Student Attendance",
                "Teacher Sessions"
            ],
            variable=self.report_type_var,
            command=self._on_report_type_change
        )
        report_type_menu.grid(row=2, column=0, sticky="ew", padx=15, pady=(0, 10))
        
        # Date range
        label = ctk.CTkLabel(
            filter_frame,
            text="Date Range:",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        label.grid(row=1, column=1, sticky="w", padx=15, pady=(10, 5))
        
        self.date_range_var = ctk.StringVar(value="Last 30 Days")
        date_range_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=[
                "Last 7 Days",
                "Last 30 Days",
                "Last 90 Days",
                "This Month",
                "Custom Range"
            ],
            variable=self.date_range_var
        )
        date_range_menu.grid(row=2, column=1, sticky="ew", padx=15, pady=(0, 10))
        
        # Additional filters (class, student) - will be shown based on report type
        self.additional_filters_frame = ctk.CTkFrame(filter_frame, fg_color="transparent")
        self.additional_filters_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=(10, 10))
        
        # Generate button
        generate_btn = ctk.CTkButton(
            filter_frame,
            text="🔄 Generate Report",
            height=40,
            command=self._generate_report
        )
        generate_btn.grid(row=4, column=0, columnspan=2, sticky="ew", padx=15, pady=(10, 15))
    
    def _create_preview_section(self, parent):
        """Tạo report preview section."""
        preview_frame = ctk.CTkFrame(parent, corner_radius=10)
        preview_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            preview_frame,
            text="📄 Report Preview",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="w", padx=15, pady=(15, 10))
        
        # Preview content
        self.preview_content = ctk.CTkTextbox(
            preview_frame,
            height=300,
            font=ctk.CTkFont(family="Courier", size=11)
        )
        self.preview_content.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Initial placeholder
        self._show_preview_placeholder()
    
    def _create_export_section(self, parent):
        """Tạo export section."""
        export_frame = ctk.CTkFrame(parent, corner_radius=10)
        export_frame.grid(row=2, column=0, sticky="ew")
        
        # Title
        title_label = ctk.CTkLabel(
            export_frame,
            text="💾 Export Report",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 10))
        
        # Export buttons
        btn_frame = ctk.CTkFrame(export_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # PDF button
        pdf_btn = ctk.CTkButton(
            btn_frame,
            text="📕 Export as PDF",
            width=150,
            command=lambda: self._export_report("pdf")
        )
        pdf_btn.pack(side="left", padx=(0, 10))
        
        # Excel button
        excel_btn = ctk.CTkButton(
            btn_frame,
            text="📗 Export as Excel",
            width=150,
            command=lambda: self._export_report("excel")
        )
        excel_btn.pack(side="left", padx=(0, 10))
        
        # CSV button
        csv_btn = ctk.CTkButton(
            btn_frame,
            text="📄 Export as CSV",
            width=150,
            command=lambda: self._export_report("csv")
        )
        csv_btn.pack(side="left")
    
    def _on_report_type_change(self, choice):
        """Handle report type change."""
        # Clear additional filters
        for widget in self.additional_filters_frame.winfo_children():
            widget.destroy()
        
        # Add specific filters based on report type
        if choice == "Class Attendance":
            self._add_class_filter()
        elif choice == "Student Attendance":
            self._add_student_filter()
    
    def _add_class_filter(self):
        """Add class filter."""
        label = ctk.CTkLabel(
            self.additional_filters_frame,
            text="Select Class:",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        label.pack(anchor="w", pady=(5, 2))
        
        self.class_filter_var = ctk.StringVar(value="All Classes")
        class_menu = ctk.CTkOptionMenu(
            self.additional_filters_frame,
            values=["All Classes", "CS101", "CS102", "MAT101"],
            variable=self.class_filter_var
        )
        class_menu.pack(fill="x", pady=(0, 5))
    
    def _add_student_filter(self):
        """Add student filter."""
        label = ctk.CTkLabel(
            self.additional_filters_frame,
            text="Student ID:",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        label.pack(anchor="w", pady=(5, 2))
        
        self.student_entry = ctk.CTkEntry(
            self.additional_filters_frame,
            placeholder_text="Enter student ID or code"
        )
        self.student_entry.pack(fill="x", pady=(0, 5))
    
    def _show_preview_placeholder(self):
        """Show placeholder in preview."""
        self.preview_content.delete("1.0", "end")
        self.preview_content.insert(
            "1.0",
            "Select filters and click 'Generate Report' to view the report preview.\n\n"
            "The report will display:\n"
            "- Summary statistics\n"
            "- Detailed attendance records\n"
            "- Charts and visualizations\n"
            "- Exportable data\n"
        )
    
    def _generate_report(self):
        """Generate report based on filters."""
        try:
            # Get filter values
            report_type = self.report_type_var.get()
            date_range = self.date_range_var.get()
            
            # Call controller to generate report
            result = self.admin_controller.generate_report(
                report_type=report_type,
                date_range=date_range
            )
            
            if result.get("success"):
                self.report_data = result.get("data", {})
                self._display_report()
            else:
                self._show_error(result.get("error", "Failed to generate report"))
                
        except Exception as e:
            self._show_error(f"Error generating report: {str(e)}")
    
    def _display_report(self):
        """Display generated report."""
        self.preview_content.delete("1.0", "end")
        
        # Format report data
        report_text = self._format_report_data()
        
        self.preview_content.insert("1.0", report_text)
    
    def _format_report_data(self) -> str:
        """
        Format report data for display.
        
        Returns:
            Formatted report text
        """
        if not self.report_data:
            return "No data available for the selected filters."
        
        lines = []
        lines.append("="*60)
        lines.append(f"ATTENDANCE REPORT - {self.report_type_var.get()}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Date Range: {self.date_range_var.get()}")
        lines.append("="*60)
        lines.append("")
        
        # Summary section
        lines.append("SUMMARY")
        lines.append("-"*60)
        summary = self.report_data.get("summary", {})
        for key, value in summary.items():
            lines.append(f"  {key}: {value}")
        lines.append("")
        
        # Details section
        lines.append("DETAILS")
        lines.append("-"*60)
        details = self.report_data.get("details", [])
        if details:
            for item in details:
                lines.append(f"  {item}")
        else:
            lines.append("  No detailed data available")
        
        lines.append("")
        lines.append("="*60)
        
        return "\n".join(lines)
    
    def _export_report(self, format_type: str):
        """
        Export report to file.
        
        Args:
            format_type: "pdf", "excel", or "csv"
        """
        if not self.report_data:
            messagebox.showwarning(
                "No Data",
                "Please generate a report first before exporting."
            )
            return
        
        # File dialog
        file_extensions = {
            "pdf": ("PDF files", "*.pdf"),
            "excel": ("Excel files", "*.xlsx"),
            "csv": ("CSV files", "*.csv")
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=file_extensions[format_type][1],
            filetypes=[file_extensions[format_type], ("All files", "*.*")],
            initialfile=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}"
        )
        
        if not filename:
            return
        
        try:
            # Call controller to export
            result = self.admin_controller.export_report(
                self.report_data,
                filename,
                format_type
            )
            
            if result.get("success"):
                messagebox.showinfo(
                    "Success",
                    f"Report exported successfully to:\n{filename}"
                )
            else:
                self._show_error(result.get("error", "Failed to export report"))
                
        except Exception as e:
            self._show_error(f"Error exporting report: {str(e)}")
    
    def _show_error(self, message: str):
        """
        Hiển thị error message.
        
        Args:
            message: Error message
        """
        messagebox.showerror("Error", message)
    
    def refresh(self):
        """Public method để refresh page."""
        self._show_preview_placeholder()
