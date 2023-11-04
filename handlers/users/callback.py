from data.loader import bot, dp, db
from data.config import product_caption, cart_products_list
from aiogram.types import CallbackQuery
import json
from data.languages import check_language, check_products_translate
from states.states import NumberState
from aiogram.dispatcher import FSMContext
from keyboards.reply import generate_main_menu, generate_change_phone, generate_categories, \
    generate_cart_products
from keyboards.inline import generate_product_detail, generate_clean_inline, generate_reconstruct_product

@dp.callback_query_handler(lambda call: 'lang' in call.data)
async def start_lang(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, lang = call.data.split('_')

    start_welcome = check_language(lang, 'start_welcome')

    await NumberState.get_phone.set()

    async with state.proxy() as data:
        data['lang'] = lang

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, f'{start_welcome}', reply_markup=generate_change_phone(lang))



@dp.callback_query_handler(lambda call: 'changeLang' in call.data)
async def start_lang(call: CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, lang = call.data.split('_')

    db.change_language_by_id(lang, chat_id)

    lang = db.get_language(call.message.chat.id)[0]
    name = call.message.chat.first_name

    main_menu_welcome = check_language(lang, 'main_menu_welcome')

    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, f'{name}! {main_menu_welcome}', reply_markup=generate_main_menu(lang))



@dp.callback_query_handler(lambda call: 'size' in call.data, state=NumberState.product_info)
async def reaction_to_size(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    async with state.proxy() as data:
        product_id = data['product_id']
        lst = [int(i) for i in call.data.split('_')[1]]


        buttons = call.message.reply_markup.inline_keyboard[1]
        for btn in buttons:
            if '✔' in btn.text:
                lst += [int(i) for i in btn.callback_data.split('_')[1]]
                break

        if lst[0] == 0:
            lst[1] = 0
        data['info'] = lst


        quantity = int(call.message.reply_markup.inline_keyboard[2][1].text)

        product = db.get_product_by_id(product_id)
        if product[3]:
            if lst[0] == 0:
                size = check_language(lang, "product_size_little")
                price = product[4]
            elif lst[0] == 1:
                size = check_language(lang, "product_size_medium")
                price = product[5]
            else:
                size = check_language(lang, "product_size_large")
                price = product[6]

            if lst[1] == 0:
                type = check_language(lang, "product_type_default")
            else:
                type = check_language(lang, "product_type_thin")

            title = f'{check_products_translate(lang, product[0])}, {size}, {type}'
        else:
            title = f'{check_products_translate(lang, product[0])}'

        caption = product_caption(lang, title, check_products_translate(lang, product[0], True), price)

        try:
            await bot.edit_message_caption(chat_id=chat_id,
                                           message_id=message_id,
                                           caption=caption,
                                           parse_mode='HTML',
                                           reply_markup=generate_product_detail(lang, lst, quantity, product[0],
                                                                                product[3]))
        except:
            pass


@dp.callback_query_handler(lambda call: 'type' in call.data, state=NumberState.product_info)
async def reaction_to_type(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    async with state.proxy() as data:
        product_id = data['product_id']
        lst = [int(i) for i in call.data.split('_')[1]]

        buttons = call.message.reply_markup.inline_keyboard[0]
        for btn in buttons:
            if '✔' in btn.text:
                lst = [int(i) for i in btn.callback_data.split('_')[1]] + lst
                break

        data['info'] = lst

        quantity = int(call.message.reply_markup.inline_keyboard[2][1].text)

        product = db.get_product_by_id(product_id)

        if product[3]:
            if lst[0] == 0:
                size = check_language(lang, "product_size_little")
                price = product[4]
            elif lst[0] == 1:
                size = check_language(lang, "product_size_medium")
                price = product[5]
            else:
                size = check_language(lang, "product_size_large")
                price = product[6]


            if lst[1] == 0:
                type = check_language(lang, "product_type_default")
            else:
                type = check_language(lang, "product_type_thin")

            title = f'{check_products_translate(lang, product[0])}, {size}, {type}'
        else:
            title = f'{check_products_translate(lang, product[0])}'

        caption = product_caption(lang, title, check_products_translate(lang, product[0], True), price)



        try:
            await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption,
                                                reply_markup=generate_product_detail(lang, lst, quantity, product[0],
                                                                                     product[3]))
        except:
            pass


@dp.callback_query_handler(lambda call: call.data == 'minus', state=NumberState.product_info)
async def reaction_to_minus(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    async with state.proxy() as data:
        product_id = data['product_id']
        lst = data['info']
        product = db.get_product_by_id(product_id)

        if product[3]:
            quantity = int(call.message.reply_markup.inline_keyboard[2][1].text)

            if lst[0] == 0:
                size = check_language(lang, "product_size_little")
                price = product[4]
            elif lst[0] == 1:
                size = check_language(lang, "product_size_medium")
                price = product[5]
            else:
                size = check_language(lang, "product_size_large")
                price = product[6]

            if lst[1] == 0:
                type = check_language(lang, "product_type_default")
            else:
                type = check_language(lang, "product_type_thin")

            title = f'{check_products_translate(lang, product[0])}, {size}, {type}'
        else:
            quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
            title = f'{check_products_translate(lang, product[0])}'
            price = product[6]

        if quantity <= 1:
            await bot.answer_callback_query(call.id, check_language(lang, 'product_quantity_min'))
        else:
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            caption = product_caption(lang, title, check_products_translate(lang, product[0], True), price)


            await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption,
                                           reply_markup=generate_product_detail(lang, lst, quantity - 1, product[0],
                                                                                product[3]))

@dp.callback_query_handler(lambda call: call.data == 'plus', state=NumberState.product_info)
async def reaction_to_plus(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    async with state.proxy() as data:
        product_id = data['product_id']
        lst = data['info']
        product = db.get_product_by_id(product_id)

        if product[3]:
            quantity = int(call.message.reply_markup.inline_keyboard[2][1].text)

            if lst[0] == 0:
                size = check_language(lang, "product_size_little")
                price = product[4]
            elif lst[0] == 1:
                size = check_language(lang, "product_size_medium")
                price = product[5]
            else:
                size = check_language(lang, "product_size_large")
                price = product[6]

            if lst[1] == 0:
                type = check_language(lang, "product_type_default")
            else:
                type = check_language(lang, "product_type_thin")

            title = f'{check_products_translate(lang, product[0])}, {size}, {type}'
        else:
            quantity = int(call.message.reply_markup.inline_keyboard[0][1].text)
            title = f'{check_products_translate(lang, product[0])}'
            price = product[6]

        chat_id = call.message.chat.id
        message_id = call.message.message_id

        caption = product_caption(lang, title, check_products_translate(lang, product[0], True), price)

        await bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=caption,
                                       reply_markup=generate_product_detail(lang, lst, quantity + 1, product[0],
                                                                            product[3]))


@dp.callback_query_handler(lambda call: 'cart' in call.data, state=NumberState.product_info)
async def add_product(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    lst = [int(i) for i in call.data.split('_')[1:]]
    product = db.get_product_by_id(lst[0])

    if product[3]:
        product_info = f'{lst[0]}_{lst[2]}_{lst[3]}'
    else:
        product_info = f'{lst[0]}'

    if db.get_cart_products(chat_id, product_info):
        db.update_cart_product(chat_id, product_info, lst[1])
    else:
        db.insert_cart_product(chat_id, product_info, lst[1])

    await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=generate_clean_inline())

    await state.finish()
    await NumberState.choose_category.set()
    await bot.send_message(chat_id=chat_id, text=f'{check_language(lang, "menu_chose_product")}', reply_markup=generate_categories(lang))




@dp.callback_query_handler(lambda call: 'cartMinus' in call.data, state='*')
async def reaction_to_minus_in_cart(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    product_info = call.data.split('cartMinus_')[1]
    quantity = int(call.message.reply_markup.inline_keyboard[1][1].text)
    if quantity <= 1:
        await bot.answer_callback_query(call.id, check_language(lang, 'product_quantity_min'))
    else:
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                            message_id=message_id,
                                            reply_markup=generate_reconstruct_product(lang, product_info, quantity-1))

@dp.callback_query_handler(lambda call: 'cartPlus' in call.data, state='*')
async def reaction_to_plus_in_cart(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    product_info = call.data.split('cartPlus_')[1]
    quantity = int(call.message.reply_markup.inline_keyboard[1][1].text)

    await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        reply_markup=generate_reconstruct_product(lang, product_info, quantity + 1))

@dp.callback_query_handler(lambda call: 'cartDelete' in call.data, state='*')
async def reaction_to_cart_delete(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    product_info = call.data.split('cartDelete_')[1]

    lst = [int(i) for i in product_info.split('_')]

    product_name = check_products_translate(lang, lst[0])

    await bot.delete_message(chat_id, message_id)

    if db.get_cart_products(chat_id, product_info):
        db.delete_cart_product(chat_id, product_info)
        await NumberState.product_cart.set()
        await bot.send_message(chat_id, f'❌ {product_name} - {check_language(lang, "deleted_from_cart")}',
                               reply_markup=generate_cart_products(lang, chat_id))
        if not db.get_cart_by_id(chat_id):
            await state.finish()
            await bot.send_message(chat_id, f'<b>{check_language(lang, "cart_empty")}</b>',
                                   parse_mode='HTML',
                                   reply_markup=generate_main_menu(lang))


@dp.callback_query_handler(lambda call: 'cartSave' in call.data, state='*')
async def reaction_to_cart_save(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    product_info = call.data.split('cartSave_')[1]
    quantity = int(call.message.reply_markup.inline_keyboard[1][1].text)

    await bot.delete_message(chat_id, message_id)

    if db.get_cart_products(chat_id, product_info):
        await NumberState.product_cart.set()
        db.update_cart_product_quantity(chat_id, product_info, quantity)
        await bot.send_message(chat_id=chat_id, text=f'{cart_products_list(lang, chat_id)}',
                               parse_mode='HTML',
                               reply_markup=generate_cart_products(lang, chat_id))


@dp.callback_query_handler(lambda call: call.data == 'cancel', state='*')
async def reaction_final_cancel(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    name = call.message.chat.full_name

    await state.finish()
    await bot.send_message(chat_id=chat_id, text=f'{name}! {check_language(lang, "main_menu_welcome")}',
                           reply_markup=generate_main_menu(lang))
    await bot.delete_message(chat_id, message_id)

@dp.callback_query_handler(lambda call: call.data == 'confirm', state=NumberState.final_state)
async def reaction_final_confirm(call: CallbackQuery, state: FSMContext):
    lang = db.get_language(call.message.chat.id)[0]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    async with state.proxy() as data:
        phone_number = db.get_user_by_id(chat_id)[2]
        delivery_type = data['delivery_type']
        payment_method = data['payment_method']
        time_order = data['time_order']

        branch = data['branch']
        location = data['location']
        comment = data['comment']
        date = call.message.date
        total_price = 0

        for i in db.get_cart_by_id(chat_id):
            product_id = int(i[1].split('_')[0])
            try:
                product_type = int(i[1].split('_')[1])
            except:
                product_type = 2
            j = db.get_product_by_id(product_id)
            if product_type == 0:
                total_price += j[4]
            elif product_type == 1:
                total_price += j[5]
            elif product_type == 2:
                total_price += j[6]


        lst = []
        for i in db.get_id_from_orders():
            lst.append(i[0])
        try:
            order_id = lst[-1] + 1
        except:
            order_id = 1


        with open('orders.json', mode='r', encoding='UTF-8') as data:
            data = json.load(data)
            data[order_id] = db.get_cart_by_id(chat_id)
            with open('orders.json', mode='w', encoding='UTF-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)


        db.insert_order(chat_id, phone_number, delivery_type, payment_method, time_order, total_price, date, branch,
                        location, comment, False)

        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id,
                                            reply_markup=generate_clean_inline())
        db.delete_cart_product_by_id(chat_id)
        await state.finish()
        await bot.send_message(chat_id=chat_id,
                               text=f'{check_language(lang, "finish_order1")}<b>#{order_id}</b>{check_language(lang, "finish_order2")}',
                               parse_mode='HTML',
                               reply_markup=generate_main_menu(lang))

