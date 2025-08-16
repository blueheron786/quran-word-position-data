# Quran Word Position Data

This repository contains word-by-word position bounds data for Quran pages, extracted from the [quran.com-images](https://github.com/quran/quran.com-images) pipeline.

## What's Included

### Generated Data
- **`quran_word_bounds.sqlite`** - SQLite database containing word and glyph position bounds
- **`*.png`** - Generated Quran page images (pages 2-5 at 1300px width)
- **Sample Data**: Currently contains data for pages 2-5 covering Sura 2 (Al-Baqarah)

### Database Schema

#### `word_bounds` Table
Contains word-level position data:
- `page_number` - Quran page number (1-604)
- `sura_number` - Sura (chapter) number 
- `ayah_number` - Ayah (verse) number within the sura
- `word_position` - Word position within the ayah
- `arabic_word` - The Arabic text of the word
- `glyph_code` - Unique identifier for the glyph
- `img_width` - Image width (1300px in this dataset)
- `min_x, max_x, min_y, max_y` - Bounding box coordinates
- `line_number` - Line number on the page
- `line_position` - Position within the line

#### `glyph_bounds` Table
Contains all glyph-level position data (includes non-word elements):
- Similar structure to `word_bounds` but includes all page elements
- `line_type` - Type of line (sura-header, bismillah, ayah-text)

## Usage Examples

### Python
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('quran_word_bounds.sqlite')
cursor = conn.cursor()

# Get all words on page 2
cursor.execute('SELECT * FROM word_bounds WHERE page_number = 2')
words = cursor.fetchall()

# Find words in a specific area
cursor.execute('''
    SELECT arabic_word, min_x, max_x, min_y, max_y 
    FROM word_bounds 
    WHERE min_x >= 100 AND max_x <= 500 
    AND page_number = 2
''')
```

### Exploration Script
Run the included exploration script to see sample data:
```bash
python explore_database.py
```

## Statistics
- **Word bounds**: 421 records
- **Glyph bounds**: 476 records  
- **Pages**: 4 (pages 2-5)
- **Suras covered**: 1 (Sura 2 - Al-Baqarah, beginning)
- **Image width**: 1300 pixels

## How It Was Generated

1. **Source**: Used the [quran.com-images](https://github.com/quran/quran.com-images) pipeline
2. **Pipeline**: Perl-based image generation with MySQL database for bounds
3. **Extraction**: Custom Python script to convert MySQL data to SQLite
4. **Images**: Generated using authentic Quran Complex fonts

### Pipeline Components
- **Docker**: Used Docker containers for MySQL and Perl environment
- **Font**: King Fahd Quran Complex fonts (QCF_BSML.TTF)
- **Database**: MySQL for generation, SQLite for distribution

## Extending the Dataset

To generate more pages:

1. Start the Docker services:
```bash
cd quran.com-images
docker-compose up -d
```

2. Generate additional pages:
```bash
docker-compose run gen /app/script/generate.pl --output ./output/ --width 1300 --pages 6..10
```

3. Extract to SQLite:
```bash
python extract_bounds_to_sqlite.py
```

## Use Cases

This data enables:
- **Word highlighting** in Quran reading applications
- **Interactive Quran interfaces** with clickable words
- **Search and navigation** by position
- **Text layout analysis** and typography research
- **Accessibility features** for screen readers
- **Educational tools** for Arabic language learning

## File Structure

```
├── README.md                      # This file
├── quran_word_bounds.sqlite       # Main database file
├── *.png                         # Generated page images (2-5)
├── explore_database.py           # Database exploration script
├── extract_bounds_to_sqlite.py   # Extraction script
└── quran.com-images/             # Source pipeline (cloned)
```

## Credits

- **Fonts**: King Fahd Quran Complex, Saudi Arabia
- **Pipeline**: [quran.com-images](https://github.com/quran/quran.com-images) project
- **Original data**: From the Quran text and traditional Madani script

## License

The code in this repository is open source. The Quran text and fonts belong to the King Fahd Quran Complex in Saudi Arabia.