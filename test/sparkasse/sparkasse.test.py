#!/usr/bin/env python

import unittest

# simple "hack" to include the main file

import sys
sys.path.append("../../")

import sparkasse

class sparkasse_test(unittest.TestCase):
    def testConvertToYNAB1(self):
        testdata1_inp = ["XXX","XXX","09.03.14","Buchungstext","Verwendungszweck","Zahlungspflichtiger","","XXX","-100,00","EUR","Info"]
        testdata1_out = [ "09/03/14", "Zahlungspflichtiger", "Unkategorisiert", "Verwendungszweck Buchungstext Info", 100, "", -100 ]

        subject = sparkasse.convertToYNAB(testdata1_inp)
        self.assertEqual(subject, testdata1_out)

    def testConvertToYNAB2(self):
        testdata2_inp = ["XXX","XXX","09.03.14","Buchungstext","Verwendungszweck","Zahlungspflichtiger","","XXX","100,00","EUR","Info"]
        testdata2_out = [ "09/03/14", "Zahlungspflichtiger", "Unkategorisiert", "Verwendungszweck Buchungstext Info", "", 100, 100 ]

        subject = sparkasse.convertToYNAB(testdata2_inp)
        self.assertEqual(subject, testdata2_out)


if __name__ == "__main__":
    unittest.main()