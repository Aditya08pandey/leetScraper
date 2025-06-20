import time, random
from tqdm import tqdm

from config import *
from db import init_db, save_question
from fetch_slugs import get_all_slugs
from fetch_content import fetch_content
from rephrase import rephrase

def main():
    init_db()
    all_qs = get_all_slugs()
    OFFSET = int(os.getenv("OFFSET", 0))
    total = min(TOTAL_TO_FETCH, len(all_qs) - OFFSET)
    print(f"Found {len(all_qs)} problems; processing from {OFFSET} to {OFFSET + total - 1}.")


    for i in range(OFFSET, OFFSET + total, BATCH_SIZE):
        batch = all_qs[i:i + BATCH_SIZE]
        print(f"\nProcessing batch {i}–{i + len(batch) - 1}")


        for q in tqdm(batch, desc="Questions"):
            slug = q["slug"]
            title = q["title"]
            diff  = q["difficulty"]

            try:
                html, tags = fetch_content(slug)
                content_md = rephrase(title, html) if REPHRASE_ENABLED else html
                save_question({
                    "slug":       slug,
                    "title":      title,
                    "difficulty": diff,
                    "tags":       tags,
                    "content_md": content_md,
                    "content_html": html
                })
            except Exception as e:
                print(f"Error with {slug}: {e}")

            time.sleep(random.uniform(SLEEP_REQ_MIN, SLEEP_REQ_MAX))

        time.sleep(random.uniform(SLEEP_BATCH_MIN, SLEEP_BATCH_MAX))

    print("\n✅ Done! Check questions.db for your data.")

if __name__ == "__main__":
    main()
