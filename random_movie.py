from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    get_random_movie,
    increase_views,
    add_history
)


router = Router()


@router.message(F.text == "🎯 Tasodifiy kino")
async def random_movie(message: Message):

    movie = await get_random_movie()

    if not movie:
        await message.answer(
            "😔 Hozircha bazada kino mavjud emas."
        )
        return

    # 👀 Ko‘rishlar
    await increase_views(movie["id"])

    # 🕐 Tarix
    await add_history(
        message.from_user.id,
        movie["id"]
    )

    caption = (
        f"🎯 <b>SIZ UCHUN TASODIFIY KINO</b>\n\n"
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📝 {movie['description'] or 'Tavsif mavjud emas'}\n\n"
        f"🎭 Janr: {movie['genre'] or 'Nomaʼlum'}\n"
        f"📅 Yil: {movie['year'] or 'Nomaʼlum'}\n"
        f"⭐ Reyting: {movie['rating']}\n"
        f"👀 Ko‘rishlar: {movie['views'] + 1}\n\n"
        f"🔢 Kod: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Yana bitta",
                    callback_data="random_again"
                )
            ]
        ]
    )

    await message.answer_video(
        video=movie["file_id"],
        caption=caption,
        reply_markup=keyboard,
        parse_mode="HTML"
    )


@router.callback_query(F.data == "random_again")
async def random_again(callback):

    movie = await get_random_movie()

    if not movie:
        await callback.answer(
            "❌ Kino topilmadi!",
            show_alert=True
        )
        return

    await increase_views(movie["id"])

    await add_history(
        callback.from_user.id,
        movie["id"]
    )

    caption = (
        f"🎯 <b>SIZ UCHUN TASODIFIY KINO</b>\n\n"
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📝 {movie['description'] or 'Tavsif mavjud emas'}\n\n"
        f"🎭 Janr: {movie['genre'] or 'Nomaʼlum'}\n"
        f"📅 Yil: {movie['year'] or 'Nomaʼlum'}\n"
        f"⭐ Reyting: {movie['rating']}\n"
        f"👀 Ko‘rishlar: {movie['views'] + 1}\n\n"
        f"🔢 Kod: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎯 Yana bitta",
                    callback_data="random_again"
                )
            ]
        ]
    )

    await callback.message.answer_video(
        video=movie["file_id"],
        caption=caption,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

    await callback.answer()