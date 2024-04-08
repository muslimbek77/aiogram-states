import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,F #new
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from mystates import Register

TOKEN = "6633348199:AAFBgQYrgCeWDRt6GUgy118vwtk5Y1hTgiY"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    full_name = message.from_user.full_name
    text = f"Salom {full_name}, Bu bizning birinchi botimiz"
    await message.answer(text)

@dp.message(Command("reg"))
async def register(message:Message,state:FSMContext):
    await message.answer(text = "Siz bizning kurslarimizga yozilish uchun ismingizni kiriting")
    await state.set_state(Register.first_name)

@dp.message(F.text,Register.first_name)
async def register_first_name(message:Message,state:FSMContext):
    first_name = message.text
    await message.answer(text = "Familyangizni kiriting")

    await state.update_data(first_name=first_name)
    await state.set_state(Register.last_name)

@dp.message(Register.first_name)
async def register_first_name_error(message:Message,state:FSMContext):
    await message.answer(text = "Ismingizni to'g'ri kiriting")
    await message.delete()



@dp.message(F.text,Register.last_name)
async def register_last_name(message:Message,state:FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await state.set_state(Register.phone_number)
    await message.answer(text = "Telefon nomeringizni kiriting")


@dp.message(F.text.regexp(r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"),Register.phone_number)
async def register_phone_number(message:Message,state:FSMContext):
    phone_number = message.text
    await state.update_data(phone_number=phone_number)
    await state.set_state(Register.photo)
    await message.answer(text = "Rasimingizni yuboring")
    
@dp.message(Register.phone_number)
async def register_phone_number_error(message:Message,state:FSMContext):
    await message.answer(text = "Telefon raqamingizni to'g'ri kiriting")
    await message.delete()

@dp.message(F.photo,Register.photo)
async def register_phone_number(message:Message,state:FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo_id=photo_id)
    await state.set_state(Register.course)
    await message.answer(text = "qaysi kursda o'qimoqchisiz")

@dp.message(F.text,Register.course)
async def register_course(message:Message,state:FSMContext):
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    photo_id = data.get("photo_id")
    course = message.text
    text = f"Yangi o'quvchi ro'yhatdan o'tdi:\nIsmi:{first_name}\nFamilyasi:{last_name}\nTel raqami:{phone_number}\nTanlagan kursi:{course}"
    await message.answer("Siz muvaffaqiyatli royhatdan o'tdingiz")

    await bot.send_photo(chat_id=999588837,photo=photo_id,caption=text)
    state.clear()

async def main():
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())