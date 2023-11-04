from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data.languages import LANGUAGES, check_language, check_products_translate, make_product_title
from data.loader import db


def generate_clean():
    return ReplyKeyboardRemove()
def generate_main_menu(lang):
    markup =ReplyKeyboardMarkup(resize_keyboard=True)

    generate_main_menu_menu = check_language(lang, 'generate_main_menu_menu')
    generate_main_menu_contacts = check_language(lang, 'generate_main_menu_contacts')
    generate_main_menu_reviews = check_language(lang, 'generate_main_menu_reviews')
    generate_main_menu_delivery = check_language(lang, 'generate_main_menu_delivery')
    generate_main_menu_settings = check_language(lang, 'generate_main_menu_settings')

    menu = KeyboardButton(text=f'{generate_main_menu_menu}')
    contacts = KeyboardButton(text=f'{generate_main_menu_contacts}')
    review = KeyboardButton(text=f'{generate_main_menu_reviews}')
    delivery = KeyboardButton(text=f'{generate_main_menu_delivery}')
    settings = KeyboardButton(text=f'{generate_main_menu_settings}')
    markup.row(menu)
    markup.row(contacts, review)
    markup.row(delivery, settings)
    return markup

def generate_settings(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    settings_change_language = check_language(lang, 'settings_change_language')
    settings_change_phone = check_language(lang, 'settings_change_phone')
    main_menu = check_language(lang, 'main_menu')

    change_lang = KeyboardButton(text=f'{settings_change_language}')
    change_num = KeyboardButton(text=f'{settings_change_phone}')
    back_btn = KeyboardButton(text=f'{main_menu}')
    markup.row(change_lang)
    markup.row(change_num)
    markup.row(back_btn)
    return markup



def generate_reviews(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    reviews_five = check_language(lang, 'review_five')
    review_four = check_language(lang, 'review_four')
    review_three = check_language(lang, 'review_three')
    review_two = check_language(lang, 'review_two')
    review_one = check_language(lang, 'review_one')
    main_menu = check_language(lang, 'main_menu')

    five = KeyboardButton(text=f'{reviews_five}')
    four = KeyboardButton(text=f'{review_four}')
    three = KeyboardButton(text=f'{review_three}')
    two = KeyboardButton(text=f'{review_two}')
    one = KeyboardButton(text=f'{review_one}')
    back_btn = KeyboardButton(text=f'{main_menu}')
    markup.row(five)
    markup.row(four)
    markup.row(three)
    markup.row(two)
    markup.row(one)
    markup.row(back_btn)
    return markup

def generate_back(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    back_btn = KeyboardButton(text=f'{check_language(lang, "back_btn")}')
    markup.row(back_btn)
    return markup

def generate_change_phone(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    settings_send_phone = check_language(lang, 'settings_send_phone')
    back_btn_lang = check_language(lang, 'back_btn')

    send_phone_num = KeyboardButton(text=f'{settings_send_phone}', request_contact=True)
    back_btn = KeyboardButton(text=f'{back_btn_lang}')
    markup.row(send_phone_num)
    markup.row(back_btn)
    return markup

def generate_change_phone_code(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    settings_send_phone_code = check_language(lang, 'settings_send_phone_code')
    back_btn_lang = check_language(lang, 'back_btn')

    send_phone_code = KeyboardButton(text=f'{settings_send_phone_code}')
    back_btn = KeyboardButton(text=f'{back_btn_lang}')
    markup.row(send_phone_code)
    markup.row(back_btn)
    return markup


def generate_categories(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)


    cart_btn_lang = check_language(lang, 'cart_btn')
    cart_btn = KeyboardButton(text=f'{cart_btn_lang}')
    markup.row(cart_btn)

    buttons = []
    categories = db.get_categories()
    for category in categories:
        category_lang = check_language(lang, f'menu_{category[0]}')
        btn = KeyboardButton(text=f'{category_lang}')
        buttons.append(btn)
    markup.add(*buttons)

    main_menu_btn_lang = check_language(lang, 'main_menu')
    main_menu_btn = KeyboardButton(text=f'{main_menu_btn_lang}')
    markup.row(main_menu_btn)
    return markup

def generate_products(lang, cotegory):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    buttons = []
    products = db.get_products_by_category(cotegory)
    for product in products:
        buttons.append(check_products_translate(lang, product[0]))
    markup.add(*buttons)


    back_btn_lang = check_language(lang, 'back_btn')
    back_btn = KeyboardButton(text=f'{back_btn_lang}')

    cart_btn_lang = check_language(lang, 'cart_btn')
    cart_btn = KeyboardButton(text=f'{cart_btn_lang}')

    markup.row(back_btn, cart_btn)

    return markup



def generate_product_keyboard(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    back_btn_lang = check_language(lang, 'back_btn')
    back_btn = KeyboardButton(text=f'{back_btn_lang}')

    cart_btn_lang = check_language(lang, 'cart_btn')
    cart_btn = KeyboardButton(text=f'{cart_btn_lang}')

    markup.row(back_btn, cart_btn)

    return markup


def generate_cart_products(lang, telegram_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    back_btn = KeyboardButton(text=f'{check_language(lang, "main_menu")}')
    cart_clear_btn = KeyboardButton(text=f'{check_language(lang, "cart_clear")}')
    markup.row(back_btn, cart_clear_btn)

    for product_info in db.get_cart_by_id(telegram_id):


        product_title = f'✏️ {make_product_title(lang, product_info[1])}'

        markup.row(product_title)

    make_order_btn = KeyboardButton(text=f'{check_language(lang, "make_order")}')
    markup.row(make_order_btn)

    return markup


def generate_delivery_type(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    type_delivery = KeyboardButton(text=check_language(lang, 'type_delivery'))
    type_pickup = KeyboardButton(text=check_language(lang, 'type_pickup'))
    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))

    markup.row(type_delivery)
    markup.row(type_pickup)
    markup.row(main_menu)

    return markup

def generate_get_location(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    get_location = KeyboardButton(text=check_language(lang, 'get_location'), request_location=True)
    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))
    back_btn = KeyboardButton(text=check_language(lang, "back_btn"))
    markup.row(get_location)
    markup.row(main_menu, back_btn)

    return markup

def generate_branches(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for i in db.get_branches():
        branch = KeyboardButton(text=i[0])
        markup.row(branch)
    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))
    back_btn = KeyboardButton(text=check_language(lang, "back_btn"))
    markup.row(main_menu, back_btn)

    return markup

def generate_time_order(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    answer = KeyboardButton(text=check_language(lang, 'time_order_answer'))
    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))
    back_btn = KeyboardButton(text=check_language(lang, "back_btn"))
    markup.row(answer)
    markup.row(main_menu, back_btn)

    return markup


def generate_make_comment(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    answer = KeyboardButton(text=check_language(lang, 'standard_comment'))
    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))
    back_btn = KeyboardButton(text=check_language(lang, "back_btn"))
    markup.row(answer)
    markup.row(main_menu, back_btn)

    return markup


def generate_payment_method(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    payment_method_cash = KeyboardButton(text=check_language(lang, 'payment_method_cash'))
    payment_method_terminal = KeyboardButton(text=check_language(lang, 'payment_method_terminal'))
    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))
    back_btn = KeyboardButton(text=check_language(lang, "back_btn"))
    markup.row(payment_method_cash, payment_method_terminal)
    markup.row(main_menu, back_btn)

    return markup

def generate_final_menu(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    main_menu = KeyboardButton(text=check_language(lang, 'main_menu'))
    back_btn = KeyboardButton(text=check_language(lang, "back_btn"))
    markup.row(main_menu, back_btn)

    return markup