import sqlite3

class DataBase:
    def __init__(self):
        self.database = sqlite3.connect('shop.db', check_same_thread=False)

    def manager(self, sql, *args,
                fetchone: bool = False,
                fetchall: bool = False,
                commit: bool = False):
        with self.database as db:
            cursor = db.cursor()
            cursor.execute(sql, args)
            if commit:
                result = db.commit()
            if fetchone:
                result = cursor.fetchone()
            if fetchall:
                result = cursor.fetchall()
            return result

    def drop_user_table(self):
        sql = '''
            DROP TABLE IF EXISTS users;
        '''
        self.manager(sql, commit=True)

    def create_users_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS users(
                telegram_id BIGINT PRIMARY KEY,
                full_name VARCHAR(100),
                phone VARCHAR(20) UNIQUE,
                language VARCHAR(10)
        )'''
        self.manager(sql, commit=True)

    def get_user_by_id(self, telegram_id):
        sql = '''
            SELECT * FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def insert_user(self, chat_id, full_name, phone, lang):
        sql = '''
            INSERT INTO users(telegram_id, full_name, phone, language) VALUES (?,?,?,?)
        '''
        self.manager(sql, chat_id, full_name, phone, lang, commit=True)

    def get_language(self, telegram_id):
        sql = '''
            SELECT language FROM users WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def change_language_by_id(self, lang, telegram_id):
        sql = '''
            UPDATE users SET language=? WHERE telegram_id=?
        '''
        self.manager(sql, lang, telegram_id, commit=True)

    def change_phone_num_by_id(self, phone, telegram_id):
        sql = '''
            UPDATE users SET phone=? WHERE telegram_id=?
        '''
        self.manager(sql, phone, telegram_id, commit=True)

    def drop_reviews_table(self):
        sql = '''
            DROP TABLE IF EXISTS reviews;
            
        '''
        self.manager(sql, commit=True)
    def create_reviews_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS reviews(
                telegram_id BIGINT PRIMARY KEY,
                grade INTEGER,
                review_reason VARCHAR(100)
            )
        '''
        self.manager(sql, commit=True)

    def insert_review(self, telegram_id, grade, review_reason):
        sql = '''
            INSERT INTO reviews(telegram_id, grade, review_reason) VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, grade, review_reason, commit=True)

    def get_review_by_id(self, telegram_id):
        sql = '''
            SELECT * FROM reviews WHERE telegram_id = ?
        '''
        return self.manager(sql, telegram_id, fetchone=True)

    def update_review(self, telegram_id, grade, review_reason):
        sql = '''
            UPDATE reviews SET grade=?, review_reason=? WHERE telegram_id=?
        '''
        self.manager(sql, grade, review_reason, telegram_id, commit=True)

    def create_code_attempts(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS code_attempts(
                phone VARCHAR(25) PRIMARY KEY,
                attempt INTEGER,
                date INTEGER
            )
        '''
        self.manager(sql, commit=True)

    def get_code_attempts_by_phone(self, phone):
        sql = '''
            SELECT * FROM code_attempts WHERE phone=?
        '''
        return self.manager(sql, phone, fetchone=True)

    def insert_code_attempt(self, phone, attempt, date):
        sql = '''
            INSERT INTO code_attempts(phone, attempt, date) VALUES (?,?,?)
        '''
        self.manager(sql, phone, attempt, date, commit=True)

    def update_code_attempt_by_phone(self, phone, attempt, date):
        sql = '''
            UPDATE code_attempts SET attempt=?, date=? WHERE phone=?
        '''
        self.manager(sql, attempt, date, phone, commit=True)

    def create_categories_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS categories(
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_title VARCHAR(50)
            )
        '''
        self.manager(sql, commit=True)

    def insert_categories(self):
        sql = '''
            INSERT INTO categories(category_title) VALUES
                ('pizza'),
                ('combo'),
                ('snacks'),
                ('desserts'),
                ('drinks'),
                ('sauces')
        '''
        self.manager(sql, commit=True)

    def get_categories(self):
        sql = '''
            SELECT category_title FROM categories
        '''
        return self.manager(sql, fetchall=True)

    def create_products_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS products(
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_category VARCHAR(50),
                product_image VARCHAR(255),
                product_size BOOLEAN,
                product_price_little INTEGER,
                product_price_medium INTEGER,
                product_price_large INTEGER
            )
        '''
        self.manager(sql, commit=True)

    def drop_products_table(self):
        sql = '''
            DROP TABLE IF EXISTS products
        '''
        self.manager(sql, commit=True)

    def get_products_by_category(self, category):
        sql = '''
            SELECT * FROM products WHERE product_category=?
        '''
        return self.manager(sql, category, fetchall=True)

    def get_product_by_id(self, id):
        sql = '''
            SELECT * FROM products WHERE product_id=?
        '''
        return self.manager(sql, id, fetchone=True)

    def add_product(self):
        sql = '''
            INSERT INTO products(
                product_category,
                product_image,
                product_size,
                product_price_little,
                product_price_medium,
                product_price_large
            )
            VALUES (?,?,?,?,?,?)
        '''
        self.manager(sql, 'drinks', 'images/2.jpg', False, 0, 0, 1000000, commit=True)

    def create_carts_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS carts(
                cart_id INTEGER,
                cart_product VARCHAR(100),
                cart_quantity INTEGER
            )
        '''
        self.manager(sql, commit=True)

    def get_cart_by_id(self, telegram_id):
        sql = '''
            SELECT * FROM carts WHERE cart_id=?
        '''
        return self.manager(sql, telegram_id, fetchall=True)

    def get_cart_products(self, telegram_id, product):
        sql = '''
            SELECT * FROM carts WHERE cart_id=? AND cart_product=?
        '''
        return self.manager(sql, telegram_id, product, fetchall=True)

    def insert_cart_product(self, telegram_id, product, quantity):
        sql = '''
            INSERT INTO carts(
                cart_id,
                cart_product,
                cart_quantity
            )
            VALUES (?,?,?)
        '''
        self.manager(sql, telegram_id, product, quantity, commit=True)

    def update_cart_product(self, telegram_id, product, quantity):
        sql = '''
            UPDATE carts 
                SET 
                    cart_quantity=cart_quantity + ? 
                WHERE
                    cart_id=? AND cart_product=?
        '''
        self.manager(sql, quantity, telegram_id, product, commit=True)

    def update_cart_product_quantity(self, telegram_id, product, quantity):
        sql = '''
            UPDATE carts 
                SET 
                    cart_quantity=? 
                WHERE
                    cart_id=? AND cart_product=?
        '''
        self.manager(sql, quantity, telegram_id, product, commit=True)

    def delete_cart_product_by_id(self, telegram_id):
        sql = '''
            DELETE FROM carts WHERE cart_id=?
        '''
        self.manager(sql, telegram_id, commit=True)

    def delete_cart_product(self, telegram_id, product):
        sql = '''
            DELETE FROM carts WHERE cart_id=? and cart_product=?
        '''
        self.manager(sql, telegram_id, product, commit=True)

    def create_branches_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS branches(
                branch_title VARCHAR(100),
                branch_address VARCHAR(100),
                branch_reference_point VARCHAR(100),
                branch_working_hours VARCHAR(100)
            )
        '''
        self.manager(sql, commit=True)

    def drop_branches(self):
        sql = '''
            DROP TABLE IF EXISTS branches
        '''
        self.manager(sql, commit=True)

    def add_branch(self, title, address, reference_point, working_hours):
        sql = '''
            INSERT INTO branches(
                branch_title,
                branch_address,
                branch_reference_point,
                branch_working_hours
            )
            VALUES (?,?,?,?)
        '''
        self.manager(sql, title, address, reference_point, working_hours, commit=True)

    def get_branches(self):
        sql = '''
            SELECT * FROM branches
        '''
        return self.manager(sql, fetchall=True)

    def drop_orders(self):
        sql = '''
            DROP TABLE IF EXISTS orders
        '''
        self.manager(sql, commit=True)
    def create_orders_table(self):
        sql = '''
            CREATE TABLE IF NOT EXISTS orders(
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_telegram_id INTEGER,
                order_phone VARCHAR(50),
                order_delivery_type VARCHAR(50),
                order_payment_method VARCHAR(50),
                order_time_order VARCHAR(50),
                order_total_price INTEGER,
                order_date VARCHAR(100),
                order_branch VARCHAR(50),
                order_location VARCHAR(100),
                order_comment VARCHAR(255),
                order_done BOOLEAN
            )
        '''
        self.manager(sql, commit=True)

    def insert_order(self, telegram_id, phone_number, delivery_type, payment_method, time_order, total_price, date,
                     branch, location, comment, done):
        sql = '''
            INSERT INTO orders(
                order_telegram_id,
                order_phone,
                order_delivery_type,
                order_payment_method,
                order_time_order,
                order_total_price,
                order_date,
                order_branch,
                order_location,
                order_comment,
                order_done
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        '''
        self.manager(sql, telegram_id, phone_number, delivery_type, payment_method, time_order, total_price, date,
                     branch, location, comment, done, commit=True)

    def get_id_from_orders(self):
        sql = '''
            SELECT order_id FROM orders
        '''
        return self.manager(sql, fetchall=True)


