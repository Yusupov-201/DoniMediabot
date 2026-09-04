from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import add_user
from keyboards.main import main_menu
from services.subscription import check_subscription


router = Router()


# =========================================================
# 🔐 MAJBURIY OBUNA TUGMALARI
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
# 🚀 START
# =========================================================

@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot
):

    # Foydalanuvchini bazaga qo‘shish
    await add_user(message.from_user)

    # Obunani tekshirish
    subscribed = await check_subscription(
        bot,
        message.from_user.id
    )

    # Obuna bo‘lmagan
    if not subscribed:

        await message.answer(
            "🎬 <b>DONIMEDIA</b>\n\n"
            "🍿 Kino olamiga xush kelibsiz!\n\n"
            "🔐 Botdan foydalanish uchun avval "
            "<b>DONIMEDIA kanaliga</b> obuna bo‘ling.\n\n"
            "Obuna bo‘lgandan keyin "
            "<b>✅ Obunani tekshirish</b> tugmasini bosing.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # Obuna bo‘lgan
    await message.answer(
        f"🎬 <b>DONIMEDIA</b>\n\n"
        f"Assalomu alaykum, "
        f"<b>{message.from_user.first_name}</b>! 👋\n\n"
        f"🍿 Kino izlashni boshlashingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================================================
# ✅ OBUNANI TEKSHIRISH
# =========================================================

@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(
    callback: CallbackQuery,
    bot
):

    subscribed = await check_subscription(
        bot,
        callback.from_user.id
    )

    # Hali obuna bo‘lmagan
    if not subscribed:

        await callback.answer(
            "❌ Siz hali kanalga obuna bo‘lmagansiz!",
            show_alert=True
        )

        return

    # Obuna tasdiqlandi
    await callback.answer(
        "✅ Obuna tasdiqlandi!",
        show_alert=True
    )

    await callback.message.answer(
        "🎬 <b>DONIMEDIA</b>\n\n"
        "✅ Obunangiz tasdiqlandi!\n\n"
        "🍿 Endi kino kodini yuborishingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )