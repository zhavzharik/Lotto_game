import random
import pandas as pd


def gen_row(unic, rows):
    calc = [1, 10, 20, 30, 40, 50, 60, 70, 80]
    numbers = []
    # генерируем цифры для первых двух строк карточки (в каждом "столбце карточки" цифры определенного десятка)
    if len(rows) < 18:
        for start in calc:
            if start == 80:
                flag = 0
                while flag < 1:
                    number = random.randint(start, start + 10)
                    if number not in unic:
                        numbers.append(number)
                        flag = 1
            elif start == 1:
                flag = 0
                while flag < 1:
                    number = random.randint(start, start + 8)
                    if number not in unic:
                        numbers.append(number)
                        flag = 1
            else:
                flag = 0
                while flag < 1:
                    number = random.randint(start, start + 9)
                    if number not in unic:
                        numbers.append(number)
                        flag = 1

        delete = random.sample(numbers, k=4)
        for d in delete:
            numbers.insert(numbers.index(d), " ")
            numbers.remove(d)

        unic_temp = set(numbers)
        unic_temp.remove(' ')
        unic.extend(list(unic_temp))
    # генерируем цифры для третьей строки карточки (сначала в тех "столбцах карточки", где пусто, потом, где одна цифра)
    if len(rows) == 18:
        check = 0
        for start in calc:
            if check < 5:
                if rows[int(start / 10)] == ' ' and rows[int(start / 10 + 9)] == ' ':
                    flag = 0
                    while flag < 1:
                        number = random.randint(start, start + 9)
                        if number not in unic:
                            numbers.append(number)
                            flag = 1
                            check += 1

                elif rows[int(start / 10)] == ' ' or rows[int(start / 10 + 9)] == ' ':
                    flag = 0
                    while flag < 1:
                        number = random.randint(start, start + 9)
                        if number not in unic:
                            numbers.append(number)
                            flag = 1
                            check += 1
                else:
                    numbers.append(' ')
            else:
                numbers.append(' ')

    return list(unic), list(numbers)


def gen_card():
    unic = []
    rows = []
    unic1, numbers1 = gen_row(unic, rows)
    rows1 = rows + numbers1
    unic2, numbers2 = gen_row(unic1, rows1)
    rows2 = rows1 + numbers2
    unic3, numbers3 = gen_row(unic2, rows2)
    data = [numbers1] + [numbers2] + [numbers3]
    df = pd.DataFrame(data)
    # если сгененировалась карточка с пустым столбцом, запускаем генерацию сначала
    if df.isin([' ']).replace([True, False], [1, 0]).sum().isin([3]).sum() == 1:
        df = gen_card()
    return df


if __name__ == '__main__':
    card = gen_card()
    print(card)
    print('*' * 35)
    print(card.isin([' ']).replace([True, False], [1, 0]).sum().isin([3]).sum())
    if card.isin([' ']).replace([True, False], [1, 0]).sum().isin([3]).sum() == 1:
        card1 = gen_card()
        print(card1)