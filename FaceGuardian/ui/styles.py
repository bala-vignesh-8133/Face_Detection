
class Theme:
    # 1. Colors
    BACKGROUND = "#0F172A"       # Deep Navy/Slate
    SURFACE    = "#1E293B"       # Lighter Navy (Cards)
    SURFACE_HOVER = "#334155"
    
    PRIMARY    = "#06B6D4"       # Cyan Neon
    SECONDARY  = "#3B82F6"       # Blue Neon
    ACCENT     = "#10B981"       # Emerald Green (Safe)
    
    DANGER     = "#EF4444"       # Red (Alert)
    WARNING    = "#F59E0B"       # Amber
    
    TEXT_MAIN  = "#F8FAFC"
    TEXT_SUB   = "#94A3B8"
    
    BORDER     = "#334155"

    # 2. Fonts
    FONT_FAMILY = "Segoe UI, Inter, Roboto, sans-serif"

    # 3. Global Stylesheet
    GLOBAL_STYLES = f"""
        QMainWindow {{
            background-color: {BACKGROUND};
        }}
        QWidget {{
            background-color: {BACKGROUND};
            color: {TEXT_MAIN};
            font-family: "{FONT_FAMILY}";
        }}
        
        /* --- Sidebar --- */
        QFrame#Sidebar {{
            background-color: {SURFACE};
            border-right: 1px solid {BORDER};
        }}
        QPushButton#NavButton {{
            background-color: transparent;
            color: {TEXT_SUB};
            text-align: left;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            border: none;
            border-left: 3px solid transparent;
            margin-bottom: 5px;
        }}
        QPushButton#NavButton:hover {{
            background-color: {SURFACE_HOVER};
            color: {TEXT_MAIN};
        }}
        QPushButton#NavButton[active="true"] {{
            background-color: {SURFACE_HOVER};
            color: {PRIMARY};
            border-left: 3px solid {PRIMARY};
        }}
        
        /* --- Top Bar --- */
        QFrame#TopBar {{
            background-color: {SURFACE};
            border-bottom: 1px solid {BORDER};
        }}
        QLabel#SystemStatus {{
            color: {ACCENT};
            font-weight: bold;
            font-size: 13px;
        }}
        
        /* --- Cards --- */
        QFrame#Card {{
            background-color: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 12px;
        }}
        QLabel#CardTitle {{
            color: {TEXT_SUB};
            font-size: 13px;
            font-weight: 600;
        }}
        QLabel#CardValue {{
            color: {TEXT_MAIN};
            font-size: 28px;
            font-weight: 800;
        }}
        
        /* --- Tables/Lists --- */
        QListWidget {{
            background-color: transparent;
            border: none;
        }}
        
        /* --- Buttons --- */
        QPushButton#PrimaryButton {{
            background-color: {PRIMARY};
            color: white;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 14px;
        }}
        QPushButton#PrimaryButton:hover {{
            background-color: {SECONDARY};
        }}
        QPushButton#DangerButton {{
            background-color: {DANGER};
            color: white;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
        }}
        
        /* --- Inputs --- */
        QLineEdit {{
            background-color: {SURFACE_HOVER};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 10px;
            color: {TEXT_MAIN};
            selection-background-color: {PRIMARY};
        }}
        QLineEdit:focus {{
            border: 1px solid {PRIMARY};
        }}
    """
