import numpy as np
from sklearn.linear_model import LinearRegression


# x enthält: [mAh, Helligkeit]
x = np.array([[3000, 50], [4000, 70], [5000, 90]])

# y enthält das Ergebnis: Laufzeit in Stunden
y = np.array([10, 12, 14])


modell = LinearRegression()

modell.fit(x, y)

vorhersage = modell.predict([[4500, 60]])
print("Die Vorhersage für die akkukapazität beträgt:", vorhersage)
