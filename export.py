from utils import get_chapter, search_keyword, AVAILABLE_TRANSLATIONS, CURRENT_TRANSLATION_KEY
from color import Colors

def export_chapter(book_name, chapter_num, filename):
    """Exports a chapter to a text file."""
    content = get_chapter(book_name, chapter_num, translation_key=CURRENT_TRANSLATION_KEY)
    if f"{Colors.RED}Error" in content: # Check for error messages
        print(content)
        return ""
    
    # Remove ANSI escape codes for cleaner export
    content_clean = Colors.strip_ansi_codes(content) # Assuming Colors class has this method
    
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(f"--- {book_name} Chapter {chapter_num} ({AVAILABLE_TRANSLATIONS[CURRENT_TRANSLATION_KEY]}) ---\n\n")
        f.write(content_clean)
    return f"{Colors.GREEN}Chapter exported to {filename}{Colors.END}"

def export_search(keyword, filename):
    """Exports search results to a text file."""
    results = search_keyword(keyword, translation_key=CURRENT_TRANSLATION_KEY)
    if not results or f"{Colors.RED}Error" in results[0]:
        print("\n".join(results))
        return ""
        
    # Remove ANSI escape codes
    clean_results = [Colors.strip_ansi_codes(r) for r in results]
    
    with open(filename, "w", encoding="utf-8-sig") as f:
        f.write(f"--- Search Results for '{keyword}' ({AVAILABLE_TRANSLATIONS[CURRENT_TRANSLATION_KEY]}) ---\n\n")
        f.write("\n".join(clean_results))
    return f"{Colors.GREEN}Search results exported to {filename}{Colors.END}"

# Add this method to the Colors class in color.py
# @staticmethod
# def strip_ansi_codes(text):
#     import re
#     return re.sub(r'\x1b\[[0-9;]*m', '', text)