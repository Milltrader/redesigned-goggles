import math
import argparse
import sys
parser = argparse.ArgumentParser(description="Data for calculations")
parser.add_argument("--type", choices =["diff", "annuity"])
parser.add_argument("--principal", default=0)
parser.add_argument("--periods", default=0)
parser.add_argument("--interest", default=0)
parser.add_argument("--payment", default=0)
args = parser.parse_args()
indata =[args.type, args.principal, args.periods, args.interest, args.payment]
if (indata[0] != "diff" and indata[0] != "annuity") or indata[0] == "diff" and args.payment != 0 or args.interest == 0:
    print("Incorrect parameters")
    exit()
if len(sys.argv) != 5:
    print("Incorrect parameters")
    exit()

if indata[0] == "diff":
    loan_principal = float(indata[1])
    periods = int(indata[2])
    loan_interest = float(indata[3])
    i = loan_interest / (12 * 100)
    tot = 0
    for m in range(periods + 1):
        D = math.ceil(loan_principal/periods + i * (loan_principal - (loan_principal * (m - 1)/periods)))
        if m == 0:
            D = 0
        else:
            tot += D
        if D > 0:
            print(f'Month {m}: payment is {D}')

    ovp = tot - loan_principal
    print()
    print(f'Overrpayment = {math.ceil(ovp)}')

elif indata[0] == "annuity":
    loan_principal = float(indata[1])
    periods = int(indata[2])
    loan_interest = float(indata[3])
    i = loan_interest / (12 * 100)
    loan_payment = float(indata[4])

    if periods != 0 and loan_principal != 0:
        loan_payment = loan_principal * ((i * (1 + i) ** periods) / (((1 + i) ** periods) - 1))
        loan_payment_rounded = math.ceil(loan_payment)
        print(f'Your annuity payment = {loan_payment_rounded}!')
        print(f'Overpayment = {int(loan_payment_rounded * periods - loan_principal)}')
    elif periods != 0 and loan_principal == 0 :
        P = loan_payment / ((i * (1 + i) ** periods) / (((1 + i) ** periods) - 1))
        print(f'Your loan principal = {int(P)}!')
        print(f'Overpayment = {math.ceil(((loan_payment * periods) - P))}')
    else:
        n = math.ceil(math.log(loan_payment / (loan_payment - i * loan_principal), 1 + i))
        res1 = n // 12
        res1_1 = n - res1 * 12
        if res1_1 == 1:
            m = "month"
        else:
            m = "months"
        if res1 == 0:
             print(f'It will take {res1_1} {m} to repay this loan!')
        elif res1_1 == 0 and res1 != 1:
             print(f'It will take {res1} years to repay this loan!')
        elif res1 == 1 and res1_1 != 0:
             print(f'It will take 1 year and {res1_1} {m} to repay this loan!')
        elif res1 == 1 and res1_1 == 0:
            print(f'It will take 1 year to repay this loan!')
        else:
             print(f'It will take {res1} years and {res1_1} {m} to repay this loan!')
        print(f'Overpayment = {math.ceil(((loan_payment * n) - loan_principal))}')
