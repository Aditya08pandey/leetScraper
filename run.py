import time, random
from tqdm import tqdm

from config import *
from db import init_db, save_question
from fetch_slugs import get_all_slugs
from fetch_content import fetch_content
from rephrase import rephrase
from bs4 import BeautifulSoup

def main():
    init_db()
    #--------------------------------------------------------------------------------

    # all_qs = get_all_slugs()
    # OFFSET = int(os.getenv("OFFSET", 0))
    # total = min(TOTAL_TO_FETCH, len(all_qs) - OFFSET)

    #--------------------------------------------------------------------------------

    all_qs = get_all_slugs()
    # sort by question_id
    all_qs.sort(key=lambda q: q["question_id"])

    # drop everything ≤ START_ID (if provided)
    start_id = os.getenv("START_ID")
    if start_id:
        start_id = int(start_id)
        all_qs = [q for q in all_qs if q["question_id"] > start_id]

   # Optionally drop IDs > END_ID
    end_id = os.getenv("END_ID")
    if end_id:
       end_id = int(end_id)
       all_qs = [q for q in all_qs if q["question_id"] <= end_id]

       
    # now just take the first TOTAL_TO_FETCH of the filtered list
    total = min(TOTAL_TO_FETCH, len(all_qs))

    # we always start at index 0
    OFFSET = 0

    #--------------------------------------------------------------------------------
    print(f"Found {len(all_qs)} problems; processing from {OFFSET} to {OFFSET + total - 1}.")


    for i in range(OFFSET, OFFSET + total, BATCH_SIZE):
        batch = all_qs[i:i + BATCH_SIZE]
        print(f"\nProcessing batch {i}–{i + len(batch) - 1}")


        for q in tqdm(batch, desc="Questions"):
            slug = q["slug"]
            title = q["title"]
            diff  = q["difficulty"]
            question_id = q["question_id"]

            try:
                html, tags = fetch_content(slug)
                # Extract plain text from HTML
                soup = BeautifulSoup(html, 'html.parser')
                content_text = soup.get_text(separator='\n', strip=True)
                content_md = rephrase(title, html) if REPHRASE_ENABLED else html
                save_question({
                    "question_id": question_id,
                    "slug":       slug,
                    "title":      title,
                    "difficulty": diff,
                    "tags":       tags,
                    "content_md": content_md,
                    "content_html": html,
                    "content_text": content_text
                })
            except Exception as e:
                print(f"Error with {slug}: {e}")

            time.sleep(random.uniform(SLEEP_REQ_MIN, SLEEP_REQ_MAX))

        time.sleep(random.uniform(SLEEP_BATCH_MIN, SLEEP_BATCH_MAX))

    print("\n✅ Done! Check questions.db for your data.")

if __name__ == "__main__":
    main()
