from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Bot,
)

from database import (
    get_movie,
    get_movie_by_id,
    increase_views,
    add_history,
    add_favorite,
    remove_favorite,
    is_favorite,
)
from services.subscription import check_subscription


router = Router()


# ============================================================
# 📢 OBUNA KLAVIATURASI
# ============================================================

def subscription_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 @buroqli kanaliga obuna bo‘lish",
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


# ============================================================
# 🎬 KINO TUGMALARI
# ============================================================

def movie_buttons(
    movie_id: int,
    favorite: bool = False
):
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
            ],
            [
                InlineKeyboardButton(
                    text="⬅️ Bosh menyu",
                    callback_data="movie_home"
                )
            ]
        ]
    )


# ============================================================
# 🎬 KINO KODI
# Faqat raqamli xabarlarni ushlaydi!
# ============================================================

@router.message(F.text.regexp(r"^\d+$"))
async def movie_code_handler(
    message: Message,
    bot: Bot
):
    code = message.text.strip()

    # --------------------------------------------------------
    # 🔐 OBUNANI TEKSHIRISH
    # --------------------------------------------------------

    subscribed = await check_subscription(
        bot,
        message.from_user.id
    )

    if not subscribed:
        await message.answer(
            "🔒 <b>DONIMEDIA</b>\n\n"
            "🎬 Kino olishdan oldin "
            "<b>@buroqli</b> kanalimizga obuna bo‘ling.\n\n"
            "1️⃣ Kanalga obuna bo‘ling\n"
            "2️⃣ Keyin <b>Obunani tekshirish</b> tugmasini bosing.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )
        return

    # --------------------------------------------------------
    # 🔎 KINONI BAZADAN TOPISH
    # --------------------------------------------------------

    try:
        movie = await get_movie(code)
    except Exception as e:
        print(
            f"❌ KINO BAZADAN QIDIRISH XATOSI: {e}"
        )

        await message.answer(
            "❌ Kino ma'lumotlarini olishda xatolik yuz berdi."
        )
        return

    # --------------------------------------------------------
    # ❌ KINO TOPILMADI
    # --------------------------------------------------------

    if not movie:
        await message.answer(
            "❌ <b>Kino topilmadi!</b>\n\n"
            f"🔢 Kino kodi: <code>{code}</code>\n\n"
            "Kino kodi noto‘g‘ri yoki bu koddagi kino "
            "hali bazaga qo‘shilmagan.",
            parse_mode="HTML"
        )
        return

    # --------------------------------------------------------
    # 👁 KO‘RISH + TARIX
    # --------------------------------------------------------

    try:
        await increase_views(movie["id"])
    except Exception as e:
        print(
            f"⚠️ Views xatosi: {e}"
        )

    try:
        await add_history(
            message.from_user.id,
            movie["id"]
        )
    except Exception as e:
        print(
            f"⚠️ History xatosi: {e}"
        )

    # --------------------------------------------------------
    # ❤️ SEVIMLILIK
    # --------------------------------------------------------

    try:
        favorite = await is_favorite(
            message.from_user.id,
            movie["id"]
        )
    except Exception as e:
        print(
            f"⚠️ Favorite tekshirish xatosi: {e}"
        )
        favorite = False

    # --------------------------------------------------------
    # 📝 KINO MATNI
    # --------------------------------------------------------

    title = movie["title"] or "Noma'lum"
    description = movie["description"] or "Tavsif mavjud emas"
    genre = movie["genre"] or "Noma'lum"
    year = movie["year"] or "Noma'lum"
    rating = movie["rating"] or "Noma'lum"
    movie_code = movie["code"]

    caption = (
        f"🎬 <b>{title}</b>\n\n"
        f"📖 <b>Tavsif:</b>\n"
        f"{description}\n\n"
        f"🎭 <b>Janr:</b> {genre}\n"
        f"📅 <b>Yil:</b> {year}\n"
        f"⭐ <b>Reyting:</b> {rating}\n"
        f"🔢 <b>Kod:</b> <code>{movie_code}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>\n"
        f"📢 @buroqli"
    )

    # --------------------------------------------------------
    # 🎥 VIDEO YUBORISH
    # --------------------------------------------------------

    file_id = movie["file_id"]

    if not file_id:
        await message.answer(
            "❌ Bu kinoning video fayli bazada topilmadi."
        )
        return

    try:
        await message.answer_video(
            video=file_id,
            caption=caption,
            reply_markup=movie_buttons(
                movie["id"],
                favorite
            ),
            parse_mode="HTML"
        )

        print(
            f"✅ KINO YUBORILDI: "
            f"code={code} | "
            f"title={title} | "
            f"user={message.from_user.id}"
        )

    except Exception as e:
        print(
            f"❌ VIDEO YUBORISH XATOSI: {repr(e)}"
        )

        await message.answer(
            "❌ <b>Videoni yuborishda xatolik yuz berdi.</b>\n\n"
            "Admin video faylini tekshirishi kerak.",
            parse_mode="HTML"
        )


# ============================================================
# ❤️ SEVIMLILARGA QO‘SHISH / OLIB TASHLASH
# ============================================================

@router.callback_query(
    F.data.startswith("favorite:")
)
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

    try:
        movie = await get_movie_by_id(movie_id)
    except Exception:
        movie = None

    try:
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

    except Exception as e:
        print(
            f"❌ FAVORITE XATOSI: {e}"
        )

        await callback.answer(
            "❌ Sevimlilarni o‘zgartirishda xatolik.",
            show_alert=True
        )


# ============================================================
# ⬅️ KINO OYNASIDAN BOSH MENYU
# ============================================================

@router.callback_query(
    F.data == "movie_home"
)
async def movie_home(
    callback: CallbackQuery
):
    try:
        from keyboards.main import main_menu

        await callback.message.answer(
            "🎬 <b>DONIMEDIA</b>\n\n"
            "Kerakli bo‘limni tanlang:",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )

        await callback.answer()

    except Exception as e:
        print(
            f"❌ BOSH MENU XATOSI: {e}"
        )

        await callback.answer(
            "❌ Menyuni ochishda xatolik.",
            show_alert=True
        )