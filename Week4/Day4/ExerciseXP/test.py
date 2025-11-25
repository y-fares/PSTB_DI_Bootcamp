import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import mlflow
import mlflow.sklearn


def step1():
    # Chargement des fichiers CSV
    train_df = pd.read_csv("fashion-mnist_train.csv")
    test_df = pd.read_csv("fashion-mnist_test.csv")
    print(f"Train shape: {train_df.shape}")
    print(f"Test shape:  {test_df.shape}")
    print(train_df.head())
    
    # Séparation des caractéristiques et des étiquettes
    y_train = train_df["label"]
    X_train = train_df.drop(columns=["label"])
    y_test = test_df["label"]
    X_test = test_df.drop(columns=["label"])

    X_train = X_train / 255.0
    X_test = X_test / 255.0

    print("Valeurs normalisées :")
    print("Min =", X_train.values.min(), " | Max =", X_train.values.max())

def step2():
    # TODO: set tracking URI to localhost:5000
    # TODO: set or create experiment 'FashionMNIST-RandomForest'

    mlflow.set_tracking_uri("http://localhost:5000")
    experiment_name = "FashionMNIST-RandomForest"
    mlflow.set_experiment(experiment_name)

    print(f"MLflow prêt — tracking sur {mlflow.get_tracking_uri()}")
    print(f"Expérience active : {experiment_name}")


step1()
step2()