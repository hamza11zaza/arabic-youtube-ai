
import os
import json
import urllib.request
import urllib.error
from pathlib import Path

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing!")

MODEL = "gemini-3.1-flash-lite"
URL = (
    f"https://generativelanguage.googleapis.com/v1beta/"
    f"models/{MODEL}:generateContent"
)

prompt = """
أنت كاتب محتوى لقناة يوتيوب عربية باللهجة السورية.

أنشئ فكرة فيديو Shorts علمي ممتع وأصلي.

الشروط:
- المدة حوالي 45 إلى 60 ثانية.
- اللهجة السورية الطبيعية.
- بدون موسيقى أو محتوى غير لائق.
- معلومة علمية دقيقة، لا تخترع حقائق.
- ابدأ بجملة تشد الانتباه.
- اكتب نص التعليق الصوتي.
- اقترح 5 مشاهد وصور مناسبة.
- اقترح عنواناً ووصفاً.
- إذا لم تكن متأكداً من معلومة، اذكر أنها تحتاج تحققاً.

أخرج النتيجة باللغة العربية.
"""

payload = {
    "contents": [{
        "parts": [{"text": prompt}]
    }]
}

request = urllib.request.Request(
    URL,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    },
    method="POST"
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    text = data["candidates"][0]["content"]["parts"][0]["text"]

    Path("output").mkdir(exist_ok=True)
    Path("output/script.txt").write_text(text, encoding="utf-8")

    print("SUCCESS: Script generated!")
    print(text)

except urllib.error.HTTPError as error:
    details = error.read().decode("utf-8", errors="replace")
    raise RuntimeError(
        f"Gemini API error {error.code}: {details}"
    )
