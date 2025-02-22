import sys
from enum import Enum
from tabulate import tabulate

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy_financial as npf


class Payments(Enum):
    ANNUAL = 0
    MONTHLY = 1


# Variables for the loan
# Principal in dollars
# Interest rate as a decimal
# Maturity in years (must be integer)
principal = 1_000_000
interestRate = 0.07
maturity = 25
paymentSchedule = Payments.ANNUAL


# Calculates annual payment given principal, interest rate, and maturity
def calculatePayment(principal, interestRate, maturity):
    pmt = npf.pmt(interestRate, maturity, principal)
    return -pmt


# Creates a dataframe for the amortization schedule
def getDf(principal, interestRate, payment, maturity, paymentSchedule):
    data = np.zeros((maturity, 4))
    remainingPrincipal = principal

    # [Time, Remaining Principal, Interest Payment, Principal Payment]
    for i in range(0, maturity):
        data[i][0] = i + 1
        data[i][1] = remainingPrincipal
        data[i][2] = remainingPrincipal * interestRate
        data[i][3] = payment - data[i][2]
        remainingPrincipal -= data[i][3]
    
    if (abs(remainingPrincipal) > 0.0001):
        sys.exit("Error creating loan schedule")

    return pd.DataFrame(data, columns=[f"Time ({'Year' if paymentSchedule == Payments.ANNUAL else 'Month'})", "Remaining Principal", "Interest Payment", "Principal Payment"])


# Creates a matplotlib plot showing the principal and interest payments over the loan lifespan
def createPlot(df, paymentSchedule):
    time = df[f"Time ({'Year' if paymentSchedule == Payments.ANNUAL else 'Month'})"]
    interestPayments = df["Interest Payment"]
    principalPayments = df["Principal Payment"]

    plt.plot(time, interestPayments, color='r', label="Interest Payments")
    plt.plot(time, principalPayments, color='b', label="Principal Payments")

    plt.xlabel(f"Time ({'Year' if paymentSchedule == Payments.ANNUAL else 'Month'})")
    plt.ylabel("Payment ($)")
    plt.title("Loan Payments")
    plt.legend()

    plt.show()
    return None


# Create loan amortization schedule and plot
def run(principal, interestRate, maturity, paymentSchedule):
    if (paymentSchedule == Payments.MONTHLY):
        interestRate /= 12
        maturity *= 12

    pmt = calculatePayment(principal, interestRate, maturity)
    df = getDf(principal, interestRate, pmt, maturity, paymentSchedule)

    print(f"\nYour {'Annual' if paymentSchedule == Payments.ANNUAL else 'Monthly'} Payment: ${pmt.round(2):,}")
    print()
    
    totalPayment = (pmt * maturity).round(2)
    print(f"Total of {maturity} {'Annual' if paymentSchedule == Payments.ANNUAL else 'Monthly'} Payments: ${totalPayment:,}")
    print()

    totalInterestPaid = df["Interest Payment"].sum().round(2)
    print(f"Total Interest Paid: ${totalInterestPaid:,}")
    print()

    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False, ))

    createPlot(df, paymentSchedule)

run(principal, interestRate, maturity, paymentSchedule)
