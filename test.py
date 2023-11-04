from database.database import DataBase
from data.languages import check_products_translate, check_language
import json

db = DataBase()


# db.drop_user_table()
# db.create_users_table()

# db.drop_reviews_table()
# db.create_reviews_table()

# db.create_code_attempts()

# db.create_categories_table()
# db.insert_categories()

# db.drop_products_table()
# db.create_products_table()

# db.add_product()

# db.create_carts_table()

db.drop_orders()
db.create_orders_table()

# lst = []
# for i in db.get_id_from_orders():
#     lst.append(i[0])
# print(lst[-1])




# order_id = 2
#
# with open('orders.json', mode='r', encoding='UTF-8') as data:
#     data = json.load(data)
#     data[order_id] = {'ds': 'as'}
#     print(data)
#     with open('orders.json', mode='w', encoding='UTF-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)



# db.drop_branches()
# db.create_branches_table()
# db.add_branch('Stranoe mesto', 'Адрес: дА', 'Ориентир: На земле', '10:00 - 19:67')


# lang = 'ru'
# chat_id = 434874523






# (1, 'pizza', 'images/1.jpg', 1, 1, 59000, 85000, 109000)






# from data.languages import LANGUAGES, check_language
#
# for i in LANGUAGES.keys():
#     try:
#         lang = LANGUAGES[i]['settings_change_phone']
#     except:
#         # lang = LANGUAGES[list(LANGUAGES.keys())[0]]['settings_change_phone']
#         continue
#     # lang = check_language(i, 'settings_change_phone')
#
#     print(lang)



# import re
# from data.config import PHONE_RESULTS
#
#
# for phone in PHONE_RESULTS:
#     ewq = re.search(phone, '901231212')
#     print(bool(ewq))






