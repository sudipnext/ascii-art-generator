#!/usr/bin/env python3
"""
ASCII Art Generator with Random Quotes - Offline Version
This version uses a local JSON file instead of database connectivity
"""

import json
import random
import pyfiglet
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
import os
base_dir = os.path.dirname(os.path.abspath(__file__))

def generate_ascii_art(text, font="big"):
    """Generate ASCII art from text using pyfiglet"""
    return pyfiglet.figlet_format(text, font=font)

def print_gradient_ascii(ascii_art, start_color=(255, 105, 180), end_color=(0, 255, 255)):
    """Print ASCII art with gradient coloring using Rich"""
    console = Console()
    lines = ascii_art.splitlines()
    max_width = max(len(line) for line in lines) if lines else 0

    for line in lines:
        rich_text = Text()
        for i, char in enumerate(line):
            ratio = i / max_width if max_width else 0
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"

            if char.strip():  # Only style visible characters
                rich_text.append(char, style=f"bold {hex_color}")
            else:
                rich_text.append(char)  # Keep space unstyled
        console.print(rich_text)


def load_quotes_from_file(quotes_file="quotes_dump.json"):
    """Load quotes from local JSON file"""
    try:
        if not os.path.exists(quotes_file):
            print(f"❌ Quotes file '{quotes_file}' not found!")
            print("💡 Run 'python extract_quotes_dump.py' to create the quotes file.")
            return None

        with open(os.path.join(base_dir, quotes_file), 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data['quotes']
    except Exception as e:
        print(f"❌ Error loading quotes: {e}")
        return None

def get_random_quote(quotes_data=None):
    """Get a random quote from the loaded quotes data"""
    if quotes_data is None:
        quotes_data = load_quotes_from_file()
    
    if not quotes_data:
        return None
    
    quote = random.choice(quotes_data)
    return {
        'quote': quote['quote'],
        'author': quote['author'],
        'category': quote['category']
    }

def display_quote(quote_data):
    """Display a beautifully formatted quote using Rich"""
    if not quote_data:
        print("Could not fetch quote from database.")
        return
    
    console = Console()
    
    # Create the quote text with proper formatting
    quote_text = f'"{quote_data["quote"]}"'
    author_text = f"— {quote_data['author']}"
    category_text = f"Category: {quote_data['category'].title()}"
    
    # Create rich text objects with styling
    quote_rich = Text(quote_text, style="italic cyan")
    author_rich = Text(author_text, style="bold magenta")
    category_rich = Text(category_text, style="dim yellow")
    
    # Combine all text elements
    full_text = Text()
    full_text.append(quote_rich)
    full_text.append("\n\n")
    full_text.append(author_rich)
    full_text.append("\n")
    full_text.append(category_rich)
    
    # Create a beautiful panel around the quote
    quote_panel = Panel(
        Align.center(full_text),
        border_style="bright_blue",
        title="✨ [bold yellow]Daily Inspiration[/bold yellow] ✨",
        title_align="center",
        padding=(1, 2)
    )
    
    console.print("\n")
    console.print(quote_panel)

def main(name="sudipnext", font="big"):
    """Main function to generate ASCII art and display quote"""
    # Generate ASCII art for the name
    ascii_art = generate_ascii_art(name, font=font)
    print_gradient_ascii(ascii_art)
    
    # Load quotes and display a random one
    quotes_data = load_quotes_from_file()
    if quotes_data:
        quote_data = get_random_quote(quotes_data)
        display_quote(quote_data)
    else:
        print("📚 No quotes available. Run with database connection or generate quotes_dump.json")

if __name__ == "__main__":
    import sys
    
    # Allow custom name and font from command line
    name = sys.argv[1] if len(sys.argv) > 1 else "sudipnext"
    font = sys.argv[2] if len(sys.argv) > 2 else "big"
    
    main(name, font)
