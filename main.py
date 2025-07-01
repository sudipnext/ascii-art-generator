#!/usr/bin/env python3
import pyfiglet
import psycopg2
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

# Load environment variables
load_dotenv()

def generate_ascii_art(text, font="big"):
    return pyfiglet.figlet_format(text, font=font)

def print_gradient_ascii(ascii_art, start_color=(255, 105, 180), end_color=(0, 255, 255)):
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

def get_random_quote():
    try:
        # Direct connection string for Neon
        conn_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}?sslmode=require"
        connection = psycopg2.connect(conn_string)
        
        cursor = connection.cursor()
        cursor.execute("SELECT quote, author, category FROM quotes ORDER BY RANDOM() LIMIT 1;")
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if result:
            return {
                'quote': result[0],
                'author': result[1], 
                'category': result[2]
            }
        return None
    except Exception as e:
        print(f"Database error: {e}")
        return None

def display_quote(quote_data):
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

if __name__ == "__main__":
    # Generate ASCII art for the name
    text = "sudipnext"
    ascii_art = generate_ascii_art(text, font="big")
    print_gradient_ascii(ascii_art)
    
    # Fetch and display a random quote
    quote_data = get_random_quote()
    display_quote(quote_data)
