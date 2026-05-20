# Claude Memory Backup

سیستم بک‌آپ خودکار مکالمات Claude برای PM دیدیموند.

## روتین روزانه

1. مکالمات مهم امروز رو copy کن
2. توی پوشه `conversations/` با فرمت `YYYY-MM-DD_topic.txt` ذخیره کن
3. push کن به GitHub
4. هر شب ساعت ۹ ایران، خلاصه اتوماتیک به `memory.md` اضافه میشه

## ستاپ اولیه

1. برو Settings > Secrets > Actions
2. یه secret جدید بساز: `GEMINI_API_KEY`
3. مقدارش رو از Google AI Studio بگیر
