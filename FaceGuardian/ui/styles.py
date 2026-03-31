
class Theme:
    """
    Professional Enterprise Theme System
    Dark Mode: Modern security dashboard aesthetic
    """
    
    # ===== DARK THEME COLORS =====
    DARK = {
        'BACKGROUND': '#0A0E1A',
        'BACKGROUND_ALT': '#141824',
        'SURFACE': '#1E2433',
        'SURFACE_ELEVATED': '#252B3F',
        'SURFACE_HOVER': '#2D3548',
        'PRIMARY': '#00D9FF',
        'PRIMARY_DARK': '#00B8D9',
        'SECONDARY': '#6366F1',
        'ACCENT': '#10B981',
        'SUCCESS': '#10B981',
        'DANGER': '#FF3B5C',
        'WARNING': '#FFAA00',
        'TEXT_MAIN': '#FFFFFF',
        'TEXT_SUB': '#94A3B8',
        'TEXT_MUTED': '#64748B',
        'BORDER': '#2D3548',
        'BORDER_LIGHT': '#3D4558',
        'SHADOW': 'rgba(0, 0, 0, 0.5)'
    }
    
    # Default constants
    BACKGROUND = DARK['BACKGROUND']
    SURFACE = DARK['SURFACE']
    SURFACE_HOVER = DARK['SURFACE_HOVER']
    PRIMARY = DARK['PRIMARY']
    SECONDARY = DARK['SECONDARY']
    ACCENT = DARK['ACCENT']
    SUCCESS = DARK['SUCCESS']
    DANGER = DARK['DANGER']
    WARNING = DARK['WARNING']
    TEXT_MAIN = DARK['TEXT_MAIN']
    TEXT_SUB = DARK['TEXT_SUB']
    BORDER = DARK['BORDER']
    SHADOW = DARK['SHADOW']
    
    FONT_FAMILY = "Segoe UI, -apple-system, BlinkMacSystemFont, Roboto, sans-serif"
    
    @staticmethod
    def get_stylesheet():
        """Generate professional enterprise stylesheet (Dark Mode Only)"""
        c = Theme.DARK
        
        sidebar_bg = c['SURFACE']
        sidebar_shadow = f"border-right: 1px solid {c['BORDER']};"
        card_shadow = f"border: 1px solid {c['BORDER']};"
        topbar_shadow = f"border-bottom: 1px solid {c['BORDER']};"
        
        return f"""
        /* ===== GLOBAL STYLES ===== */
        QMainWindow {{
            background-color: {c['BACKGROUND']};
        }}
        
        QWidget {{
            background-color: transparent;
            color: {c['TEXT_MAIN']};
            font-family: "{Theme.FONT_FAMILY}";
            font-size: 14px;
        }}
        
        /* ===== SIDEBAR (ELEVATED WITH SHADOW) ===== */
        QFrame#Sidebar {{
            background-color: {sidebar_bg};
            {sidebar_shadow}
            min-width: 220px;
            max-width: 220px;
        }}
        
        QPushButton#NavButton {{
            background-color: transparent;
            color: {c['TEXT_SUB']};
            text-align: left;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            border: none;
            border-left: 3px solid transparent;
            margin: 2px 12px;
            border-radius: 6px;
        }}
        
        QPushButton#NavButton:hover {{
            background-color: {c['SURFACE_HOVER']};
            color: {c['TEXT_MAIN']};
            border-left: 3px solid {c['PRIMARY']};
        }}
        
        QPushButton#NavButton[active="true"] {{
            background-color: {c['SURFACE_HOVER']};
            color: {c['PRIMARY']};
            border-left: 3px solid {c['PRIMARY']};
            font-weight: 700;
        }}
        
        /* ===== TOP BAR (PROFESSIONAL HEIGHT & SPACING) ===== */
        QFrame#TopBar {{
            background-color: {c['SURFACE']};
            {topbar_shadow}
            min-height: 56px;
            max-height: 56px;
        }}
        
        QLabel#SystemStatus {{
            color: {c['ACCENT']};
            font-weight: 600;
            font-size: 12px;
            padding: 6px 14px;
            background-color: {c['SURFACE_HOVER']};
            border-radius: 14px;
            border: 1px solid {c['ACCENT']};
        }}
        
        /* ===== PROFESSIONAL CARDS (ELEVATED WITH SHADOW) ===== */
        QFrame#Card {{
            background-color: {c['SURFACE']};
            {card_shadow}
            border-radius: 8px;
            padding: 20px;
        }}
        
        QFrame#Card:hover {{
            border-color: {c['PRIMARY']};
        }}
        
        QLabel#CardTitle {{
            color: {c['TEXT_SUB']};
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QLabel#CardValue {{
            color: {c['TEXT_MAIN']};
            font-size: 32px;
            font-weight: 700;
        }}
        
        /* ===== MODERN BUTTONS ===== */
        QPushButton#PrimaryButton {{
            background-color: {c['PRIMARY']};
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            font-size: 14px;
            border: none;
        }}
        
        QPushButton#PrimaryButton:hover {{
            background-color: {c['PRIMARY_DARK']};
        }}
        
        QPushButton#PrimaryButton:pressed {{
            background-color: {c['PRIMARY_DARK']};
            padding-top: 11px;
            padding-bottom: 9px;
        }}
        
        QPushButton#DangerButton {{
            background-color: {c['DANGER']};
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 600;
            border: none;
        }}
        
        QPushButton#DangerButton:hover {{
            background-color: #A52A2A;
        }}
        
        QPushButton#SecondaryButton {{
            background-color: transparent;
            color: {c['PRIMARY']};
            border: 1.5px solid {c['PRIMARY']};
            border-radius: 6px;
            padding: 9px 20px;
            font-weight: 600;
        }}
        
        QPushButton#SecondaryButton:hover {{
            background-color: {c['PRIMARY']};
            color: white;
        }}
        
        /* ===== PROFESSIONAL INPUTS ===== */
        QLineEdit {{
            background-color: {c['SURFACE']};
            border: 1.5px solid {c['BORDER']};
            border-radius: 6px;
            padding: 10px 14px;
            color: {c['TEXT_MAIN']};
            font-size: 14px;
            selection-background-color: {c['PRIMARY']};
        }}
        
        QLineEdit:focus {{
            border: 1.5px solid {c['PRIMARY']};
            background-color: {c['SURFACE']};
        }}
        
        QLineEdit:hover {{
            border-color: {c['BORDER_LIGHT']};
        }}
        
        QComboBox {{
            background-color: {c['SURFACE']};
            border: 1.5px solid {c['BORDER']};
            border-radius: 6px;
            padding: 10px 14px;
            color: {c['TEXT_MAIN']};
            font-size: 14px;
        }}
        
        QComboBox:hover {{
            border-color: {c['PRIMARY']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            padding-right: 10px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {c['SURFACE']};
            border: 1.5px solid {c['BORDER']};
            border-radius: 6px;
            selection-background-color: {c['PRIMARY']};
            selection-color: white;
            color: {c['TEXT_MAIN']};
            padding: 6px;
        }}
        
        /* ===== MODERN SCROLLBARS ===== */
        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {c['BORDER']};
            border-radius: 5px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {c['TEXT_MUTED']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {c['BORDER']};
            border-radius: 5px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {c['TEXT_MUTED']};
        }}
        
        /* ===== PROGRESS BARS ===== */
        QProgressBar {{
            background-color: {c['SURFACE_HOVER']};
            border-radius: 6px;
            text-align: center;
            color: {c['TEXT_MAIN']};
            font-weight: 600;
            border: none;
            height: 10px;
        }}
        
        QProgressBar::chunk {{
            background-color: {c['PRIMARY']};
            border-radius: 6px;
        }}
        
        /* ===== PROFESSIONAL LISTS ===== */
        QListWidget {{
            background-color: transparent;
            border: none;
            outline: none;
        }}
        
        QListWidget::item {{
            background-color: {c['SURFACE']};
            border: 1px solid {c['BORDER']};
            border-radius: 6px;
            padding: 14px;
            margin-bottom: 8px;
            color: {c['TEXT_MAIN']};
        }}
        
        QListWidget::item:hover {{
            background-color: {c['SURFACE_HOVER']};
            border-color: {c['BORDER_LIGHT']};
        }}
        
        QListWidget::item:selected {{
            background-color: {c['SURFACE_HOVER']};
            color: {c['PRIMARY']};
            border-color: {c['PRIMARY']};
            font-weight: 600;
        }}
        
        /* ===== TOOLTIPS ===== */
        QToolTip {{
            background-color: {c['SURFACE_ELEVATED']};
            color: {c['TEXT_MAIN']};
            border: 1px solid {c['BORDER']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        /* ===== STATUS BADGES ===== */
        QLabel#StatusBadge {{
            background-color: {c['ACCENT']};
            color: white;
            border-radius: 10px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        
        QLabel#DangerBadge {{
            background-color: {c['DANGER']};
            color: white;
            border-radius: 10px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 700;
        }}
        
        QLabel#WarningBadge {{
            background-color: {c['WARNING']};
            color: white;
            border-radius: 10px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 700;
        }}
        """
    
    @classmethod
    def get_global_styles(cls):
        """Get default dark theme styles for backward compatibility"""
        return cls.get_stylesheet()


# For backward compatibility
Theme.GLOBAL_STYLES = Theme.get_stylesheet()
