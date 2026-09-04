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

router = Router()


# ==========================================
# MAJBURIY OBUNA TEKSHIRISH
# ==========================================

async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        print(
            f"OBUNA: user={user_id} | "
            f"channel={CHANNEL_ID} | "
            f"status={member.status}"
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except Exception as e:
        print(f"OBUNA TEKSHIRISH XATOSI: {e}")
        return False


# ==========================================
# OBUNA TUGMALARI
# ==========================================

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


# ==========================================
# /START
# ==========================================

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
            "👋 Kino botimizga xush kelibsiz!\n\n"
            "🔒 Botdan foydalanish uchun avval "
            "kanalimizga obuna bo‘ling.\n\n"
            "Obuna bo‘lgandan keyin "
            "<b>✅ Obunani tekshirish</b> tugmasini bosing.",
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


# ==========================================
# OBUNANI QAYTA TEKSHIRISH
# ==========================================

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

    await callback.message.edit_text(
        "✅ <b>Obuna tasdiqlandi!</b>\n\n"
        "🎬 DONIMEDIA'ga xush kelibsiz!\n"
        "🍿 Kino izlashni boshlashingiz mumkin.",
        reply_markup=None,
        parse_mode="HTML"
    )

    await callback.message.answer(
        "🏠 Bosh menyu",
        reply_markup=main_menu()
    )

    await callback.answer()