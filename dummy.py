import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
columns = ["Name", "Marks"]
df = pd.read_csv("input.csv", usecols=columns)
print("Contents in csv file:\n", df)
plt.plot(df.Name, df.Marks)
plt.show()
