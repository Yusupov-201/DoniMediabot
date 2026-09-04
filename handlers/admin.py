from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMIN_ID
from database import add_movie
from keyboards.admin import admin_menu


router = Router()


# =========================
# ADMIN TEKSHIRISH
# =========================

def is_admin(user_id: int) -> bool:
    return int(user_id) == 8124227367


# =========================
# KINO QO'SHISH STATES
# =========================

class AddMovie(StatesGroup):
    code = State()
    title = State()
    genre = State()
    year = State()
    rating = State()
    description = State()
    video = State()


# =========================
# /ADMIN
# =========================

@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):

    print(
        f"ADMIN CHECK: "
        f"user_id={message.from_user.id} | "
        f"ADMIN_ID={ADMIN_ID}"
    )

    if message.from_user.id != ADMIN_ID:
        await message.answer(
            f"❌ Siz admin emassiz.\n\n"
            f"ID: <code>{message.from_user.id}</code>",
            parse_mode="HTML"
        )
        return

    await state.clear()

    await message.answer(
        "👑 <b>DONIMEDIA ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )


# =========================
# KINO QO'SHISH
# =========================

@router.message(F.text == "➕ Kino qo'shish")
async def add_movie_start(
    message: Message,
    state: FSMContext
):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Siz admin emassiz.")
        return

    await state.clear()
    await state.set_state(AddMovie.code)

    await message.answer(
        "➕ <b>Yangi kino qo‘shish</b>\n\n"
        "Kino kodini yuboring.\n\n"
        "Masalan: <code>125</code>",
        parse_mode="HTML"
    )

# =========================
# KINO KODI
# =========================

@router.message(AddMovie.code)
async def movie_code(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    if not message.text or not message.text.strip().isdigit():
        await message.answer(
            "❌ Kod faqat raqamlardan iborat bo‘lishi kerak.\n"
            "Masalan: <code>125</code>",
            parse_mode="HTML"
        )
        return

    await state.update_data(
        code=int(message.text.strip())
    )

    await state.set_state(AddMovie.title)

    await message.answer(
        "🎬 Kino nomini yuboring."
    )


# =========================
# KINO NOMI
# =========================

@router.message(AddMovie.title)
async def movie_title(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    if not message.text or not message.text.strip():
        await message.answer("❌ Kino nomini yuboring.")
        return

    await state.update_data(
        title=message.text.strip()
    )

    await state.set_state(AddMovie.genre)

    await message.answer(
        "🎭 Kino janrini yuboring.\n\n"
        "Masalan: Komediya, Jangari, Drama"
    )


# =========================
# JANR
# =========================

@router.message(AddMovie.genre)
async def movie_genre(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    if not message.text or not message.text.strip():
        await message.answer("❌ Janrni yuboring.")
        return

    await state.update_data(
        genre=message.text.strip()
    )

    await state.set_state(AddMovie.year)

    await message.answer(
        "📅 Kino yilini yuboring.\n\n"
        "Masalan: <code>2026</code>",
        parse_mode="HTML"
    )


# =========================
# YIL
# =========================

@router.message(AddMovie.year)
async def movie_year(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    if not message.text or not message.text.strip().isdigit():
        await message.answer(
            "❌ Yil faqat raqam bo‘lishi kerak.\n"
            "Masalan: <code>2026</code>",
            parse_mode="HTML"
        )
        return

    await state.update_data(
        year=int(message.text.strip())
    )

    await state.set_state(AddMovie.rating)

    await message.answer(
        "⭐ Kino reytingini yuboring.\n\n"
        "Masalan: <code>8.5</code>",
        parse_mode="HTML"
    )


# =========================
# REYTING
# =========================

@router.message(AddMovie.rating)
async def movie_rating(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    if not message.text:
        await message.answer("❌ Reytingni yuboring.")
        return

    try:
        rating = float(
            message.text.strip().replace(",", ".")
        )
    except ValueError:
        await message.answer(
            "❌ Reyting noto‘g‘ri.\n"
            "Masalan: <code>8.5</code>",
            parse_mode="HTML"
        )
        return

    if rating < 0 or rating > 10:
        await message.answer(
            "❌ Reyting 0 dan 10 gacha bo‘lishi kerak."
        )
        return

    await state.update_data(
        rating=rating
    )

    await state.set_state(AddMovie.description)

    await message.answer(
        "📝 Kino haqida qisqa tavsif yuboring."
    )


# =========================
# TAVSIF
# =========================

@router.message(AddMovie.description)
async def movie_description(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    if not message.text or not message.text.strip():
        await message.answer(
            "❌ Tavsifni yuboring."
        )
        return

    await state.update_data(
        description=message.text.strip()
    )

    await state.set_state(AddMovie.video)

    await message.answer(
        "🎥 Endi kino videosini yuboring.\n\n"
        "Videoni Telegramga <b>Video</b> sifatida yuboring.",
        parse_mode="HTML"
    )


# =========================
# VIDEO
# =========================

@router.message(AddMovie.video, F.video)
async def movie_video(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    data = await state.get_data()

    try:
        await add_movie(
            code=data["code"],
            title=data["title"],
            description=data["description"],
            genre=data["genre"],
            year=data["year"],
            rating=data["rating"],
            file_id=message.video.file_id
        )

    except Exception as e:

        print(f"Kino saqlash xatosi: {e}")

        await message.answer(
            "❌ <b>Kino saqlanmadi!</b>\n\n"
            f"Xatolik: <code>{e}</code>",
            parse_mode="HTML"
        )

        await state.clear()
        return

    await message.answer(
        "✅ <b>KINO MUVAFFAQIYATLI SAQLANDI!</b>\n\n"
        f"🎬 Nomi: <b>{data['title']}</b>\n"
        f"🔢 Kod: <code>{data['code']}</code>\n"
        f"🎭 Janr: {data['genre']}\n"
        f"📅 Yil: {data['year']}\n"
        f"⭐ Reyting: {data['rating']}\n\n"
        "👥 Foydalanuvchilar kino kodini yuborib "
        "kinoni olishlari mumkin.",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

    await state.clear()


# =========================
# VIDEO EMAS
# =========================

@router.message(AddMovie.video)
async def wrong_video(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    await message.answer(
        "❌ Iltimos, kinoni <b>video</b> sifatida yuboring.",
        parse_mode="HTML"
    )


# =========================
# STATISTIKA
# =========================

@router.message(F.text == "📊 Statistika")
async def statistics(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    await state.clear()

    await message.answer(
        "📊 <b>DONIMEDIA STATISTIKA</b>\n\n"
        "Statistika funksiyasi mavjud.",
        parse_mode="HTML"
    )


# =========================
# BOSH MENYU
# =========================

@router.message(F.text == "⬅️ Bosh menyu")
async def admin_back(
    message: Message,
    state: FSMContext
):

    if not is_admin(message.from_user.id):
        return

    await state.clear()

    await message.answer(
        "🏠 Bosh menyuga qaytdingiz."
    )