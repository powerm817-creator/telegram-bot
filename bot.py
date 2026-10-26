import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, ChatMemberHandler

# Logging ကို စနစ်တကျ ပြုလုပ်ရန်
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Member အပြောင်းအလဲရှိတိုင်း ဒီ Function အလုပ်လုပ်ပါမယ်
async def track_chats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    result = update.chat_member
    if result is None:
        return

    #  പഴയ အခြေအနေနှင့် လက်ရှိ အခြေအနေကို နှိုင်းယှဉ်ခြင်း
    old_member = result.old_chat_member
    new_member = result.new_chat_member

    # ဥပမာ - Member တစ်ဦးသည် Group မှ ထွက်သွားခဲ့လျှင် (Left)
    if old_member.status in ["member", "restricted"] and new_member.status == "left":
        user_id = new_member.user.id
        chat_id = update.effective_chat.id
        
        try:
            # ထွက်သွားသူကို ထပ်မဝင်နိုင်အောင် Ban လိုက်မည်
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            logging.info(f"User {user_id} left and has been banned automatically.")
        except Exception as e:
            logging.error(f"Failed to ban user: {e}")

def main():
    # BotFather ဆီက ရလာတဲ့ Token ကို ထည့်ပါ
    application = ApplicationBuilder().token("8801003985:AAGeCEjaNvHmjCeRmte8ecPQIQ9oICoHY0E").build()

    # Chat Member အပြောင်းအလဲများကို ဖမ်းယူရန် Handler ထည့်သွင်းခြင်း
    application.add_handler(ChatMemberHandler(track_chats, ChatMemberHandler.CHAT_MEMBER))

    # Bot ကို စတင် Run ခြင်း
    application.run_polling()

if __name__ == '__main__':
    main()
