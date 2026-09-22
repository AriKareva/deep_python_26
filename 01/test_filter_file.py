import os
import tempfile
import unittest
from . import solution as sl


class TestFilterFile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = ['роза', 'вулкан', 'чапаев', 'пустота']
        cls.stop = ['азора']
        cls.text = "\n".join([
            "а Роза упала на лапу Азора",
            "Роза пахнет розой",
            "розан и роза в одном саду",
            "АЗОРА прячется в тени",
            "Азор спал на крыльце",
            "Вулкан проснулся сегодня утром",
            "чапаев и пустота рядом",
            "Чапаев шел по пустоте",
            "пустота пустота пустота",
            "Вулкан и роза вместе",
            "Тихий вечер в старом парке",
            "Роза Роза Роза трижды",
            "азора АЗОРА азора трижды",
            "кот и пес играли во дворе",
            "Вулканы бывают разные",
        ])

        with tempfile.NamedTemporaryFile(
            'w', delete=False, encoding='utf-8'
        ) as f:
            f.write(cls.text)
            cls.filename = f.name

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.filename):
            os.remove(cls.filename)

    def test_target_in_res(self):
        res = list(sl.filter_file(self.filename, self.target, self.stop))
        self.assertIn('Роза пахнет розой', res)
        self.assertIn('Вулкан проснулся сегодня утром', res)
        self.assertIn('розан и роза в одном саду', res)

    def test_stop_not_in_res(self):
        res = list(sl.filter_file(self.filename, self.target, self.stop))
        self.assertNotIn('а Роза упала на лапу Азора', res)
        self.assertNotIn('АЗОРА прячется в тени', res)
        self.assertNotIn('азора АЗОРА азора трижды', res)

    def test_strict_equality(self):
        res = list(sl.filter_file(self.filename, self.target, self.stop))
        self.assertNotIn('Вулканы бывают разные', res)
        self.assertIn('розан и роза в одном саду', res)

    def test_no_duplicates(self):
        res = list(sl.filter_file(self.filename, self.target, self.stop))
        self.assertEqual(res.count('чапаев и пустота рядом'), 1)
        self.assertEqual(res.count('пустота пустота пустота'), 1)
        self.assertEqual(res.count('Роза Роза Роза трижды'), 1)
        self.assertEqual(res.count('Вулкан и роза вместе'), 1)

    def test_no_coincidence(self):
        res = list(sl.filter_file(self.filename, self.target, self.stop))
        self.assertNotIn('Азор спал на крыльце', res)
        self.assertNotIn('Тихий вечер в старом парке', res)
        self.assertNotIn('кот и пес играли во дворе', res)

    def test_is_generator(self):
        g = sl.filter_file(self.filename, self.target, self.stop)
        self.assertTrue(hasattr(g, '__iter__'))
        self.assertTrue(hasattr(g, '__next__'))

    def test_order(self):
        res = list(sl.filter_file(self.filename, self.target, self.stop))
        exp = [
            "Роза пахнет розой",
            "розан и роза в одном саду",
            "Вулкан проснулся сегодня утром",
            "чапаев и пустота рядом",
            "Чапаев шел по пустоте",
            "пустота пустота пустота",
            "Вулкан и роза вместе",
            "Роза Роза Роза трижды",
        ]
        self.assertEqual(res, exp)

    def test_firdt_line(self):
        g = sl.filter_file(self.filename, self.target, self.stop)
        self.assertEqual(next(g), 'Роза пахнет розой')
