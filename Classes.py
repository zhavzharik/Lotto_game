import random
from functions import gen_card


class Card:
    """Класс карточка (для игры в лото)"""
    def __init__(self, name):
        self.name = name
        self.card = gen_card()
        self.is_keg = False
        self.comp_cross_out_nb = False

    # печатаем карточку игрока
    def print_card(self):
        print('-' * 9, f"{self.name}", '-' * 8)
        print(self.card.to_string(index=False, header=False))
        print('-' * 26)

    # проверяем, есть ли бочонок на карточке
    def check_keg(self, keg):
        if self.card.replace([' ', '-'], 0).isin([keg]).replace([True, False], [1, 0]).sum().sum() == 1:
            self.is_keg = True

    # зачеркиваем цифру бочонка на карточке
    def cross_out_nb(self, keg):
        if self.is_keg:
            self.card.replace(keg, '-', inplace=True)
            self.is_keg = False
            self.comp_cross_out_nb = True

    # считаем сумму цифр на карточке
    def calc_sum(self):
        return int(self.card.replace([' ', '-'], 0).sum().sum())


class Bag:
    """Класс мешок (для игры в лото)"""
    def __init__(self):
        self.bag_numbers = random.sample(range(1, 91), k=90)
        self.new_keg = None

    # генерируем новый бочонок из мешка
    @property
    def gen_new_keg(self):
        self.new_keg = random.sample(self.bag_numbers, k=1)
        return int(self.new_keg[0])

    # удаляем бочонок из мешка
    def update_bag(self, nb):
        self.bag_numbers.remove(nb)

    # количество бочонков в мешке
    def __len__(self):
        return len(self.bag_numbers)


class Player:
    """Родительский  класс для игроков (компьютер и пользователь)"""

    def __init__(self, name):
        self.name = name
        self.card = Card(name)
        self.is_player = True
        self.is_winner = False

    # для печати имени
    def __str__(self):
        return f"{self.name}"

    # проверка победителя
    def check_winner(self):
        summa = self.card.calc_sum()
        if summa == 0:
            self.is_winner = True


class Computer(Player):
    """Дочерний  класс для игроков (компьютер)"""

    # компьютер всегда правильно зачеркивает свои цифры, если они есть
    def play_card(self, keg):
        self.card.check_keg(keg)
        self.card.cross_out_nb(keg)
        if self.card.comp_cross_out_nb:
            print(f"{self.name}, зачеркнул цифру {keg}")
            self.card.comp_cross_out_nb = False


class User(Player):
    """Дочерний  класс для игроков (пользователь)"""

    def __init__(self, name):
        super().__init__(name)
        self.answer = None

    def get_answer(self, keg):
        while True:
            self.answer = input(f'{self.name}, Зачеркнуть цифру {keg}?:(y/n): ')
            if self.answer == 'y' or self.answer == 'n':
                return self.answer

    # если пользователь ошибётся при зачеркивании цифры, он выбывает из игры
    def play_card(self, keg):
        self.answer = self.get_answer(keg)
        self.card.check_keg(keg)
        if self.answer == 'y' and self.card.is_keg:
            self.card.cross_out_nb(keg)
            print(f"{self.name}, на Вашей карточке зачеркнута цифра {keg}")
        elif self.answer == 'y' and not self.card.is_keg:
            self.is_player = False
            print(f"{self.name}, Вы пытались зачеркнуть цифру, её нет на карточке. Для Вас игра окончена.")
        elif self.answer == 'n' and self.card.is_keg:
            self.is_player = False
            print(f"{self.name}, Вы не зачеркнули цифру. Для Вас игра окончена.")
        elif self.answer == 'n' and not self.card.is_keg:
            print(f"{self.name}, Ok!")


class Game:
    """Класс игра"""
    def __init__(self):
        self.bag = Bag()
        self.new_keg = None
        self.nb_users = self.get_nb_users
        self.nb_computers = self.get_nb_computers
        self.players = []
        self.player = {}
        self.game_over = False

    @property
    def get_nb_users(self):
        while True:
            self.nb_users = int(input('Введите количество игроков-пользователей: '))
            if isinstance(self.nb_users, int):
                return self.nb_users

    @property
    def get_nb_computers(self):
        while True:
            self.nb_computers = int(input('Введите количество игроков-компьютеров: '))
            if isinstance(self.nb_computers, int):
                return self.nb_computers

    # генерация списка игроков
    def gen_list_players(self):
        for i in range(self.nb_computers):
            self.player = Computer(f"Comp {i + 1}")
            self.players.append(self.player)
        for i in range(self.nb_users):
            self.player = User(f"User {i + 1}")
            self.players.append(self.player)

    # печать карточек всех игроков из списка
    def print_all_card(self):
        for player in self.players:
            player.card.print_card()

    # проверка и печать победителя
    def print_winner(self):
        if len(self.players) > 1:
            for player in self.players:
                player.check_winner()
                if player.is_winner:
                    print('Стоп ИГРА! У нас есть победитель!')
                    self.print_all_card()
                    print(f'{player.name} победил, так как первым зачеркнул все цифры на карточке! \nДо встречи в '
                          f'следующий раз!')
                    self.game_over = True
                    break
        else:
            print('Стоп ИГРА!')
            print(f'{self.players[0].name} победил, так как остальные участники выбыли из игры или не захотели играть!'
                  f'\nДо встречи в следующий раз!')
            self.game_over = True

    # один ход игры (рандомно определяем бочонок, игроки зачеркивают цифры, кто неправильно зачеркнул, выбывает)
    def game_continue(self):
        self.new_keg = self.bag.gen_new_keg
        self.bag.update_bag(self.new_keg)
        print(f"Бочонок: {self.new_keg}, (осталось: {len(self.bag)})")
        self.print_all_card()
        for player in self.players:
            player.play_card(self.new_keg)
        for player in self.players:
            if not player.is_player:
                self.players.remove(player)

    # повтор одного ходы игры, пока игра не завершится
    def all_game(self):
        print('Начинаем играть!')
        self.gen_list_players()
        while not self.game_over:
            try:
                self.game_continue()
                self.print_winner()
            except IndexError:
                print("Победителей нет, так как все участники выбыли из игры!")
                break


if __name__ == '__main__':
    user = User('user1')
    bag = Bag()
    new_keg = bag.gen_new_keg
    bag.update_bag(new_keg)
    print(f"Бочонок: {new_keg}, (осталось: {len(bag)})")
    user.card.print_card()
    user.play_card(new_keg)
    user.card.print_card()
