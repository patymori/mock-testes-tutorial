import unittest


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('python'.upper(), 'PYTHON')

    def test_isupper(self):
        self.assertTrue('PYTHON'.isupper())
        self.assertFalse('Python'.isupper())

    def test_split(self):
        s = 'Python Brasil [15]'
        self.assertEqual(s.split(), ['Python', 'Brasil', '[15]'])
        with self.assertRaises(TypeError):
            s.split(3)


if __name__ == '__main__':
    unittest.main()
