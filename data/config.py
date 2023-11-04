from data.languages import check_language, check_products_translate
from data.loader import db, bot, dp
import math

PHONE_RESULTS = [r'\+998\d{9}$',
                 r'\b\d{9}$']

GRADES = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four'
}

def unix_in_time(time):
    if time < 0:
        return False
    minuts = time // 60
    seconds = time % 60
    if minuts == 0:
        show_minuts = '0'
    elif minuts < 10:
        show_minuts = f'0{minuts}'
    else:
        show_minuts = minuts

    if seconds == 0:
        show_seconds = '00'
    elif seconds < 10:
        show_seconds = f'0{seconds}'
    else:
        show_seconds = seconds

    return f'{show_minuts}:{show_seconds}'

def price_spaces(num=0):
    num = str(num)
    reversed = ''
    count = 0
    for i in range(len(num)-1, -1, -1):
        if count >= 2:
            reversed += f'{num[i]} '
            count = 0
        else:
            reversed += num[i]
            count += 1
    spaces = ''
    for i in range(len(reversed)-1, -1, -1):
        spaces += reversed[i]

    ans = ''
    if spaces[0] == ' ':
        for i in range(1, len(spaces)):
            ans += spaces[i]
    else:
        ans = spaces
    return ans

def product_caption(lang, title, description, price):
    caption = f'<b>{title}</b>\n\n{description}\n\n<b>{check_language(lang, "product_price")}: {price_spaces(price)} {check_language(lang, "currency")}</b>'

    return caption

def cart_products_list(lang, telegram_id):
    products = db.get_cart_by_id(telegram_id)
    count = 0
    product_text = ''
    total_price = 0
    for product in products:
        product_info = [int(j) for j in product[1].split('_')]
        product_id = product_info[0]
        product_name = check_products_translate(lang, product_id)
        product_quantity = product[2]
        count += 1



        if len(product_info) > 1:
            if product_info[1] == 0:
                product_size = check_language(lang, 'product_size_little')
                product_price = db.get_product_by_id(product_id)[4]
            elif product_info[1] == 1:
                product_size = check_language(lang, 'product_size_medium')
                product_price = db.get_product_by_id(product_id)[5]
            else:
                product_size = check_language(lang, 'product_size_large')
                product_price = db.get_product_by_id(product_id)[6]

            if product_info[2] == 0:
                product_type = check_language(lang, 'product_type_default')
            else:
                product_type = check_language(lang, 'product_type_thin')

            product_title = f'{product_name}, {product_size}, {product_type}'
        else:
            product_price = db.get_product_by_id(product_id)[6]
            product_title = f'{product_name}'

        general_price = product_price * product_quantity

        text = f'''<b>{count}. {product_title}</b>
{product_quantity} x {price_spaces(product_price)} {check_language(lang, "currency")}= <b>{price_spaces(general_price)} {check_language(lang, "currency")}</b>\n\n'''
        product_text += text
        total_price += general_price

    caption = f'<b>{check_language(lang, "your_cart")}:</b>\n\n\n{product_text}\n<b>{check_language(lang, "total")}: {price_spaces(total_price)} {check_language(lang, "currency")}</b>'
    return caption


def branches_list(lang):
    branches = db.get_branches()
    answer = ''

    for branch in branches:
        text = f'''📍 <b>{branch[0]}</b>\n{branch[1]}\n{branch[2]}\n{branch[3]}\n\n'''
        answer += text

    return answer

def final_caption(lang, telegram_id, type, phone_number, payment_method, time_order, branch, comment):
    if type == 'pickup':
        type = check_language(lang, 'type_pickup')
    else:
        type = check_language(lang, 'type_delivery')


    if payment_method == 'cash':
        payment_method = check_language(lang, 'payment_method_cash')
    else:
        payment_method = check_language(lang, 'payment_method_terminal')


    if comment:
        comment = f'\n{check_language(lang, "final_comment")}: <b>{comment}</b>'
    else:
        comment = ''


    if branch:
        branch = f'\n{check_language(lang, "final_pickup_from")}: <b>{branch}</b>'
    else:
        branch = ''


    answer = f'''{check_language(lang, 'final_type')}: <b>{type}</b>
{check_language(lang, 'final_phone_number')}: <b>{phone_number}</b>
{check_language(lang, 'final_payment_method')}: <b>{payment_method}</b>
{check_language(lang, 'final_time_order')}: <b>{time_order}</b>{comment}{branch}

▫️▫️▫️▫️▫️▫️▫️

'''

    products = db.get_cart_by_id(telegram_id)
    count = 0
    total_price = 0
    for product in products:
        product_info = [int(j) for j in product[1].split('_')]
        product_id = product_info[0]
        product_name = check_products_translate(lang, product_id)
        product_quantity = product[2]
        count += 1

        if len(product_info) > 1:
            if product_info[1] == 0:
                product_size = check_language(lang, 'product_size_little')
                product_price = db.get_product_by_id(product_id)[4]
            elif product_info[1] == 1:
                product_size = check_language(lang, 'product_size_medium')
                product_price = db.get_product_by_id(product_id)[5]
            else:
                product_size = check_language(lang, 'product_size_large')
                product_price = db.get_product_by_id(product_id)[6]

            if product_info[2] == 0:
                product_type = check_language(lang, 'product_type_default')
            else:
                product_type = check_language(lang, 'product_type_thin')

            product_title = f'{product_name}, {product_size}, {product_type}'
        else:
            product_price = db.get_product_by_id(product_id)[6]
            product_title = f'{product_name}'

        general_price = product_price * product_quantity

        text = f'''<b>{count}. {product_title}</b>
{product_quantity} x {price_spaces(product_price)} {check_language(lang, "currency")}= <b>{price_spaces(general_price)} {check_language(lang, "currency")}</b>\n\n'''
        answer += text
        total_price += general_price

    answer += f'''▫️▫️▫️▫️▫️▫️▫️

{check_language(lang, 'sum')}: <b>{price_spaces(total_price)} {check_language(lang, "currency")}</b>
'''
    return answer


def check_location(x, y, r):
    my_coordinates = {"latitude": 41.264121, "longitude": 69.156761}
    x = x - my_coordinates['longitude']
    y = y - my_coordinates['latitude']
    hypotenuse = math.sqrt(x ** 2 + y ** 2)
    if hypotenuse <= r:
        return True
    else:
        return False