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
    check_subscription,
    get_unsubscribed_channels
)


router = Router()


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
                    text="✅ Obunani tekshirish",
                    callback_data="check_subscription"
                )
            ]

        ]
    )


def subscription_text(unsubscribed=None):

    if unsubscribed:

        channels = "\n".join(
            f"❌ {channel['name']}"
            for channel in unsubscribed
        )

    else:

        channels = (
            "❌ @buroqli\n"
            "❌ @storis_moskva"
        )

    return (
        "🔐 <b>MAJBURIY OBUNA</b>\n\n"
        "🎬 <b>DONIMEDIA</b> botidan foydalanish "
        "uchun quyidagi kanallarga obuna bo‘ling:\n\n"
        f"{channels}\n\n"
        "1️⃣ Birinchi kanalga obuna bo‘ling.\n"
        "2️⃣ Ikkinchi kanalga obuna bo‘ling.\n"
        "3️⃣ <b>✅ Obunani tekshirish</b> tugmasini bosing.\n\n"
        "🍿 Shundan keyin barcha funksiyalardan "
        "foydalanishingiz mumkin."
    )


@router.message(CommandStart())
async def start_handler(
    message: Message,
    bot
):

    # Foydalanuvchini bazaga qo'shish
    try:
        await add_user(message.from_user)
    except Exception as e:
        print(
            f"⚠️ USER QO'SHISH XATOSI: {e}"
        )

    # Obunani tekshirish
    try:

        unsubscribed = await get_unsubscribed_channels(
            bot,
            message.from_user.id
        )

    except Exception as e:

        print(
            f"❌ OBUNANI TEKSHIRISH XATOSI: {e}"
        )

        await message.answer(
            "❌ Obunani tekshirishda xatolik yuz berdi.\n"
            "Iltimos, birozdan keyin qayta urinib ko‘ring."
        )

        return

    # Obuna to'liq emas
    if unsubscribed:

        await message.answer(
            subscription_text(unsubscribed),
            reply_markup=subscription_keyboard(),
            parse_mode="HTML"
        )

        return

    # Obuna to'liq
    await message.answer(
        f"🎬 <b>DONIMEDIA</b>\n\n"
        f"Assalomu alaykum, "
        f"<b>{message.from_user.first_name}</b>! 👋\n\n"
        f"✅ Barcha majburiy obunalar tasdiqlandi.\n\n"
        f"🍿 Kino kodini yuboring yoki menyudan "
        f"kerakli bo‘limni tanlang.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


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

    # Hali obuna bo'lmagan kanal mavjud
    if unsubscribed:

        channels_text = "\n".join(
            f"❌ {channel['name']}"
            for channel in unsubscribed
        )

        await callback.answer(
            "❌ Hali barcha kanallarga obuna bo‘lmagansiz!",
            show_alert=True
        )

        try:

            await callback.message.answer(
                "🔐 <b>OBUNA YETISHMAYAPTI</b>\n\n"
                "Siz hali quyidagi kanal(lar)ga "
                "obuna bo‘lmagansiz:\n\n"
                f"{channels_text}\n\n"
                "Avval obuna bo‘ling, keyin "
                "<b>✅ Obunani tekshirish</b> tugmasini bosing.",
                reply_markup=subscription_keyboard(),
                parse_mode="HTML"
            )

        except Exception as e:

            print(
                f"❌ OBUNA XABAR XATOSI: {e}"
            )

        return

    # Ikkala kanalga ham obuna
    await callback.answer(
        "✅ Barcha obunalar tasdiqlandi!",
        show_alert=True
    )

    try:

        await callback.message.answer(
            "🎬 <b>DONIMEDIA</b>\n\n"
            "✅ Ikkala kanalga ham obuna tasdiqlandi!\n\n"
            "🍿 Endi kino kodini yuborishingiz "
            "yoki menyudan foydalanishingiz mumkin.",
            reply_markup=main_menu(),
            parse_mode="HTML"
        )

    except Exception as e:

        print(
            f"❌ MENU XABAR XATOSI: {e}"
        )