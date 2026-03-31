"""
🤖 «Сенің идеяң — біздің өнер 🎨» — Telegram Bot
AI Creative Services | Қазақша + Орысша
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)

# ========================
# ⚙️ БАПТАУЛАР — МІНДЕТТі ӨЗГЕРТІҢІЗ
# ========================
import os

BOT_TOKEN = os.getenv("8754227384:AAFlaA-7Bq6wVR8wVAOZqUwY86bCjJuJG4k") 

ADMIN_ID      =tel:1313252587               

BUSINESS_NAME = "Сенің идеяң — біздің өнер 🎨"

# Төлем деректері
KASPI_NUMBER  = "+7 7474513371"          
KASPI_NAME    = "Сабира С"            
CARD_NUMBER   = "0000 0000 0000 0000"       
CARD_BANK     = "Halyk / Forte / т.б."  

# ========================
# 📋 ҚЫЗМЕТТЕР КАТАЛОГЫ
# ========================
SERVICES = {
    "photo": {
        "name_kz": "🖼 Фото жасау (AI)",
        "name_ru": "🖼 Генерация фото (AI)",
        "desc_kz": (
            "Жасанды интеллект арқылы кез-келген стильде фото жасаймыз:\n\n"
            "• Портрет, пейзаж, өнімнің суреті\n"
            "• Брендинг үшін визуал\n"
            "• Аватар, профиль суреті\n"
            "• Рекламалық баннер"
        ),
        "desc_ru": (
            "Создаём фото любого стиля с помощью ИИ:\n\n"
            "• Портрет, пейзаж, предметная съёмка\n"
            "• Визуал для брендинга\n"
            "• Аватар, фото профиля\n"
            "• Рекламный баннер"
        ),
        "price_kz": "1 фото — 2 000 ₸\n5 фото — 8 000 ₸\n10 фото — 14 000 ₸",
        "price_ru": "1 фото — 2 000 ₸\n5 фото — 8 000 ₸\n10 фото — 14 000 ₸",
        "time_kz":  "1–3 сағат",
        "time_ru":  "1–3 часа",
    },
    "video": {
        "name_kz": "🎬 Видео жасау (AI)",
        "name_ru": "🎬 Создание видео (AI)",
        "desc_kz": (
            "AI арқылы видео роликтер:\n\n"
            "• Реклама (15–60 сек)\n"
            "• Өнімнің презентациясы\n"
            "• Слайд-шоу + музыка\n"
            "• Reels / TikTok контенті"
        ),
        "desc_ru": (
            "Видеоролики с помощью ИИ:\n\n"
            "• Рекламный ролик (15–60 сек)\n"
            "• Презентация продукта\n"
            "• Слайд-шоу + музыка\n"
            "• Контент для Reels / TikTok"
        ),
        "price_kz": "15 сек — 5 000 ₸\n30 сек — 8 000 ₸\n60 сек — 13 000 ₸",
        "price_ru": "15 сек — 5 000 ₸\n30 сек — 8 000 ₸\n60 сек — 13 000 ₸",
        "time_kz":  "3–24 сағат",
        "time_ru":  "3–24 часа",
    },
    "animation": {
        "name_kz": "✨ Анимация жасау",
        "name_ru": "✨ Создание анимации",
        "desc_kz": (
            "Анимациялық контент:\n\n"
            "• Логотип анимациясы\n"
            "• Motion graphic\n"
            "• Animated стикерлер\n"
            "• GIF баннерлер"
        ),
        "desc_ru": (
            "Анимационный контент:\n\n"
            "• Анимация логотипа\n"
            "• Motion graphic\n"
            "• Анимированные стикеры\n"
            "• GIF-баннеры"
        ),
        "price_kz": "Лого анимация — 6 000 ₸\nGIF баннер — 3 000 ₸\nSticker pack (5 шт) — 7 000 ₸",
        "price_ru": "Анимация лого — 6 000 ₸\nGIF-баннер — 3 000 ₸\nSticker pack (5 шт) — 7 000 ₸",
        "time_kz":  "6–48 сағат",
        "time_ru":  "6–48 часов",
    },
    "invitation": {
        "name_kz": "💌 Шақыру қағазы",
        "name_ru": "💌 Пригласительные",
        "desc_kz": (
            "Цифрлық шақыру қағаздары:\n\n"
            "• Той (некеге тіркелу, ұзату)\n"
            "• Туған күн\n"
            "• Корпоратив\n"
            "• Анимациялық + статикалық нұсқа"
        ),
        "desc_ru": (
            "Цифровые пригласительные:\n\n"
            "• Свадьба, помолвка, девичник\n"
            "• День рождения\n"
            "• Корпоратив\n"
            "• Анимированная + статичная версия"
        ),
        "price_kz": "Статик — 3 000 ₸\nАнимация — 6 000 ₸\nВидео шақыру — 9 000 ₸",
        "price_ru": "Статичное — 3 000 ₸\nАнимированное — 6 000 ₸\nВидео-приглашение — 9 000 ₸",
        "time_kz":  "3–12 сағат",
        "time_ru":  "3–12 часов",
    },
    "voice": {
        "name_kz": "🎙 Дауыс жазу (AI)",
        "name_ru": "🎙 Озвучка голосом (AI)",
        "desc_kz": (
            "AI дауысымен озвучка:\n\n"
            "• Реклама үшін диктор дауысы\n"
            "• Подкаст жазу\n"
            "• IVR / автожауапшы\n"
            "• Қазақша / орысша / ағылшынша"
        ),
        "desc_ru": (
            "Озвучка с помощью ИИ-голоса:\n\n"
            "• Голос диктора для рекламы\n"
            "• Запись подкаста\n"
            "• IVR / автоответчик\n"
            "• Казахский / русский / английский"
        ),
        "price_kz": "1 мин — 2 500 ₸\n5 мин — 10 000 ₸\n10 мин — 18 000 ₸",
        "price_ru": "1 мин — 2 500 ₸\n5 мин — 10 000 ₸\n10 мин — 18 000 ₸",
        "time_kz":  "1–6 сағат",
        "time_ru":  "1–6 часов",
    },
    "music": {
        "name_kz": "🎵 Ән / музыка жазу",
        "name_ru": "🎵 Написание песни / музыки",
        "desc_kz": (
            "AI арқылы музыкалық контент:\n\n"
            "• Толық ән (сөз + ән)\n"
            "• Фон музыкасы (background)\n"
            "• Джингл / рекламалық мелодия\n"
            "• Туған күн, той әні"
        ),
        "desc_ru": (
            "Музыкальный контент с помощью ИИ:\n\n"
            "• Полная песня (текст + вокал)\n"
            "• Фоновая музыка\n"
            "• Джингл / рекламная мелодия\n"
            "• Песня на день рождения, свадьбу"
        ),
        "price_kz": "Фон музыка — 4 000 ₸\nДжингл (15–30 сек) — 6 000 ₸\nТолық ән — 12 000 ₸",
        "price_ru": "Фоновая музыка — 4 000 ₸\nДжингл (15–30 сек) — 6 000 ₸\nПолная песня — 12 000 ₸",
        "time_kz":  "6–48 сағат",
        "time_ru":  "6–48 часов",
    },
}

# ========================
# ⌨️ KEYBOARDS
# ========================
def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇰🇿 Қазақша", callback_data="lang_kz"),
        InlineKeyboardButton("🇷🇺 Русский",  callback_data="lang_ru"),
    ]])

def main_menu_keyboard(lang):
    kb = []
    keys = list(SERVICES.keys())
    for i in range(0, len(keys), 2):
        row = [
            InlineKeyboardButton(SERVICES[k][f"name_{lang}"], callback_data=f"svc_{k}_{lang}")
            for k in keys[i:i+2]
        ]
        kb.append(row)
    kb.append([InlineKeyboardButton(
        "💰 Барлық бағалар" if lang == "kz" else "💰 Все цены",
        callback_data=f"allprices_{lang}"
    )])
    kb.append([InlineKeyboardButton(
        "📞 Менеджерге хабарласу" if lang == "kz" else "📞 Связаться с менеджером",
        callback_data=f"manager_{lang}"
    )])
    return InlineKeyboardMarkup(kb)

def service_keyboard(lang, svc_key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "💳 Тапсырыс / Төлем" if lang == "kz" else "💳 Заказать / Оплатить",
            callback_data=f"order_{svc_key}_{lang}"
        )],
        [InlineKeyboardButton(
            "❓ Сұрақ қою" if lang == "kz" else "❓ Задать вопрос",
            callback_data=f"question_{svc_key}_{lang}"
        )],
        [InlineKeyboardButton("⬅️ Артқа / Назад", callback_data=f"back_{lang}")],

def payment_keyboard(lang, svc_key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Kaspi QR / номер",          callback_data=f"pay_kaspi_{svc_key}_{lang}")],
        [InlineKeyboardButton("💳 Банк картасы / Карта",      callback_data=f"pay_card_{svc_key}_{lang}")],
        [InlineKeyboardButton("💵 Қолма-қол / Наличные",      callback_data=f"pay_cash_{svc_key}_{lang}")],
        [InlineKeyboardButton("🔄 Алмасу / Бартер",           callback_data=f"pay_barter_{lang}")],
        [InlineKeyboardButton("⬅️ Артқа / Назад",             callback_data=f"svc_{svc_key}_{lang}")],
    ])

def back_keyboard(lang):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("⬅️ Артқа / Назад", callback_data=f"back_{lang}")
    ]])

def screenshot_keyboard(lang):
    return InlineKeyboardMarkup([[
        InlineKeyboardButton(
            "📸 Скриншот жібердім / Отправил скриншот",
            callback_data=f"sent_screenshot_{lang}"
        )]])

# ========================
# 📨 HANDLERS
# ========================
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"👋 Сәлем!\n\n"
        f"🎨 *{BUSINESS_NAME}*\n\n"
        f"Жасанды интеллект арқылы сіздің идеяңызды өнерге айналдырамыз!\n\n"
        f"—\n\n"
        f"👋 Привет!\n\n"
        f"🎨 *{BUSINESS_NAME}*\n\n"
        f"Превращаем ваши идеи в искусство с помощью ИИ!\n\n"
        f"Тілді таңдаңыз / Выберите язык 👇"
    )
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=lang_keyboard())

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- ТІЛ ТАҢДАУ ---
    if data.startswith("lang_"):
        lang = data.split("_")[1]
        menu_text = (
            f"🎨 *{BUSINESS_NAME}*\n\nҚандай қызмет қажет? Таңдаңыз 👇"
            if lang == "kz" else
            f"🎨 *{BUSINESS_NAME}*\n\nКакая услуга вас интересует? Выберите 👇"
        )
        await query.edit_message_text(menu_text, parse_mode="Markdown",
                                      reply_markup=main_menu_keyboard(lang))

    # --- ҚЫЗМЕТ ТАҢДАУ ---
    elif data.startswith("svc_"):
        _, svc_key, lang = data.split("_", 2)
        svc = SERVICES[svc_key]
        text = (
            f"*{svc[f'name_{lang}']}*\n\n"
            f"{svc[f'desc_{lang}']}\n\n"
            f"💰 *{'Бағасы' if lang == 'kz' else 'Цены'}:*\n{svc[f'price_{lang}']}\n\n"
            f"⏱ *{'Орындалу уақыты' if lang == 'kz' else 'Срок'}:* {svc[f'time_{lang}']}"
        )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=service_keyboard(lang, svc_key))

    # --- БАРЛЫҚ БАҒАЛАР ---
    elif data.startswith("allprices_"):
        lang = data.split("_")[1]
        lines = [
            f"💰 *{'Барлық қызметтер бағасы' if lang == 'kz' else 'Все цены на услуги'}:*\n"
        ]
        for svc in SERVICES.values():
            lines.append(f"*{svc[f'name_{lang}']}*")
            lines.append(svc[f"price_{lang}"])
            lines.append(f"⏱ {svc[f'time_{lang}']}\n")
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown",
                                      reply_markup=back_keyboard(lang))

    # --- ТАПСЫРЫС / ТӨЛЕМ ТҮРІН ТАҢДАУ ---
    elif data.startswith("order_"):
        _, svc_key, lang = data.split("_", 2)
        text = (
            "💳 *Төлем жасау жолын таңдаңыз:*"
            if lang == "kz" else
            "💳 *Выберите удобный способ оплаты:*"
        )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=payment_keyboard(lang, svc_key))

    # --- KASPI ТӨЛЕМ ---
    elif data.startswith("pay_kaspi_"):
        parts = data.split("_")
        lang = parts[-1]
        if lang == "kz":
            text = (
                f"📱 *Kaspi арқылы төлем*\n\n"
                f"Kaspi-ге аударыңыз:\n"
                f"📞 Нөмір: `{KASPI_NUMBER}`\n"
                f"👤 Аты: *{KASPI_NAME}*\n\n"
                f"*Төлем жасағаннан кейін:*\n"
                f"1️⃣ Скриншот жіберіңіз\n"
                f"2️⃣ Тапсырыс мәлімет жазыңыз\n"
                f"3️⃣ Менеджер байланысады ✅\n\n"
                f"❗ Алдын-ала 50% аванс қабылданады"
            )
        else:
            text = (
                f"📱 *Оплата через Kaspi*\n\n"
                f"Переведите на Kaspi:\n"
                f"📞 Номер: `{KASPI_NUMBER}`\n"
                f"👤 Имя: *{KASPI_NAME}*\n\n"
                f"*После оплаты:*\n"
                f"1️⃣ Пришлите скриншот\n"
                f"2️⃣ Опишите детали заказа\n"
                f"3️⃣ Менеджер свяжется ✅\n\n"
                f"❗ Принимается аванс 50%"
            )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=screenshot_keyboard(lang))

    # --- КАРТА ТӨЛЕМ ---
    elif data.startswith("pay_card_"):
        parts = data.split("_")
        lang = parts[-1]
        if lang == "kz":
            text = (
                f"💳 *Банк картасы арқылы төлем*\n\n"
                f"Карта нөмірі: `{CARD_NUMBER}`\n"
                f"Банк: *{CARD_BANK}*\n"
                f"Аты: *{KASPI_NAME}*\n\n"
                f"Аударғаннан кейін скриншот жіберіңіз 📸"
            )
        else:
            text = (
                f"💳 *Оплата банковской картой*\n\n"
                f"Номер карты: `{CARD_NUMBER}`\n"
                f"Банк: *{CARD_BANK}*\n"
                f"Имя: *{KASPI_NAME}*\n\n"
                f"После перевода пришлите скриншот 📸"
            )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=screenshot_keyboard(lang))

    # --- ҚОЛМА-ҚОЛ ---
    elif data.startswith("pay_cash_"):
        parts = data.split("_")
        lang = parts[-1]
        text = (
            "💵 *Қолма-қол төлем*\n\n"
            "Менеджермен кездесу орны мен уақытын келісіңіз.\n"
            "Байланысу үшін төмендегі батырманы басыңыз 👇"
            if lang == "kz" else
            "💵 *Оплата наличными*\n\n"
            "Согласуйте место и время встречи с менеджером.\n"
            "Нажмите кнопку ниже для связи 👇"
        )
        await query.edit_message_text(text, parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    "📞 Менеджерге хабарласу" if lang == "kz" else "📞 Написать менеджеру",
                    callback_data=f"manager_{lang}"
                ) ]]) )

    # --- БАРТЕР ---
    elif data.startswith("pay_barter_"):
        lang = data.split("_")[-1]
        text = (
            "🔄 *Алмасу / Бартер*\n\n"
            "Бартер ұсынысыңызды жазыңыз — не ұсына аласыз?\n"
            "Менеджер қарастырып, жауап береді 🤝"
            if lang == "kz" else
            "🔄 *Бартер*\n\n"
            "Напишите ваше предложение по бартеру — что вы готовы предложить?\n"
            "Менеджер рассмотрит и ответит вам 🤝"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    # --- СКРИНШОТ ЖІБЕРІЛДІ ---
    elif data.startswith("sent_screenshot_"):
        lang = data.split("_")[-1]
        text = (
            "✅ Рахмет! Скриншотты осы чатқа жіберіңіз.\n"
            "Менеджер 15 минут ішінде байланысады 🙌"
            if lang == "kz" else
            "✅ Спасибо! Пришлите скриншот прямо в этот чат.\n"
            "Менеджер свяжется в течение 15 минут 🙌"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    # --- СҰРАҚ ҚОЮ ---
    elif data.startswith("question_"):
        _, svc_key, lang = data.split("_", 2)
        svc = SERVICES[svc_key]
        text = (
            f"✍️ *{svc[f'name_{lang}']}* бойынша сұрағыңызды жазыңыз.\n\n"
            f"Менеджер жауап береді (09:00–22:00) 🙏"
            if lang == "kz" else
            f"✍️ Напишите вопрос по услуге *{svc[f'name_{lang}']}*.\n\n"
            f"Менеджер ответит (09:00–22:00) 🙏"
        )
        await query.edit_message_text(text, parse_mode="Markdown")

    # --- МЕНЕДЖЕР ---
    elif data.startswith("manager_"):
        lang = data.split("_")[1]
        text = (
            f"📞 *Менеджермен байланыс*\n\n"
            f"📱 Kaspi / WhatsApp: `{KASPI_NUMBER}`\n"
            f"⏰ Жұмыс уақыты: 09:00 – 22:00\n\n"
            f"Немесе осы чатта хабарламаңызды жазыңыз — жауап береміз! 🙌"
            if lang == "kz" else
            f"📞 *Связь с менеджером*\n\n"
            f"📱 Kaspi / WhatsApp: `{KASPI_NUMBER}`\n"
            f"⏰ Режим работы: 09:00 – 22:00\n\n"
            f"Или напишите прямо здесь — обязательно ответим! 🙌"
        )
        await query.edit_message_text(text, parse_mode="Markdown",
                                      reply_markup=back_keyboard(lang))

    # --- АРТҚА ---
    elif data.startswith("back_"):
        lang = data.split("_")[1]
        menu_text = (
            f"🎨 *{BUSINESS_NAME}*\n\nҚандай қызмет қажет? Таңдаңыз 👇"
            if lang == "kz" else
            f"🎨 *{BUSINESS_NAME}*\n\nКакая услуга вас интересует? Выберите 👇"
        )
        await query.edit_message_text(menu_text, parse_mode="Markdown",
                                      reply_markup=main_menu_keyboard(lang))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кез-келген хабарламаны (скриншот, мәтін, дауыс) adminге жіберу"""
    user = update.effective_user
    chat_id = update.effective_chat.id
    msg = update.message

    # Adminге хабар жіберу
    notify = (
        f"📩 *Жаңа хабарлама!*\n"
        f"👤 {user.full_name} (@{user.username or '—'})\n"
        f"🆔 Chat ID: `{chat_id}`"
    )
    await context.bot.send_message(ADMIN_ID, notify, parse_mode="Markdown")
    await context.bot.forward_message(ADMIN_ID, chat_id, msg.message_id)

    # Клиентке автожауап
    if msg.photo:
        reply = (
            "✅ Скриншот алынды! Менеджер 15 минут ішінде тексеріп, байланысады. / "
            "✅ Скриншот получен! Менеджер проверит и свяжется в течение 15 минут."
        )
    elif msg.voice or msg.audio:
        reply = (
            "🎙 Дауыстық хабарлама алынды! Тыңдап жауап береміз. / "
            "🎙 Голосовое сообщение получено! Прослушаем и ответим."
        )
    else:
        reply = (
            "✅ Хабарламаңыз алынды! Менеджер жауап береді (09:00–22:00). / "
            "✅ Сообщение получено! Менеджер ответит (09:00–22:00)."
        )
    await msg.reply_text(reply)

# ========================
# 🚀 ІСКЕ ҚОСУ
# ========================
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))
    print(f"✅ «{BUSINESS_NAME}» боты іске қосылды!")
    app.run_polling()

if __name__ == "__main__":
    main()
