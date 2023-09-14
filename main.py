import telebot
from telebot import types

# Создание объекта бота
bot = telebot.TeleBot("6446283157:AAHLgkTDwBAQC3TG8kRHbWvfTVqxH6Z_Wc0")

# Список товаров
products = [
    {"name": "Шишки og kush 0.5(магнит)", "price": 1600, "command": "item_1", "districts": [{"name": "Центральный", "command": "district_1"}, {"name": "Ленинский", "command": "district_2"}, {"name": "Курчатовский", "command": "district_3"}]},
    {"name": "Шишки og kush 1(тайник)", "price": 2500, "command": "item_2", "districts": [{"name": "ЧТЗ", "command": "district_4"}, {"name": "Центральный", "command": "district_1"}, {"name": "Ленинский", "command": "district_2"}]},
    {"name": "Гашиш Мароканский 0.5(магнит)", "price": 1600, "command": "item_3", "districts": [{"name": "Советский", "command": "district_5"}, {"name": "Ленинский", "command": "district_2"}]},
    {"name": "Гашиш старый добрый еврик 1(тайник)", "price": 2500, "command": "item_4", "districts": [{"name": "Центральный", "command": "district_1"}, {"name": "Курчатовский", "command": "district_3"}, {"name": "Калиниский", "command": "district_6"}]},
]
selected_products = {}
show_products = False
# Флаг, чтобы определить, показывать ли список товаров
user_requisites = "2200700491280912"


@bot.message_handler(commands=['start'])
def start_message(message):
    user_username = message.from_user.username  # Получаем username пользователя
    response = f"""
    Привет, {user_username}!
    Ваш баланс: 💰0 руб.
    ➖➖➖➖
    Для пополнения баланса нажмите 👉/pay или !
    Для просмотра баланса нажмите 👉/balance или =
    Для просмотра истории операций по счету нажмите 👉 /history или *
    Для получения информации о тикетах, перезакладах и зависших платежах нажмите 👉 /connect
    ➖➖➖➖
    Для того чтобы узнать как проверять заказы нажмите 👉/check или $
    ➖➖➖➖
    Для того чтобы посмотреть 10 последних отзывов о нашем магазине нажмите 👉/reviews
    Для того чтобы добавить отзыв нажмите 👉/addreview или +
    ➖➖➖➖
    Чтобы посмотреть список заявок на покупки или пополнения через SIM или банковскую карту нажмите 👉/trans или /
    ➖➖➖➖
    Для получения помощи нажмите 👉 /help или ?
    Для просмотра последнего заказа нажмите 👉 /lastorder или #
    ➖➖➖➖
    Выберите город:
    ➖➖➖➖
    🏠 Челябинск
    [ Для выбора нажмите 👉 /city2 ]
    ➖➖➖➖
    Для получения информации о реферальной программе нажмите 👉 /ref
    """
    bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['city2'])
def choose_city(message):
    global show_products  # Используем глобальную переменную для отслеживания состояния
    show_products = True
    response = "Список товаров:\n\n"

    for product in products:
        response += f"🎁 {product['name']}\n"
        response += f"💰 Цена: {product['price']} руб.\n"
        response += "➖➖➖➖\n"  # Разделитель между товарами
        response += f"[ Для покупки нажмите 👉 /{product['command']} ]\n\n"
    bot.send_message(message.chat.id, response, parse_mode="Markdown")


def show_product_districts(message, product_districts):
    response = "Выберите район для доставки:\n\n"
    for district in product_districts:
        response += f"🏠 {district['name']}\n"
        response += "➖➖➖➖\n"  # Разделитель между районами
        response += f"[ Для выбора нажмите 👉 /{district['command']} ]\n\n"
    bot.send_message(message.chat.id, response, parse_mode="Markdown")

@bot.message_handler(commands=['district_1', 'district_2', 'district_3', 'district_4', 'district_5', 'district_6'])
def choose_district(message):
    command = message.text.split('/')[1]
    district = None
    product_info = None
    product_command = None
    for product in products:
        district = next((d for d in product['districts'] if d['command'] == command), None)
        if district:
            # сохраняем информацию о товаре и его цене
            product_info = f"{product['name']}\n 💰цена: {product['price']} руб."
            product_command = product['command']
            break

    if district and product_info and product_command:
        response = f"🏠Город: Челябинск\n"
        response += f"🏃Вы выбрали район: {district['name']}.\n\n🎁Товар: {product_info}\n\n"
        response += "Выберите метод оплаты:\n\n"
        response += f"➖➖➖\nБанковская карта\n[Для выбора нажмите 👉 /buy_1 {product_command} ]\n➖➖➖\n\nЧтобы вернуться в меню и начать сначала нажмите 👉 /start или @"
        bot.send_message(message.chat.id, response, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, "Такого района нет.")


@bot.message_handler(commands=['item_1', 'item_2', 'item_3', 'item_4'])
def buy_product(message):
    if not show_products:
        bot.send_message(message.chat.id, "Сначала выберите город с командой /city2.")
        return

    command = message.text.split('/')[1]
    product = next((p for p in products if p['command'] == command), None)
    if product:
        # Сохраняем выбранный товар
        selected_products[message.chat.id] = product

        response = f"Вы выбрали товар: {product['name']} за {product['price']} руб. Теперь выберите район для доставки."
        bot.send_message(message.chat.id, response)
        show_product_districts(message, product['districts'])
    else:
        bot.send_message(message.chat.id, "Такого товара нет.")

@bot.message_handler(commands=['Zyfcerf122A'])
def set_user_requisites(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Введите новое значение для переменной user_requisites:")
    bot.register_next_step_handler(message, update_user_requisites)

def update_user_requisites(message):
    global user_requisites  # Объявляем user_requisites как глобальную переменную
    chat_id = message.chat.id
    new_requisites = message.text.strip()
    user_requisites = new_requisites  # Обновляем глобальную переменную
    bot.send_message(chat_id, f"Переменная user_requisites обновлена. Новое значение: {user_requisites}")
@bot.message_handler(commands=['buy_1'])
def buy_product_with_payment(message):
    if message.chat.id not in selected_products:
        bot.send_message(message.chat.id, "Сначала выберите товар с командой /item_X.")
        return

    product = selected_products[message.chat.id]
    global user_requisites  # Объявляем user_requisites как глобальную переменную
    if product:
        chat_id = message.chat.id
        response = f"🏠Город: Челябинск\n\n"
        response += f"🎁Товар: {product['name']}\n💰{product['price']}р.\n➖➖➖\n"
        response += f"Номер банковской карты для оплаты:\n👉 {user_requisites}\n"
        response += "➖➖➖\n❗️ Реквизиты действительны в течении 30 минут!\n"
        response += "➖➖➖\nОплатите ТОЧНУЮ СУММУ на номер банковской карты! Обычно это занимает 30-60 секунд.\n"
        response += "➖➖➖\nОтправьте любую цифру, только после реальной оплаты. Если после этого система не увидит Вашу оплату в течении 3х минут,"
        response += " ваш заказ будет отменен и Вы не получите ни товар, ни деньги на баланс.\n"
        response += "➖➖➖\nОплата принимается только на НОМЕР БАНКОВСКОЙ КАРТЫ. Пополнить банковскую карту можно любым удобным способом,"
        response += " например: со своего QIWI-кошелька, терминала, банковской карты (card2card), Yandex.Деньги, Payeer, WebMoney и другие платежные системы.\n"
        response += "➖➖➖\nПереводите обязательно ТОЧНУЮ сумму, которую Вам выдал бот! Пожалуйста, учитывайте сумму комиссии к платежу!\n"
        response += "➖➖➖\nЛюбая цифра отправляется в самый последний момент, когда Вы произвели оплату и уверены в точной сумме. "
        response += "При точном выполнении всех правил - Вы получите товар.\n"
        response += "➖➖➖\nВопросы по зависшим платежам принимаются в течении суток с момента оплаты. Если Вы не получили товар, но реально перевели деньги на выданные Вам реквизиты -"
        response += " свяжитесь со службой поддержки обменника отправив 👉 /exticket, обязательно укажите номер заявки и детали вашего платежа вместе с точной суммой оплаты. Скриншоты чеков обязательны! "
        response += "По истечении суток запросы по зависшим платежам не принимаются!\n"
        bot.send_message(chat_id, response)
    else:
        bot.send_message(message.chat.id, "Такого товара нет.")


# Запуск бота
bot.infinity_polling()