from random import randint
from emoji import emojize

import config

# emoji dict
emoji = {
    "e_hello" : emojize(":waving_hand:"),
    "e_gear" : emojize(":gear:"),
    "e_condiction" : [
        emojize(":cross_mark:"),
        emojize(":check_mark_button:")
    ]
}


# keyboard text
keyboard_text_start = "Что вы хотите сделать?"


# start text
start_main_text = """

Я ваш помочник с экономическими задачами Аркадий!

Я могу помочать вам решить следующие задачи:
- Построить общую КПВ
- Найти точку рыночного равновесия [ТРР]
- Расчитать объем дефицита/излишка для заданных функций спроса и предложения и уровня цены
- Расчитать прибыль фирмы

Если у Вас есть вопросы, введите /help, и я постараюсь вам помочь
"""
second_start_main_text = "Что вы хотите сделать?"


#help text
help_main_text = """
Возникли вопросы по командам?

Я помогу вам разобраться с ними!

Просто выберите о каком пункте Вы хотите узнать подробней
1 - построение общей КПВ
2 - нахождение точки рыночного равновесия
3 - расчет объема дефицита/излишка
4 - расчет прибыля фирмы
"""

help_question_text = "Что-нибудь еще?"

help_point_text = [

        """
Построение графика КПВ.
(КПВ - Кривая Производственных Возможностей)

Тут все просто!

Вы вводите максимальное количество товаров А и Б для двух производителей.

Я же строю для тебя график, который показиывает общую КПВ для этих товаров.

P.S. Так как я не являюсь мощным вычислительным средством, то лимит на количество товаров будет составлять 10000
Если он будет превышен, то я автоматически снижу количество до максимального значения.
""",

        """
Рассчет точки рыночного равновесия.

Ничего сложного тут нет!

Заданы функции спроса и предложения:

Qd = A*P - B (функция спроса)
Qs = C - D*P (функция предложения)

Вы вводите коэффициенты A, B, C и D, а я рассчитаю вам равновесную цену P и равновесный объем Q

Равновесная цена P и равновесный объем Q - параметры рыночного равновесия.
""",

        """
инфа по пунтку 3
""",

        """
инфа по пункту 4
"""
    ]


# settings text
# base solution text
solution_flag_text = f"""
{emoji['e_gear']}Настройки{emoji['e_gear']}
Показывать решение для расчета ТРР: {emoji['e_condiction'][config.solution_ep_flag]}
Показывать решение для определения ДиИ: {emoji['e_condiction'][config.solution_def_surp_flag]}
"""


# solution text
# update solution text func 
def update_solution_text(solution_ep_flag_id, solution_def_surp_flag_id):
    global solution_flag_text

    solution_flag_text = f"""
{emoji['e_gear']}Настройки{emoji['e_gear']}
Показывать решение для расчета ТРР: {emoji['e_condiction'][solution_ep_flag_id]}
Показывать решение для определения ДиИ: {emoji['e_condiction'][solution_def_surp_flag_id]}
"""


# func for create solution text for equilibrium point
def create_solution_ep_text(A: float, B: float, C: float, D: float, P: float, Q: float) -> str:
    text = f"""
Функции спроса и предложения задаются следующими функциями:

Qd = {A}*P {'-' if B > 0 else '+'} {abs(B)} (функция спроса)
Qs = {C} {'-' if D > 0 else '+'} {abs(D)}*P (функция предложения)

Для нахождения ТРР, то есть параметров равновесия, приравняем функцию спроса к функции предложения:

Qd = Qs
{A}*P {'-' if B > 0 else '+'} {abs(B)} = {C} {'-' if D > 0 else '+'} {abs(D)}*P
{A + D}*P = {round(C + B, 2)}

P = {P} - равновесная стоимость

Чтобы найти равновесный объем, подставим равновесную стоимость в любую из функций сроса или предложения:

Q = {A}*{P} {'-' if B > 0 else '+'} {abs(B)}

Q = {Q}
"""
    return text


# func for create solution text for deficit and surplus
def create_solution_def_surp_text(A: float, B: float, C: float, D: float, E: float, P: float, Qd: float, Qs: float, Q: float, condition: str) -> str:
    support_comparison_text = "P = E" if condition == "равновесия" else f"""
P {'>' if condition == "дефицита" else '<'} E

Значит на рынке будет ситуация {condition}.

Расчитаем размер {condition}.

Qd = {A}*{E} {'-' if B > 0 else '+'} {abs(B)}
Qs = {C} {'-' if D > 0 else '+'} {abs(D)}*{E}

Отсюда:

Q = {'Qd - Qs' if condition == 'дефицита' else 'Qs - Qd'}

Q = {Qd if condition == 'дефицита' else Qs} - {Qs if condition == 'дефицита' else Qd}

Q = {Q}

"""
        
    text = f"""
Функции спроса и предложения задаются следующими функциями:

Qd = {A}*P {'-' if B > 0 else '+'} {abs(B)} (функция спроса)
Qs = {C} {'-' if D > 0 else '+'} {abs(D)}*P (функция предложения)

Для определения дефицита/излишка, найдем ТРР.
Для этого приравняем функцию спроса к функции предложения:

Qd = Qs
{A}*P {'-' if B > 0 else '+'} {abs(B)} = {C} {'-' if D > 0 else '+'} {abs(D)}*P
{A + D}*P = {round(C + B, 2)}

P = {P} - равновесная стоимость

Далее сравним равновесную цену P с заданной ценой товара E:

{support_comparison_text}

"""
    return text


# request text
# graph 
graph_request = [
    "Введите максимальный объем производства товара А для первого производителя",
    "Введите максимальный объем производства товара Б для первого производителя",
    "Введите максимальный объем производства товара А для второго производителя",
    "Введите максимальный объем производства товара Б для второго производителя"
]
# equilibrium point
ep_request = [
    "Введите коэффициент A",
    "Введите коэффициент B",
    "Введите коэффициент C",
    "Введите коэффициент D"
]
# deficite and surplus
def_surp_request = [
    "Введите коэффициент A",
    "Введите коэффициент B",
    "Введите коэффициент C",
    "Введите коэффициент D",
    "Введите уровень цены Е"
]
# profit
profit_request = [
    "Введите объем производства в штуках",
    "Введите цену в штуках (руб. за единицу товара)",
    "Введите данные о постоянных издержках \n (название издержки - размер издержки)",
    "Введите данные о переменных издержках \n (название издержки - размер издержки)"
]

# filter answer text
incorrect_message_text = "Извините, но я не понимаю вас"
incorrect_settings_data_text = "Прошу использовать только приведенные ниже кнопки"
incorrect_num_text = "Прошу вводить только числа"
incorrect_negative_num_text = "Прошу вводить положительные числа"
incorrect_zero_message_text = "Прошу вводить числа не равные нулю"

incorrect_command = """
Хотел бы я поболтать, но нужно заняться делом!
Прошу, выберите, что хотите сделать
"""

correct_data_example = f"Пример вводимых данных: {randint(20, 600)}"


# buttons text
button_graph = 'Построить общую КПВ.'
button_equilibrium_point = 'Найти ТРР.'
button_deficit_and_surplus = 'Определить дефицит/излишек.'
button_profit = 'Рассчитать прибыль фирмы.'

button_none_costs = 'Издержек нет.'

button_back_to_menu = 'Вернуться на главную.'

button_switch_solution = {
    "ep" : [
        'Включить решение ТРР',
        'Выключить решение ТРР'
    ],
    
    "def_surp" : [
        'Включить решение ДиИ',
        'Выключить решение ДиИ'
    ]
}

button_help_1 = '1'
button_help_2 = '2'
button_help_3 = '3'
button_help_4 = '4'

button_indev = 'Кнопка еще не готова' 
