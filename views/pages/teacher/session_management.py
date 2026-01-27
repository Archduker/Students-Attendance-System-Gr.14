"""
Attendance Management Page - Quản lý điểm danh
==============================================

Trang quản lý attendance với 2 trạng thái:
1. History: Xem danh sách sessions + Quick Actions
2. Manual Entry: Chỉnh sửa trạng thái attendance của sinh viên
"""

import customtkinter as ctk
from typing import Optional, List
from datetime import datetime

from core.models import Teacher
from controllers.teacher_controller import TeacherController
from views.components.modal import Modal
from views.pages.teacher.create_session import CreateSessionDialog


class SessionManagementPage(ctk.CTkFrame):
    """
    Attendance Management page với 2 trạng thái.
    """
    
    def __init__(self, parent, teacher: Teacher, controller: TeacherController):
        super().__init__(parent, fg_color="transparent")
        self.pack(expand=True, fill="both")
        
        self.teacher = teacher
        self.controller = controller
        
        self.selected_session_idx = None  # Track selected session index
        self.current_state = "history"  # State management: "history" hoặc "manual_entry"
        self.recent_sessions = []
        self.students = [] # Initialize students list
        
        self._setup_ui()
        self._load_real_data()
        
        # Start auto-refresh loop (30 seconds)
        self.after(30000, self._auto_refresh_loop)

    def _load_real_data(self):
        """Fetch real data from database"""
        try:
            # 1. Get classes map (id -> name)
            classes = self.controller.get_class_list(self.teacher)
            class_map = {c.class_id: c for c in classes}
            
            # 2. Get recent sessions
            raw_sessions = self.controller.get_session_list(self.teacher)
            # Sort by start_time desc
            raw_sessions.sort(key=lambda x: x.start_time, reverse=True)
            
            self.recent_sessions = []
            for s in raw_sessions:
                c = class_map.get(s.class_id)
                course_name = c.class_name if c else s.class_id
                
                # Get stats (n+1 but acceptable for small list)
                report = self.controller.get_session_report(self.teacher, s.session_id)
                current = report.get('present_count', 0) if report else 0
                max_count = report.get('total_students', 0) if report else 0
                
                # Format date: "Jan 12th, 2026"
                date_str = s.start_time.strftime("%b %d, %Y")
                
                status = "ACTIVE" if s.is_open() else "CLOSED"
                
                self.recent_sessions.append({
                    "course": course_name,
                    "status": status,
                    "date": date_str,
                    "current": current,
                    "max": max_count,
                    "raw_session": s # Store raw object for actions
                })
                
            # Only render if in history state (auto-refresh will call this from loop)
            if self.current_state == "history":
                self._render_session_list()
            
        except Exception as e:
            print(f"❌ Error loading real data: {e}")
            import traceback
            traceback.print_exc()

    def _auto_refresh_loop(self):
        """Auto-refresh data every 30 seconds"""
        if self.winfo_exists():
            try:
                print(f"🔄 Auto-refreshing session data...")
                self._load_real_data()
                
                # Re-render UI based on current state
                if self.current_state == "history":
                    print(f"📋 Rendering history state...")
                    self._render_session_list()
                
            except Exception as e:
                print(f"❌ Error in auto-refresh: {e}")
                import traceback
                traceback.print_exc()
            
            # Schedule next refresh
            self.after(30000, self._auto_refresh_loop)

    def refresh_data(self):
        """Public method to refresh session data (called from CreateSessionDialog callback)"""
        self.selected_session_idx = None  # Reset selection
        self._load_real_data()
        if self.current_state == "history":
            self._render_session_list()

    def _setup_ui(self):
        """Setup UI components"""
        # Header (chung cho cả 2 states)
        self._create_header()
        
        # Content area (thay đổi theo state)
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.pack(expand=True, fill="both", pady=(20, 0))
        
        # Render state mặc định
        self._render_current_state()
    
    def _create_header(self):
        """Create page header with tabs"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Left side: Title & Subtitle
        title_area = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_area.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            title_area,
            text="Attendance Management",
            font=("Inter", 24, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_area,
            text="Review lab sessions or manually update student status for cohorts (~60 students)",
            font=("Inter", 12),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(2, 0))
        
        # Right side: Tab Switcher + Create Button
        tab_area = ctk.CTkFrame(header_frame, fg_color="transparent")
        tab_area.pack(side="right")
        
        # Create Session Button
        ctk.CTkButton(
            tab_area,
            text="+ Create Session",
            fg_color="#6366F1",
            text_color="white",
            font=("Inter", 11, "bold"),
            height=36,
            corner_radius=18,
            hover_color="#4F46E5",
            command=self._open_create_session_dialog
        ).pack(side="left", padx=(0, 12))
        
        # History Tab
        self.history_tab = ctk.CTkButton(
            tab_area,
            text="HISTORY",
            fg_color="#000000" if self.current_state == "history" else "transparent",
            text_color="white" if self.current_state == "history" else "#64748B",
            border_width=0 if self.current_state == "history" else 1,
            border_color="#E2E8F0",
            font=("Inter", 11, "bold"),
            width=100,
            height=36,
            corner_radius=18,
            hover_color="#333333" if self.current_state == "history" else "#F1F5F9",
            command=lambda: self._switch_state("history")
        )
        self.history_tab.pack(side="left", padx=(0, 8))
        
        # Manual Entry Tab
        self.manual_tab = ctk.CTkButton(
            tab_area,
            text="MANUAL ENTRY",
            fg_color="#000000" if self.current_state == "manual_entry" else "transparent",
            text_color="white" if self.current_state == "manual_entry" else "#64748B",
            border_width=0 if self.current_state == "manual_entry" else 1,
            border_color="#E2E8F0",
            font=("Inter", 11, "bold"),
            width=130,
            height=36,
            corner_radius=18,
            hover_color="#333333" if self.current_state == "manual_entry" else "#F1F5F9",
            command=lambda: self._switch_state("manual_entry")
        )
        self.manual_tab.pack(side="left")
    
    def _switch_state(self, new_state):
        """Switch between History and Manual Entry states"""
        if self.current_state == new_state:
            return
        
        self.current_state = new_state
        
        # Update tab buttons
        if self.current_state == "history":
            self.history_tab.configure(fg_color="#000000", text_color="white", border_width=0)
            self.manual_tab.configure(fg_color="transparent", text_color="#64748B", border_width=1)
        else:
            self.history_tab.configure(fg_color="transparent", text_color="#64748B", border_width=1)
            self.manual_tab.configure(fg_color="#000000", text_color="white", border_width=0)
        
        # Re-render content
        self._render_current_state()
    
    def _open_create_session_dialog(self):
        """Open Create Session dialog with callback to refresh data"""
        dialog = CreateSessionDialog(
            self.winfo_toplevel(),
            self.teacher,
            self.controller,
            on_success=self.refresh_data
        )
        self.winfo_toplevel().wait_window(dialog)
    
    def _render_current_state(self):
        """Render UI theo state hiện tại"""
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        if self.current_state == "history":
            self._render_history_state()
        else:
            self._render_manual_entry_state()
    
    # ========================================================================
    # STATE 1: HISTORY
    # ========================================================================
    
    def _render_history_state(self):
        """Render History state: Recent Sessions + Quick Actions"""
        # Grid layout: 3:1
        self.content_area.grid_columnconfigure(0, weight=3)
        self.content_area.grid_columnconfigure(1, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)
        
        # Left: Recent Sessions
        self._create_recent_sessions_panel(self.content_area)
        
        # Right: Quick Actions
        self._create_quick_actions_panel(self.content_area)
    
    def _create_recent_sessions_panel(self, parent):
        """Recent Sessions panel"""
        panel = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        # Top bar
        top_bar = ctk.CTkFrame(panel, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=25)
        
        ctk.CTkLabel(
            top_bar,
            text="RECENT SESSIONS",
            font=("Inter", 11, "bold"),
            text_color="#94A3B8"
        ).pack(side="left")
        
        # Search box
        search_frame = ctk.CTkFrame(
            top_bar,
            fg_color="transparent",
            border_width=1,
            border_color="#E2E8F0",
            corner_radius=20,
            width=200,
            height=35
        )
        search_frame.pack(side="right")
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Arial", 12),
            text_color="#94A3B8"
        ).pack(side="left", padx=(12, 5))
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="Find session",
            border_width=0,
            fg_color="transparent",
            height=30,
            font=("Inter", 11)
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Column headers
        headers = ctk.CTkFrame(panel, fg_color="#F8FAFC", height=40)
        headers.pack(fill="x", padx=1)
        headers.pack_propagate(False)
        
        headers.grid_columnconfigure(0, weight=2)
        headers.grid_columnconfigure(1, weight=1)
        headers.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(
            headers,
            text="COURSE",
            font=("Inter", 10, "bold"),
            text_color="#94A3B8"
        ).grid(row=0, column=0, sticky="w", padx=30)
        
        ctk.CTkLabel(
            headers,
            text="DATE",
            font=("Inter", 10, "bold"),
            text_color="#94A3B8"
        ).grid(row=0, column=1, sticky="w", padx=10)
        
        ctk.CTkLabel(
            headers,
            text="HEADCOUNT",
            font=("Inter", 10, "bold"),
            text_color="#94A3B8"
        ).grid(row=0, column=2, sticky="e", padx=30)
        
        # Session list
        self.session_list_frame = ctk.CTkScrollableFrame(panel, fg_color="transparent")
        self.session_list_frame.pack(fill="both", expand=True, padx=10, pady=(10, 20))
        
        self._render_session_list()
        
    def _render_session_list(self):
        """Render recent sessions list"""
        # Clear existing
        for widget in self.session_list_frame.winfo_children():
            widget.destroy()
            
        # Add sessions
        for i, session in enumerate(self.recent_sessions):
            self._add_session_item(
                self.session_list_frame, 
                i,
                session["course"], 
                session["status"], 
                session["date"], 
                session["current"], 
                session["max"]
            )
            
    def _handle_session_click(self, index):
        """Handle click on a session item"""
        self.selected_session_idx = index
        self._render_session_list()
        
    def _add_session_item(self, parent, index, course_name, status, date_str, current, max_count):
        """Add a session item"""
        is_selected = (index == self.selected_session_idx)
        bg_color = "#EFF6FF" if is_selected else "transparent"
        border_width = 1 if is_selected else 0
        border_color = "#3B82F6" if is_selected else "#E2E8F0" # Fallback color, won't show if width 0
        
        item = ctk.CTkFrame(
            parent, 
            fg_color=bg_color, 
            height=70, 
            border_width=border_width,
            border_color=border_color,
            corner_radius=10
        )
        item.pack(fill="x", pady=5)
        item.pack_propagate(False)
        
        # Bind click event
        item.bind("<Button-1>", lambda e: self._handle_session_click(index))
        
        item.grid_columnconfigure(0, weight=2)
        item.grid_columnconfigure(1, weight=1)
        item.grid_columnconfigure(2, weight=1)
        
        # Course info
        course_frame = ctk.CTkFrame(item, fg_color="transparent")
        course_frame.grid(row=0, column=0, sticky="w", padx=20)
        
        l1 = ctk.CTkLabel(
            course_frame,
            text=course_name,
            font=("Inter", 13, "bold"),
            text_color="#0F172A"
        )
        l1.pack(anchor="w")
        
        status_color = "#94A3B8" if status == "CLOSED" else "#22C55E"
        l2 = ctk.CTkLabel(
            course_frame,
            text=status,
            font=("Inter", 10, "bold"),
            text_color=status_color
        )
        l2.pack(anchor="w", pady=(2, 0))
        
        # Date
        l3 = ctk.CTkLabel(
            item,
            text=date_str,
            font=("Inter", 12, "bold"),
            text_color="#334155"
        )
        l3.grid(row=0, column=1, sticky="w", padx=10)
        
        # Headcount with progress bar
        count_frame = ctk.CTkFrame(item, fg_color="transparent")
        count_frame.grid(row=0, column=2, sticky="e", padx=20)
        
        l4 = ctk.CTkLabel(
            count_frame,
            text=f"{current}/{max_count}",
            font=("Inter", 12, "bold"),
            text_color="#334155"
        )
        l4.pack(anchor="e")
        
        # Progress bar
        progress_bg = ctk.CTkFrame(count_frame, height=6, width=100, fg_color="#E2E8F0", corner_radius=3)
        progress_bg.pack(anchor="e", pady=(5, 0))
        progress_bg.pack_propagate(False)
        
        fill_width = int(100 * (current / max_count if max_count > 0 else 0))
        progress_fill = ctk.CTkFrame(progress_bg, height=6, width=fill_width, fg_color="#6366F1", corner_radius=3)
        progress_fill.place(x=0, y=0)
        
        # Make children clickable too
        for widget in [course_frame, count_frame, progress_bg, progress_fill, l1, l2, l3, l4]:
             widget.bind("<Button-1>", lambda e: self._handle_session_click(index))
    
    def _create_quick_actions_panel(self, parent):
        """Quick Actions panel"""
        panel = ctk.CTkFrame(parent, fg_color="transparent")
        panel.grid(row=0, column=1, sticky="nsew")
        
        ctk.CTkLabel(
            panel,
            text="QUICK ACTIONS",
            font=("Inter", 11, "bold"),
            text_color="#94A3B8",
            anchor="w"
        ).pack(fill="x", padx=10, pady=(0, 15))
        
        # Action cards
        self._add_action_card(
            panel, 
            "QR Lab Key", 
            "SESSION START", 
            "🔳", 
            "#EEF2FF", 
            "#6366F1",
            on_click=self._handle_qr_lab_key
        )
        self._add_action_card(
            panel, 
            "Remote Link", 
            "HYBRID MODE", 
            "🔗", 
            "#FFFFFF", 
            "#64748B",
            on_click=self._handle_remote_link
        )
        self._add_action_card(
            panel, 
            "Bulk CSV", 
            "9C9DA2", 
            "📄", 
            "#FFFFFF", 
            "#64748B",
            on_click=self._handle_bulk_csv
        )
    
    def _handle_bulk_csv(self):
        """Handle Bulk CSV export action"""
        if self.selected_session_idx is None:
            # Show beautiful error modal
            Modal(
                self,
                title="Yêu cầu chọn lớp",
                message="Vui lòng chọn một lớp học trong danh sách bên trái trước khi xuất file CSV.",
                type="warning",
                button_text="Đã hiểu"
            )
            return

        selected_session = self.recent_sessions[self.selected_session_idx]
        course_name = selected_session["course"]
        
        # Mock success action
        Modal(
            self,
            title="Xuất file thành công",
            message=f"Đã xuất file báo cáo điểm danh cho lớp {course_name} thành công!\nFile được lưu tại: Downloads/Attendance_{course_name}.csv",
            type="success",
            button_text="Đóng"
        )
    
    def _add_action_card(self, parent, title, subtitle, icon, bg_color, text_color, on_click=None):
        """Add an action card"""
        card = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, height=90)
        card.pack(fill="x", pady=6)
        card.pack_propagate(False)
        
        # Icon
        icon_frame = ctk.CTkFrame(card, width=50, height=50, fg_color=bg_color, corner_radius=12)
        icon_frame.pack(side="left", padx=20)
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text=icon,
            font=("Arial", 20)
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        # Text
        text_frame = ctk.CTkFrame(card, fg_color="transparent")
        text_frame.pack(side="left", pady=20)
        
        ctk.CTkLabel(
            text_frame,
            text=title,
            font=("Inter", 12, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        subtitle_color = "#6366F1" if "SESSION START" in subtitle else "#94A3B8"
        ctk.CTkLabel(
            text_frame,
            text=subtitle,
            font=("Inter", 10, "bold"),
            text_color=subtitle_color
        ).pack(anchor="w", pady=(2, 0))
        
        # Add click handler if provided
        if on_click:
            card.bind("<Button-1>", lambda e: on_click())
            # Make all children clickable too
            for widget in [icon_frame, text_frame]:
                widget.bind("<Button-1>", lambda e: on_click())
                for child in widget.winfo_children():
                    child.bind("<Button-1>", lambda e: on_click())
            
            # Hover effect
            card.bind("<Enter>", lambda e: card.configure(fg_color="#F8FAFC"))
            card.bind("<Leave>", lambda e: card.configure(fg_color="white"))
    
    def _handle_qr_lab_key(self):
        """Handle QR Lab Key button click"""
        try:
            print("🔳 QR Lab Key clicked!")  # Debug
            
            from tkinter import messagebox
            from views.components import QRLabModal
            
            # Check if controller exists
            if not hasattr(self, 'controller') or self.controller is None:
                print("❌ Error: Controller not found")
                messagebox.showerror(
                    "Lỗi",
                    "Controller không được khởi tạo đúng"
                )
                return
            
            # Check if teacher exists  
            if not hasattr(self, 'teacher') or self.teacher is None:
                print("❌ Error: Teacher not found")
                messagebox.showerror(
                    "Lỗi",
                    "Teacher object không tồn tại"
                )
                return
            
            print(f"✅ Teacher: {self.teacher.full_name}")
            
            # Get teacher's classes
            try:
                classes = self.controller.get_class_list(self.teacher)
                print(f"✅ Found {len(classes)} classes")
            except Exception as e:
                print(f"❌ Error getting classes: {e}")
                messagebox.showerror(
                    "Lỗi",
                    f"Không thể lấy danh sách lớp: {str(e)}"
                )
                return
            
            if not classes:
                print("⚠️ No classes found")
                messagebox.showwarning(
                    "Thông báo",
                    "Bạn chưa được phân công lớp nào.\nVui lòng liên hệ admin."
                )
                return
            
            # Use first class for demo
            class_id = classes[0].class_id
            print(f"✅ Using class: {class_id}")
            
            # Generate QR code
            try:
                print("🔄 Generating QR code...")
                result = self.controller.handle_generate_qr_code(
                    teacher=self.teacher,
                    class_id=class_id
                )
                print(f"✅ Result: {result.get('success')}")
            except Exception as e:
                print(f"❌ Error generating QR: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror(
                    "Lỗi",
                    f"Lỗi khi tạo QR code: {str(e)}"
                )
                return
            
            if not result.get("success"):
                error_msg = result.get("message", "Không thể tạo QR code")
                print(f"❌ Generation failed: {error_msg}")
                messagebox.showerror("Lỗi", error_msg)
                return
            
            # Open modal with QR code
            try:
                print("🔓 Opening modal...")
                modal = QRLabModal(
                    master=self,
                    session_data=result["session_data"],
                    qr_image=result["qr_image"],
                    on_refresh=lambda: self._refresh_qr_code(class_id),
                    on_close=None
                )
                print("✅ Modal opened successfully!")
            except Exception as e:
                print(f"❌ Error opening modal: {e}")
                import traceback
                traceback.print_exc()
                messagebox.showerror(
                    "Lỗi",
                    f"Lỗi khi mở modal: {str(e)}"
                )
                
        except Exception as e:
            print(f"❌ Unexpected error in _handle_qr_lab_key: {e}")
            import traceback
            traceback.print_exc()
            from tkinter import messagebox
            messagebox.showerror(
                "Lỗi",
                f"Lỗi không xác định: {str(e)}"
            )
        
    def _refresh_qr_code(self, class_id):
        """Refresh QR code"""
        try:
            result = self.controller.handle_generate_qr_code(
                teacher=self.teacher,
                class_id=class_id
            )
            
            if result.get("success"):
                return result["qr_image"]
            
            return None
        except Exception as e:
            print(f"Error refreshing QR: {e}")
            return None
    
    def _handle_remote_link(self):
        """Handle Remote Link button click - displays secret code for remote students"""
        try:
            print("🔗 Remote Link clicked!")
            
            from tkinter import messagebox
            
            # Get teacher's classes
            classes = self.controller.get_class_list(self.teacher)
            
            if not classes:
                messagebox.showwarning(
                    "Thông báo",
                    "Bạn chưa được phân công lớp nào.\nVui lòng liên hệ admin."
                )
                return
            
            # Use first class
            class_id = classes[0].class_id
            
            # Generate or get existing session
            result = self.controller.handle_generate_qr_code(
                teacher=self.teacher,
                class_id=class_id
            )
            
            if not result.get("success"):
                messagebox.showerror(
                    "Lỗi",
                    result.get("message", "Không thể lấy secret code")
                )
                return
            
            # Display secret code
            session_data = result["session_data"]
            secret_code = session_data.get("secret_code", "N/A")
            class_name = session_data.get("class_name", "N/A")
            
            messagebox.showinfo(
                "Remote Link - Secret Code",
                f"📝 SECRET CODE FOR REMOTE STUDENTS\n\n"
                f"Class: {class_name}\n"
                f"Code: {secret_code}\n\n"
                f"Share this code with remote students.\n"
                f"They can enter it in the 'Enter Secret Code' option."
            )
            
        except Exception as e:
            print(f"Error in Remote Link: {e}")
            import traceback
            traceback.print_exc()
            from tkinter import messagebox
            messagebox.showerror(
                "Lỗi",
                f"Lỗi khi lấy Remote Link: {str(e)}"
            )
    
    # ========================================================================
    # STATE 2: MANUAL ENTRY
    # ========================================================================
    
    def _render_manual_entry_state(self):
        """Render Manual Entry state: Student roster"""
        # Single column layout
        container = ctk.CTkFrame(self.content_area, fg_color="transparent")
        container.pack(expand=True, fill="both")
        
        # Roster header
        self._create_roster_header(container)
        
        # Student list
        self._create_student_list(container)
    
    def _create_roster_header(self, parent):
        """Roster header with search and actions"""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        # Left side: Title & subtitle
        title_area = ctk.CTkFrame(header, fg_color="transparent")
        title_area.pack(side="left")
        
        ctk.CTkLabel(
            title_area,
            text="Data Science Roster",
            font=("Inter", 20, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            title_area,
            text="Machine Learning - Cohort Average: 60 Scholars",
            font=("Inter", 12),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(2, 0))
        
        # Right side: Search + Button
        action_area = ctk.CTkFrame(header, fg_color="transparent")
        action_area.pack(side="right")
        
        # Search box
        search_frame = ctk.CTkFrame(
            action_area,
            fg_color="#F8FAFC",
            border_width=1,
            border_color="#E2E8F0",
            corner_radius=20,
            width=200,
            height=38
        )
        search_frame.pack(side="left", padx=(0, 12))
        search_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            search_frame,
            text="🔍",
            font=("Arial", 12),
            text_color="#94A3B8"
        ).pack(side="left", padx=(12, 5))
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="Search scholar...",
            border_width=0,
            fg_color="transparent",
            font=("Inter", 11)
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Set 100% Present button
        ctk.CTkButton(
            action_area,
            text="SET 100% PRESENT",
            fg_color="#000000",
            text_color="white",
            font=("Inter", 11, "bold"),
            height=38,
            corner_radius=20,
            hover_color="#333333",
            command=self._set_all_present
        ).pack(side="left")
    
    def _create_student_list(self, parent):
        """Student list with attendance status"""
        list_frame = ctk.CTkScrollableFrame(parent, fg_color="white", corner_radius=15)
        list_frame.pack(fill="both", expand=True)
        
        # Add students
        for student in self.students:
            self._add_student_row(list_frame, student)
    
    def _add_student_row(self, parent, student):
        """Add a student row with status buttons"""
        row = ctk.CTkFrame(parent, fg_color="transparent", height=70)
        row.pack(fill="x", padx=20, pady=8)
        row.pack_propagate(False)
        
        # Avatar
        initials = "".join([word[0].upper() for word in student["name"].split()[:2]])
        avatar = ctk.CTkLabel(
            row,
            text=initials,
            width=45,
            height=45,
            fg_color="#E9D5FF",
            text_color="#7C3AED",
            font=("Inter", 13, "bold"),
            corner_radius=22
        )
        avatar.pack(side="left", padx=(0, 15))
        
        # Info
        info_frame = ctk.CTkFrame(row, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=student["name"],
            font=("Inter", 13, "bold"),
            text_color="#0F172A"
        ).pack(anchor="w")
        
        ping_text = f"ID: {student['id']} LAST PING: {student['last_ping']}"
        ctk.CTkLabel(
            info_frame,
            text=ping_text,
            font=("Inter", 10),
            text_color="#94A3B8"
        ).pack(anchor="w", pady=(2, 0))
        
        # Status buttons
        status_frame = ctk.CTkFrame(row, fg_color="transparent")
        status_frame.pack(side="right")
        
        current_status = student["status"]
        
        # Present button
        present_active = current_status == "present"
        present_btn = ctk.CTkButton(
            status_frame,
            text="✓",
            width=35,
            height=35,
            corner_radius=17,
            fg_color="#10B981" if present_active else "transparent",
            text_color="white" if present_active else "#94A3B8",
            border_width=0 if present_active else 2,
            border_color="#E2E8F0",
            hover_color="#059669" if present_active else "#F1F5F9",
            font=("Arial", 16, "bold"),
            command=lambda s=student: self._set_student_status(s, "present")
        )
        present_btn.pack(side="left", padx=4)
        
        # Late button
        late_active = current_status == "late"
        late_btn = ctk.CTkButton(
            status_frame,
            text="🕐",
            width=35,
            height=35,
            corner_radius=17,
            fg_color="#F59E0B" if late_active else "transparent",
            text_color="white" if late_active else "#94A3B8",
            border_width=0 if late_active else 2,
            border_color="#E2E8F0",
            hover_color="#D97706" if late_active else "#F1F5F9",
            font=("Arial", 14),
            command=lambda s=student: self._set_student_status(s, "late")
        )
        late_btn.pack(side="left", padx=4)
        
        # Absent button
        absent_active = current_status == "absent"
        absent_btn = ctk.CTkButton(
            status_frame,
            text="✕",
            width=35,
            height=35,
            corner_radius=17,
            fg_color="#EF4444" if absent_active else "transparent",
            text_color="white" if absent_active else "#94A3B8",
            border_width=0 if absent_active else 2,
            border_color="#E2E8F0",
            hover_color="#DC2626" if absent_active else "#F1F5F9",
            font=("Arial", 16, "bold"),
            command=lambda s=student: self._set_student_status(s, "absent")
        )
        absent_btn.pack(side="left", padx=4)
        
        # Separator
        sep = ctk.CTkFrame(parent, height=1, fg_color="#F1F5F9")
        sep.pack(fill="x", padx=20)
    
    def _set_student_status(self, student, status):
        """Set student attendance status"""
        student["status"] = status
        # Re-render to update UI
        self._render_current_state()
    
    def _set_all_present(self):
        """Set all students to present"""
        for student in self.students:
            student["status"] = "present"
        # Re-render to update UI
        self._render_current_state()
