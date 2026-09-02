from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    get_movie,
    increase_views,
    add_history,
    add_favorite,
    remove_favorite,
    is_favorite
)

from services.subscription import check_subscription
from config import CHANNEL_ID


router = Router()


def subscription_keyboard():

    username = CHANNEL_ID.replace("@", "")

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url=f"https://t.me/{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Obunani tekshirish",
                    callback_data="check_subscription"
                )
            ]
        ]
    )


def movie_buttons(movie_id, favorite=False):

    favorite_text = (
        "💔 Sevimlidan olib tashlash"
        if favorite
        else
        "❤️ Sevimlilarga qo‘shish"
    )

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=favorite_text,
                    callback_data=f"favorite:{movie_id}"
                )
            ]
        ]
    )


@router.message(F.text == "🎬 Kino kodlari")
async def movie_code_start(message: Message):

    await message.answer(
        "🎬 <b>Kino kodlari</b>\n\n"
        "🔢 Kino kodini yuboring.\n\n"
        "Masalan: <code>125</code>",
        parse_mode="HTML"
    )


@router.message(F.text.regexp(r"^\d+$"))
async def movie_code_handler(message: Message, bot):

    code = message.text.strip()

    # 🔐 Majburiy obuna
    subscribed = await check_subscription(
        bot,
        message.from_user.id
    )

    if not subscribed:

        await message.answer(
            "🔐 <b>DONIMEDIA</b>\n\n"
            "Kino olishdan oldin kanalimizga "
            "obuna bo‘ling.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # 🔎 Kod bo‘yicha kino
    movie = await get_movie(code)

    if not movie:

        await message.answer(
            "❌ <b>Kino topilmadi!</b>\n\n"
            "🔢 Kodni tekshirib qayta yuboring.",
            parse_mode="HTML"
        )

        return

    # 👀 Ko‘rish
    await increase_views(movie["id"])

    # 🕐 Tarix
    await add_history(
        message.from_user.id,
        movie["id"]
    )

    favorite = await is_favorite(
        message.from_user.id,
        movie["id"]
    )

    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📝 {movie['description'] or 'Tavsif mavjud emas'}\n\n"
        f"🎭 Janr: {movie['genre'] or 'Nomaʼlum'}\n"
        f"📅 Yil: {movie['year'] or 'Nomaʼlum'}\n"
        f"⭐ Reyting: {movie['rating']}\n"
        f"👀 Ko‘rishlar: {movie['views'] + 1}\n\n"
        f"🔢 Kod: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    await message.answer_video(
        video=movie["file_id"],
        caption=caption,
        reply_markup=movie_buttons(
            movie["id"],
            favorite
        ),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("favorite:"))
async def favorite_handler(
    callback: CallbackQuery
):

    movie_id = int(
        callback.data.split(":")[1]
    )

    user_id = callback.from_user.id

    favorite = await is_favorite(
        user_id,
        movie_id
    )

    if favorite:

        await remove_favorite(
            user_id,
            movie_id
        )

        await callback.answer(
            "💔 Sevimlilardan olib tashlandi"
        )

        await callback.message.edit_reply_markup(
            reply_markup=movie_buttons(
                movie_id,
                False
            )
        )

    else:

        await add_favorite(
            user_id,
            movie_id
        )

        await callback.answer(
            "❤️ Sevimlilarga qo‘shildi!"
        )

        await callback.message.edit_reply_markup(
            reply_markup=movie_buttons(
                movie_id,
                True
            )
        )