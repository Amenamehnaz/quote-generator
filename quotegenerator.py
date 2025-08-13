#!/usr/bin/env python3
"""
Quote Generator – pick a random inspirational quote from quotes.txt,
or manage your quotes via a simple CLI.

Usage:
  python quote_generator.py            # print a random quote
  python quote_generator.py --count    # show how many quotes you have
  python quote_generator.py --list     # list all quotes with numbers
  python quote_generator.py --add "Stay hungry, stay foolish.|Steve Jobs"
  python quote_generator.py --remove 12  # remove quote #12
"""

import argparse   # for command-line arguments
import os         # for file handling
import random     # for random quote selection
from typing import List, Tuple  # for type hints

QUOTES_FILE = "quotes.txt"
DEFAULT_QUOTES = [
    "The best way to get started is to quit talking and begin doing.|Walt Disney",
    "Whether you think you can or you think you can’t, you’re right.|Henry Ford",
    "It always seems impossible until it’s done.|Nelson Mandela",
    "Stay hungry, stay foolish.|Steve Jobs",
    "You miss 100% of the shots you don’t take.|Wayne Gretzky",
    "If you’re going through hell, keep going.|Winston Churchill",
    "Dream big and dare to fail.|Norman Vaughan",
    "The secret of getting ahead is getting started.|Mark Twain",
    "Small steps every day.|Unknown",
    "Do one thing every day that scares you.|Eleanor Roosevelt"
]

def ensure_quotes_file() -> None:
    """Create quotes.txt with default quotes if it doesn’t exist."""
    if not os.path.exists(QUOTES_FILE):
        with open(QUOTES_FILE, "w", encoding="utf-8") as f:
            for line in DEFAULT_QUOTES:
                f.write(line.strip() + "\n")

def load_quotes() -> List[Tuple[str, str]]:
    """Load quotes from quotes.txt and return as list of (text, author)."""
    ensure_quotes_file()
    quotes = []
    with open(QUOTES_FILE, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            if "|" in raw:
                text, author = raw.split("|", 1)
            else:
                text, author = raw, "Unknown"
            quotes.append((text.strip(), author.strip()))
    return quotes

def save_quotes(quotes: List[Tuple[str, str]]) -> None:
    """Save quotes list back to quotes.txt."""
    with open(QUOTES_FILE, "w", encoding="utf-8") as f:
        for text, author in quotes:
            if author and author.lower() != "unknown":
                f.write(f"{text}|{author}\n")
            else:
                f.write(f"{text}\n")

def print_random_quote() -> None:
    """Print a random quote."""
    quotes = load_quotes()
    if not quotes:
        print("No quotes found. Add one with --add.")
        return
    text, author = random.choice(quotes)
    print(f"“{text}” — {author}")

def list_quotes() -> None:
    """List all quotes with numbers."""
    quotes = load_quotes()
    if not quotes:
        print("No quotes yet. Add some with --add.")
        return
    for i, (text, author) in enumerate(quotes, start=1):
        print(f"{i}. {text} — {author}")

def add_quote(raw: str) -> None:
    """Add a new quote from input string."""
    raw = raw.strip()
    if not raw:
        print("Provide a non-empty quote.")
        return
    if "|" in raw:
        text, author = raw.split("|", 1)
    else:
        text, author = raw, "Unknown"
    quotes = load_quotes()
    quotes.append((text.strip(), author.strip()))
    save_quotes(quotes)
    print("✅ Added.")

def remove_quote(index: int) -> None:
    """Remove quote by its index number."""
    quotes = load_quotes()
    if not (1 <= index <= len(quotes)):
        print(f"Index out of range. Must be 1..{len(quotes)}")
        return
    removed = quotes.pop(index - 1)
    save_quotes(quotes)
    print(f"🗑️ Removed: “{removed[0]}” — {removed[1]}")

def main():
    parser = argparse.ArgumentParser(description="Random Quote Generator")
    parser.add_argument("--list", action="store_true", help="List all quotes")
    parser.add_argument("--count", action="store_true", help="Show total quote count")
    parser.add_argument("--add", metavar="QUOTE", help='Add a quote: "text|author" or "text"')
    parser.add_argument("--remove", metavar="N", type=int, help="Remove quote number N (from --list)")
    args = parser.parse_args()

    if args.add:
        add_quote(args.add)
        return
    if args.remove is not None:
        remove_quote(args.remove)
        return
    if args.list:
        list_quotes()
        return
    if args.count:
        print(len(load_quotes()))
        return

    # Default: print a random quote
    print_random_quote()

if __name__ == "__main__":
    main()
