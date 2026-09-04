from aiogram import Bot
from config import CHANNEL_ID


async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        channel = CHANNEL_ID.strip()

        if channel.lstrip("-").isdigit():
            channel = int(channel)

        member = await bot.get_chat_member(
            chat_id=channel,
            user_id=user_id
        )

        print(
            f"🔎 OBUNA TEKSHIRUV: "
            f"user={user_id} | "
            f"channel={channel} | "
            f"status={member.status}"
        )

        return member.status in {
            "member",
            "administrator",
            "creator"
        }

    except Exception as e:
        print(f"❌ OBUNA XATOSI: {type(e).__name__}: {e}")
        return False