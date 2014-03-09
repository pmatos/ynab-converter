#!/usr/bin/env python
import csv
import re
import sys

# License: MIT, Author: Markus Seidl
# Converts from the "Sparkasse CSV-MT940" to the popular YNAB import format.
# Usage: python sparkasse.py infile outfile

# File layout:
# _Sparkasse_
# Auftragskonto, Buchungstag, Valutadatum, Buchungstext, Verwendungszweck, Beguenstigter/Zahlungspflichtiger, Kontonummer, BLZ, Betrag, Waehrung, Info
# =======
# _YNAB_
# Date,Payee,Category,Memo,Outflow,Inflow
# 01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,

# Date: DD/MM/YY

def categorizeRow(auftragskonto, buchungstag, valutadatum, buchungstext, verwendungszweck, beguenstigter_zahlungspflichtiger, kontonummer, blz, betrag, waehrung, info):
    """This method could be used to determine automagically a category for the given entry."""
    return "Unkategorisiert"

def convertToYNAB(row):
    """Converts the read row into the YNAB format explained above"""
    auftragskonto = row[0]
    buchungstag = row[1]
    valutadatum = row[2]
    buchungstext = row[3]
    verwendungszweck = row[4]
    beguenstigter_zahlungspflichtiger = row[5]
    kontonummer = row[6]
    blz = row[7]
    betrag = float(row[8].replace(',', '.'))
    waehrung = row[9]
    info = row[10]

    ynab_date = valutadatum.replace('.', '/')
    ynab_payee = beguenstigter_zahlungspflichtiger
    ynab_category = categorizeRow(auftragskonto, buchungstag, valutadatum, buchungstext, verwendungszweck, beguenstigter_zahlungspflichtiger, kontonummer, blz, betrag, waehrung, info)
    ynab_memo = str(verwendungszweck) + " " + str(buchungstext) +  " " + str(info)
    ynab_outflow = ""
    ynab_inflow = ""
    if betrag < 0:
        ynab_outflow = -betrag
    else:
        ynab_inflow = betrag

    return [ynab_date, ynab_payee, ynab_category, ynab_memo, ynab_outflow, ynab_inflow, betrag]

def convertFile(inFileName, outFileName):
    firstLine = True
    with open(outFileName, 'w') as out:
        csvwriter = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ["Date", "Payee", "Category", "Memo", "Outflow", "Inflow"]
        csvwriter.writerow(header)

        with open(inFileName, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in csvreader:
                if firstLine:
                    firstLine = False
                    continue

                ynab_row = convertToYNAB(row)
                csvwriter.writerow(ynab_row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
		print "Syntax: %s infile outfile" % (sys.argv[0])
    else:
		print "Converting from %s to %s" % (sys.argv[1], sys.argv[2])
		convertFile(sys.argv[1], sys.argv[2])

