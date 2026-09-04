from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import CHANNEL_ID
from database import add_user
from keyboards.main import main_menu
from services.subscription import check_subscription


router = Router()


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


@router.message(CommandStart())
async def start_handler(message: Message, bot: Bot):

    await add_user(message.from_user)

    subscribed = await check_subscription(
        bot,
        message.from_user.id
    )

    if not subscribed:
        await message.answer(
            "🎬 <b>DONIMEDIA</b>\n\n"
            "🔒 Botdan foydalanish uchun avval "
            "kanalga obuna bo‘ling.\n\n"
            "1️⃣ Kanalga obuna bo‘ling\n"
            "2️⃣ Keyin <b>✅ Obunani tekshirish</b> tugmasini bosing.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )
        return

    await message.answer(
        f"🎬 <b>DONIMEDIA</b>\n\n"
        f"Assalomu alaykum, "
        f"<b>{message.from_user.first_name}</b>! 👋\n\n"
        "🍿 Kino izlashni boshlashingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(
    callback: CallbackQuery,
    bot: Bot
):

    subscribed = await check_subscription(
        bot,
        callback.from_user.id
    )

    if not subscribed:
        await callback.answer(
            "❌ Siz hali kanalga obuna bo‘lmagansiz!",
            show_alert=True
        )
        return

    await callback.answer(
        "✅ Obuna tasdiqlandi!",
        show_alert=True
    )

    await callback.message.answer(
        "🎬 <b>DONIMEDIA</b>\n\n"
        "✅ Obuna tasdiqlandi!\n"
        "🍿 Kino izlashni boshlashingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )