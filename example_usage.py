#!/usr/bin/env python3
"""
Example usage of the Quran word position bounds database.
This script demonstrates common use cases for the word bounds data.
"""

import sqlite3

def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect('quran_word_bounds.sqlite')

def highlight_words_in_area(x1, y1, x2, y2, page_num=2):
    """Find all words within a rectangular area on a page."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT arabic_word, min_x, max_x, min_y, max_y, sura_number, ayah_number
        FROM word_bounds 
        WHERE page_number = ?
        AND min_x >= ? AND max_x <= ? 
        AND min_y >= ? AND max_y <= ?
        ORDER BY min_y, min_x
    ''', (page_num, x1, x2, y1, y2))
    
    words = cursor.fetchall()
    conn.close()
    
    print(f"Words in area ({x1},{y1}) to ({x2},{y2}) on page {page_num}:")
    for word in words:
        print(f"  {word[0]} - Sura {word[5]}, Ayah {word[6]} - ({word[1]},{word[3]}) to ({word[2]},{word[4]})")
    
    return words

def get_ayah_words(sura_num, ayah_num):
    """Get all words for a specific ayah with their positions."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT arabic_word, word_position, min_x, max_x, min_y, max_y, page_number
        FROM word_bounds 
        WHERE sura_number = ? AND ayah_number = ?
        ORDER BY word_position
    ''', (sura_num, ayah_num))
    
    words = cursor.fetchall()
    conn.close()
    
    print(f"Sura {sura_num}, Ayah {ayah_num}:")
    for word in words:
        print(f"  {word[1]:2d}. {word[0]} - Page {word[6]} - ({word[2]},{word[4]}) to ({word[3]},{word[5]})")
    
    return words

def find_word_occurrences(arabic_word):
    """Find all occurrences of a specific Arabic word."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT page_number, sura_number, ayah_number, word_position, min_x, max_x, min_y, max_y
        FROM word_bounds 
        WHERE arabic_word = ?
        ORDER BY page_number, sura_number, ayah_number, word_position
    ''', (arabic_word,))
    
    occurrences = cursor.fetchall()
    conn.close()
    
    print(f"Occurrences of '{arabic_word}':")
    for occ in occurrences:
        print(f"  Page {occ[0]}, Sura {occ[1]}, Ayah {occ[2]}, Word {occ[3]} - ({occ[4]},{occ[6]}) to ({occ[5]},{occ[7]})")
    
    return occurrences

def get_page_layout(page_num):
    """Get the layout structure of a page (lines and words)."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Get all glyphs on the page grouped by line
    cursor.execute('''
        SELECT line_number, line_type, COUNT(*) as glyph_count,
               MIN(min_y) as top, MAX(max_y) as bottom,
               MIN(min_x) as left, MAX(max_x) as right
        FROM glyph_bounds 
        WHERE page_number = ?
        GROUP BY line_number, line_type
        ORDER BY line_number
    ''', (page_num,))
    
    lines = cursor.fetchall()
    conn.close()
    
    print(f"Page {page_num} layout:")
    for line in lines:
        print(f"  Line {line[0]} ({line[1]}): {line[2]} glyphs - Y: {line[3]}-{line[4]}, X: {line[5]}-{line[6]}")
    
    return lines

def word_click_handler(x, y, page_num):
    """Simulate a click handler - find which word was clicked."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT arabic_word, sura_number, ayah_number, word_position, min_x, max_x, min_y, max_y
        FROM word_bounds 
        WHERE page_number = ?
        AND ? >= min_x AND ? <= max_x 
        AND ? >= min_y AND ? <= max_y
    ''', (page_num, x, x, y, y))
    
    word = cursor.fetchone()
    conn.close()
    
    if word:
        print(f"Clicked on '{word[0]}' - Sura {word[1]}, Ayah {word[2]}, Word {word[3]}")
        print(f"  Bounds: ({word[4]},{word[6]}) to ({word[5]},{word[7]})")
        return word
    else:
        print(f"No word found at position ({x},{y}) on page {page_num}")
        return None

def main():
    """Demonstrate various use cases."""
    print("Quran Word Bounds Database - Usage Examples")
    print("=" * 50)
    
    # Example 1: Get words in the first ayah we have data for
    print("\n1. Get all words in Sura 2, Ayah 1:")
    get_ayah_words(2, 1)
    
    # Example 2: Find words in a specific area (top-left region of page 2)
    print("\n2. Find words in top-left area of page 2:")
    highlight_words_in_area(0, 0, 600, 400, 2)
    
    # Example 3: Find occurrences of specific word
    print("\n3. Find all occurrences of 'ٱلْكِتَٰبُ' (the Book):")
    find_word_occurrences('ٱلْكِتَٰبُ')
    
    # Example 4: Get page layout
    print("\n4. Page 2 layout structure:")
    get_page_layout(2)
    
    # Example 5: Simulate clicking on a word
    print("\n5. Simulate clicking at position (850, 400) on page 2:")
    word_click_handler(850, 400, 2)
    
    print("\n" + "=" * 50)
    print("These examples show how to use the word bounds data for:")
    print("- Building interactive Quran interfaces")
    print("- Implementing word highlighting")
    print("- Creating search functionality")
    print("- Developing click/touch handlers")
    print("- Analyzing page layout and structure")

if __name__ == '__main__':
    main()
