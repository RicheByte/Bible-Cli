# config.py
from color import Colors # <--- ADD THIS LINE



DEFAULT_TRANSLATION = "kjv"

AVAILABLE_TRANSLATIONS = {
    "kjv": "King James Version",
    "bbe": "Bible in Basic English"
}


# CLI Colors for different elements
CLI_COLORS = {
    "header": Colors.HEADER,
    "prompt": Colors.BLUE,
    "error": Colors.RED,
    "success": Colors.GREEN,
    "highlight": Colors.YELLOW,
    "verse_meta": Colors.CYAN, # For "Book Chapter:Verse" part
}