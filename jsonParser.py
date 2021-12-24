import json
from time import sleep
from apartmentClass import Apartment


def get_int(price: str) -> int:
    res = ''
    for char in price:
        if char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.']:
            res += char
    return int(res.split('.')[0])


def main():
    print('Я Вам помогу выбрать квартиру с оптимальным местоположением\nНо прежде ответьте на несколько вопросов:')
    print(f"Введите желаемое количество комнат (варианты: " + ', '.join(
        rooms) + "), можете перечислить несколько через запятую: ")
    room_number = input()
    while room_number not in rooms:
        print("Некорректный ввод")
        room_number = input()

    print(f"Введите минимальную площадь (от {min_areas}) в м²: ")
    min_area = int(input())
    while min_area < min_areas:
        print("Некорректный ввод")
        min_area = int(input())

    print(f"Введите максимальную площадь (до {max_areas}) в м²: ")
    max_area = int(input())
    while max_area > max_areas:
        print("Некорректный ввод")
        max_area = int(input())

    print(f"Введите максимальную цену (до {prices} ₽) в рублях: ")
    max_price = int(input())
    while max_price > prices:
        print("Некорректный ввод")
        max_price = int(input())

    print("Хотите учесть еще параметры? (да или нет)")
    ans = input()
    while ans not in ['да', 'нет']:
        print("Некорректный ввод")
        ans = input()

    dict_of_potentials = {}

    if ans == 'да':
        print("Введите желаемый тип комнат (варианты: " + ', '.join(
            rooms_type) + "), можете перечислить несколько через запятую: ")
        room_type = input()
        while room_type not in rooms_type:
            print("Некорректный ввод")
            room_type = input()

        print("Желаемый тип отделки (варианты: " + ', '.join(repairs) + "): ")
        repair = input()
        while repair not in repairs:
            print("Некорректный ввод")
            repair = input()

        print("Желаемый санузел (варианты: " + ', '.join(bathrooms) + "): ")
        bathroom = input()
        while bathroom not in bathrooms:
            print("Некорректный ввод")
            bathroom = input()

        print("Желаемый балкон (варианты: " + ', '.join(balcony) + "): ")
        balcon = input()
        while balcon not in balcony:
            print("Некорректный ввод")
            balcon = input()

        print("Желаемый вид из окна (варианты: " + ', '.join(window_views) + "): ")
        window_view = input()
        while window_view not in window_views:
            print("Некорректный ввод")
            window_view = input()

        print("Желаемые дополнительные опции (варианты: " + ', '.join(optionals) + "): ")
        optional = input()
        while optional not in optionals:
            print("Некорректный ввод")
            optional = input()

        print('Идет поиск лучшего варианта...')
        sleep(5)

        current_request = Apartment(room_number, min_area, max_area, max_price, room_type, repair, bathroom, balcon,
                                    window_view, optional)

        cnt = 0
        for j in range(len(apartments)):
            if apartments[f'{j}'] not in didnt_load:
                if apartments[f'{j}']["Количество комнат"].split(' ')[0] in current_request.room_number:
                    if current_request.min_area <= get_int(
                            apartments[f'{j}']["Общая площадь"]) <= current_request.max_area:
                        if get_int(apartments[f'{j}']["Общая площадь"]) < current_request.max_area:
                            if get_int(apartments[f'{j}']["Цена"]) < current_request.max_price:

                                if current_request.room_type == 'не важно' or apartments[f'{j}']["Тип комнат"] == current_request.room_type:
                                    if current_request.repair == 'не важно' or apartments[f'{j}']["Отделка"] == current_request.repair:
                                        if current_request.bathroom == 'не важно' or apartments[f'{j}']["Санузел"] == current_request.bathroom:
                                            if current_request.balcony == 'не важно' or apartments[f'{j}']["Балкон или лоджия"] == current_request.balcony:
                                                if current_request.window_view == 'не важно' or apartments[f'{j}']["Вид из окон"] == current_request.window_view:
                                                    if current_request.optional == 'не важно' or apartments[f'{j}']["Дополнительно"] == current_request.optional:
                                                        dict_of_potentials[f'{cnt}'] = apartments[f'{j}']
                                                        cnt += 1





    else:
        print('Идет поиск лучшего варианта...')
        sleep(5)

        current_request = Apartment(room_number, min_area, max_area, max_price)

        cnt = 0
        for j in range(len(apartments)):
            if apartments[f'{j}'] not in didnt_load:
                if apartments[f'{j}']["Количество комнат"].split(' ')[0] in current_request.room_number:
                    if current_request.min_area <= get_int(
                            apartments[f'{j}']["Общая площадь"]) <= current_request.max_area:
                        if get_int(apartments[f'{j}']["Общая площадь"]) < current_request.max_area:
                            if get_int(apartments[f'{j}']["Цена"]) < current_request.max_price:
                                dict_of_potentials[f'{cnt}'] = apartments[f'{j}']
                                cnt += 1

    print(dict_of_potentials)
    print(len(dict_of_potentials))


# словарь словарей всех квартир
apartments = json.load(open('apartments.json', encoding='utf-8'))

# список индексов квартир без адреса
didnt_load = []

rooms = ["не важно"]
rooms_type = ["не важно"]
min_areas = 150
max_areas = 0
repairs = ["не важно"]
finishing = ["не важно"]
bathrooms = ["не важно"]
balcony = ["не важно"]
window_views = ["не важно"]
optionals = ["не важно"]
prices = 0

for i in range(len(apartments)):
    if apartments[f'{i}']["Широта"] == "?":
        didnt_load.append(f'{i}')
    else:
        try:
            if apartments[f'{i}']["Количество комнат"] not in rooms:
                rooms.append(apartments[f'{i}']["Количество комнат"])
        except:
            pass
        try:
            if apartments[f'{i}']["Тип комнат"] not in rooms_type:
                rooms_type.append(apartments[f'{i}']["Тип комнат"])
        except:
            pass
        try:
            if int(apartments[f'{i}']["Общая площадь"][:-3]) > max_areas:
                max_areas = int(apartments[f'{i}']["Общая площадь"][:-3])
        except:
            pass
        try:
            if int(apartments[f'{i}']["Общая площадь"][:-3]) < min_areas:
                min_areas = int(apartments[f'{i}']["Общая площадь"][:-3])
        except:
            pass
        try:
            if apartments[f'{i}']["Отделка"] not in repairs:
                repairs.append(apartments[f'{i}']["Отделка"])
        except:
            pass
        try:
            if apartments[f'{i}']["Отделка"] not in repairs:
                repairs.append(apartments[f'{i}']["Отделка"])
        except:
            pass
        try:
            if apartments[f'{i}']["Санузел"] not in bathrooms:
                bathrooms.append(apartments[f'{i}']["Санузел"])
        except:
            pass
        try:
            if apartments[f'{i}']["Балкон или лоджия"] not in balcony:
                balcony.append(apartments[f'{i}']["Балкон или лоджия"])
        except:
            pass
        try:
            if apartments[f'{i}']["Вид из окон"] not in window_views:
                window_views.append(apartments[f'{i}']["Вид из окон"])
        except:
            pass
        try:
            if apartments[f'{i}']["Дополнительно"] not in optionals:
                optionals.append(apartments[f'{i}']["Дополнительно"])
        except:
            pass
        try:
            if get_int(apartments[f'{i}']["Цена"][:-2]) > prices:
                prices = get_int(apartments[f'{i}']["Цена"][:-2])
        except:
            pass

# итоговые варианты характеристик
rooms = ['1', '2', '3', '4', '6', 'студия', 'не важно']
rooms_type = ['изолированные', 'смежные', 'не важно']
repairs = ['черновая', 'без отделки', 'чистовая', 'не важно']
finishing = ['не важно']
bathrooms = ['несколько', 'совмещенный', 'раздельный', 'не важно']
balcony = ['балкон', 'лоджия', 'нет', 'не важно']
window_views = ['на улицу', 'во двор', 'на улицу, во двор', 'не важно']
optionals = ['мебель', 'панорамные окна', 'не важно']
