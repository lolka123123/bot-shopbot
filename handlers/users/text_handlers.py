from data.loader import dp, bot, db
from aiogram.types import Message
from states.states import NumberState
from aiogram.dispatcher import FSMContext
import re
import time
from random import randint
from data.languages import LANGUAGES, check_language, check_products_translate, make_product_title
from data.config import PHONE_RESULTS, GRADES, unix_in_time, product_caption, cart_products_list, branches_list, \
    final_caption, check_location
from keyboards.inline import generate_choose_language, generate_change_language, generate_product_detail, \
    generate_reconstruct_product, generate_final_confirm
from keyboards.reply import generate_clean, generate_main_menu, generate_settings, generate_reviews, \
    generate_change_phone, generate_back, generate_change_phone_code, generate_categories, generate_products, \
    generate_product_keyboard, generate_cart_products, generate_delivery_type, generate_branches, generate_time_order, \
    generate_make_comment, generate_payment_method, generate_final_menu, generate_get_location

async def start_language(message: Message, state=None):
    # chat_id = message.chat.id
    # message_id = message.message_id
    # await NumberState.language.set()
    await message.answer('Выберите язык:\nChoose language:', reply_markup=generate_choose_language(LANGUAGES))

@dp.message_handler(state=NumberState.get_phone, content_types=['text', 'contact'])
async def get_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang = data['lang']
        found = False
        if message.text == check_language(lang, 'back_btn'):
            await state.finish()
            await start_language(message)
        else:
            if message.content_type == 'text':
                sent_phone = message.text
            else:
                if '+' in message.contact.phone_number:
                    sent_phone = message.contact.phone_number
                else:
                    sent_phone = '+' + message.contact.phone_number
            for phone_result in PHONE_RESULTS:
                result = re.search(phone_result, sent_phone)
                if result:
                    phone = ''
                    if '+998' in sent_phone:
                        lst = sent_phone.split(' ')
                        for i in lst:
                            phone += i
                    else:
                        lst = sent_phone.split(' ')
                        phone += '+998'
                        for i in lst:
                            phone += i

                    if bool(db.get_code_attempts_by_phone(phone)) == False:
                        db.insert_code_attempt(phone, 5, 0)

                    if list(db.get_code_attempts_by_phone(phone))[1] <= 0:  # условие не сробатывает
                        await state.finish()
                        send_code_limit = check_language(lang, 'send_code_limit')
                        await message.answer(f'{send_code_limit}')
                        await start_language(message)
                    else:
                        last_change_date = list(db.get_code_attempts_by_phone(phone))[2]
                        if last_change_date + 60 <= message.date.timestamp() or last_change_date == 0:  # основной код
                            attempts = list(db.get_code_attempts_by_phone(phone))[1] - 1
                            db.update_code_attempt_by_phone(phone, attempts, int(message.date.timestamp()))

                            answer = ''

                            for i in range(4):  # 4 значный код
                                random_num = str(randint(0, 9))
                                answer += random_num

                            print(f'{message.chat.id} - {phone} - {answer}')

                            code_attempts = 3

                            async with state.proxy() as data:
                                data['phone'] = phone
                                data['answer'] = answer
                                data['code_attempts'] = code_attempts

                            await NumberState.get_phone_code.set()

                            send_code = check_language(lang, 'send_code')
                            sent_your_phone = check_language(lang, 'sent_your_phone')
                            await message.answer(f'{sent_your_phone}: {phone}\n{send_code} 1234',
                                                 reply_markup=generate_change_phone_code(lang))

                        else:  # условие не сробатывает
                            await state.finish()
                            cooldown_time = (last_change_date + 60) - int(message.date.timestamp())
                            send_code_cooldown = check_language(lang, 'send_code_cooldown')
                            await message.answer(f'{send_code_cooldown}: {unix_in_time(cooldown_time)}')
                            await start_language(message)

                    found = True
                    break
            if found == False:
                # await state.finish()
                await again_ask_phone(message, lang)

async def again_ask_phone(message: Message, lang, state=None):
    # await NumberState.get_phone.set()
    ask_phone_mistake = check_language(lang, 'ask_phone_mistake')

    await message.answer(f'{ask_phone_mistake}')


@dp.message_handler(state=NumberState.get_phone_code)
async def get_code(message: Message, state: FSMContext):
    code = message.text
    async with state.proxy() as data:
        answer = data['answer']
        phone = data['phone']
        lang = data['lang']
        code_attempts = data['code_attempts']
        if message.text == check_language(lang, 'back_btn'): # назад
            await state.finish()
            await start_language(message)

        elif message.text == check_language(lang, 'settings_send_phone_code'):
            if list(db.get_code_attempts_by_phone(phone))[1] <= 0:  # условие не сробатывает
                await state.finish()
                send_code_limit = check_language(lang, 'send_code_limit')
                await message.answer(f'{send_code_limit}')
                await start_language(message)
            else:
                last_change_date = list(db.get_code_attempts_by_phone(phone))[2]
                if last_change_date + 60 <= message.date.timestamp() or last_change_date == 0: # основной код
                    await state.finish()
                    await NumberState.get_phone_code.set()
                    attempts = list(db.get_code_attempts_by_phone(phone))[1] - 1
                    db.update_code_attempt_by_phone(phone, attempts, int(message.date.timestamp()))

                    answer = ''
                    for i in range(4):  # 4 значный код
                        random_num = str(randint(0, 9))
                        answer += random_num

                    print(f'{message.chat.id} - {phone} - {answer}')

                    code_attempts = 3

                    data['answer'] = answer
                    data['phone'] = phone
                    data['code_attempts'] = code_attempts

                    send_code_again = check_language(lang, 'send_code_again')
                    sent_your_phone = check_language(lang, 'sent_your_phone')
                    await message.answer(f'{sent_your_phone}: {phone}\n{send_code_again} 1234',
                                         reply_markup=generate_change_phone_code(lang))
                else: # условие не сробатывает
                    await NumberState.get_phone_code.set()

                    cooldown_time = (last_change_date + 60) - int(message.date.timestamp())
                    send_code_cooldown = check_language(lang, 'send_code_cooldown')
                    await message.answer(f'{send_code_cooldown}: {unix_in_time(cooldown_time)}',
                                         reply_markup=generate_change_phone_code(lang))


        else:
            if code_attempts <= 0: # условие не сробатывает
                send_code_limit_attempts = check_language(lang, 'send_code_limit_attempts')
                await message.answer(f'{send_code_limit_attempts}')
            else:
                if code == answer:
                    chat_id = message.chat.id
                    full_name = message.from_user.full_name
                    db.insert_user(chat_id, full_name, phone, lang)
                    await state.finish()
                    name = message.from_user.first_name
                    await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                                         reply_markup=generate_main_menu(lang))

                else:
                    data['code_attempts'] -= 1
                    await again_ask_change_phone_code(message, lang)
                    # Написать функцию

async def again_ask_phone_code(message: Message, lang, state=None):
    send_code_mistake = check_language(lang, 'send_code_mistake')
    await message.answer(f'{send_code_mistake}')


# ----------main_menu
for language in LANGUAGES.keys():
    try:
        lang_key = LANGUAGES[language]['main_menu']
        @dp.message_handler(regexp=f'{lang_key}')
        async def show_main_menu(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]
                name = message.from_user.first_name
                await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}', reply_markup=generate_main_menu(lang))
    except:
        continue



# ----------settings
for language in LANGUAGES.keys():
    try:
        generate_main_menu_settings = LANGUAGES[language]['generate_main_menu_settings']
        @dp.message_handler(regexp=f'{generate_main_menu_settings}')
        async def show_settings(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]

                generate_main_menu_settings = check_language(lang, 'generate_main_menu_settings')

                await message.answer(f'{generate_main_menu_settings}', reply_markup=generate_settings(lang))
    except:
        continue


# ----------change_language
for language in LANGUAGES.keys():
    try:
        settings_change_language = LANGUAGES[language]['settings_change_language']
        @dp.message_handler(regexp=f'{settings_change_language}')
        async def change_language(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]

                chat_id = message.chat.id
                message_id = message.message_id

                settings_ask_language = check_language(lang, 'settings_ask_language')

                await message.answer(text='.', reply_markup=generate_clean())

                await bot.delete_message(chat_id, message_id + 1)

                await message.answer(f'{settings_ask_language}', reply_markup=generate_change_language(LANGUAGES))
    except:
        continue



# ----------change_phone
for language in LANGUAGES.keys():
    try:
        settings_change_phone = LANGUAGES[language]['settings_change_phone']
        @dp.message_handler(regexp=f'{settings_change_phone}')
        async def change_phone(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]

                settings_ask_phone = check_language(lang, 'settings_ask_phone')

                await NumberState.change_phone.set()
                await message.answer(f'{settings_ask_phone}', reply_markup=generate_change_phone(lang))
    except:
        continue



@dp.message_handler(state=NumberState.change_phone, content_types=['text', 'contact'])
async def change_phone(message: Message, state: FSMContext):
    if db.get_user_by_id(message.chat.id):
        lang = db.get_language(message.chat.id)[0]
        # print(message)
        found = False
        if message.text == check_language(lang, 'back_btn'):
            await state.finish()
            name = message.from_user.first_name
            await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                                 reply_markup=generate_main_menu(lang))
        else:
            if message.content_type == 'text':
                sent_phone = message.text
            else:
                if '+' in message.contact.phone_number:
                    sent_phone = message.contact.phone_number
                else:
                    sent_phone = '+' + message.contact.phone_number
            for phone_result in PHONE_RESULTS:
                result = re.search(phone_result, sent_phone)
                if result:
                    phone = ''
                    if '+998' in sent_phone:
                        lst = sent_phone.split(' ')
                        for i in lst:
                            phone += i
                    else:
                        lst = sent_phone.split(' ')
                        phone += '+998'
                        for i in lst:
                            phone += i

                    if bool(db.get_code_attempts_by_phone(phone)) == False:
                        db.insert_code_attempt(phone, 5, 0)

                    if list(db.get_code_attempts_by_phone(phone))[1] <= 0:  # условие не сробатывает
                        await state.finish()
                        send_code_limit = check_language(lang, 'send_code_limit')
                        await message.answer(f'{send_code_limit}', reply_markup=generate_main_menu(lang))
                    else:
                        last_change_date = list(db.get_code_attempts_by_phone(phone))[2]
                        if last_change_date + 60 <= message.date.timestamp() or last_change_date == 0:  # основной код

                            attempts = list(db.get_code_attempts_by_phone(phone))[1] - 1
                            db.update_code_attempt_by_phone(phone, attempts, int(message.date.timestamp()))

                            answer = ''
                            for i in range(4):  # 4 значный код
                                random_num = str(randint(0, 9))
                                answer += random_num

                            print(f'{message.chat.id} - {phone} - {answer}')

                            code_attempts = 3

                            async with state.proxy() as data:
                                data['phone'] = phone
                                data['answer'] = answer
                                data['code_attempts'] = code_attempts

                            await NumberState.change_phone_code.set()

                            send_code = check_language(lang, 'send_code')
                            sent_your_phone = check_language(lang, 'sent_your_phone')
                            await message.answer(f'{sent_your_phone}: {phone}\n{send_code} 1234',
                                                 reply_markup=generate_change_phone_code(lang))

                        else:  # условие не сробатывает
                            await state.finish()
                            cooldown_time = (last_change_date + 60) - int(message.date.timestamp())
                            send_code_cooldown = check_language(lang, 'send_code_cooldown')
                            await message.answer(f'{send_code_cooldown}: {unix_in_time(cooldown_time)}',
                                                 reply_markup=generate_main_menu(lang))

                    found = True
                    break

            if found == False:
                # await state.finish()
                await again_ask_change_phone(message, lang)


async def again_ask_change_phone(message: Message, lang, state=None):
    ask_phone_mistake = check_language(lang, 'ask_phone_mistake')
    # await NumberState.change_phone.set()
    await message.answer(f'{ask_phone_mistake}')

@dp.message_handler(state=NumberState.change_phone_code)
async def change_phone_code(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]
    code = message.text
    async with state.proxy() as data:
        answer = data['answer']
        phone = data['phone']
        code_attempts = data['code_attempts']
        if message.text == check_language(lang, 'back_btn'): # назад
            await state.finish()
            name = message.from_user.first_name
            await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                                 reply_markup=generate_main_menu(lang))
        elif message.text == check_language(lang, 'settings_send_phone_code'): # переслать код
            if list(db.get_code_attempts_by_phone(phone))[1] <= 0:  # условие не сробатывает
                send_code_limit = check_language(lang, 'send_code_limit')
                await message.answer(f'{send_code_limit}')
            else:
                last_change_date = list(db.get_code_attempts_by_phone(phone))[2]
                if last_change_date + 60 <= message.date.timestamp() or last_change_date == 0:  # основной код
                    await state.finish()
                    await NumberState.change_phone_code.set()

                    attempts = list(db.get_code_attempts_by_phone(phone))[1] - 1
                    db.update_code_attempt_by_phone(phone, attempts, int(message.date.timestamp()))

                    answer = ''
                    for i in range(4):  # 4 значный код
                        random_num = str(randint(0, 9))
                        answer += random_num

                    print(f'{message.chat.id} - {phone} - {answer}')

                    code_attempts = 3

                    data['answer'] = answer
                    data['phone'] = phone
                    data['code_attempts'] = code_attempts

                    send_code_again = check_language(lang, 'send_code_again')
                    sent_your_phone = check_language(lang, 'sent_your_phone')
                    await message.answer(f'{sent_your_phone}: {phone}\n{send_code_again} 1234',
                                         reply_markup=generate_change_phone_code(lang))

                else:  # условие не сробатывает
                    await NumberState.change_phone_code.set()
                    cooldown_time = (last_change_date + 60) - int(message.date.timestamp())
                    send_code_cooldown = check_language(lang, 'send_code_cooldown')
                    await message.answer(f'{send_code_cooldown}: {unix_in_time(cooldown_time)}',
                                         reply_markup=generate_change_phone_code(lang))



        else: # проверка кода
            if code_attempts <= 0: # условие не сробатывает
                send_code_limit_attempts = check_language(lang, 'send_code_limit_attempts')
                await message.answer(f'{send_code_limit_attempts}')
            else:
                if code == answer:
                    chat_id = message.chat.id
                    db.change_phone_num_by_id(phone, chat_id)

                    changed_phone = check_language(lang, 'changed_phone')

                    await state.finish()
                    await message.answer(f'{changed_phone}', reply_markup=generate_main_menu(lang))

                else:
                    data['code_attempts'] -= 1
                    await again_ask_change_phone_code(message, lang)




async def again_ask_change_phone_code(message: Message, lang, state=None):
    send_code_mistake = check_language(lang, 'send_code_mistake')
    await message.answer(f'{send_code_mistake}')


# ----------delivery
for language in LANGUAGES.keys():
    try:
        generate_main_menu_delivery = LANGUAGES[language]['generate_main_menu_delivery']
        @dp.message_handler(regexp=f'{generate_main_menu_delivery}')
        async def show_delivery(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]

                delivery_info = check_language(lang, 'delivery_info')

                await message.answer(f'{delivery_info}', reply_markup=generate_main_menu(lang))
            else:
                pass


    except:
        continue



# ----------contacts
for language in LANGUAGES.keys():
    try:
        generate_main_menu_contacts = LANGUAGES[language]['generate_main_menu_contacts']
        @dp.message_handler(regexp=f'{generate_main_menu_contacts}')
        async def show_contacts(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]

                contacts_info = check_language(lang, 'contacts_info')

                await message.answer(f'{contacts_info}', reply_markup=generate_main_menu(lang))




    except:
        continue



# ----------reviews
for language in LANGUAGES.keys():
    try:
        generate_main_menu_reviews = LANGUAGES[language]['generate_main_menu_reviews']
        @dp.message_handler(regexp=f'{generate_main_menu_reviews}')
        async def show_reviews(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]

                reviews_info = check_language(lang, 'reviews_info')

                await NumberState.get_review.set()
                await message.answer(f'{reviews_info}', reply_markup=generate_reviews(lang))
    except:
        continue

    # ----------reviews_main_menu
    try:
        main_menu = LANGUAGES[language]['main_menu']
        @dp.message_handler(regexp=f'{main_menu}', state=NumberState.get_review)
        async def show_main_menu_from_reviews(message: Message, state: FSMContext):
            await state.finish()
            await show_main_menu(message)
    except:
        continue

    # ----------reviews_grade
    @dp.message_handler(state=NumberState.get_review)
    async def show_review_grade(message: Message, state: FSMContext):
        chat_id = message.chat.id
        lang = db.get_language(message.chat.id)[0]
        for grade_int, grade_text in GRADES.items():
            if message.text == check_language(lang, f'review_{grade_text}'):
                grade = grade_int
                await state.finish()
                await NumberState.get_review_info.set()
                async with state.proxy() as data:
                    data['grade'] = grade
                review_grade_info = check_language(lang, f'review_{grade_text}_info')
                await message.answer(f'{review_grade_info}', reply_markup=generate_back(lang))
        if message.text == check_language(lang, 'review_five'):
            grade = 5
            if db.get_review_by_id(chat_id):
                db.update_review(chat_id, grade, '.')
            else:
                db.insert_review(chat_id, grade, '.')
            await state.finish()
            review_grade_info = check_language(lang, f'review_five_info')
            await message.answer(f'{review_grade_info}', reply_markup=generate_main_menu(lang))




# ----------reviews_info
@dp.message_handler(state=NumberState.get_review_info)
async def show_review_info(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_language(message.chat.id)[0]
    if message.text == check_language(lang, 'back_btn'):
        await state.finish()
        await NumberState.get_review.set()
        await show_reviews(message)
    else:
        async with state.proxy() as data:
            grade = data['grade']
            if db.get_review_by_id(chat_id):
                db.update_review(chat_id, grade, message.text)
            else:
                db.insert_review(chat_id, grade, message.text)

            review_sent = check_language(lang, 'review_sent')
            await state.finish()
            await message.answer(f'{review_sent}')
            name = message.from_user.first_name
            await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                                 reply_markup=generate_main_menu(lang))


@dp.message_handler(regexp=f'test')
async def test(message: Message):
    print(unix_in_time(0))





# ---------menu
for language in LANGUAGES.keys():
    try:
        menu = LANGUAGES[language]['menu']
        @dp.message_handler(regexp=f'{menu}')
        async def show_choice_delivery(message: Message):
            if db.get_user_by_id(message.chat.id):
                lang = db.get_language(message.chat.id)[0]
                await NumberState.choose_category.set()
                menu_chose_categories = check_language(lang, 'menu_choose_categories')
                await message.answer(f'{menu_chose_categories}', reply_markup=generate_categories(lang))
    except:
        continue



@dp.message_handler(state=NumberState.choose_category)
async def show_categories(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]
    chat_id = message.chat.id

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'cart_btn'):
        if db.get_cart_by_id(chat_id):
            await state.finish()
            await NumberState.product_cart.set()
            await message.answer(f'{cart_products_list(lang, chat_id)}', parse_mode='HTML',
                                 reply_markup=generate_cart_products(lang, chat_id))
        else:
            await message.answer(f'<b>{check_language(lang, "cart_empty")}</b>', parse_mode='HTML')
    else:
        cotegories = [i[0] for i in db.get_categories()]
        for cotegory in cotegories:
            if message.text == check_language(lang, f'menu_{cotegory}'):
                await state.finish()
                await NumberState.choose_product.set()
                async with state.proxy() as data:
                    data['cotegory'] = cotegory
                await message.answer(f'{message.text}', reply_markup=generate_products(lang, cotegory))



@dp.message_handler(state=NumberState.choose_product)
async def show_products(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]
    chat_id = message.chat.id
    if message.text == check_language(lang, 'back_btn'):
        await state.finish()
        await NumberState.choose_category.set()
        menu_chose_categories = check_language(lang, 'menu_choose_categories')
        await message.answer(f'{menu_chose_categories}', reply_markup=generate_categories(lang))
    elif message.text == check_language(lang, 'cart_btn'):
        if db.get_cart_by_id(chat_id):
            await state.finish()
            await NumberState.product_cart.set()
            await message.answer(f'{cart_products_list(lang, chat_id)}', parse_mode='HTML',
                                 reply_markup=generate_cart_products(lang, chat_id))
        else:
            await message.answer(f'<b>{check_language(lang, "cart_empty")}</b>', parse_mode='HTML')
    else:
        async with state.proxy() as data:
            cotegory = data['cotegory']
            products_lang = {check_products_translate(lang, i[0]): i[0] for i in db.get_products_by_category(cotegory)}
            for key, value in products_lang.items():
                if message.text == key:
                    await message.answer(message.text, reply_markup=generate_product_keyboard(lang))
                    await NumberState.product_info.set()
                    chat_id = message.chat.id
                    product = db.get_product_by_id(value)

                    if product[3]:
                        title = f'{check_products_translate(lang, product[0])}, {check_language(lang, "product_size_large")}, {check_language(lang, "product_type_default")}'
                    else:
                        title = f'{check_products_translate(lang, product[0])}'


                    caption = product_caption(lang, title, check_products_translate(lang, product[0], True), product[6])

                    lst = [2, 0]
                    data['info'] = lst
                    quantity = 1
                    data['product_id'] = product[0]

                    with open(product[2], mode='rb') as img:
                        await bot.send_photo(chat_id=chat_id,
                                             photo=img,
                                             caption=caption,
                                             parse_mode='HTML',
                                             reply_markup=generate_product_detail(lang, lst, quantity, product[0], product[3]))


@dp.message_handler(state=NumberState.product_info)
async def show_product_info(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]
    chat_id = message.chat.id
    if message.text == check_language(lang, 'back_btn'):
        async with state.proxy() as data:
            cotegory = data['cotegory']
        await NumberState.choose_product.set()
        await message.answer(f'{check_language(lang, "menu_choose_products")}', reply_markup=generate_products(lang, cotegory))
    elif message.text == check_language(lang, 'cart_btn'):
        if db.get_cart_by_id(chat_id):
            await state.finish()
            await NumberState.product_cart.set()
            await message.answer(f'{cart_products_list(lang, chat_id)}', parse_mode='HTML',
                                 reply_markup=generate_cart_products(lang, chat_id))
        else:
            await message.answer(f'<b>{check_language(lang, "cart_empty")}</b>', parse_mode='HTML')


@dp.message_handler(state=NumberState.product_cart)
async def show_cart_menu(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]
    chat_id = message.chat.id
    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'cart_clear'):
        await state.finish()
        for i in db.get_cart_by_id(chat_id):
            db.delete_cart_product_by_id(i[0])
        await message.answer(f'{check_language(lang, "cart_cleaned")}', reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'make_order'):
        await state.finish()
        await NumberState.choose_delivery_type.set()
        await message.answer(text=check_language(lang, 'choose_delivery_type'), reply_markup=generate_delivery_type(lang))


    else:
        products = {}
        products_cart = db.get_cart_by_id(chat_id)
        for i in products_cart:
            products[f'✏️ {make_product_title(lang, i[1])}'] = i
        for key, value in products.items():
            if message.text == key:
                product_image = db.get_product_by_id(int(value[1].split('_')[0]))[2]
                product_info = value[1]
                quantity = int(value[2])
                caption = make_product_title(lang, value[1])
                with open(product_image, mode='rb') as img:
                    await bot.send_photo(chat_id=chat_id,
                                         photo=img,
                                         caption=caption,
                                         parse_mode='HTML',
                                         reply_markup=generate_reconstruct_product(lang, product_info, quantity))



@dp.message_handler(state=NumberState.choose_delivery_type)
async def show_delivery_type(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]

    if message.text == check_language(lang, 'type_pickup'):
        await NumberState.choose_branch.set()
        async with state.proxy() as data:
            data['delivery_type'] = 'pickup'
        await message.answer(text=branches_list(lang),
                             parse_mode='HTML',
                             reply_markup=generate_branches(lang))
    elif message.text == check_language(lang, 'type_delivery'):
        await NumberState.get_location.set()
        async with state.proxy() as data:
            data['delivery_type'] = 'delivery'
        await message.answer(text=check_language(lang, 'choose_address'),
                             parse_mode='HTML',
                             reply_markup=generate_get_location(lang))


    elif message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))

@dp.message_handler(state=NumberState.get_location, content_types=['text', 'location'])
async def show_get_location(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'back_btn'):
        await NumberState.choose_delivery_type.set()
        await message.answer(text=check_language(lang, 'choose_delivery_type'),
                             reply_markup=generate_delivery_type(lang))
    elif message.location:
        location = message.location
        radius = 0.1
        if check_location(location['longitude'], location['latitude'], radius):
            async with state.proxy() as data:
                data['branch'] = None
                data['location'] = f'{location["latitude"]}_{location["longitude"]}'

            await NumberState.time_order.set()
            await message.answer(text=check_language(lang, 'time_order'),
                                 parse_mode='HTML',
                                 reply_markup=generate_time_order(lang))
        else:
            await message.answer(text=check_language(lang, 'out_of_location'))



@dp.message_handler(state=NumberState.choose_branch)
async def show_choose_branch(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'back_btn'):
        await NumberState.choose_delivery_type.set()
        await message.answer(text=check_language(lang, 'choose_delivery_type'),
                             reply_markup=generate_delivery_type(lang))
    else:
        for branch in db.get_branches():
            if message.text == branch[0]:
                async with state.proxy() as data:
                    data['branch'] = branch[0]
                    data['location'] = None

                await NumberState.time_order.set()
                await message.answer(text=check_language(lang, 'time_order'),
                                     parse_mode='HTML',
                                     reply_markup=generate_time_order(lang))

@dp.message_handler(state=NumberState.time_order)
async def show_time_order(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'back_btn'):
        async with state.proxy() as data:
            if data['branch']:
                await NumberState.choose_branch.set()
                await message.answer(text=branches_list(lang),
                                     parse_mode='HTML',
                                     reply_markup=generate_branches(lang))
            else:
                await NumberState.get_location.set()
                await message.answer(text=check_language(lang, 'choose_address'),
                                     parse_mode='HTML',
                                     reply_markup=generate_get_location(lang))
    else:
        words_count = 0
        for i in range(len(message.text)):
            words_count += 1
        if words_count > 50:
            await message.answer(text=check_language(lang, 'text_limit'))
        else:
            async with state.proxy() as data:
                data['time_order'] = message.text
            await NumberState.make_comment.set()
            await message.answer(text=check_language(lang, 'ask_comment'),
                                 parse_mode='HTML',
                                 reply_markup=generate_make_comment(lang))


@dp.message_handler(state=NumberState.make_comment)
async def show_make_comment(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'back_btn'):
        await NumberState.time_order.set()
        await message.answer(text=check_language(lang, 'time_order'),
                             parse_mode='HTML',
                             reply_markup=generate_time_order(lang))
    else:
        if message.text == check_language(lang, 'standard_comment'):
            async with state.proxy() as data:
                data['comment'] = None
            await NumberState.payment_method.set()
            await message.answer(text=check_language(lang, 'payment_method'),
                                 parse_mode='HTML',
                                 reply_markup=generate_payment_method(lang))
        else:
            words_count = 0
            for i in range(len(message.text)):
                words_count += 1
            if words_count > 50:
                await message.answer(text=check_language(lang, 'text_limit'))
            else:
                async with state.proxy() as data:
                    data['comment'] = message.text
                await NumberState.payment_method.set()
                await message.answer(text=check_language(lang, 'payment_method'),
                                     parse_mode='HTML',
                                     reply_markup=generate_payment_method(lang))

@dp.message_handler(state=NumberState.payment_method)
async def show_payment_method(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]
    chat_id = message.chat.id

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'back_btn'):
        await NumberState.make_comment.set()
        await message.answer(text=check_language(lang, 'ask_comment'),
                             parse_mode='HTML',
                             reply_markup=generate_make_comment(lang))
    else:
        if message.text == check_language(lang, 'payment_method_cash'):
            async with state.proxy() as data:
                delivery_type = data['delivery_type']
                branch = data['branch']
                time_order = data['time_order']
                comment = data['comment']
                payment_method = 'cash'
                data['payment_method'] = payment_method
                phone_number = db.get_user_by_id(chat_id)[2]

            await NumberState.final_state.set()
            await bot.send_message(chat_id=chat_id,
                                   text=check_language(lang, 'final'),
                                   parse_mode='HTML',
                                   reply_markup=generate_final_menu(lang))
            await bot.send_message(chat_id=chat_id,
                                   text=final_caption(lang, chat_id, delivery_type, phone_number,
                                                      payment_method, time_order, branch, comment),
                                   parse_mode='HTML',
                                   reply_markup=generate_final_confirm(lang))
        elif message.text == check_language(lang, 'payment_method_terminal'):
            async with state.proxy() as data:
                delivery_type = data['delivery_type']
                branch = data['branch']
                time_order = data['time_order']
                comment = data['comment']
                payment_method = 'terminal'
                data['payment_method'] = payment_method
                phone_number = db.get_user_by_id(chat_id)[2]

            await NumberState.final_state.set()
            await bot.send_message(chat_id=chat_id,
                                   text=check_language(lang, 'final'),
                                   parse_mode='HTML',
                                   reply_markup=generate_final_menu(lang))
            await bot.send_message(chat_id=chat_id,
                                   text=final_caption(lang, chat_id, delivery_type, phone_number,
                                                      payment_method, time_order, branch, comment),
                                   parse_mode='HTML',
                                   reply_markup=generate_final_confirm(lang))


@dp.message_handler(state=NumberState.final_state)
async def show_final(message: Message, state: FSMContext):
    lang = db.get_language(message.chat.id)[0]

    if message.text == check_language(lang, 'main_menu'):
        await state.finish()
        name = message.from_user.first_name
        await message.answer(f'{name}! {check_language(lang, "main_menu_welcome")}',
                             reply_markup=generate_main_menu(lang))
    elif message.text == check_language(lang, 'back_btn'):
        await NumberState.payment_method.set()
        await message.answer(text=check_language(lang, 'payment_method'),
                             parse_mode='HTML',
                             reply_markup=generate_payment_method(lang))