# from scipy.linalg import solve
import numpy as np
import telebot
from config import *


bot = telebot.TeleBot(token)


def create_matrix(message, size):
    """
        Функция получает на вход размер матрицы и её элементы, в виде
        строки с разделителем ",", отправляет пользователю созданную
        матрицу, возвращает эту матрицу. В случае возникновения исключений
        перенаправляет на функцию получения новых элементов матрицы
    """
    #todo Дописать перенаправление на получение новых значений в случае искл.
    try:
        numbers = list(map(float, message.text.split(',')))
        a = np.zeros(size)
        for i in range(len(a)):
            for j in range(len(a[i])):
                a[i][j] = numbers[0]
                numbers.pop(0)
        send_matrix(message, a)
        return a
    except Exception as e:
        error(message, e, create_matrix)
    # bot.register_next_step_handler(message.from_user.id, change)


def error(message, exception, func):
    """
        Функция сообщает об исключении: на вход получает сообщение,
        вызвавшее исключение, это исключение, и функцию, которую
        необходимо запустить для повторной попытки ввода значений.
    """
    error_msg = (f'Неверный ввод размера матрицы\n'
                 f'Пользователь: {message.from_user.first_name}\n'
                 f'Сообщение: {message.text}\n'
                 f'Поднятое исключение: {exception}')
    bot.send_message(admin_id, error_msg)
    bot.send_message(message.from_user.id,
                     'Ты что-то неверно ввёл.\n'
                     'Давай ещё раз')
    # traceback.print_exc(file=sys.stdout)
    bot.register_next_step_handler(message, func)


def send_matrix(message, matrix):
    """
            Функция получает на вход матрицу, затем преобразовывает
            её в строку, для читабельного отображения в сообщении,
            и отправляет её пользователю.
            Срез строки необходим для удаления лишних двух символов
            в конце матрицы, после её полного формирования.
    """
    str_matrix = '| '
    for row in matrix:
        row_str = ''
        for el in row:
            row_str += str(el) + ' '
        str_matrix += row_str + '|\n| '
    str_matrix = str_matrix[:-2]
    msg = 'Вот так выглядит твоя матрица:\n' + str_matrix  # + 'Изменить?'
    bot.send_message(message.from_user.id, msg)


@bot.message_handler(commands=['start'])
def bot_start(message):
    """
            Функция получают команду начала работы бота
            и запускает его.
    """
    bot.send_message(message.from_user.id, start_message)


@bot.message_handler(commands=['slau'])
def slau_start(message):
    """
            Функция начинает ввод для решения слау
    """
    bot.send_message(message.from_user.id, slau_start_msg)
    bot.register_next_step_handler(message, slau)

#todo написать решение если уже объявлена первая матрица и решить СЛАУ
# дописать функцию slau()


def slau(message, matrix=None):
    """
            Функция получает размер матрицы в виде текста
            с разделителем ',', затем преобразует его в кортеж
            и передаёт его в следующую функцию. В случае возник-
            новения исключений, перезапускает себя(через функцию error).
            При формировании первой матрицы, переменная matrix -> None,
            после объявления первой матрицы функция формирует вторую.
    """
    try:
        size = tuple(map(int, message.text.split(',')))
        bot.send_message(message.from_user.id, slau_fill_msg)
        #bot.send_message(message.from_user.id, str(matrix))
        bot.register_next_step_handler(message, coefficient_matrix, size)
    except Exception as e:
        error(message, e, slau)


def coefficient_matrix(message, size):
    """
                Функция продолжает формирование матрицы. Получает: размер
                матрицы в виде кортежа и сообщение, в котором содержатся
                элементы матрицы. В случае исключения перезапускает себя.
                Дальше передаёт сформированную матрицу в функцию для
                формирования второй матрицы.
    """
    try:
        matrix = create_matrix(message, size)
        # todo Написать нормальное сообщение
        # bot.send_message(message.from_user.id, 'Текст')
        bot.register_next_step_handler(message, slau, matrix)
    except Exception as e:
        error(message, e, coefficient_matrix)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
