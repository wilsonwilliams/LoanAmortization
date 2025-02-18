import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy_financial as npf
import sys


# Variables for the loan
# Principal in dollars
# Interest rate as a decimal
# Maturity in years (must be integer)
principal = 1_000_000
interestRate = 0.07
maturity = 25


# Calculates annual payment given principal, interest rate, and maturity
def calculatePayment(principal, interestRate, maturity):
    pmt = npf.pmt(interestRate, maturity, principal)
    return -pmt


# Creates a dataframe for the amortization schedule
def getDf(principal, interestRate, payment, maturity):
    data = np.zeros((maturity, 4))
    remainingPrincipal = principal

    # [Year, Remaining Principal, Interest Payment, Principal Payment]
    for i in range(0, maturity):
        data[i][0] = i + 1
        data[i][1] = remainingPrincipal
        data[i][2] = remainingPrincipal * interestRate
        data[i][3] = payment - data[i][2]
        remainingPrincipal -= data[i][3]
    
    if (abs(remainingPrincipal) > 0.0001):
        sys.exit("Error creating loan schedule")

    return pd.DataFrame(data, columns=["Year", "Remaining Principal", "Interest Payment", "Principal Payment"])


# Creates a matplotlib plot showing the principal and interest payments over the loan lifespan
def createPlot(df):
    years = df["Year"]
    interestPayments = df["Interest Payment"]
    principalPayments = df["Principal Payment"]

    plt.plot(years, interestPayments, color='r', label="Interest Payments")
    plt.plot(years, principalPayments, color='b', label="Principal Payments")

    plt.xlabel("Year")
    plt.ylabel("Payment ($)")
    plt.title("Loan Payments")
    plt.legend()

    plt.show()
    return None


# Create loan amortization schedule and plot
def run(principal, interestRate, maturity):
    pmt = calculatePayment(principal, interestRate, maturity)
    df = getDf(principal, interestRate, pmt, maturity)
    createPlot(df)


run(principal, interestRate, maturity)
