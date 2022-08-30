from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import bot
from keyboard.client_kb import cancel_markup, gender_markup


class FSMAdmin(StatesGroup):  # Finite State Machine
    photo = State()
    name = State()
    age = State()
    gender = State()
    region = State()


async def fsm_start(message: types.Message):
    if message.chat.type == "private":
        await FSMAdmin.photo.set()
        await message.answer(f"Привет {message.from_user.full_name} "
                             f"скинь фотку ...",
                             reply_markup=cancel_markup)
    else:
        await message.reply("Пиши в личку!")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = f"@{message.from_user.username}"
        data['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Как звать?")


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer("Какого года?")


async def load_age(message: types.Message, state: FSMContext):
    try:
        if int(message.text) < 2008 and int(message.text) < 1950:
            await message.answer("Доступ запрещен")
        else:
            async with state.proxy() as data:
                data['age'] = 2022 - int(message.text)
            await FSMAdmin.next()
            await message.answer("Какой пол?", reply_markup=gender_markup)
    except:
        await message.answer("Пиши числа!!!!")


async def load_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
    await FSMAdmin.next()
    await message.answer("Какой регион?")


async def load_region(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['region'] = message.text
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=f"Name: {data['name']}\n"
                                     f"Age: {data['age']}\n"
                                     f"Gender: {data['gender']}\n"
                                     f"Region: {data['region']}\n\n"
                                     f"{data['username']}")
    await state.finish()
    await message.answer("Все свободен )")


async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer("Регистрация отменена!")


def register_handlers_fsmanketa(dp: Dispatcher):
    dp.register_message_handler(cancel_registration, state='*', commands='cancel')
    dp.register_message_handler(cancel_registration,
                                Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_gender, state=FSMAdmin.gender)
    dp.register_message_handler(load_region, state=FSMAdmin.region)