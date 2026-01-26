import customtkinter as ctk
from typing import Callable, Dict, Any

class ChangePasswordModal(ctk.CTkToplevel):
    def __init__(
        self, 
        parent, 
        on_save: Callable[[str, str], None], # (old_pass, new_pass) -> None
        title="Change Password"
    ):
        super().__init__(parent)
        
        self.title(title)
        self.geometry("400x480")
        self.resizable(False, False)
        
        self.on_save = on_save
        
        # Initialize UI first
        self._init_ui()
        
        # Center modal
        self.update_idletasks()
        try:
            x = parent.winfo_rootx() + (parent.winfo_width() - 400) // 2
            y = parent.winfo_rooty() + (parent.winfo_height() - 480) // 2
            self.geometry(f"+{x}+{y}")
        except:
            self.eval('tk::PlaceWindow . center')
            
        # Modal behavior
        self.transient(parent)
        self.lift()
        self.focus_force()
        
        # Defer grab_set
        self.after(100, self._safe_grab_set)
        
    def _safe_grab_set(self):
        try:
            if self.winfo_exists():
                self.grab_set()
        except:
            self.after(100, lambda: self.grab_set() if self.winfo_exists() else None)
        
    def _init_ui(self):
        self.configure(fg_color="white")
        
        # Title
        ctk.CTkLabel(
            self, text="Change Password", font=("Inter", 20, "bold"), text_color="#0F172A"
        ).pack(pady=(30, 20))
        
        # Form Container
        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=40)
        
        # Old Password
        ctk.CTkLabel(form, text="Current Password", font=("Inter", 12, "bold"), text_color="#64748B").pack(anchor="w", pady=(0, 5))
        self.old_pass_entry = ctk.CTkEntry(
            form, width=320, height=40, border_color="#E2E8F0", 
            fg_color="#F8FAFC", text_color="#0F172A", show="•"
        )
        self.old_pass_entry.pack(pady=(0, 15))
        
        # New Password
        ctk.CTkLabel(form, text="New Password", font=("Inter", 12, "bold"), text_color="#64748B").pack(anchor="w", pady=(0, 5))
        self.new_pass_entry = ctk.CTkEntry(
            form, width=320, height=40, border_color="#E2E8F0", 
            fg_color="#F8FAFC", text_color="#0F172A", show="•"
        )
        self.new_pass_entry.pack(pady=(0, 15))
        
        # Confirm New Password
        ctk.CTkLabel(form, text="Confirm New Password", font=("Inter", 12, "bold"), text_color="#64748B").pack(anchor="w", pady=(0, 5))
        self.confirm_pass_entry = ctk.CTkEntry(
            form, width=320, height=40, border_color="#E2E8F0", 
            fg_color="#F8FAFC", text_color="#0F172A", show="•"
        )
        self.confirm_pass_entry.pack(pady=(0, 15))
        
        # Error Label
        self.error_label = ctk.CTkLabel(
            form, text="", font=("Inter", 11), text_color="#EF4444"
        )
        self.error_label.pack(pady=(0, 5))

        # Buttons
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.pack(fill="x", padx=40, pady=30, side="bottom")
        
        ctk.CTkButton(
            btns, text="Cancel", fg_color="transparent", border_width=1, border_color="#E2E8F0",
            text_color="#64748B", width=100, command=self.destroy
        ).pack(side="left")
        
        ctk.CTkButton(
            btns, text="Confirm", fg_color="#3B82F6", text_color="white",
            width=200, command=self._save
        ).pack(side="right")
        
    def _save(self):
        old_pass = self.old_pass_entry.get()
        new_pass = self.new_pass_entry.get()
        confirm_pass = self.confirm_pass_entry.get()
        
        # Client-side validation
        if not all([old_pass, new_pass, confirm_pass]):
            self.error_label.configure(text="All fields are required")
            return
            
        if new_pass != confirm_pass:
            self.error_label.configure(text="New passwords do not match")
            return
            
        if new_pass == old_pass:
            self.error_label.configure(text="New password cannot be same as old password")
            return
            
        self.on_save(old_pass, new_pass)
        self.destroy()
