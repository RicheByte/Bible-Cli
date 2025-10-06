from utils import (
    get_verse, get_chapter, list_books, search_keyword, random_verse,
    set_current_translation, get_next_location, get_previous_location,
    CURRENT_LOCATION
)
from config import AVAILABLE_TRANSLATIONS, CLI_COLORS, DEFAULT_TRANSLATION

from study import daily_verse, topic_lookup, memorization_quiz, TOPICS # <--- THIS LINE MUST BE CORRECT
from export import export_chapter, export_search
from autocomplete import setup_autocomplete
from color import Colors
from config import CLI_COLORS

def display_help():
    """Displays available commands and their usage."""
    help_text = f"""
{Colors.HEADER}=== Bible CLI Help ==={Colors.END}
{Colors.BOLD}Navigation:{Colors.END}
  {CLI_COLORS["prompt"]}verse <book> <chapter> <verse> [highlight_word]{Colors.END} - Display a specific verse.
  {CLI_COLORS["prompt"]}chapter <book> <chapter> [highlight_word]{Colors.END}   - Display an entire chapter.
  {CLI_COLORS["prompt"]}next{Colors.END}  - Go to the next verse.
  {CLI_COLORS["prompt"]}prev{Colors.END}  - Go to the previous verse.
  
{Colors.BOLD}Search & Study:{Colors.END}
  {CLI_COLORS["prompt"]}search <keyword>{Colors.END} - Search for a keyword across the Bible.
  {CLI_COLORS["prompt"]}daily{Colors.END}          - Get a random 'verse of the day'.
  {CLI_COLORS["prompt"]}topic <topic_name>{Colors.END} - Look up verses related to a topic (e.g., love, faith).
  {CLI_COLORS["prompt"]}quiz{Colors.END}           - Start a memorization quiz (placeholder).

{Colors.BOLD}Settings & Utilities:{Colors.END}
  {CLI_COLORS["prompt"]}set_translation <abbr>{Colors.END} - Set the active Bible translation (e.g., kjv, niv).
                          Available: {', '.join(AVAILABLE_TRANSLATIONS.keys())}
  {CLI_COLORS["prompt"]}export chapter <book> <chapter> <filename>{Colors.END} - Export a chapter to a file.
  {CLI_COLORS["prompt"]}export search <keyword> <filename>{Colors.END} - Export search results to a file.
  {CLI_COLORS["prompt"]}history{Colors.END}        - View recent navigation history (placeholder).
  {CLI_COLORS["prompt"]}help{Colors.END}           - Show this help message.
  {CLI_COLORS["prompt"]}exit{Colors.END}           - Exit the CLI.
"""
    print(help_text)

def parse_command(command_input):
    """Parses a command string into a command and arguments."""
    parts = command_input.strip().split()
    cmd = parts[0].lower() if parts else ""
    args = parts[1:]
    return cmd, args

def main():
    books = list_books()
    setup_autocomplete(books + list(AVAILABLE_TRANSLATIONS.keys()) + list(TOPICS.keys())) # Autocomplete for books, translations, and topics
    
    
    print(f"{CLI_COLORS['header']}=== Bible CLI 2.0 ==={Colors.END}")
    print(f"{CLI_COLORS['highlight']}")
    print("               |")
    print("           \\       /")
    print("             .---. ")
    print("        '-.  |   |  .-'")
    print("          ___|   |___")
    print("     -=  [           ]  =-")
    print("         `---.   .---' ")
    print("      __||__ |   | __||__")
    print("      '-..-' |   | '-..-'")
    print("        ||   |   |   ||")
    print("        ||_.-|   |-,_||")
    print("      .-\"`   `\"'`'`   `\"-.")
    print("    .'                    '.")
    print(f"{Colors.END}")

    print(f"{CLI_COLORS['success']}Ready to explore the Scriptures. Type 'help' for commands.{Colors.END}")
    print(f"Current translation: {AVAILABLE_TRANSLATIONS[CURRENT_LOCATION['translation']].upper()}")

    while True:
        try:
            command_input = input(f"\n{CLI_COLORS['prompt']}bible_cli> {Colors.END}").strip()
            if not command_input:
                continue

            cmd, args = parse_command(command_input)

            if cmd == "exit":
                break
            elif cmd == "help":
                display_help()
            elif cmd == "verse":
                if len(args) < 3:
                    print(f"{CLI_COLORS['error']}Usage: verse <book> <chapter> <verse> [highlight_word]{Colors.END}")
                    continue
                book, chapter, verse = args[0], int(args[1]), int(args[2])
                highlight_word = args[3] if len(args) > 3 else None
                print(get_verse(book, chapter, verse, highlight_word))
            elif cmd == "chapter":
                if len(args) < 2:
                    print(f"{CLI_COLORS['error']}Usage: chapter <book> <chapter> [highlight_word]{Colors.END}")
                    continue
                book, chapter = args[0], int(args[1])
                highlight_word = args[2] if len(args) > 2 else None
                print(get_chapter(book, chapter, highlight_word))
            elif cmd == "search":
                if not args:
                    print(f"{CLI_COLORS['error']}Usage: search <keyword>{Colors.END}")
                    continue
                keyword = " ".join(args)
                results = search_keyword(keyword)
                if results:
                    print(f"{Colors.BOLD}--- Search Results for '{keyword}' ({len(results)} found) ---{Colors.END}")
                    for r in results[:20]: # Show top 20 results
                        print(r)
                    if len(results) > 20:
                        print(f"{Colors.BLUE}...(showing first 20 results).{Colors.END}")
                else:
                    print(f"{Colors.BLUE}No results found for '{keyword}'.{Colors.END}")
            elif cmd == "daily":
                print(daily_verse())
            elif cmd == "topic":
                if not args:
                    print(f"{CLI_COLORS['error']}Usage: topic <topic_name>{Colors.END}")
                    continue
                topic_name = args[0]
                print(topic_lookup(topic_name))
            elif cmd == "quiz":
                memorization_quiz()
            elif cmd == "set_translation":
                if len(args) != 1:
                    print(f"{CLI_COLORS['error']}Usage: set_translation <abbr>. Available: {', '.join(AVAILABLE_TRANSLATIONS.keys())}{Colors.END}")
                    continue
                set_current_translation(args[0])
                # Update autocomplete options if needed (e.g., if different translations have different book lists)
                setup_autocomplete(list_books() + list(AVAILABLE_TRANSLATIONS.keys()) + list(TOPICS.keys()))
            elif cmd == "export":
                if len(args) < 3:
                    print(f"{CLI_COLORS['error']}Usage: export chapter <book> <chapter> <filename> OR export search <keyword> <filename>{Colors.END}")
                    continue
                export_type = args[0].lower()
                if export_type == "chapter":
                    if len(args) < 4:
                        print(f"{CLI_COLORS['error']}Usage: export chapter <book> <chapter> <filename>{Colors.END}")
                        continue
                    book, chapter, filename = args[1], int(args[2]), args[3]
                    print(export_chapter(book, chapter, filename))
                elif export_type == "search":
                    if len(args) < 3:
                        print(f"{CLI_COLORS['error']}Usage: export search <keyword> <filename>{Colors.END}")
                        continue
                    keyword_parts = args[1:-1]
                    keyword = " ".join(keyword_parts)
                    filename = args[-1]
                    print(export_search(keyword, filename))
                else:
                    print(f"{CLI_COLORS['error']}Invalid export type. Use 'chapter' or 'search'.{Colors.END}")
            elif cmd == "next":
                next_loc = get_next_location()
                if next_loc:
                    print(get_verse(next_loc["book"], next_loc["chapter"], next_loc["verse"]))
                else:
                    print(f"{Colors.BLUE}End of Bible reached (or no current location set).{Colors.END}")
            elif cmd == "prev":
                prev_loc = get_previous_location()
                if prev_loc:
                    print(get_verse(prev_loc["book"], prev_loc["chapter"], prev_loc["verse"]))
                else:
                    print(f"{Colors.BLUE}Beginning of Bible reached (or no current location set).{Colors.END}")
            else:
                print(f"{CLI_COLORS['error']}Unknown command: '{cmd}'. Type 'help' for available commands.{Colors.END}")
        except ValueError as e:
            print(f"{CLI_COLORS['error']}Input Error: {e}. Please ensure chapter/verse are numbers.{Colors.END}")
        except Exception as e:
            print(f"{CLI_COLORS['error']}An unexpected error occurred: {e}{Colors.END}")

if __name__ == "__main__":
    main()