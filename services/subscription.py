from aiogram import Bot
from config import CHANNEL_ID


async def check_subscription(bot: Bot, user_id: int) -> bool:
    try:
        chat_id = CHANNEL_ID.strip()

        if chat_id.lstrip("-").isdigit():
            chat_id = int(chat_id)

        member = await bot.get_chat_member(
            chat_id=chat_id,
            user_id=user_id
        )

        print(
            f"🔎 OBUNA: user={user_id} | "
            f"channel={chat_id} | "
            f"status={member.status}"
        )

        return member.status in (
            "member",
            "administrator",
            "creator"
        )

    except Exception as e:
        print(f"❌ OBUNA TEKSHIRISHDA XATO: {e}")
        return False