import readline

def setup_autocomplete(options):
    """Sets up readline for tab completion with provided options."""
    def completer(text, state):
        matches = [o for o in options if o.lower().startswith(text.lower())]
        return matches[state] if state < len(matches) else None
    
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")