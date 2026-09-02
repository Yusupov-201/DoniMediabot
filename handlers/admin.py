from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMIN_ID
from database import add_movie
from keyboards.admin import admin_menu


router = Router()


class AddMovie(StatesGroup):
    code = State()
    title = State()
    genre = State()
    year = State()
    rating = State()
    description = State()
    video = State()


@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Siz admin emassiz.")
        return

    await state.clear()

    await message.answer(
        "👑 <b>DONIMEDIA ADMIN PANEL</b>\n\n"
        "Kerakli bo‘limni tanlang:",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )


@router.message(F.text == "➕ Kino qo'shish")
async def add_movie_start(message: Message, state: FSMContext):

    if message.from_user.id != ADMIN_ID:
        return

    await state.set_state(AddMovie.code)

    await message.answer(
        "➕ <b>Yangi kino qo‘shish</b>\n\n"
        "🔢 Kino kodini yuboring:\n\n"
        "Masalan: <code>125</code>",
        parse_mode="HTML"
    )


@router.message(AddMovie.code)
async def movie_code(message: Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer("❌ Kod faqat raqamlardan iborat bo‘lsin.")
        return

    await state.update_data(code=message.text)

    await state.set_state(AddMovie.title)

    await message.answer("🎬 Kino nomini yuboring:")


@router.message(AddMovie.title)
async def movie_title(message: Message, state: FSMContext):

    await state.update_data(title=message.text)

    await state.set_state(AddMovie.genre)

    await message.answer(
        "🎭 Kino janrini yuboring:\n\n"
        "Masalan: Jangari, Komediya"
    )


@router.message(AddMovie.genre)
async def movie_genre(message: Message, state: FSMContext):

    await state.update_data(genre=message.text)

    await state.set_state(AddMovie.year)

    await message.answer(
        "📅 Kino yilini yuboring:\n\n"
        "Masalan: 2026"
    )


@router.message(AddMovie.year)
async def movie_year(message: Message, state: FSMContext):

    if not message.text or not message.text.isdigit():
        await message.answer("❌ Yilni raqam bilan kiriting.")
        return

    await state.update_data(year=int(message.text))

    await state.set_state(AddMovie.rating)

    await message.answer(
        "⭐ Kino reytingini yuboring:\n\n"
        "Masalan: 8.5"
    )


@router.message(AddMovie.rating)
async def movie_rating(message: Message, state: FSMContext):

    try:
        rating = float(message.text)
    except (ValueError, TypeError):
        await message.answer(
            "❌ Reyting noto‘g‘ri.\n"
            "Masalan: 8.5"
        )
        return

    await state.update_data(rating=rating)

    await state.set_state(AddMovie.description)

    await message.answer(
        "📝 Kino haqida qisqa tavsif yuboring:"
    )


@router.message(AddMovie.description)
async def movie_description(message: Message, state: FSMContext):

    await state.update_data(description=message.text)

    await state.set_state(AddMovie.video)

    await message.answer(
        "🎥 Endi kino videosini yuboring.\n\n"
        "Video sifatida yuborishingiz mumkin."
    )


@router.message(AddMovie.video, F.video)
async def movie_video(message: Message, state: FSMContext):

    data = await state.get_data()

    await state.update_data(
        file_id=message.video.file_id
    )

    data = await state.get_data()

    try:
        await add_movie(
            code=data["code"],
            title=data["title"],
            description=data["description"],
            genre=data["genre"],
            year=data["year"],
            rating=data["rating"],
            file_id=data["file_id"]
        )

    except Exception as e:

        print(f"Kino saqlash xatosi: {e}")

        await message.answer(
            "❌ Kino saqlashda xatolik yuz berdi.\n\n"
            "Kod allaqachon mavjud bo‘lishi mumkin."
        )

        await state.clear()
        return

    await message.answer(
        "✅ <b>KINO SAQLANDI!</b>\n\n"
        f"🎬 <b>{data['title']}</b>\n"
        f"🔢 Kod: <code>{data['code']}</code>\n"
        f"🎭 Janr: {data['genre']}\n"
        f"📅 Yil: {data['year']}\n"
        f"⭐ Reyting: {data['rating']}\n\n"
        "🍿 Endi foydalanuvchilar kino kodini yuborib "
        "kinoni olishlari mumkin.",
        reply_markup=admin_menu(),
        parse_mode="HTML"
    )

    await state.clear()


@router.message(AddMovie.video)
async def wrong_video(message: Message):

    await message.answer(
        "❌ Iltimos, kino faylini <b>video</b> ko‘rinishida yuboring.",
        parse_mode="HTML"
    )


@router.message(F.text == "📊 Statistika")
async def statistics(message: Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📊 <b>DONIMEDIA STATISTIKA</b>\n\n"
        "Bu bo‘limni keyingi bosqichda to‘liq qilamiz.",
        parse_mode="HTML"
    )