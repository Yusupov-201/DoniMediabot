from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database import (
    get_favorites,
    remove_favorite,
    get_movie_by_id,
)
from keyboards.main import main_menu

router = Router()


# ❤️ Sevimlilar tugmasi
@router.message(F.text == "❤️ Sevimlilar")
async def favorites_handler(message: Message):
    user_id = message.from_user.id

    try:
        movies = await get_favorites(user_id)
    except Exception as e:
        print(f"❌ FAVORITELAR XATOSI: {e}")
        await message.answer(
            "❌ Sevimlilarni yuklashda xatolik yuz berdi."
        )
        return

    if not movies:
        await message.answer(
            "❤️ <b>Sevimlilar</b>\n\n"
            "Hozircha sevimli kinolaringiz yo‘q. 🍿\n\n"
            "Kino topib, <b>❤️ Sevimlilarga qo‘shish</b> "
            "tugmasini bosing.",
            parse_mode="HTML"
        )
        return

    text = (
        "❤️ <b>SEVIMLI KINOLARINGIZ</b>\n\n"
        f"🎬 Jami: <b>{len(movies)}</b> ta kino\n\n"
    )

    for i, movie in enumerate(movies, start=1):
        title = movie["title"] or "Noma'lum"
        code = movie["code"]

        text += (
            f"{i}. 🎬 <b>{title}</b>\n"
            f"   🔢 Kod: <code>{code}</code>\n\n"
        )

    text += (
        "🍿 Kino kodini yuborsangiz, filmni olishingiz mumkin."
    )

    await message.answer(
        text,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# ❤️ Sevimlidan o‘chirish
@router.callback_query(F.data.startswith("remove_favorite:"))
async def remove_favorite_callback(callback: CallbackQuery):
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
        await remove_favorite(
            user_id,
            movie_id
        )

        await callback.answer(
            "💔 Sevimlilardan olib tashlandi!"
        )

        # Agar video xabari bo‘lsa, tugmalarni yangilaymiz
        try:
            from handlers.movies import movie_buttons

            await callback.message.edit_reply_markup(
                reply_markup=movie_buttons(
                    movie_id,
                    False
                )
            )
        except Exception as e:
            print(
                f"⚠️ Tugmani yangilashda xato: {e}"
            )

    except Exception as e:
        print(
            f"❌ FAVORITELARDAN O‘CHIRISH XATOSI: {e}"
        )

        await callback.answer(
            "❌ O‘chirishda xatolik yuz berdi.",
            show_alert=True
        )


# ❤️ Sevimlilar ro‘yxatidan kino ochish
@router.callback_query(F.data.startswith("favorite_movie:"))
async def favorite_movie_callback(
    callback: CallbackQuery,
    bot
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

    try:
        movie = await get_movie_by_id(movie_id)
    except Exception as e:
        print(
            f"❌ KINO TOPISH XATOSI: {e}"
        )
        await callback.answer(
            "❌ Kino topilmadi.",
            show_alert=True
        )
        return

    if not movie:
        await callback.answer(
            "❌ Kino topilmadi.",
            show_alert=True
        )
        return

    title = movie["title"] or "Noma'lum"
    description = (
        movie["description"]
        or "Tavsif mavjud emas"
    )
    genre = movie["genre"] or "Noma'lum"
    year = movie["year"] or "Noma'lum"
    rating = movie["rating"] or "Noma'lum"
    code = movie["code"]
    file_id = movie["file_id"]

    caption = (
        f"🎬 <b>{title}</b>\n\n"
        f"📖 <b>Tavsif:</b>\n"
        f"{description}\n\n"
        f"🎭 <b>Janr:</b> {genre}\n"
        f"📅 <b>Yil:</b> {year}\n"
        f"⭐ <b>Reyting:</b> {rating}\n"
        f"🔢 <b>Kod:</b> <code>{code}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>\n"
        f"📢 @buroqli"
    )

    try:
        from handlers.movies import movie_buttons

        favorite = True

        await callback.message.answer_video(
            video=file_id,
            caption=caption,
            reply_markup=movie_buttons(
                movie_id,
                favorite
            ),
            parse_mode="HTML"
        )

        await callback.answer()

    except Exception as e:
        print(
            f"❌ FAVORITE VIDEO XATOSI: {e}"
        )

        await callback.answer(
            "❌ Videoni yuborishda xatolik.",
            show_alert=True
        )