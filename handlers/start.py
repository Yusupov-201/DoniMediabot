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

from services.subscription import (
    get_unsubscribed_channels
)


router = Router()


# =========================================================
# OBUNA TUGMALARI
# =========================================================

def subscription_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📢 1️⃣ @buroqli",
                    url="https://t.me/buroqli"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📢 2️⃣ @storis_moskva",
                    url="https://t.me/storis_moskva"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📢 3️⃣ @nasheedsl",
                    url="https://t.me/nasheedsl"
                )
            ],

            [
                InlineKeyboardButton(
                    text="📢 4️⃣ @kurtlar_vadisi_storis",
                    url="https://t.me/kurtlar_vadisi_storis"
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
# START
# =========================================================

@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot
):

    # Foydalanuvchini bazaga yozish
    try:

        await add_user(
            message.from_user
        )

    except Exception as e:

        print(
            f"⚠️ USER XATOSI: {e}"
        )

    # Obunalarni tekshirish
    try:

        unsubscribed = await get_unsubscribed_channels(
            bot,
            message.from_user.id
        )

    except Exception as e:

        print(
            f"❌ OBUNA TEKSHIRISH XATOSI: {e}"
        )

        await message.answer(
            "❌ Obunani tekshirishda xatolik yuz berdi.\n"
            "Iltimos, keyinroq qayta urinib ko‘ring."
        )

        return

    # Obuna bo'lmagan kanal bor
    if unsubscribed:

        channels_text = "\n".join(
            f"❌ {channel['name']}"
            for channel in unsubscribed
        )

        await message.answer(
            "🔐 <b>DONIMEDIA — MAJBURIY OBUNA</b>\n\n"

            "🎬 Botdan foydalanish uchun "
            "quyidagi kanallarga obuna bo‘ling:\n\n"

            f"{channels_text}\n\n"

            "👇 Kanallarga obuna bo‘ling va "
            "<b>✅ Obunani tekshirish</b> tugmasini bosing.",
            
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # Hammasiga obuna
    await message.answer(
        f"🎬 <b>DONIMEDIA</b>\n\n"
        f"Assalomu alaykum, "
        f"<b>{message.from_user.first_name}</b>! 👋\n\n"
        "✅ Barcha 4 ta kanalga obuna tasdiqlandi!\n\n"
        "🍿 Endi kino kodini yuboring yoki "
        "menyudan kerakli bo‘limni tanlang.",
        
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


# =========================================================
# OBUNANI TEKSHIRISH
# =========================================================

@router.callback_query(
    F.data == "check_subscription"
)
async def check_subscription_callback(
    callback: CallbackQuery,
    bot
):

    user_id = callback.from_user.id

    try:

        unsubscribed = await get_unsubscribed_channels(
            bot,
            user_id
        )

    except Exception as e:

        print(
            f"❌ OBUNA CALLBACK XATOSI: {e}"
        )

        await callback.answer(
            "❌ Tekshirishda xatolik yuz berdi.",
            show_alert=True
        )

        return

    # Hali obuna bo'lmagan kanal bor
    if unsubscribed:

        channels_text = "\n".join(
            f"❌ {channel['name']}"
            for channel in unsubscribed
        )

        await callback.answer(
            "❌ Hali barcha kanallarga obuna bo‘lmagansiz!",
            show_alert=True
        )

        await callback.message.answer(
            "🔐 <b>OBUNA YETISHMAYAPTI</b>\n\n"

            "Quyidagi kanallarga hali "
            "obuna bo‘lmagansiz:\n\n"

            f"{channels_text}\n\n"

            "Obuna bo‘lgach yana "
            "<b>✅ Obunani tekshirish</b> tugmasini bosing.",
            
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # Hammasi yaxshi
    await callback.answer(
        "✅ 4 ta kanalga obuna tasdiqlandi!",
        show_alert=True
    )

    await callback.message.answer(
        "🎬 <b>DONIMEDIA</b>\n\n"
        "✅ Barcha majburiy obunalar tasdiqlandi!\n\n"
        "🍿 Endi botdan foydalanishingiz mumkin.",
        
        reply_markup=main_menu(),
        parse_mode="HTML"
    )