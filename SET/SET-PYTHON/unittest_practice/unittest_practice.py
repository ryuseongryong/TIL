import unittest
import lib_calc


class TddTest(unittest.TestCase):

    a = 0
    b = 0
    result = 0

    def setUp(self):
        self.a = 10
        self.b = 20

    def testAdd(self):
        self.result = lib_calc.add(self.a, self.b)

        self.assertEqual(self.result, 31)

    def testSubstract(self):
        self.result = lib_calc.substract(self.a, self.b)

        if self.result > 10:
            boolval = True
        else:
            boolval = False

        self.assertTrue(boolval)

    def testDivision(self):
        self.assertRaises(ZeroDivisionError, lib_calc.division, 4, 1)

    def testMultiply(self):
        nonechk = True
        self.result = lib_calc.multiply(10, 9)

        if self.result > 100:
            nonechk = None

        self.assertIsNone(nonechk)

    def tearDown(self):
        print(' 결과 값: ' + str(self.result))


if __name__ == '__main__':
    unittest.main()
