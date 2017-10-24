#!/usr/bin/env python
import csv
import re
import sys

# License: MIT, Author: Paulo Matos
# Converts from the (German) IngDiba CSV Format to the popular YNAB import format.
# Usage: python ingdiba.py infile outfile

# _YNAB_
# Date,Payee,Category,Memo,Outflow,Inflow
# 01/25/12,Sample Payee,,Sample Memo for an outflow,100.00,

# Date: DD/MM/YY

def convertToYNAB(row):
    """Converts the read row into the YNAB format explained above"""
    ynab_date = row[1].replace('.', '/')
    ynab_payee = row[2]


    ynab_category = "Unkategorisiert"
    ynab_memo = ' - '.join([row[3], row[4]])

    ynab_outflow = ""
    ynab_inflow = ""
    betrag = float(row[5].replace('.', '').replace(',', '.'))
    if betrag < 0:
        ynab_outflow = -betrag
    else:
        ynab_inflow = betrag

    return [ynab_date, ynab_payee, ynab_category, ynab_memo, ynab_outflow, ynab_inflow]

def convertFile(inFileName, outFileName):
    lineNum = 0
    with open(outFileName, 'w') as out:
        csvwriter = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ["Date", "Payee", "Category", "Memo", "Outflow", "Inflow"]
        csvwriter.writerow(header)

        with open(inFileName, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for row in csvreader:
                lineNum = lineNum + 1
                if lineNum < 8:
                    continue
                if len(row) != 9:
                    return

                ynab_row = convertToYNAB(row)
                csvwriter.writerow(ynab_row)

if __name__ == "__main__":
    if len(sys.argv) < 2:
		print "Syntax: %s infile outfile" % (sys.argv[0])
    else:
		print "Converting from %s to %s" % (sys.argv[1], sys.argv[2])
		convertFile(sys.argv[1], sys.argv[2])
