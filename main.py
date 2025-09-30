
from random import choice, shuffle
from PyQt5.QtWidgets import QApplication
from time import sleep


app = QApplication([])  # Створюємо додаток

from main_window import *  # Імпортуємо все з файлу main_window / створюються вікно
from menu_window import * # створюються вікно


class Question():
    def __init__(self, question, answer, wrong_answer1, wrong_answer2, wrong_answer3):
        self.question = question  # Текст питання
        self.answer = answer  # Правильна відповідь
        self.wrong_answer1 = wrong_answer1  # Перший неправильний варіант
        self.wrong_answer2 = wrong_answer2  # Другий неправильний варіант
        self.wrong_answer3 = wrong_answer3  # Третій неправильний варіант
        self.is_active = True  # Чи активне це питання (чи можна його ставити)
        self.count_ask = 0  # Лічильник, скільки разів відповіли за гру
        self.count_right = 0  # Лічильник правильних відповідей на це питання


    def got_right(self):
        # Викликається, якщо відповідь на питання була правильною
        self.count_ask += 1  # Збільшуємо кількість разів, коли питання ставилося
        self.count_right += 1  # Збільшуємо кількість правильних відповідей


    def got_wrong(self):
        # Викликається, якщо відповідь на питання була неправильною
        self.count_ask += 1  # Збільшуємо кількість разів, коли питання ставилося

# Створюємо об'єкти питань
q1 = Question('Яблуко', 'apple', 'application', 'pinapple', 'apply')  # Питання про "Яблуко"
q2 = Question('Дім', 'house', 'horse', 'hurry', 'hour')  # Питання про "Дім"
q3 = Question('Миша', 'mouse', 'mouth', 'muse', 'museum')  # Питання про "Миша"
q4 = Question('Число', 'number', 'digit', 'amount', 'summary')  # Питання про "Число"


questions = [q1, q2, q3, q4]  # Список усіх питань
radio_buttons = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]  # Список радіокнопок для варіантів відповідей


def new_question():
    ''' Показує нове питання '''
    global cur_q  # Використовуємо глобальну змінну для поточного питання
    cur_q = choice(questions)  # Вибираємо випадкове питання зі списку
    lb_Question.setText(cur_q.question)  # Встановлюємо текст питання у відповідний QLabel
    lb_Correct.setText(cur_q.answer)  # Встановлюємо правильну відповідь (для перевірки)
    shuffle(radio_buttons)  # Перемішуємо список радіокнопок


    # Призначаємо текст для кожної радіокнопки
    radio_buttons[0].setText(cur_q.wrong_answer1)  # Перший неправильний варіант
    radio_buttons[1].setText(cur_q.wrong_answer2)  # Другий неправильний варіант
    radio_buttons[2].setText(cur_q.wrong_answer3)  # Третій неправильний варіант
    radio_buttons[3].setText(cur_q.answer)  # Правильний варіант


    # Скидаємо вибір радіокнопок
    RadioGroup.setExclusive(False)  # Тимчасово дозволяємо зняти всі позначки
    for button in radio_buttons:  # Проходимо по всіх радіокнопках
        button.setChecked(False)  # Знімаємо позначку
    RadioGroup.setExclusive(True)  # Повертаємо обмеження на вибір лише однієї кнопки


    AnsGroupBox.hide()  # Ховаємо панель результату
    RadioGroupBox.show()  # Показуємо панель варіантів відповіді
    btn_OK.setText('Відповісти')  # Змінюємо текст кнопки на "Відповісти"


def check():
    ''' Перевіряє правильність відповіді '''
    RadioGroup.setExclusive(False)  # Тимчасово дозволяємо зняти всі позначки
    for answer in radio_buttons:  # Проходимо по всіх радіокнопках
        if answer.isChecked():  # Якщо кнопка вибрана
            if answer.text() == lb_Correct.text():  # Якщо текст відповідає правильній відповіді
                cur_q.got_right()  # Оновлюємо статистику питання (правильна відповідь)
                lb_Result.setText('Вірно!')  # Встановлюємо текст результату
            else:
                cur_q.got_wrong()  # Оновлюємо статистику питання (неправильна відповідь)
                lb_Result.setText('Не вірно!')  # Встановлюємо текст результату
            break  # Виходимо з циклу, оскільки відповідь знайдена
    RadioGroup.setExclusive(True)  # Повертаємо обмеження на вибір лише однієї кнопки
    RadioGroupBox.hide()  # Ховаємо панель варіантів відповіді
    AnsGroupBox.show()  # Показуємо панель результату
    btn_OK.setText('Наступне питання')  # Змінюємо текст кнопки на "Наступне питання"


def click_ok():
    ''' Обробляє натискання кнопки '''
    if btn_OK.text() == 'Відповісти':  # Якщо текст кнопки "Відповісти"
        check()  # Викликаємо функцію перевірки відповіді
    else:  # Якщо текст кнопки "Наступне питання"
        new_question()  # Показуємо нове питання

def rest():
    """
    Функція для відпочинку.
    """
    win_card.hide()  # Ховаємо головне вікно
    n = box_Minutes.value() * 60  # Отримуємо час відпочинку в секундах
    sleep(n)  # Затримка на вказаний час
    win_card.show()  # Показуємо головне вікно

def menu_generation():
    if cur_q.count_ask == 0:
        c = 0
    else:
        c = (cur_q.count_right / cur_q.count_ask) * 100 # 56,74
    
    text = f'Всього разів відповіли: {cur_q.count_ask}\n'\
        f'Вірних відповідей: {cur_q.count_right}\n'\
        f'Успішність: {round(c, 2)}%'
    lb_statistic.setText(text)
    menu_win.show()
    win_card.hide()
    
def clear():
    le_question.clear()
    le_right_ans.clear()
    le_wrong_ans1.clear()
    le_wrong_ans2.clear()
    le_wrong_ans3.clear()
    
btn_clear.clicked.connect(clear)

def add_question():
    new_q = Question(le_question.text(), le_right_ans.text(), le_wrong_ans1.text(),
                     le_wrong_ans2.text(), le_wrong_ans3())
    questions.append(new_q)
    clear()
    
btn_add_question.clicked.connect(add_question)
    
           

    
def back_menu():
    menu_win.hide()
    win_card.show()
    
btn_Menu.clicked.connect(menu_generation)

btn_back.clicked.connect(back_menu)

btn_Sleep.clicked.connect(rest)

btn_OK.clicked.connect(click_ok)  # Підключаємо функцію click_ok до натискання кнопки


# Показуємо перше питання
new_question()  # Викликаємо функцію для показу першого питання
app.exec_()  # Запускаємо головний цикл програми