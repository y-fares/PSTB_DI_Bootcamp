import pandas as pd

df = pd.DataFrame({
    "Nom": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35]
}, index=["a", "b", "c"])

print(df.loc["b", "Nom"])  # Résultat : 'Bob'
print(df.loc["a":"c", "Nom"])  # Résultat : de Alice à Charlie (inclus)