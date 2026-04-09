import asyncio
import sqlite3
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8754227384:AAEUXtTBoOVajScixmGg-ccRV086mUQ5zrw"
ADMIN_ID = 1313252587

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 БАЗА
conn = sqlite3.connect("clients.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    date TEXT,
    time TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# 🚀 REMINDER
async def reminder_admin(name, phone, date, time):
    try:
        target = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
        remind = target - timedelta(hours=1)

        wait = (remind - datetime.now()).total_seconds()

        if wait > 0:
            await asyncio.sleep(wait)

            await bot.send_message(
                ADMIN_ID,
                f"⏰ 1 сағаттан кейін клиент келеді!\n{name} {phone}"
            )
    except:
        pass

# START
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Сәлем! Онлайн запись бот 👋")

# 📩 САЙТТАН КЕЛГЕН ЗАЯВКА
@dp.message()
async def handle(message: types.Message):
    text = message.text

    if "Жаңа клиент" in text:
        try:
            lines = text.split("\n")

            name = lines[1].replace("Аты: ", "")
            phone = lines[2].replace("Телефон: ", "")
            date = lines[3].replace("Күні: ", "")
            time = lines[4].replace("Уақыты: ", "")

            # 💾 САҚТАУ
            cursor.execute(
                "INSERT INTO clients (name, phone, date, time) VALUES (?, ?, ?, ?)",
                (name, phone, date, time)
            )
            conn.commit()

            # 📩 АДМИНГЕ ЖІБЕРУ
            await bot.send_message(
                ADMIN_ID,
                f"🆕 Жаңа клиент!\n\n👤 {name}\n📞 {phone}\n📅 {date} {time}"
            )

            # ⏰ REMINDER
            asyncio.create_task(reminder_admin(name, phone, date, time))

            await message.answer("✅ Запись қабылданды")

        except:
            await message.answer("❌ Қате формат")

# 📊 ЕСЕП
@dp.message(Command("report"))
async def report(message: types.Message):
    cursor.execute("SELECT COUNT(*) FROM clients")
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*) FROM clients 
    WHERE date = date('now')
    """)
    today = cursor.fetchone()[0]

    text = f"""
📊 Есеп:

👥 Барлығы: {total}
📅 Бүгін: {today}
💰 Табыс: {today * 5000} тг
"""

    await message.answer(text)

# 🚀 ЗАПУСК
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
