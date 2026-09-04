from aiogram import Bot

from config import (
    CHANNEL_ID_1,
    CHANNEL_ID_2
)


# =========================================================
# MAJBURIY OBUNA KANALLARI
# =========================================================

CHANNELS = [
    {
        "id": CHANNEL_ID_1,
        "name": "@buroqli",
        "url": "https://t.me/buroqli"
    },
    {
        "id": CHANNEL_ID_2,
        "name": "@storis_moskva",
        "url": "https://t.me/storis_moskva"
    }
]


# =========================================================
# BITTA KANALNI TEKSHIRISH
# =========================================================

async def check_one_channel(
    bot: Bot,
    user_id: int,
    channel_id: str
) -> bool:

    try:

        chat_id = str(channel_id).strip()

        # -100... ko'rinishidagi ID bo'lsa
        if chat_id.lstrip("-").isdigit():
            chat_id = int(chat_id)

        member = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        print(
            f"🔎 OBUNA TEKSHIRISH | "
            f"user={user_id} | "
            f"channel={chat_id} | "
            f"status={member.status}"
        )

        return member.status in {
            "member",
            "administrator",
            "creator"
        }

    except Exception as e:

        print(
            f"❌ OBUNA XATOSI | "
            f"channel={channel_id} | "
            f"{type(e).__name__}: {e}"
        )

        return False


# =========================================================
# IKKALA KANALNI TEKSHIRISH
# =========================================================

async def check_subscription(
    bot: Bot,
    user_id: int
) -> bool:

    """
    Foydalanuvchi ikkala kanalga ham
    obuna bo'lgan bo'lsa True qaytaradi.

    Bittasiga obuna bo'lmasa False qaytaradi.
    """

    for channel in CHANNELS:

        subscribed = await check_one_channel(
            bot=bot,
            user_id=user_id,
            channel_id=channel["id"]
        )

        if not subscribed:
            return False

    return True


# =========================================================
# OBUNA BO'LMAGAN KANALLARNI TOPISH
# =========================================================

async def get_unsubscribed_channels(
    bot: Bot,
    user_id: int
):
    """
    Foydalanuvchi obuna bo'lmagan
    kanallarni qaytaradi.
    """

    unsubscribed = []

    for channel in CHANNELS:

        subscribed = await check_one_channel(
            bot=bot,
            user_id=user_id,
            channel_id=channel["id"]
        )

        if not subscribed:
            unsubscribed.append(channel)

    return unsubscribed