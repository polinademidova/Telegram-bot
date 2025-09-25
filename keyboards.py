from pyrogram.types import KeyboardButton
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import emoji

btn_info = KeyboardButton(f'{emoji.INFORMATION} Инфо')
btn_games = KeyboardButton(f'{emoji.VIDEO_GAME} Игры')
btn_profile = KeyboardButton(f'{emoji.PERSON} Профиль')

btn_time = KeyboardButton(f'{emoji.TIMER_CLOCK} Время')
btn_image = KeyboardButton(f'{emoji.FRAMED_PICTURE} Сгенерировать изображение')

btn_rps = KeyboardButton(f'{emoji.PLAY_BUTTON} Камень-Ножницы-Бумага')
btn_quest = KeyboardButton(f'{emoji.CITYSCAPE_AT_DUSK} Квест')
btn_back = btn_profile = KeyboardButton(f'{emoji.BACK_ARROW} Назад')

btn_rock = KeyboardButton(f'{emoji.ROCK} Камень')
btn_scissors = KeyboardButton(f'{emoji.SCISSORS} Ножницы')
btn_paper = KeyboardButton(f'{emoji.NOTEBOOK} Бумага')

kb_main = ReplyKeyboardMarkup(
    keyboard=[
            [btn_info, btn_games],
            [btn_profile, btn_image, btn_time],
        ],
    resize_keyboard=True
)

kb_games = ReplyKeyboardMarkup(
    keyboard=[
            [btn_rps],
        [btn_quest, btn_back]
        ],
    resize_keyboard=True
)

kb_rps = ReplyKeyboardMarkup(
    keyboard=[
            [btn_rock, btn_scissors, btn_paper],
            [btn_back]
        ],
    resize_keyboard=True
)
inline_kb_start_quest = InlineKeyboardMarkup([
    [InlineKeyboardButton('Пройти квест',
                          callback_data = 'start_quest')]
])
inline_kb_choice_door= InlineKeyboardMarkup ([
    [InlineKeyboardButton('🚪⬅️Левая дверь', callback_data='left_door')],
    [InlineKeyboardButton('➡️🚪Правая дверь', callback_data='right_door')]
    ])

inline_kb_left_door= InlineKeyboardMarkup ([
    [InlineKeyboardButton('🍔Чревоугодие', callback_data='hamburger')],
    [InlineKeyboardButton('😡Гнев', callback_data='rage')],
    [InlineKeyboardButton('🙄Гордыня', callback_data='face_with_rolling_eyes')]
    ])

inline_kb_right_door= InlineKeyboardMarkup ([
    [InlineKeyboardButton('🧚🏻Загадать желание у феи', callback_data='fairy')],
    [InlineKeyboardButton('👸🏼Пойти с прекрасной принцессой', callback_data='princess')]
    ])

inline_kb_wishes= InlineKeyboardMarkup ([
    [InlineKeyboardButton('👑Власть', callback_data='crown')],
    [InlineKeyboardButton('❤️Любовь', callback_data='heart')],
    [InlineKeyboardButton('🤩Популярность', callback_data='star_struck')]
    ])