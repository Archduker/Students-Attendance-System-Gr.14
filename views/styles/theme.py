"""
Styles - Theme Configuration
============================

Cấu hình theme, colors, fonts cho UI.
"""

# =============================================================================
# COLOR PALETTE
# =============================================================================
COLORS = {
    # Primary colors
    "primary": "#3B82F6",        # Blue
    "primary_hover": "#2563EB",
    "primary_light": "#DBEAFE",
    
    # Secondary colors
    "secondary": "#6B7280",      # Gray
    "secondary_hover": "#4B5563",
    
    # Status colors
    "success": "#10B981",        # Green
    "success_light": "#D1FAE5",
    "warning": "#F59E0B",        # Yellow
    "warning_light": "#FEF3C7",
    "error": "#EF4444",          # Red
    "error_light": "#FEE2E2",
    "info": "#3B82F6",           # Blue
    "info_light": "#DBEAFE",
    
    # Background colors
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F3F4F6",
    "bg_tertiary": "#E5E7EB",
    "bg_dark": "#1F2937",
    
    # Text colors
    "text_primary": "#111827",
    "text_secondary": "#6B7280",
    "text_tertiary": "#9CA3AF",
    "text_white": "#FFFFFF",
    
    # Border colors
    "border": "#E5E7EB",
    "border_focus": "#3B82F6",
}

# Dark mode colors
COLORS_DARK = {
    "bg_primary": "#1F2937",
    "bg_secondary": "#111827",
    "bg_tertiary": "#374151",
    "text_primary": "#F9FAFB",
    "text_secondary": "#D1D5DB",
    "border": "#374151",
}

# =============================================================================
# TYPOGRAPHY
# =============================================================================
FONTS = {
    "family": "Segoe UI",
    "family_mono": "Consolas",
    
    # Font sizes
    "size_xs": 10,
    "size_sm": 12,
    "size_base": 14,
    "size_lg": 16,
    "size_xl": 18,
    "size_2xl": 24,
    "size_3xl": 30,
    
    # Font weights
    "weight_normal": "normal",
    "weight_bold": "bold",
}

# =============================================================================
# SPACING
# =============================================================================
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24,
    "xl": 32,
    "2xl": 48,
}

# =============================================================================
# BORDER RADIUS
# =============================================================================
RADIUS = {
    "sm": 4,
    "md": 8,
    "lg": 12,
    "xl": 16,
    "full": 9999,
}

# =============================================================================
# SHADOWS
# =============================================================================
SHADOWS = {
    "sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px rgba(0, 0, 0, 0.1)",
    "lg": "0 10px 15px rgba(0, 0, 0, 0.1)",
}
