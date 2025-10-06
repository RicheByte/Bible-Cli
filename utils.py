import json, random
from color import highlight, Colors, colorize_book
from config import DEFAULT_TRANSLATION, AVAILABLE_TRANSLATIONS

# Global variable to store loaded Bibles
BIBLE_DATA = {}
CURRENT_TRANSLATION_KEY = DEFAULT_TRANSLATION
CURRENT_BIBLE = None # Will hold the currently active bible data

# Keep track of current navigation point
CURRENT_LOCATION = {"book": None, "chapter": None, "verse": None, "translation": DEFAULT_TRANSLATION}

def load_bible_data(translation_key):
    """Loads a specific translation's JSON data into BIBLE_DATA."""
    try:
        filepath = f'bible_data/{translation_key}.json'
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            BIBLE_DATA[translation_key] = json.load(f)
            print(f"Loaded {AVAILABLE_TRANSLATIONS.get(translation_key, translation_key).upper()} successfully.")
            return True
    except FileNotFoundError:
        print(f"{Colors.RED}Error: Translation file '{filepath}' not found.{Colors.END}")
        return False
    except json.JSONDecodeError:
        print(f"{Colors.RED}Error: Could not decode JSON from '{filepath}'.{Colors.END}")
        return False

def set_current_translation(translation_key):
    """Sets the active translation for the CLI."""
    global CURRENT_TRANSLATION_KEY, CURRENT_BIBLE, CURRENT_LOCATION
    if translation_key not in AVAILABLE_TRANSLATIONS:
        print(f"{Colors.RED}Unknown translation: {translation_key}. Available: {', '.join(AVAILABLE_TRANSLATIONS.keys())}{Colors.END}")
        return False
    
    if translation_key not in BIBLE_DATA:
        if not load_bible_data(translation_key):
            return False
            
    CURRENT_TRANSLATION_KEY = translation_key
    CURRENT_BIBLE = BIBLE_DATA[translation_key]
    CURRENT_LOCATION["translation"] = translation_key
    print(f"{Colors.GREEN}Translation set to: {AVAILABLE_TRANSLATIONS[translation_key].upper()}{Colors.END}")
    return True

# Initialize default translation on startup
if not set_current_translation(DEFAULT_TRANSLATION):
    print(f"{Colors.RED}Failed to load default translation '{DEFAULT_TRANSLATION}'. Please check 'bible_data/' folder.{Colors.END}")
    # Exit or handle gracefully if default fails

def list_books(translation_key=None):
    """Returns a list of book names for the current or specified translation."""
    bible = BIBLE_DATA.get(translation_key, CURRENT_BIBLE)
    if not bible: return []
    # Since bible is a dict, return its keys
    return list(bible.keys())

def find_book_by_abbrev(abbrev, translation_key=None):
    """Finds a full book name by its abbreviation."""
    bible = BIBLE_DATA.get(translation_key, CURRENT_BIBLE)
    if not bible: return None
    for book_name, book_obj in bible.items():
        if book_obj.get("abbrev", "").lower() == abbrev.lower():
            return book_name
    return None

def get_book_data(book_name, translation_key=None):
    """Retrieves the full book object for a given book name."""
    bible = BIBLE_DATA.get(translation_key, CURRENT_BIBLE)
    if not bible: return None
    return bible.get(book_name)


def get_verse(book_name, chapter_num, verse_num, highlight_word=None, translation_key=None):
    """Retrieves and formats a single verse."""
    book_obj = get_book_data(book_name, translation_key)
    if not book_obj:
        return f"{Colors.RED}Book '{book_name}' not found.{Colors.END}"

    try:
        # JSON structure is [{ "book": ..., "chapters": [ [v1, v2], [v1, v2] ] }]
        # Chapter and verse numbers are 1-based, so use index-1
        verse_text = book_obj["chapters"][chapter_num - 1][verse_num - 1]
        
        formatted_text = highlight(verse_text, highlight_word, Colors.YELLOW)
        
        # Update current location
        CURRENT_LOCATION.update({"book": book_name, "chapter": chapter_num, "verse": verse_num})
        
        book_color = colorize_book(book_name)
        return (f"{book_color}{book_name}{Colors.END} {Colors.CYAN}{chapter_num}:{verse_num}{Colors.END} - {formatted_text}")
    except IndexError:
        return f"{Colors.RED}Verse {book_name} {chapter_num}:{verse_num} not found.{Colors.END}"
    except Exception as e:
        return f"{Colors.RED}Error getting verse: {e}{Colors.END}"


def get_chapter(book_name, chapter_num, highlight_word=None, translation_key=None):
    """Retrieves and formats all verses in a chapter."""
    book_obj = get_book_data(book_name, translation_key)
    if not book_obj:
        return f"{Colors.RED}Book '{book_name}' not found.{Colors.END}"

    try:
        chapter_verses = book_obj["chapters"][chapter_num - 1]
        
        output = []
        for i, verse_text in enumerate(chapter_verses):
            formatted_text = highlight(verse_text, highlight_word, Colors.YELLOW)
            book_color = colorize_book(book_name)
            output.append(f"{book_color}{book_name}{Colors.END} {Colors.CYAN}{chapter_num}:{i+1}{Colors.END} - {formatted_text}")
            
        # Update current location to the last verse of the chapter for "next" command context
        CURRENT_LOCATION.update({"book": book_name, "chapter": chapter_num, "verse": len(chapter_verses)})
        return "\n".join(output)
    except IndexError:
        return f"{Colors.RED}Chapter {book_name} {chapter_num} not found.{Colors.END}"
    except Exception as e:
        return f"{Colors.RED}Error getting chapter: {e}{Colors.END}"

def search_keyword(keyword, translation_key=None):
    """Searches for a keyword across the entire Bible (or current translation)."""
    bible = BIBLE_DATA.get(translation_key, CURRENT_BIBLE)
    if not bible:
        return [f"{Colors.RED}No Bible data loaded for search.{Colors.END}"]
    
    results = []
    for book_name, book_obj in bible.items():
        for chap_idx, chapter_verses in enumerate(book_obj["chapters"]):
            for verse_idx, verse_text in enumerate(chapter_verses):
                if keyword.lower() in verse_text.lower():
                    formatted_text = highlight(verse_text, keyword, Colors.YELLOW)
                    book_color = colorize_book(book_name)
                    results.append(
                        f"{book_color}{book_name}{Colors.END} "
                        f"{Colors.CYAN}{chap_idx+1}:{verse_idx+1}{Colors.END} - {formatted_text}"
                    )
    return results


def random_verse(translation_key=None):
    """Returns a random verse from the current or specified translation."""
    bible = BIBLE_DATA.get(translation_key, CURRENT_BIBLE)
    if not bible: 
        return f"{Colors.RED}No Bible data loaded for random verse.{Colors.END}"

    # Pick a random book name
    random_book_name = random.choice(list(bible.keys()))
    random_book_obj = bible[random_book_name]

    # Pick random chapter and verse
    random_chapter_index = random.randrange(len(random_book_obj["chapters"]))
    random_chapter_num = random_chapter_index + 1

    random_verse_index = random.randrange(len(random_book_obj["chapters"][random_chapter_index]))
    random_verse_num = random_verse_index + 1

    return get_verse(random_book_name, random_chapter_num, random_verse_num, translation_key=translation_key)


# --- Navigation functions ---

def get_next_location():
    """Calculates the next verse's location."""
    current = CURRENT_LOCATION
    if not current["book"]: return None
    
    book_obj = get_book_data(current["book"], current["translation"])
    if not book_obj: return None

    # Try next verse in current chapter
    if current["verse"] < len(book_obj["chapters"][current["chapter"] - 1]):
        return {"book": current["book"], "chapter": current["chapter"], "verse": current["verse"] + 1}
    
    # Try next chapter in current book
    if current["chapter"] < len(book_obj["chapters"]):
        return {"book": current["book"], "chapter": current["chapter"] + 1, "verse": 1}
        
    # Try next book
    all_books = list_books(current["translation"])
    try:
        current_book_index = all_books.index(current["book"])
        if current_book_index < len(all_books) - 1:
            next_book_name = all_books[current_book_index + 1]
            return {"book": next_book_name, "chapter": 1, "verse": 1}
    except ValueError:
        pass # Current book not in list

    return None # End of Bible

def get_previous_location():
    """Calculates the previous verse's location."""
    current = CURRENT_LOCATION
    if not current["book"]: return None
    
    book_obj = get_book_data(current["book"], current["translation"])
    if not book_obj: return None

    # Try previous verse in current chapter
    if current["verse"] > 1:
        return {"book": current["book"], "chapter": current["chapter"], "verse": current["verse"] - 1}
    
    # Try previous chapter in current book
    if current["chapter"] > 1:
        prev_chapter_num = current["chapter"] - 1
        # Get last verse of previous chapter
        prev_chapter_verses_count = len(book_obj["chapters"][prev_chapter_num - 1])
        return {"book": current["book"], "chapter": prev_chapter_num, "verse": prev_chapter_verses_count}
        
    # Try previous book
    all_books = list_books(current["translation"])
    try:
        current_book_index = all_books.index(current["book"])
        if current_book_index > 0:
            prev_book_name = all_books[current_book_index - 1]
            prev_book_obj = get_book_data(prev_book_name, current["translation"])
            # Go to the last chapter of the previous book
            prev_book_last_chapter_num = len(prev_book_obj["chapters"])
            # Go to the last verse of the last chapter of the previous book
            prev_book_last_chapter_last_verse = len(prev_book_obj["chapters"][prev_book_last_chapter_num - 1])
            return {"book": prev_book_name, "chapter": prev_book_last_chapter_num, "verse": prev_book_last_chapter_last_verse}
    except ValueError:
        pass

    return None # Beginning of Bible