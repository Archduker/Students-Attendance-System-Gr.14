import customtkinter as ctk

class Modal(ctk.CTkToplevel):
    """
    A unified, beautiful modal dialog.
    """
    def __init__(
        self, 
        master, 
        title: str = "Notification", 
        message: str = "",
        type: str = "success", # success, info, warning, error
        button_text: str = "Continue",
        on_close = None
    ):
        super().__init__(master)
        
        self.title(title)
        self.geometry("400x280")
        self.resizable(False, False)
        
        # Center the modal
        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - 200
        y = master.winfo_y() + (master.winfo_height() // 2) - 140
        self.geometry(f"+{x}+{y}")
        
        # Modal effect - make it transient and grab focus
        self.transient(master)
        self.grab_set()
        
        self.on_close = on_close
        self.protocol("WM_DELETE_WINDOW", self._close)
        
        # Styling based on type
        colors = {
            "success": ("#DCFCE7", "#166534", "✅"), # Green-100 bg, Green-800 text
            "info": ("#EFF6FF", "#1E40AF", "ℹ️"),
            "warning": ("#FEF3C7", "#92400E", "⚠️"),
            "error": ("#FEE2E2", "#991B1B", "❌"),
        }
        bg_col, text_col, icon = colors.get(type, colors["info"])
        
        self.configure(fg_color="white")
        
        # Content
        
        # Icon Circle
        icon_frm = ctk.CTkFrame(self, fg_color=bg_col, width=60, height=60, corner_radius=30)
        icon_frm.pack(pady=(30, 15))
        ctk.CTkLabel(icon_frm, text=icon, font=("Arial", 28)).place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        ctk.CTkLabel(self, text=title, font=("Inter", 18, "bold"), text_color="#1E293B").pack(pady=(0, 5))
        
        # Message
        ctk.CTkLabel(
            self, 
            text=message, 
            font=("Inter", 13), 
            text_color="#64748B", 
            wraplength=340
        ).pack(pady=(0, 25))
        
        # Button
        ctk.CTkButton(
            self,
            text=button_text,
            font=("Inter", 13, "bold"),
            fg_color="#000000",
            text_color="white",
            hover_color="#333333",
            corner_radius=20,
            width=200,
            height=40,
            command=self._close
        ).pack(pady=(0, 20))

    def _close(self):
        if self.on_close:
            self.on_close()
        self.destroy()
