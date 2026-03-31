
class Translator:
    """
    Localization Manager for English and Tamil.
    """
    LANG_EN = "English"
    LANG_TA = "Tamil"
    
    _current_lang = LANG_EN
    
    # Translation Dictionary
    _data = {
        "Commander Dashboard": {
            LANG_EN: "Commander Dashboard",
            LANG_TA: "தலைமையகக் கட்டுப்பாட்டு அறை"
        },
        "Live Surveillance": {
            LANG_EN: "Live Surveillance",
            LANG_TA: "நேரடி கண்காணிப்பு"
        },
        "Verification Scanner": {
            LANG_EN: "Verification Scanner",
            LANG_TA: "சரிபார்ப்பு ஸ்கேனர்"
        },
        "Report Missing Child": {
            LANG_EN: "Report Missing Child",
            LANG_TA: "காணாமல் போன குழந்தையைப் பதிவு செய்"
        },
        "Missing Children DB": {
            LANG_EN: "Missing Children DB",
            LANG_TA: "குழந்தைகள் தகவல் தளம்"
        },
        "Active Alerts": {
            LANG_EN: "Active Alerts",
            LANG_TA: "நேரடி எச்சரிக்கைகள்"
        },
        "System Settings": {
            LANG_EN: "System Settings",
            LANG_TA: "அமைப்பு அமைப்புகள்"
        },
        "Logout": {
            LANG_EN: "Logout",
            LANG_TA: "வெளியேறு"
        },
        "SYSTEM ACTIVE": {
            LANG_EN: "SYSTEM ACTIVE",
            LANG_TA: "இயக்கத்தில் உள்ளது"
        },
        "REGISTER REPORT": {
            LANG_EN: "REGISTER REPORT",
            LANG_TA: "பதிவு செய்"
        },
        "Select Photo": {
            LANG_EN: "Select Photo",
            LANG_TA: "புகைப்படத்தைத் தேர்ந்தெடு"
        },
        "UPLOAD PHOTO": {
            LANG_EN: "UPLOAD PHOTO",
            LANG_TA: "புகைப்படத்தைப் பதிவேற்று"
        },
        "Approve Case": {
            LANG_EN: "Approve Case",
            LANG_TA: "வழக்கை அங்கீகரி"
        },
        "Close Case": {
            LANG_EN: "Close Case",
            LANG_TA: "வழக்கை முடி"
        },
        "CHILD's FULL NAME": {
            LANG_EN: "CHILD'S FULL NAME",
            LANG_TA: "குழந்தையின் முழு பெயர்"
        },
        "AGE (approximate)": {
            LANG_EN: "AGE (approximate)",
            LANG_TA: "வயது (தோராயமாக)"
        },
        "LAST SEEN LOCATION": {
            LANG_EN: "LAST SEEN LOCATION",
            LANG_TA: "கடைசியாகக் காணப்பட்ட இடம்"
        },
        "DATE MISSING": {
            LANG_EN: "DATE MISSING",
            LANG_TA: "காணாமல் போன தேதி"
        },
        "GUARDIAN CONTACT": {
            LANG_EN: "GUARDIAN CONTACT",
            LANG_TA: "பாதுகாவலர் தொடர்பு எண்"
        },
        "AADHAR NUMBER": {
            LANG_EN: "AADHAR NUMBER",
            LANG_TA: "ஆதார் எண்"
        },
        "Merge into existing profile (New Angle)": {
            LANG_EN: "Merge into existing profile (New Angle)",
            LANG_TA: "ஏற்கனவே உள்ள சுயவிவரத்துடன் இணைக்கவும்"
        },
        "Role": {
            LANG_EN: "Role",
            LANG_TA: "பணி"
        },
        "Case": {
            LANG_EN: "Case",
            LANG_TA: "வழக்கு"
        },
        "Approved and Active!": {
            LANG_EN: "Approved and Active!",
            LANG_TA: "அங்கீகரிக்கப்பட்டு செயல்பாட்டில் உள்ளது!"
        },
        "MATCH FOUND": {
            LANG_EN: "MATCH FOUND",
            LANG_TA: "குழந்தை கண்டறியப்பட்டது!"
        },
        "SCANNING": {
            LANG_EN: "SCANNING",
            LANG_TA: "தேடுதல் நடைபெறுகிறது..."
        },
        "Unknown": {
            LANG_EN: "Unknown",
            LANG_TA: "அடையாளம் தெரியவில்லை"
        },
        "TARGET ANALYSIS": {
            LANG_EN: "TARGET ANALYSIS",
            LANG_TA: "இலக்கு பகுப்பாய்வு"
        },
        "SECURITY LOCK ACTIVE": {
            LANG_EN: "SECURITY LOCK ACTIVE",
            LANG_TA: "பாதுகாப்பு பூட்டு செயல்பாட்டில் உள்ளது"
        }
    }

    @classmethod
    def set_language(cls, lang):
        if lang in [cls.LANG_EN, cls.LANG_TA]:
            cls._current_lang = lang

    @classmethod
    def get_language(cls):
        return cls._current_lang

    @classmethod
    def tr(cls, key):
        """Translate the given key based on current language."""
        if key in cls._data:
            return cls._data[key].get(cls._current_lang, key)
        return key
