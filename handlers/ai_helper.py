from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from services.ai_helper import ask_ai


router = Router()


class AIChat(StatesGroup):
    waiting_message = State()


@router.message(F.text == "🤖 AI yordamchi")
async def ai_start(message: Message, state: FSMContext):

    await state.set_state(AIChat.waiting_message)

    await message.answer(
        "🤖 <b>DONIMEDIA AI YORDAMCHI</b>\n\n"
        "Savolingizni yozing 🎬\n\n"
        "Masalan:\n"
        "• Menga komediya kino tavsiya qil\n"
        "• Fantastik kino kerak\n"
        "• DONIMEDIA qanday ishlaydi?\n\n"
        "❌ Chiqish: /cancel",
        parse_mode="HTML"
    )


@router.message(AIChat.waiting_message)
async def ai_chat(message: Message, state: FSMContext):

    if not message.text:
        await message.answer("✍️ Iltimos, matn yozing.")
        return

    text = message.text.strip()

    if text.lower() == "/cancel":
        await state.clear()
        await message.answer("🤖 AI yordamchi yopildi.")
        return

    await message.answer("🤖 Javob tayyorlanmoqda...")

    try:
        answer = await ask_ai(text)

        await message.answer(
            f"🤖 <b>DONIMEDIA AI</b>\n\n{answer}",
            parse_mode="HTML"
        )

    except Exception as e:

        print(f"❌ AI ERROR: {type(e).__name__}: {e}")

        await message.answer(
            "❌ AI ishlashida xatolik yuz berdi.\n"
            "Terminaldagi AI ERROR ni tekshiring."
        )