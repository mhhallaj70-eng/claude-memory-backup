import os
import json
import datetime
import urllib.request

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
CONVERSATIONS_FOLDER = "conversations"
MEMORY_FILE = "memory.md"

def read_conversations():
    today = datetime.date.today().isoformat()
    texts = []
    for fname in sorted(os.listdir(CONVERSATIONS_FOLDER)):
        if fname.startswith(today) and fname.endswith(".txt"):
            with open(os.path.join(CONVERSATIONS_FOLDER, fname), encoding="utf-8") as f:
                texts.append(f"=== {fname} ===\n{f.read()}")
    return "\n\n".join(texts)

def summarize(conversations):
    prompt = f"""تو دستیار یه مدیر محصول هستی. متن زیر مکالمات امروز اون با Claude هست.

یه خلاصه فشرده بنویس شامل:
1. **تصمیمات کلیدی**
2. **وظایف باز** (با چک‌باکس)
3. **نکات مهم برای Claude بعدی**
4. **آپدیت‌های محصول یا تیم**

فرمت: Markdown فارسی، فشرده.

مکالمات:
{conversations}"""

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["candidates"][0]["content"]["parts"][0]["text"]

def append_to_memory(summary):
    today = datetime.date.today().strftime("%Y/%m/%d")
    entry = f"\n\n---\n\n## {today}\n\n{summary}\n"
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def main():
    print("شروع بک‌آپ...")
    conversations = read_conversations()
    if not conversations.strip():
        print("هیچ مکالمه‌ای برای امروز پیدا نشد.")
        return
    print("در حال خلاصه‌سازی با Gemini...")
    summary = summarize(conversations)
    print("خلاصه آماده شد.")
    append_to_memory(summary)
    print("memory.md آپدیت شد.")

if __name__ == "__main__":
    main()
