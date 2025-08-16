#!/usr/bin/env python3
"""
Explore the Quran word position bounds SQLite database.
This script shows example queries and usage of the database.
"""

import sqlite3
import sys

def connect_db(db_path='quran_word_bounds.sqlite'):
    """Connect to the SQLite database."""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def show_schema(cursor):
    """Show database schema."""
    print("=== DATABASE SCHEMA ===")
    
    # Show tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        print(f"\nTable: {table_name}")
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  {col[1]} ({col[2]})")

def show_summary_stats(cursor):
    """Show summary statistics."""
    print("\n=== SUMMARY STATISTICS ===")
    
    # Word bounds
    cursor.execute('SELECT COUNT(*) FROM word_bounds')
    word_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM glyph_bounds')
    glyph_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(DISTINCT page_number) FROM word_bounds')
    page_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT MIN(page_number), MAX(page_number) FROM word_bounds')
    min_page, max_page = cursor.fetchone()
    
    cursor.execute('SELECT COUNT(DISTINCT sura_number) FROM word_bounds')
    sura_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT MIN(sura_number), MAX(sura_number) FROM word_bounds')
    min_sura, max_sura = cursor.fetchone()
    
    print(f"Total word bounds: {word_count:,}")
    print(f"Total glyph bounds: {glyph_count:,}")
    print(f"Pages available: {page_count} (range: {min_page}-{max_page})")
    print(f"Suras covered: {sura_count} (range: {min_sura}-{max_sura})")

def show_sample_data(cursor):
    """Show sample data from the database."""
    print("\n=== SAMPLE WORD BOUNDS (first 10 words) ===")
    
    cursor.execute('''
    SELECT page_number, sura_number, ayah_number, word_position, 
           arabic_word, min_x, max_x, min_y, max_y
    FROM word_bounds 
    ORDER BY page_number, sura_number, ayah_number, word_position 
    LIMIT 10
    ''')
    
    words = cursor.fetchall()
    
    print(f"{'Page':<4} {'Sura':<4} {'Ayah':<4} {'Pos':<3} {'Word':<15} {'X':<9} {'Y':<9}")
    print("-" * 65)
    
    for word in words:
        x_range = f"{word['min_x']}-{word['max_x']}"
        y_range = f"{word['min_y']}-{word['max_y']}"
        print(f"{word['page_number']:<4} {word['sura_number']:<4} {word['ayah_number']:<4} "
              f"{word['word_position']:<3} {word['arabic_word']:<15} {x_range:<9} {y_range:<9}")

def show_page_stats(cursor, page_num):
    """Show statistics for a specific page."""
    print(f"\n=== PAGE {page_num} STATISTICS ===")
    
    # Word count on page
    cursor.execute('SELECT COUNT(*) FROM word_bounds WHERE page_number = ?', (page_num,))
    word_count = cursor.fetchone()[0]
    
    # Glyph count on page
    cursor.execute('SELECT COUNT(*) FROM glyph_bounds WHERE page_number = ?', (page_num,))
    glyph_count = cursor.fetchone()[0]
    
    # Lines on page
    cursor.execute('SELECT COUNT(DISTINCT line_number) FROM glyph_bounds WHERE page_number = ?', (page_num,))
    line_count = cursor.fetchone()[0]
    
    # Suras on page
    cursor.execute('SELECT COUNT(DISTINCT sura_number) FROM word_bounds WHERE page_number = ?', (page_num,))
    sura_count = cursor.fetchone()[0]
    
    print(f"Words: {word_count}")
    print(f"Glyphs: {glyph_count}")
    print(f"Lines: {line_count}")
    print(f"Suras: {sura_count}")

def find_word_positions(cursor, arabic_word):
    """Find all positions of a specific Arabic word."""
    print(f"\n=== POSITIONS OF WORD: {arabic_word} ===")
    
    cursor.execute('''
    SELECT page_number, sura_number, ayah_number, word_position, 
           min_x, max_x, min_y, max_y
    FROM word_bounds 
    WHERE arabic_word = ?
    ORDER BY page_number, sura_number, ayah_number, word_position
    ''', (arabic_word,))
    
    positions = cursor.fetchall()
    
    if not positions:
        print("No instances found.")
        return
    
    print(f"Found {len(positions)} instance(s):")
    print(f"{'Page':<4} {'Sura':<4} {'Ayah':<4} {'Pos':<3} {'Bounds (x, y)':<20}")
    print("-" * 40)
    
    for pos in positions:
        bounds = f"({pos['min_x']},{pos['min_y']})-({pos['max_x']},{pos['max_y']})"
        print(f"{pos['page_number']:<4} {pos['sura_number']:<4} {pos['ayah_number']:<4} "
              f"{pos['word_position']:<3} {bounds:<20}")

def show_example_queries(cursor):
    """Show example SQL queries."""
    print("\n=== EXAMPLE QUERIES ===")
    
    examples = [
        ("Get all words in Sura 1", 
         "SELECT * FROM word_bounds WHERE sura_number = 1"),
        
        ("Get all words on page 2", 
         "SELECT * FROM word_bounds WHERE page_number = 2"),
        
        ("Find words in a specific rectangular area", 
         "SELECT * FROM word_bounds WHERE min_x >= 100 AND max_x <= 500 AND min_y >= 50 AND max_y <= 200"),
        
        ("Count words per ayah in Sura 1", 
         "SELECT ayah_number, COUNT(*) as word_count FROM word_bounds WHERE sura_number = 1 GROUP BY ayah_number"),
        
        ("Get all glyphs on a specific line", 
         "SELECT * FROM glyph_bounds WHERE page_number = 2 AND line_number = 1 ORDER BY line_position"),
    ]
    
    for title, query in examples:
        print(f"\n{title}:")
        print(f"  {query}")

def main():
    """Main function to explore the database."""
    print("Quran Word Position Bounds Database Explorer")
    print("=" * 50)
    
    # Connect to database
    conn = connect_db()
    if not conn:
        print("Failed to connect to database.")
        sys.exit(1)
    
    cursor = conn.cursor()
    
    try:
        # Show schema
        show_schema(cursor)
        
        # Show summary statistics
        show_summary_stats(cursor)
        
        # Show sample data
        show_sample_data(cursor)
        
        # Show page statistics for page 2
        show_page_stats(cursor, 2)
        
        # Find specific word (using first word from sample)
        cursor.execute('SELECT arabic_word FROM word_bounds LIMIT 1')
        first_word = cursor.fetchone()[0]
        find_word_positions(cursor, first_word)
        
        # Show example queries
        show_example_queries(cursor)
        
        print(f"\n=== DATABASE FILE ===")
        print("Database file: quran_word_bounds.sqlite")
        print("You can query this database using any SQLite tool or programming language with SQLite support.")
        
    except Exception as e:
        print(f"Error during exploration: {e}")
        
    finally:
        conn.close()

if __name__ == '__main__':
    main()
