from aiogram.dispatcher.filters.state import State, StatesGroup

class NumberState(StatesGroup):
    get_phone = State()
    get_phone_code = State()

    change_phone = State()
    change_phone_code = State()

    get_review = State()
    get_review_info = State()

    choose_category = State()
    choose_product = State()
    product_info = State()
    product_cart = State()

    choose_delivery_type = State()
    choose_branch = State()
    get_location = State()
    time_order = State()
    make_comment = State()
    payment_method = State()
    final_state = State()

    don = State()
