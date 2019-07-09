import pandas as pd
from libraries.bridge import *

from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO
from IPython.display import Image
import pydotplus

col_names = [PROGRAM_NAME, PROG_BLK_NUM, TOOL_NUMBER, OPERATION_CODE]
class_names = ['6', '99', '0', '21', '9', '10', '1','2', '8', '7']
file_path = r'C:\TFM\data\weka\machine.csv'
plot_path = r'C:\TFM\data\weka\machine.png'
# load dataset


def decision_tree():

    machine = pd.read_csv(file_path, header=0, delimiter=',')
    print(machine.head())

    # split dataset in features and target variable
    feature_cols = [PROGRAM_NAME, PROG_BLK_NUM, TOOL_NUMBER]
    X = machine[feature_cols]  # Features
    y = machine[OPERATION_CODE]

    # Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=1)  # 70% training and 30% test

    # Create Decision Tree classifer object
    clf = DecisionTreeClassifier()

    # Train Decision Tree Classifer
    clf = clf.fit(X_train, y_train)

    # Predict the response for test dataset
    y_pred = clf.predict(X_test)

    # Model Accuracy, how often is the classifier correct?
    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    dot_data = StringIO()
    export_graphviz(clf, out_file=dot_data,
                    filled=True, rounded=True,
                    special_characters=True, feature_names=feature_cols, class_names=class_names)
    graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
    graph.write_png(plot_path)
    Image(graph.create_png())




