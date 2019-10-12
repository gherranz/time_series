# Dependencies

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt

from libraries.bridge import *


col_names = [PROGRAM_NAME, PROG_BLK_NUM, TOOL_NUMBER, OPERATION_CODE]
class_names = ['6', '99', '0', '21', '9', '10', '1','2', '8', '7']
file_path = r'C:\TFM\data\weka\machine.csv'
plot_path = r'C:\TFM\data\weka\machine.png'
train_path = r'C:\TFM\data\weka\machine_train.csv'
test_path = r'C:\TFM\data\weka\machine_test_2.csv'
# load dataset


def k_means_model():
    """
    Function to generate a K-means model with the necessary data.
    """

    # Load the train and test datasets to create two DataFrames
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    # print("***** Train_Set *****")
    # print(train.head())
    # print("\n")
    # print("***** Test_Set *****")
    # print(test.head())
    #
    # print("***** Train_Set *****")
    # print(train.describe())
    # print("\n")
    # print("***** Test_Set *****")
    # print(test.describe())
    #
    # print("*****In the train set*****")
    # print(train.isna().sum())
    # print("\n")
    # print("*****In the test set*****")
    # print(test.isna().sum())

    # Fill missing values with mean column values in the train set
    train.fillna(train.mean(), inplace=True)
    # Fill missing values with mean column values in the test set
    test.fillna(test.mean(), inplace=True)

    X = np.array(train.drop(['CNC_Operation_Code'], 1).astype(int))
    y = np.array(train['CNC_Operation_Code'])

    kmeans = KMeans(n_clusters=len(class_names))  # You want cluster the passenger records into 2: Survived or Not survived
    kmeans.fit(X)

    KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
           n_clusters=len(class_names), n_init=10, n_jobs=1, precompute_distances='auto',
           random_state=None, tol=0.0001, verbose=0)

    correct = 0
    for i in range(len(X)):
        predict_me = np.array(X[i].astype(float))
        predict_me = predict_me.reshape(-1, len(predict_me))
        prediction = kmeans.predict(predict_me)
        if prediction[0] == y[i]:
            correct += 1

    print(correct / len(X))

    kmeans = KMeans(n_clusters=len(class_names), max_iter=600, algorithm='auto')
    kmeans.fit(X)

    KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=600,
           n_clusters=len(class_names), n_init=10, n_jobs=1, precompute_distances='auto',
           random_state=None, tol=0.0001, verbose=0)

    correct = 0
    for i in range(len(X)):
        predict_me = np.array(X[i].astype(float))
        predict_me = predict_me.reshape(-1, len(predict_me))
        prediction = kmeans.predict(predict_me)
        if prediction[0] == y[i]:
            correct += 1

    print(correct / len(X))

    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans.fit(X_scaled)

    KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=600,
           n_clusters=len(class_names), n_init=10, n_jobs=1, precompute_distances='auto',
           random_state=None, tol=0.0001, verbose=0)

    correct = 0
    for i in range(len(X)):
        predict_me = np.array(X[i].astype(float))
        predict_me = predict_me.reshape(-1, len(predict_me))
        prediction = kmeans.predict(predict_me)
        if prediction[0] == y[i]:
            correct += 1

    print(correct / len(X))

