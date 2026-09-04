from aiogram import Router, F, Bot

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


router = Router()


# =========================================================
# 📢 OBUNA KLAVIATURASI
# =========================================================

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


# =========================================================
# ❤️ KINO TUGMALARI
# =========================================================

def movie_buttons(movie_id: int, favorite: bool = False):

    if favorite:
        text = "💔 Sevimlidan olib tashlash"
    else:
        text = "❤️ Sevimlilarga qo‘shish"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"favorite:{movie_id}"
                )
            ]
        ]
    )


# =========================================================
# 🎬 KINO KODI
# =========================================================

@router.message(F.text)
async def movie_code_handler(
    message: Message,
    bot: Bot
):

    text = message.text.strip()

    print(
        f"🎬 XABAR KELDI | "
        f"user={message.from_user.id} | "
        f"text={text}"
    )

    # -----------------------------------------------------
    # KOMANDALAR
    # -----------------------------------------------------

    if text.startswith("/"):
        print(
            f"ℹ️ Komanda o'tkazib yuborildi: {text}"
        )
        return

    # -----------------------------------------------------
    # FAQAT RAQAMLI KOD
    # -----------------------------------------------------

    if not text.isdigit():

        print(
            f"ℹ️ Kino kodi emas: {text}"
        )

        await message.answer(
            "🎬 <b>DONIMEDIA</b>\n\n"
            "🔢 Kino olish uchun kino kodini yuboring.\n\n"
            "Masalan:\n"
            "<code>123</code>",
            parse_mode="HTML"
        )

        return

    code = text

    print(
        f"🔎 KINO KODI QABUL QILINDI: {code}"
    )

    # =====================================================
    # 🔐 OBUNANI TEKSHIRISH
    # =====================================================

    try:

        subscribed = await check_subscription(
            bot,
            message.from_user.id
        )

        print(
            f"🔐 OBUNA: "
            f"user={message.from_user.id} | "
            f"result={subscribed}"
        )

    except Exception as e:

        print(
            f"❌ OBUNA XATOSI: "
            f"{type(e).__name__}: {e}"
        )

        await message.answer(
            "❌ Obunani tekshirishda xatolik yuz berdi.\n\n"
            "Birozdan keyin qayta urinib ko‘ring."
        )

        return

    # -----------------------------------------------------
    # OBUNA YO‘Q
    # -----------------------------------------------------

    if not subscribed:

        print(
            f"🚫 OBUNA YO‘Q | "
            f"user={message.from_user.id}"
        )

        await message.answer(
            "🔒 <b>DONIMEDIA</b>\n\n"
            "Kino olishdan oldin "
            "<b>@buroqli</b> kanaliga obuna bo‘ling.\n\n"
            "Obuna bo‘lgach, "
            "<b>✅ Obunani tekshirish</b> tugmasini bosing.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # =====================================================
    # 🎬 DATABASE'DAN KINO QIDIRISH
    # =====================================================

    print(
        f"🔎 DATABASE: kino qidirilmoqda | code={code}"
    )

    try:

        movie = await get_movie(code)

    except Exception as e:

        print(
            f"❌ DATABASE XATOSI: "
            f"{type(e).__name__}: {e}"
        )

        await message.answer(
            "❌ Kino bazasida xatolik yuz berdi."
        )

        return

    # =====================================================
    # ❌ KINO TOPILMADI
    # =====================================================

    if not movie:

        print(
            f"❌ KINO TOPILMADI | code={code}"
        )

        await message.answer(
            "❌ <b>Kino topilmadi!</b>\n\n"
            f"🔢 Kod: <code>{code}</code>\n\n"
            "Kino kodi noto‘g‘ri yoki kino hali "
            "bazaga qo‘shilmagan.",
            parse_mode="HTML"
        )

        return

    # =====================================================
    # ✅ KINO TOPILDI
    # =====================================================

    print(
        f"✅ KINO TOPILDI | "
        f"id={movie['id']} | "
        f"code={movie['code']} | "
        f"title={movie['title']}"
    )

    # =====================================================
    # 👁 KO‘RISHNI OSHIRISH
    # =====================================================

    try:

        await increase_views(
            movie["id"]
        )

        print(
            f"👁 VIEW +1 | movie_id={movie['id']}"
        )

    except Exception as e:

        print(
            f"⚠️ VIEW XATOSI: {e}"
        )

    # =====================================================
    # 🕘 TARIXGA QO‘SHISH
    # =====================================================

    try:

        await add_history(
            message.from_user.id,
            movie["id"]
        )

        print(
            f"🕘 HISTORY +1 | "
            f"user={message.from_user.id}"
        )

    except Exception as e:

        print(
            f"⚠️ HISTORY XATOSI: {e}"
        )

    # =====================================================
    # ❤️ SEVIMLILIKNI TEKSHIRISH
    # =====================================================

    try:

        favorite = await is_favorite(
            message.from_user.id,
            movie["id"]
        )

    except Exception as e:

        print(
            f"⚠️ FAVORITE TEKSHIRISH XATOSI: {e}"
        )

        favorite = False

    # =====================================================
    # 📝 MA'LUMOTLAR
    # =====================================================

    title = movie["title"] or "Noma'lum"

    description = (
        movie["description"]
        or "Tavsif mavjud emas"
    )

    genre = movie["genre"] or "Noma'lum"

    year = movie["year"] or "Noma'lum"

    rating = movie["rating"] or "Noma'lum"

    movie_code = movie["code"] or code

    file_id = movie["file_id"]

    caption = (
        f"🎬 <b>{title}</b>\n\n"
        f"📖 {description}\n\n"
        f"🎭 Janr: {genre}\n"
        f"📅 Yil: {year}\n"
        f"⭐ Reyting: {rating}\n"
        f"🔢 Kod: <code>{movie_code}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    # =====================================================
    # 🎥 FILE_ID TEKSHIRISH
    # =====================================================

    if not file_id:

        print(
            f"❌ FILE_ID BO‘SH | "
            f"movie_id={movie['id']}"
        )

        await message.answer(
            "❌ Bu kinoning video fayli topilmadi.\n\n"
            "Administrator kinoni qayta qo‘shishi kerak."
        )

        return

    print(
        f"📤 VIDEO YUBORILMOQDA | "
        f"code={code} | "
        f"title={title}"
    )

    # =====================================================
    # 🎥 VIDEO YUBORISH
    # =====================================================

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
            f"✅ VIDEO YUBORILDI | "
            f"code={code} | "
            f"title={title}"
        )

    except Exception as e:

        print(
            f"❌ VIDEO YUBORISH XATOSI: "
            f"{type(e).__name__}: {e}"
        )

        await message.answer(
            "❌ Kino videosini yuborishda xatolik yuz berdi."
        )


# =========================================================
# ❤️ SEVIMLILARGA QO‘SHISH / OLIB TASHLASH
# =========================================================

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

        favorite = await is_favorite(
            user_id,
            movie_id
        )

        # -------------------------------------------------
        # 💔 OLIB TASHLASH
        # -------------------------------------------------

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

            print(
                f"💔 FAVORITE O‘CHIRILDI | "
                f"user={user_id} | "
                f"movie={movie_id}"
            )

        # -------------------------------------------------
        # ❤️ QO‘SHISH
        # -------------------------------------------------

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

            print(
                f"❤️ FAVORITE QO‘SHILDI | "
                f"user={user_id} | "
                f"movie={movie_id}"
            )

    except Exception as e:

        print(
            f"❌ FAVORITE XATOSI: "
            f"{type(e).__name__}: {e}"
        )

        await callback.answer(
            "❌ Xatolik yuz berdi.",
            show_alert=True
        )