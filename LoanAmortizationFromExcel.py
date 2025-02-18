import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("LoanAmortization.xlsx", sheet_name="Schedule")

print(df)
print(df.columns.to_list())

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
