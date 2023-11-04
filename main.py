from data.loader import dp, executor
import handlers

if __name__ == '__main__':
    executor.start_polling(dp)