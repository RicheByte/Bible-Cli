class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    ORANGE = '\033[33m' # Added for more options

def highlight(text, word, color=Colors.YELLOW):
    """Highlights a specific word in the text with a given color."""
    if not word:
        return text
    # Case-insensitive replacement
    parts = text.split(word) # Simple split, might need regex for complex cases
    # Rejoin with colored word
    return (f"{color}{word}{Colors.END}").join(parts)

def colorize_book(book_name):
    """Assigns a consistent color to each book for visual distinction."""
    # Simple hash-based coloring for now
    colors = [Colors.BLUE, Colors.CYAN, Colors.GREEN, Colors.YELLOW, Colors.ORANGE, Colors.RED]
    index = sum(ord(char) for char in book_name) % len(colors)
    return colors[index]