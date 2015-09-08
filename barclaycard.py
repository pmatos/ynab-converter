#!/usr/bin/env python
import csv
import re
import sys

# License: MIT, Author: Matthias Nieuwenhuisen, Markus Seidl
# Converts from the (German) Barclaycard CSV Format to the popular YNAB import format.
# Usage: python barclaycard.py infile outfile

# File layout:
# _Barclaycard Germany_
# Buchung/ Valuta, Belegdatum, Beschreibung, Kartennummer, Karteninhaber, Betrag
# =======
# _YNAB_
# Date,Payee,Category,Memo,Outflow,Inflow
# 01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,

# Date: DD/MM/YY

def categorizeRow(buchungstag, valutadatum, verwendungszweck, kartennummer, betrag):
    """This method could be used to determine automagically a category for the given entry."""
    return "Unkategorisiert"

def convertToYNAB(row):
    """Converts the read row into the YNAB format explained above"""
    kartennummer = row[3]
    buchungstag = row[1]
    valutadatum = row[0]
    verwendungszweck = row[2]
    betrag = 0
    if row[5][-1] == '-':
        betrag = -float(row[5][0:-1].replace(',', '.'))
    else:
        betrag = float(row[5][0:-1].replace(',', '.'))

    print 'betrag: ' + str(betrag)

    ynab_date = valutadatum.replace('.', '/')
    #ynab_payee = beguenstigter_zahlungspflichtiger
    ynab_payee = str(verwendungszweck)
    ynab_category = categorizeRow(buchungstag, valutadatum, verwendungszweck, kartennummer, betrag)
    ynab_memo = str(verwendungszweck)
    ynab_outflow = ""
    ynab_inflow = ""
    if betrag < 0:
        ynab_outflow = -betrag
    else:
        ynab_inflow = betrag

    return [ynab_date, ynab_payee, ynab_category, ynab_memo, ynab_outflow, ynab_inflow, betrag]

def convertFile(inFileName, outFileName):
    lineNum = 0
    with open(outFileName, 'w') as out:
        csvwriter = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ["Date", "Payee", "Category", "Memo", "Outflow", "Inflow"]
        csvwriter.writerow(header)

        with open(inFileName, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in csvreader:
                lineNum = lineNum + 1
                if lineNum < 13:
                    continue
                if len(row) != 6:
                    return

                ynab_row = convertToYNAB(row)
                csvwriter.writerow(ynab_row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
		print "Syntax: %s infile outfile" % (sys.argv[0])
    else:
		print "Converting from %s to %s" % (sys.argv[1], sys.argv[2])
		convertFile(sys.argv[1], sys.argv[2])

