from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.languages import LANGUAGES, check_language, check_products_translate
from database.database import DataBase

db = DataBase()

def generate_clean_inline():
    return InlineKeyboardMarkup()
def generate_choose_language(languages):
    markup = InlineKeyboardMarkup()
    for lang in languages:
        btn = InlineKeyboardButton(text=languages[lang]['lang'], callback_data=f'lang_{lang}')
        markup.row(btn)
    return markup


def generate_change_language(languages):
    markup = InlineKeyboardMarkup()
    for lang in languages:
        btn = InlineKeyboardButton(text=languages[lang]['lang'], callback_data=f'changeLang_{lang}')
        markup.row(btn)
    return markup

def generate_product_detail(lang, lst, quantity, product_id, size=False):
    markup = InlineKeyboardMarkup()
    if size:
        little_btn = InlineKeyboardButton(f'{"✔" if lst[0] == 0 else ""} {check_language(lang, "product_size_little")}',
                                          callback_data='size_0')
        medium_btn = InlineKeyboardButton(f'{"✔" if lst[0] == 1 else ""} {check_language(lang, "product_size_medium")}',
                                          callback_data='size_1')
        large_btn = InlineKeyboardButton(f'{"✔" if lst[0] == 2 else ""} {check_language(lang, "product_size_large")}',
                                         callback_data='size_2')

        markup.row(little_btn, medium_btn, large_btn)

        if lst[0] == 0:
            default_btn = InlineKeyboardButton(
                f'✔ {check_language(lang, "product_type_default")}',
                callback_data='type_0')

            markup.row(default_btn)
        else:
            default_btn = InlineKeyboardButton(f'{"✔" if lst[1] == 0 else ""} {check_language(lang, "product_type_default")}',
                                               callback_data='type_0')
            thin_btn = InlineKeyboardButton(f'{"✔" if lst[1] == 1 else ""} {check_language(lang, "product_type_thin")}',
                                            callback_data='type_1')

            markup.row(default_btn, thin_btn)




    minus_btn = InlineKeyboardButton('➖', callback_data='minus')
    quan_btn = InlineKeyboardButton(f'{quantity}', callback_data='ad')
    plus_btn = InlineKeyboardButton('➕', callback_data='plus')

    markup.row(minus_btn, quan_btn, plus_btn)



    if db.get_product_by_id(product_id)[3]:
        cart_btn = InlineKeyboardButton(f'{check_language(lang, "cart_add_btn")}',
                                        callback_data=f'cart_{product_id}_{quantity}_{lst[0]}_{lst[1]}')
    else:
        cart_btn = InlineKeyboardButton(f'{check_language(lang, "cart_add_btn")}',
                                        callback_data=f'cart_{product_id}_{quantity}')
    markup.row(cart_btn)

    return markup

def generate_reconstruct_product(lang, product_info, quantity):
    markup = InlineKeyboardMarkup()

    delete_product = InlineKeyboardButton(f'{check_language(lang, "delete_from_cart")}',
                                          callback_data=f'cartDelete_{product_info}')
    save_product = InlineKeyboardButton(f'{check_language(lang, "save_product")}',
                                        callback_data=f'cartSave_{product_info}')

    minus_btn = InlineKeyboardButton('➖', callback_data=f'cartMinus_{product_info}')
    quan_btn = InlineKeyboardButton(f'{quantity}', callback_data='ad')
    plus_btn = InlineKeyboardButton('➕', callback_data=f'cartPlus_{product_info}')

    markup.row(delete_product)
    markup.row(minus_btn, quan_btn, plus_btn)
    markup.row(save_product)

    return markup

def generate_final_confirm(lang):
    markup = InlineKeyboardMarkup()

    # confirm = InlineKeyboardButton(check_language(lang, 'confirm'),
    #                                       callback_data='confirm')
    # cancel = InlineKeyboardButton(check_language(lang, 'cancel'),
    #                                callback_data='cancel')

    confirm = InlineKeyboardButton(text=check_language(lang, 'confirm'),
                                   callback_data='confirm')
    cancel = InlineKeyboardButton(text=check_language(lang, 'cancel'),
                                  callback_data='cancel')
    markup.row(confirm)
    markup.row(cancel)

    return markup



