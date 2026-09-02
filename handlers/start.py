from aiogram import Router, F
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


router = Router()


async def check_subscription(bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except Exception as e:
        print(f"Obuna tekshirish xatosi: {e}")
        return False


def subscription_keyboard():
    channel_username = CHANNEL_ID.replace("@", "")

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📢 Kanalga obuna bo‘lish",
                    url=f"https://t.me/{channel_username}"
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
async def start_handler(message: Message, bot):

    await add_user(message.from_user)

    subscribed = await check_subscription(
        bot,
        message.from_user.id
    )

    if not subscribed:
        await message.answer(
            "🎬 <b>DONIMEDIA</b>\n\n"
            "🍿 Kino olamiga xush kelibsiz!\n\n"
            "🔐 Botdan foydalanish uchun "
            "avval kanalimizga obuna bo‘ling.\n\n"
            "👇 Obuna bo‘lgach, "
            "<b>«Obunani tekshirish»</b> tugmasini bosing.",
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )
        return

    await message.answer(
        f"🎬 <b>DONIMEDIA</b>\n\n"
        f"Assalomu alaykum, "
        f"<b>{message.from_user.first_name}</b>! 👋\n\n"
        f"🍿 Kino izlashni boshlashingiz mumkin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(
    callback: CallbackQuery,
    bot
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

    await callback.message.delete()

    await callback.message.answer(
        "✅ <b>Obuna tasdiqlandi!</b>\n\n"
        "🎬 DONIMEDIA'ga xush kelibsiz!\n"
        "🍿 Kino izlashni boshlang.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

    await callback.answer()