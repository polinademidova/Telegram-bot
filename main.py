from pyrogram import Client, filters
from pyrogram.types import ForceReply

import config
import datetime
import keyboards
import random

import json
import base64
from FushionBrain_AI import generate

bot = Client(
    api_id = config.API_ID,
    api_hash = config.API_HASH,
    bot_token = config.BOT_TOKEN,
    name = 'prosto_lipton_bot'
)
stickers = [ 'CAACAgIAAxkBAAENLe1nPfurZ4yizi9z9QxvUCfqc1FWGgAC9wADVp29CgtyJB1I9A0wNgQ',
            'CAACAgIAAxkBAAENMepnQI5pDdpZDraNQzyV0UZ_RFRalgACAQ8AAulVBRj8cJCcySLCgjYE',
            'CAACAgIAAxkBAAENMexnQI60CyGw83VdS9pavC2YSHUnxgACvDMAArtcAUhmByJnUyKZBTYE',
            'CAACAgIAAxkBAAENPrxnSheyx2JNJxD0NeMml8Rq01SDvAACtj4AArkHyUrNyEKw2u2OqDYE',
            'CAACAgIAAxkBAAENPr5nShfxzbRNBu_cz5YcrbGz8ci7FAACJD8AAlUDaEgBW9n4mcteezYE',
            'CAACAgIAAxkBAAENMchnQHs96q-fu4stZw9R6hYlxZcvogACRF4AAi3haEi5O6MC2jMvlTYE'
             ]

def button_filter(button):
   async def func(_, __, msg):
       return msg.text == button.text
   return filters.create(func, "ButtonFilter", button=button)

@bot.on_message(filters.command('start'))
async def start(bot, message):
    await message.reply('Добро пожаловать!',
                        reply_markup=keyboards.kb_main)
    with open ('users.json', 'r') as file:
        users = json.load(file)
    if str(message.from_user.id) not in users.keys():
        users[message.from_user.id] = 100
        with open('users.json', 'w') as file:
            json.dump(users, file)

@bot.on_message(filters.command('info') | button_filter(keyboards.btn_info))
async def info(bot, message):
    await message.reply('Привет! Тут описание что может этот бот и список команд')

@bot.on_message(filters.command('games') | button_filter(keyboards.btn_games))
async def games(bot, message):
    await message.reply('Выбери игру', reply_markup=keyboards.kb_games)

@bot.on_message(filters.command('time')  | button_filter(keyboards.btn_time))
async def time(bot, message):
    date_time = datetime.datetime.now()
    formatted_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
    await message.reply(f"Текущие дата и время: {formatted_time}")

@bot.on_message(filters.command('back') | button_filter(keyboards.btn_back))
async def back(bot, message):
    await message.reply('Вернуться в главное меню', reply_markup=keyboards.kb_main)

@bot.on_message(filters.command("image"))
async def image(bot, message):
    if len(message.text.split()) > 1:
        query = message.text.replace('/image', '')
        await message.reply_text(f"Генерирую изображение по запросу '{query}' \nОжидание около минуты")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg', reply_to_message_id=message.id)
        else:
            await message.reply_text("Возникла ошибка, попробуйте еще раз", reply_to_message_id=message.id)
    else:
        await message.reply_text("Введите запрос")

query_text = 'Введи запрос для генерации изображения'
@bot.on_message(button_filter(keyboards.btn_image))
async def image2(bot, message):
    await bot.send_message(message.chat.id, query_text, reply_markup=ForceReply(True))
@bot.on_message(filters.reply)
async def reply(bot, message):
    if message.reply_to_message.text == query_text:
        query = message.text
        await message.reply_text(f"Генерирую изображение по запросу **{query}**. Ожидание около минуты")
        images = await generate(query)
        if images:
            image_data = base64.b64decode(images[0])
            img_num = random.randint(1, 99)
            with open(f"images/image{img_num}.jpg", "wb") as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, f'images/image{img_num}.jpg', reply_to_message_id=message.id, reply_markup=keyboards.kb_main)
        else:
            await message.reply_text("Возникла ошибка, попробуйте еще раз", reply_to_message_id=message.id, reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('game') | button_filter(keyboards.btn_rps))
async def back(bot, message):
    with open ('users.json', 'r') as file:
        users = json.load(file)
    if users[str(message.from_user.id)] >= 10:
        await message.reply('Выбери чем будешь ходить', reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f"На твоем счету недостаточно средств. На твоем счету {users[str(message.from_user.id)]}. Мин.сумма для игры - 10.")

@bot.on_message(button_filter(keyboards.btn_rock) | button_filter(keyboards.btn_scissors) | button_filter(keyboards.btn_paper) )
async def choice_rps(bot, message):
    with open ('users.json', 'r') as file:
        users = json.load(file)

    rock = keyboards.btn_rock.text
    scissors = keyboards.btn_scissors.text
    paper = keyboards.btn_paper.text

    user = message.text
    pc = random.choice([rock, scissors, paper])

    if user==pc:
        await message.reply('Ничья')
    elif (user==rock and pc==paper) or (user==scissors and pc==rock) or (user==paper and pc==scissors):
        await message.reply(f'Ты проиграл :( бот выбрал {pc}', reply_markup = keyboards.kb_games)
        users[str(message.from_user.id)] += 10
    else:
        await message.reply(f'Ты выиграл :) бот выбрал {pc}', reply_markup = keyboards.kb_games)
        users[str(message.from_user.id)] -= 10
    with open('users.json', 'w') as file:
        json.dump(users, file)

@bot.on_message(filters.command('quest') | button_filter(keyboards.btn_quest))
async def kvest(bot, message):
    await message.reply_text('Хотите ли вы отправиться в увлекательное путешествие с неожиданными поворотами и загадками?)',
                             reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(bot, query):
    if query.data == "start_quest":
        await bot.answer_callback_query(query.id,
        text='Добро пожаловать в Квест под названием Грехи и Желания! ',
        show_alert=True)
        await query.message.reply_text('Ты стоишь перед 2умя дверьми. Какую из них выберешь?',
        reply_markup = keyboards.inline_kb_choice_door)

    elif query.data == "left_door":
        await query.message.reply_text('Ты попал в комнату с грехами. Выбери один, чтобы пройти дальше',
        reply_markup = keyboards.inline_kb_left_door)

    elif query.data == "right_door":
        await query.message.reply_text('Ты попал в комнату к фее и принцессе. Выбери одну из них.',
        reply_markup = keyboards.inline_kb_right_door)

    elif query.data == 'fairy':
        await query.message.reply_text('Фея может исполнить одно из трех желаний. Выбери какое оно будет?',
        reply_markup = keyboards.inline_kb_wishes)

    elif query.data == 'hamburger':
        await bot.answer_callback_query(query.id, text='Ты слишком много ешь, отчего больше не в состоянии ходить. Ты остаешься в этой комнате до конца жизни', show_alert=True)

    elif query.data == 'rage':
        await bot.answer_callback_query(query.id, text='Твоя ярость не знает границ, из-за чего тебя изгоняют из квеста навсегда', show_alert=True)

    elif query.data == 'face_with_rolling_eyes':
        await bot.answer_callback_query(query.id, text='Ты ничего не получаешь от этого и не проходишь дальше', show_alert=True)

    elif query.data == 'princess':
        await bot.answer_callback_query(query.id, text='Принцесса оказалась оборотнем, который убивает тебя', show_alert=True)

    elif query.data == 'crown':
        await bot.answer_callback_query(query.id, text='Народ устроил революцию и тебя свергли. К сожалению, ты проиграл', show_alert=True)

    elif query.data == 'heart':
        await bot.answer_callback_query(query.id, text='Ты находишь любовь всей своей жизни, вы вместе выходите из комнаты. Ты выиграл!', show_alert=True)

    elif query.data == 'star_struck':
        await bot.answer_callback_query(query.id, text='Твоя популярность испортила тебя и ты начал вести пагубный образ жизни. Ты не проходишь дальше', show_alert=True)

@bot.on_message(filters.command('echo'))
async def echo(bot, message):
    if message.text.lower() == "привет":
        await message.reply('Привет :)')
    elif message.text.lower() == 'пока':
        await message.reply('Пока!')
    else:
        await message.reply(f'Ты написал {message.text}')


@bot.on_message(filters.command('sticker'))
async def sticker(bot, message):
    await bot.send_sticker(message.chat.id, random.choice(stickers))

bot.run()
