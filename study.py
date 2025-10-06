from utils import random_verse, BIBLE_DATA, get_book_data, CURRENT_TRANSLATION_KEY, get_verse
from color import Colors
from config import AVAILABLE_TRANSLATIONS



TOPICS = {
    "love": [("John", 3, 16), ("1 Corinthians", 13, 4)], # Example: (book, chapter, verse)
    "faith": [("Hebrews", 11, 1), ("James", 2, 17)],
    "grace": [("Ephesians", 2, 8), ("Titus", 2, 11)],
    "creation": [("Genesis", 1, 1), ("Psalm", 19, 1)],
}

def daily_verse():
    """Returns a random verse as the 'verse of the day'."""
    print(f"{Colors.HEADER}--- DAILY VERSE ({AVAILABLE_TRANSLATIONS[CURRENT_TRANSLATION_KEY].upper()}) ---{Colors.END}")
    return random_verse(translation_key=CURRENT_TRANSLATION_KEY)

def topic_lookup(topic):
    """Looks up verses related to a given topic."""
    topic_lower = topic.lower()
    if topic_lower not in TOPICS:
        return f"{Colors.RED}Topic '{topic}' not found. Try: {', '.join(TOPICS.keys())}{Colors.END}"
    
    verses_for_topic = TOPICS[topic_lower]
    output = [f"{Colors.HEADER}--- TOPIC: {topic.upper()} ---{Colors.END}"]
    
    for book_name, chapter, verse in verses_for_topic:
        output.append(get_verse(book_name, chapter, verse, translation_key=CURRENT_TRANSLATION_KEY))
    
    return "\n".join(output)

# Placeholder for Memorization Quiz Mode
def memorization_quiz():
    print(f"{Colors.YELLOW}Memorization Quiz Mode (coming soon!)...{Colors.END}")
    # Logic to present a verse, hide words, ask user to fill in, etc.