from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

# запуск своего телеграмбота
api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

"""
инициализация клавиатуры, где параметры:
row_width - количество столбцов кнопок, (int)
resize_keyboard - будет ли клавиатура растягиваться, (bool)
one_time_keyboard - разовая ли клавиатура, (bool)
"""
kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)

# инициализация самих кнопок
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')

# расположение кнопок в линию
kb.row(button_1, button_2)


@dp.message_handler(commands=['start'])
async def start(message):
    print('Кто-то вошел в бот')
    await message.answer(f'Привет!\nЯ бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    print('Поступил запрос на расчет Calories')
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    # для мужчин: 10 х вес(кг) + 6,25 x рост(см) – 5 х возраст(г) + 5
    await message.answer(f'Ваша норма каллорий (для мужчин) '
                         f'{10 * int(data["first"]) + 6.25 * int(data["second"]) - 5 * int(data["third"]) + 5}')
    # для женщин: 10 x вес(кг) + 6,25 x рост(см) – 5 x возраст(г) – 161
    await message.answer(f'Ваша норма каллорий (для женщин) '
                         f'{10 * int(data["first"]) + 6.25 * int(data["second"]) - 5 * int(data["third"]) - 161}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
