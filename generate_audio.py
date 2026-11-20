
import asyncio
import re
from pathlib import Path
import edge_tts

SCRIPT_FILE = Path("output/script.txt")
AUDIO_FILE = Path("output/voice.mp3")
VOICE = "ar-SY-LaithNeural"

def extract_voiceover(script):
    if not SCRIPT_FILE.exists():
        raise FileNotFoundError("output/script.txt not found")

    text = SCRIPT_FILE.read_text(encoding="utf-8")

    if "نص التعليق الصوتي" in text:
        text = text.split("نص التعليق الصوتي", 1)[1]

        for marker in ["خطة المشاهد", "ملاحظة علمية"]:
            if marker in text:
                text = text.split(marker, 1)[0]

    lines = []

    for line in text.splitlines():
        line = re.sub(r"\(\d+:\d+-\d+:\d+\)", "", line)
        line = re.sub(r"\([^)]*\)", "", line)
        line = line.strip().strip('"“”«»')

        if line and not line.startswith("#"):
            lines.append(line)

    result = " ".join(lines)

    if len(result) < 30:
        raise ValueError("Could not extract enough voiceover text")

    return result

async def main():
    AUDIO_FILE.parent.mkdir(exist_ok=True)

    text = extract_voiceover(SCRIPT_FILE)

    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate="+5%"
    )

    await communicate.save(str(AUDIO_FILE))

    print("SUCCESS: Arabic Syrian voice generated!")
    print(f"Audio saved: {AUDIO_FILE}")

asyncio.run(main())
