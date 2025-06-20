import cohere
from config import COHERE_API_KEY, COHERE_MODEL

client = cohere.Client(COHERE_API_KEY)

def rephrase(title, html):
    prompt = f"""You are a precise coding-problem rewriter.
Keep the title exactly as "{title}".
Always use the word "array" (never "list").
Do not change logic, I/O format, constraints, or examples—only reword phrasing.
Output ONLY Markdown with sections:

## {title}

### Problem
(Your rephrased problem statement here)

### Input
(Describe input format)

### Output
(Describe output format)

### Constraints
(List constraints)

### Example
(Show the same example, reworded slightly if needed.)

--- Original Problem (HTML content) ---
{html}
"""

    try:
        response = client.generate(
            model=COHERE_MODEL,
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000,
            p=0.75,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        return response.generations[0].text.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
