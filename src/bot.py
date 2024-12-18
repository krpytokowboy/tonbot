# Logging module
import logging

# Aiogram imports
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Local modules to work with Database and Ton network
import config
import ton
import db


# Now all the info about bot work will be printed out to console
logging.basicConfig(level=logging.INFO)

# Initialize the bot and dispatcher
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def welcome_handler(message: types.Message):
    # Function that sends the welcome message with main keyboard to user

    uid = message.from_user.id  # Not neccessary, just to make code shorter

    # If user doesn't exist in database, insert it
    if not db.check_user(uid):
        db.add_user(uid)

    # Keyboard with two main buttons: Deposit and Balance
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Invest'))
    keyboard.row(KeyboardButton('Balance'))

    # Send welcome text and include the keyboard
    await message.answer('Hi! I am NiftyBot.\n\n'
                         'How can I help you today?',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands='balance')
@dp.message_handler(Text(equals='balance', ignore_case=True))
async def balance_handler(message: types.Message):
    # Function that shows user his current balance

    uid = message.from_user.id

    # Get user balance from database
    # Also don't forget that 1 TON = 1e9 (billion) NanoTON
    user_balance = db.get_balance(uid) / 1e9

    # Format balance and send to user
    await message.answer(f'Your balance: *{user_balance:.2f} TON*',
                         parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands='invest')
@dp.message_handler(Text(equals='invest', ignore_case=True))
async def deposit_handler(message: types.Message):
    # Function that gives user the address to deposit

    uid = message.from_user.id

    # Keyboard with deposit URL
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Invest',
                                  url=f'ton://transfer/{config.DEPOSIT_ADDRESS}?=text{uid}')
    
    # keyboard.add(button)

    # Send text that explains how to make a deposit
    await message.answer('Simply send any amount of TON to this address:',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)
    
    await message.answer(f'`{config.DEPOSIT_ADDRESS}`',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)

    await message.answer(f'And include the following comment:',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)

    await message.answer(f'`{uid}`',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)
                         
            
if __name__ == '__main__':
    # Create Aiogram executor for our bot
    ex = executor.Executor(dp)

    # Launch the deposit waiter with our executor
    ex.loop.create_task(ton.start())

    # Launch the bot
    ex.start_polling()
