from aiogram import Bot

from config import (
    CHANNEL_ID_1,
    CHANNEL_ID_2,
    CHANNEL_ID_3,
    CHANNEL_ID_4
)


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
    },
    {
        "id": CHANNEL_ID_3,
        "name": "@nasheedsl",
        "url": "https://t.me/nasheedsl"
    },
    {
        "id": CHANNEL_ID_4,
        "name": "@kurtlar_vadisi_storis",
        "url": "https://t.me/kurtlar_vadisi_storis"
    }
]


async def check_one_channel(
    bot: Bot,
    user_id: int,
    channel_id: str
) -> bool:

    try:

        chat_id = str(channel_id).strip()

        if chat_id.lstrip("-").isdigit():
            chat_id = int(chat_id)

        member = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        print(
            f"🔎 OBUNA | "
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


async def check_subscription(
    bot: Bot,
    user_id: int
) -> bool:

    """
    Foydalanuvchi 4 ta kanalning
    HAMMASIGA obuna bo'lgan bo'lsa True.
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


async def get_unsubscribed_channels(
    bot: Bot,
    user_id: int
):

    """
    Obuna bo'lmagan kanallarni qaytaradi.
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