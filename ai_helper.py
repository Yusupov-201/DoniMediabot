from google import genai
from config import GEMINI_API_KEY


# =========================================================
# 🤖 GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# =========================================================
# 🎬 DONIMEDIA AI SOZLAMALARI
# =========================================================

SYSTEM_PROMPT = """
Sen DONIMEDIA Telegram botining AI yordamchisisan.

Sening vazifang:
- foydalanuvchiga kino tanlashda yordam berish;
- janr va kayfiyatga qarab kino tavsiya qilish;
- kino haqida umumiy ma'lumot berish;
- DONIMEDIA botidan foydalanishni tushuntirish;
- foydalanuvchining oddiy savollariga javob berish.

Qoidalar:
- Faqat o'zbek tilida javob ber.
- Javoblarni qisqa, tushunarli va foydali qil.
- Do'stona ohangda gapir.
- Agar aniq ma'lumotni bilmasang, uydirma qilma.
- DONIMEDIA bazasida borligi haqida ma'lumot berilmagan kinoni
  bazada bor deb aytma.
"""


# =========================================================
# 🤖 AI SO'ROV
# =========================================================

async def ask_ai(message: str) -> str:

    response = await client.aio.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            SYSTEM_PROMPT,
            f"Foydalanuvchi savoli:\n{message}"
        ]
    )

    if not response.text:
        return "❌ AI javob qaytarmadi."

    return response.text