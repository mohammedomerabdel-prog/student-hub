import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# رابط الأخبار العاجلة والسبق الإعلامي (Google News RSS - اللغة العربية)
RSS_URL = "https://news.google.com/rss?hl=ar&gl=SA&ceid=SA:ar"

def fetch_latest_news():
    try:
        # جلب البيانات من المصدر
        req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()

        # تحليل بيانات XML
        root = ET.fromstring(xml_data)
        news_items = []

        # استخراج أول 10 أخبار عاجلة
        for item in root.findall('./channel/item')[:10]:
            title = item.find('title').text if item.find('title') is not None else 'بدون عنوان'
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''

            news_items.append({
                "title": title,
                "link": link,
                "published_at": pub_date
            })

        # تجهيز الهيكل النهائي للملف
        data_to_save = {
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": "السبق الإعلامي وآخر الأخبار",
            "articles": news_items
        }

        # حفظ البيانات في ملف json
        file_name = "latest_news.json"
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data_to_save, file, ensure_ascii=False, indent=4)

        print(f"تم بنجاح جلب الأخبار وحفظها في الملف: {file_name}")

    except Exception as e:
        print(f"حدث خطأ أثناء جلب الأخبار: {e}")

if __name__ == "__main__":
    fetch_latest_news()
  
