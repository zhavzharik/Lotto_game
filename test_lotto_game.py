import pytest
import unittest
import random
from Classes import Card, Bag, Player, Computer, User


class TestCard(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        self.card = Card("Max")
        self.leo = Card("Leo")

    def tearDown(self):
        del self.card
        del self.leo

    def test_init(self):
        self.assertEqual(self.card.name, "Max")
        self.assertFalse(self.card.is_keg)
        self.assertEqual(self.card.comp_cross_out_nb, False)

    def test_str(self):
        self.assertNotEqual(self.card.__str__(), self.leo.__str__())

    def test_len(self):
        self.assertEqual(len(self.card), 3)

    def test_eq(self):
        self.assertEqual(len(self.card), len(self.leo))

    def test_rt(self):
        self.assertTrue(self.card > self.leo)

    def test_check_keg(self):
        self.card.check_keg(25)
        self.assertTrue(self.card.is_keg)

    def test_cross_out_nb(self):
        self.card.cross_out_nb(25)
        self.assertFalse(self.card.is_keg)

    def test_calc_sum(self):
        self.assertGreaterEqual(self.card.calc_sum(), 0)


class TestBag:

    def setup(self):
        self.bag = Bag()
        self.sack = Bag()

    def teardown(self):
        del self.bag
        del self.sack

    def test_init(self):
        assert self.bag.new_keg == None
        assert len(self.bag.bag_numbers) == 90

    def test_str(self):
        assert list(self.bag.__str__())

    def test_len(self):
        assert len(self.bag.bag_numbers) == 90

    def test_ge(self):
        assert len(self.bag.bag_numbers) >= len(self.sack.bag_numbers)

    def test_eq(self):
        assert len(self.bag.bag_numbers) == len(self.sack.bag_numbers)

    def test_lt(self):
        self.bag.update_bag(12)
        assert len(self.bag.bag_numbers) < len(self.sack.bag_numbers)

    def test_gen_new_keg(self):
        assert self.bag.gen_new_keg <= 90

    def test_update_bag(self):
        self.bag.update_bag(50)
        assert len(self.bag.bag_numbers) == 89
        self.bag.update_bag(52)
        assert len(self.bag.bag_numbers) == 88


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Max")
        self.player2 = Player("Leo")

    def tearDown(self):
        del self.player
        del self.player2

    def test_init(self):
        self.assertEqual(self.player.name, "Max")
        self.assertTrue(self.player.is_player)
        self.assertFalse(self.player.is_winner)

    def test_str(self):
        self.assertEqual(self.player.__str__(), "Max")

    def test_check_winner(self):
        self.assertGreaterEqual(self.player.card.calc_sum(), 0)
        self.assertFalse(self.player.is_winner)

    def test_eq(self):
        self.assertEqual(self.player, self.player2)


class TestComputer(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        self.computer = Computer("Werter")

    def tearDown(self):
        del self.computer

    def test_str(self):
        self.assertEqual(self.computer.__str__(), "Werter")

    def test_play_card(self):
        self.assertEqual(self.computer.__str__(), "Werter")
        self.assertEqual(self.computer.name, "Werter")
        self.computer.card.check_keg(26)
        self.assertTrue(self.computer.card.is_keg)
        self.computer.play_card(26)
        self.assertFalse(self.computer.card.is_keg)
        self.assertFalse(self.computer.card.cross_out_nb(26))


class TestUser(unittest.TestCase):

    def setUp(self):
        random.seed(42)
        self.user = User("Lana")

    def tearDown(self):
        del self.user

    def test_init(self):
        self.assertEqual(self.user.name, "Lana")
        self.assertEqual(self.user.answer, None)

    def test_get_answer(self):
        with self.assertRaises(Exception):
            self.user.get_answer(85)

    def test1_play_card(self):
        with self.assertRaises(Exception):
            self.user.play_card(85)

    def test2_play_card(self):
        with self.assertRaises(OSError):
            self.user.play_card(23)














