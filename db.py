import sqlite3, json
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
  CREATE TABLE IF NOT EXISTS questionAditya (
    question_id  INTEGER PRIMARY KEY,
    slug         TEXT,
    title        TEXT,
    difficulty   TEXT,
    tags         TEXT,       -- JSON array of strings
    content_md   TEXT,       -- rephrased Markdown
    content_html TEXT,       -- original HTML content from LeetCode
    content_text TEXT,       -- plain text content
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
""")
    conn.commit()
    conn.close()

def save_question(q):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
  INSERT OR IGNORE INTO questionAditya (question_id, slug, title, difficulty, tags, content_md, content_html, content_text)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?);
""", (
  q['question_id'],
  q['slug'],
  q['title'],
  q['difficulty'],
  json.dumps(q['tags']),
  q['content_md'],
  q['content_html'],
  q['content_text']
))

    conn.commit()
    conn.close()
