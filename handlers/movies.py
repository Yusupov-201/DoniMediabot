from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Bot
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

router = Router()


# =========================================================
# 🔐 MAJBURIY OBUNA
# =========================================================

def subscription_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url="https://t.me/buroqli"
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


# =========================================================
# ❤️ KINO TUGMALARI
# =========================================================

def movie_buttons(movie_id: int, favorite: bool = False):

    if favorite:
        favorite_text = "💔 Sevimlidan olib tashlash"
    else:
        favorite_text = "❤️ Sevimlilarga qo‘shish"

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


# =========================================================
# 🎬 KINO KODI
# =========================================================

@router.message(F.text.regexp(r"^\d+$"))
async def movie_code_handler(
    message: Message,
    bot: Bot
):

    code = message.text.strip()

    # 🔐 OBUNA TEKSHIRISH
    subscribed = await check_subscription(
        bot,
        message.from_user.id
    )

    if not subscribed:

        await message.answer(
            "🔒 <b>DONIMEDIA</b>\n\n"
            "Kino olishdan oldin kanalimizga obuna bo‘ling.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # 🔎 KINO QIDIRISH
    movie = await get_movie(code)

    if not movie:

        await message.answer(
            "❌ <b>Kino topilmadi!</b>\n\n"
            f"🔢 Siz yuborgan kod: <code>{code}</code>\n\n"
            "Kod to‘g‘ri ekanligini tekshirib qayta yuboring.",
            parse_mode="HTML"
        )

        return

    # 👁 KO‘RISHNI OSHIRISH
    await increase_views(movie["id"])

    # 🕐 TARIXGA QO‘SHISH
    await add_history(
        message.from_user.id,
        movie["id"]
    )

    # ❤️ SEVIMLI HOLATI
    favorite = await is_favorite(
        message.from_user.id,
        movie["id"]
    )

    # 📝 TAVSIF
    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📖 {movie['description'] or 'Tavsif mavjud emas'}\n\n"
        f"🎭 Janr: {movie['genre'] or 'Noma’lum'}\n"
        f"📅 Yil: {movie['year'] or 'Noma’lum'}\n"
        f"⭐ Reyting: {movie['rating'] or 'Noma’lum'}\n"
        f"🔢 Kod: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    # 🎥 VIDEONI YUBORISH
    try:

        await message.answer_video(
            video=movie["file_id"],
            caption=caption,
            reply_markup=movie_buttons(
                movie["id"],
                favorite
            ),
            parse_mode="HTML"
        )

    except Exception as e:

        print(f"❌ VIDEO YUBORISH XATOSI: {e}")

        await message.answer(
            "❌ Kino videosini yuborishda xatolik yuz berdi."
        )


# =========================================================
# ❤️ SEVIMLIGA QO‘SHISH / OLIB TASHLASH
# =========================================================

@router.callback_query(F.data.startswith("favorite:"))
async def favorite_handler(
    callback: CallbackQuery
):

    try:
        movie_id = int(
            callback.data.split(":")[1]
        )
    except (ValueError, IndexError):

        await callback.answer(
            "❌ Kino ID noto‘g‘ri.",
            show_alert=True
        )

        return

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
            "💔 Sevimlilardan olib tashlandi."
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