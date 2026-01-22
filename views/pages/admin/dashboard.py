"""
Admin Dashboard UI - Trang tổng quan hệ thống
=============================================

Dashboard hiển thị:
- Tổng số users, classes, sessions
- Hoạt động gần đây
- Thống kê điểm danh
"""

import customtkinter as ctk
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


class AdminDashboard(ctk.CTkFrame):
    """
    Admin Dashboard Page - Tổng quan hệ thống.
    
    Features:
        - Summary cards: tổng users, classes, sessions
        - Recent activity log
        - Attendance statistics
        - Quick actions
        
    Example:
        >>> dashboard = AdminDashboard(parent, admin_controller)
        >>> dashboard.pack(fill="both", expand=True)
    """
    
    def __init__(
        self, 
        parent, 
        admin_controller,
        **kwargs
    ):
        """
        Khởi tạo Admin Dashboard.
        
        Args:
            parent: Parent widget
            admin_controller: AdminController instance
        """
        super().__init__(parent, **kwargs)
        
        self.admin_controller = admin_controller
        self.stats_data: Dict[str, Any] = {}
        
        self._init_ui()
        self._load_data()
    
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
        """Tạo header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Admin Dashboard",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(side="left")
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="🔄 Refresh",
            width=100,
            command=self._refresh_data
        )
        refresh_btn.pack(side="right")
    
    def _create_content(self):
        """Tạo main content."""
        content_frame = ctk.CTkScrollableFrame(self)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        content_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Summary Cards
        self._create_summary_cards(content_frame)
        
        # Charts and Stats
        self._create_stats_section(content_frame)
        
        # Recent Activity
        self._create_activity_section(content_frame)
    
    def _create_summary_cards(self, parent):
        """Tạo summary cards."""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Total Users Card
        self.users_card = self._create_stat_card(
            cards_frame,
            "👥 Total Users",
            "0",
            "All system users",
            0, 0
        )
        
        # Total Classes Card
        self.classes_card = self._create_stat_card(
            cards_frame,
            "📚 Total Classes",
            "0",
            "Active classes",
            0, 1
        )
        
        # Total Sessions Card
        self.sessions_card = self._create_stat_card(
            cards_frame,
            "📝 Total Sessions",
            "0",
            "This month",
            0, 2
        )
    
    def _create_stat_card(
        self, 
        parent, 
        title: str, 
        value: str, 
        subtitle: str,
        row: int,
        col: int
    ) -> ctk.CTkFrame:
        """
        Tạo một stat card.
        
        Args:
            parent: Parent widget
            title: Tiêu đề card
            value: Giá trị hiển thị
            subtitle: Phụ đề
            row: Grid row
            col: Grid column
            
        Returns:
            Card frame
        """
        card = ctk.CTkFrame(parent, corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        title_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#1f6aa5"
        )
        value_label.pack(pady=5)
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            card,
            text=subtitle,
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        subtitle_label.pack(pady=(5, 15))
        
        # Store value label for updates
        card.value_label = value_label
        
        return card
    
    def _create_stats_section(self, parent):
        """Tạo statistics section."""
        stats_frame = ctk.CTkFrame(parent, corner_radius=10)
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(0, 10), pady=(0, 20))
        
        # Title
        title_label = ctk.CTkLabel(
            stats_frame,
            text="📈 Attendance Statistics (Last 7 Days)",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(15, 10), padx=15, anchor="w")
        
        # Stats content
        self.stats_content = ctk.CTkFrame(stats_frame, fg_color="transparent")
        self.stats_content.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Placeholder - sẽ được thay thế bằng chart thực tế
        placeholder = ctk.CTkLabel(
            self.stats_content,
            text="Chart: Attendance trends over time\n(To be implemented with matplotlib)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        placeholder.pack(pady=30)
    
    def _create_activity_section(self, parent):
        """Tạo recent activity section."""
        activity_frame = ctk.CTkFrame(parent, corner_radius=10)
        activity_frame.grid(row=1, column=2, sticky="nsew", padx=(10, 0), pady=(0, 20))
        
        # Title
        title_label = ctk.CTkLabel(
            activity_frame,
            text="🔔 Recent Activity",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(15, 10), padx=15, anchor="w")
        
        # Activity list
        self.activity_list = ctk.CTkScrollableFrame(
            activity_frame,
            fg_color="transparent"
        )
        self.activity_list.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Placeholder activities
        self._add_activity_item("User 'admin' logged in", "2 minutes ago")
        self._add_activity_item("New class 'CS101' created", "15 minutes ago")
        self._add_activity_item("User 'teacher1' updated", "1 hour ago")
    
    def _add_activity_item(self, text: str, time: str):
        """
        Thêm activity item vào list.
        
        Args:
            text: Nội dung activity
            time: Thời gian
        """
        item_frame = ctk.CTkFrame(self.activity_list, fg_color="transparent")
        item_frame.pack(fill="x", pady=5)
        
        # Activity text
        activity_label = ctk.CTkLabel(
            item_frame,
            text=text,
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        activity_label.pack(fill="x")
        
        # Time
        time_label = ctk.CTkLabel(
            item_frame,
            text=time,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        time_label.pack(fill="x")
    
    def _load_data(self):
        """Load dashboard data từ controller."""
        try:
            # Get dashboard stats from controller
            result = self.admin_controller.get_dashboard_stats()
            
            if result.get("success"):
                self.stats_data = result.get("data", {})
                self._update_ui()
            else:
                self._show_error(result.get("error", "Failed to load data"))
                
        except Exception as e:
            self._show_error(f"Error loading data: {str(e)}")
    
    def _update_ui(self):
        """Update UI với data mới."""
        # Update summary cards
        if self.stats_data:
            total_users = self.stats_data.get("total_users", 0)
            total_classes = self.stats_data.get("total_classes", 0)
            total_sessions = self.stats_data.get("total_sessions", 0)
            
            self.users_card.value_label.configure(text=str(total_users))
            self.classes_card.value_label.configure(text=str(total_classes))
            self.sessions_card.value_label.configure(text=str(total_sessions))
    
    def _refresh_data(self):
        """Refresh dashboard data."""
        self._load_data()
    
    def _show_error(self, message: str):
        """
        Hiển thị error message.
        
        Args:
            message: Error message
        """
        # TODO: Implement proper error dialog
        print(f"Error: {message}")
    
    def refresh(self):
        """Public method để refresh dashboard."""
        self._refresh_data()
