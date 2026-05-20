"""
Claude Memory Backup — دیدیموند PM
====================================
هر روز اتوماتیک اجرا میشه و:
1. فایل‌های مکالمه امروز رو از پوشه conversations می‌خونه
2. با Gemini API خلاصه می‌سازه (رایگان)
3. نتیجه رو به Google Doc اضافه می‌کنه
"""

import json
import os
import sys
import datetime
import urllib.request
from google.oauth2 import service_account
from googleapiclient.discovery import build

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default = {
            "gemini_api_key": "YOUR_GEMINI_API_KEY",
            "google_credentials_json": "credentials.json",
            "google_doc_id": "YOUR_GOOGLE_DOC_ID",
            "conversations_folder": "conversations"
        }
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)
        print("✅ config.json ساخته شد — مقادیر رو پر کن.")
        sys.exit(0)
    with open(CONFIG_FILE, encoding="utf-8") as f:
        return json.load(f)

def read_conversations(folder):
    today = datetime.date.today().isoformat()
    texts = []
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"📁 پوشه '{folder}' ساخته شد.")
        return ""
    for fname in sorted(os.listdir(folder)):
        if fname.startswith(today) and fname.endswith(".txt"):
            path = os.path.join(folder, fname)
            with open(path, encoding="utf-8") as f:
                texts.append(f"=== {fname} ===\n{f.read()}")
    return "\n\n".join(texts)

def summarize_gemini(conversations, api_key):
    prompt = f"""تو دستیار یه مدیر محصول هستی. متن زیر مکالمات امروز اون با Claude هست.

یه خلاصه فشرده بنویس شامل:
1. تصمیمات کلیدی
2. وظایف باز (با ☐)
3. نکات مهم برای Claude بعدی
4. آپدیت‌های محصول یا تیم

فرمت: Markdown فارسی، فشرده.

مکالمات:
{conversations}"""

    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}]
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result["candidates"][0]["content"]["parts"][0]["text"]

def append_to_google_doc(doc_id, credentials_path, text):
    creds = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=["https://www.googleapis.com/auth/documents"]
    )
    service = build("docs", "v1", credentials=creds)
    today = datetime.date.today().strftime("%Y/%m/%d")
    content = f"\n\n{'='*50}\n📅 بک‌آپ {today}\n{'='*50}\n\n{text}\n"
    doc = service.documents().get(documentId=doc_id).execute()
    end_index = doc["body"]["content"][-1]["endIndex"] - 1
    service.documents().batchUpdate(
        documentId=doc_id,
        body={"requests": [{"insertText": {"location": {"index": end_index}, "text": content}}]}
    ).execute()

def main():
    print("🔄 Claude Memory Backup شروع شد...")
    config = load_config()
    conversations = read_conversations(config["conversations_folder"])
    if not conversations.strip():
        print("⚠️  هیچ مکالمه‌ای برای امروز پیدا نشد.")
        print(f"   فایل‌ها رو با فرمت {datetime.date.today().isoformat()}_topic.txt در پوشه conversations بذار.")
        return
    print("🤖 در حال خلاصه‌سازی با Gemini...")
    summary = summarize_gemini(conversations, config["gemini_api_key"])
    print("✅ خلاصه آماده شد.")
    print("☁️  در حال آپلود به Google Drive...")
    append_to_google_doc(config["google_doc_id"], config["google_credentials_json"], summary)
    print("✅ بک‌آپ با موفقیت ذخیره شد!")
    print(f"   https://docs.google.com/document/d/{config['google_doc_id']}")

if __name__ == "__main__":
    main()
