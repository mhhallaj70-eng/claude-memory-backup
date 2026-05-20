import os
import datetime

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

def append_to_memory(content):
    today = datetime.date.today().strftime("%Y/%m/%d")
    entry = f"\n\n---\n\n## {today}\n\n{content}\n"
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

def main():
    print("شروع بک‌آپ...")
    conversations = read_conversations()
    if not conversations.strip():
        print("هیچ مکالمه‌ای برای امروز پیدا نشد.")
        return
    append_to_memory(conversations)
    print("memory.md آپدیت شد.")

if __name__ == "__main__":
    main()
