import sqlite3, json
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
  CREATE TABLE IF NOT EXISTS questionAditya (
    slug         TEXT PRIMARY KEY,
    title        TEXT,
    difficulty   TEXT,
    tags         TEXT,       -- JSON array of strings
    content_md   TEXT,       -- rephrased Markdown
    content_html TEXT,       -- original HTML content from LeetCode
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
""")
    conn.commit()
    conn.close()

def save_question(q):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
  INSERT OR IGNORE INTO questionAditya (slug, title, difficulty, tags, content_md, content_html)
  VALUES (?, ?, ?, ?, ?, ?);
""", (
  q['slug'],
  q['title'],
  q['difficulty'],
  json.dumps(q['tags']),
  q['content_md'],
  q['content_html']
))

    conn.commit()
    conn.close()
