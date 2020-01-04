# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 10:11:34 2019

@author: hpendyal
"""
# student name: heramb pendyala

import matplotlib.pyplot as plt  
import pandas as pd  


url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'Class'] # Assign column names to the dataset
dataset = pd.read_csv(url, names=names) # Read dataset to pandas dataframe
X = dataset.iloc[:, :-1].values # the feature set 'sepal-length', 'sepal-width', 'petal-length', 'petal-width'
y = dataset.iloc[:, 4].values # 'Class'

# percentage split 80% training and 20% testing
from sklearn.model_selection import train_test_split  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)  

# K Neighbors classifier with k=13
from sklearn.neighbors import KNeighborsClassifier  
classifier = KNeighborsClassifier(n_neighbors=13)  #knn classifier
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)  

# display the classificaiton report, confusion matrix and accuracy of the classifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print(confusion_matrix(y_test, y_pred))  
print(classification_report(y_test, y_pred)) 
print(accuracy_score(y_test,y_pred))


print()
print('#------# Solving the question no 2 #------#')
"""
i. Use a list of numbers in the range of 1-100, and filter to generate a list called 
“neighbors” which include only odd numbers in that range. 
"""
a = list(range(1,101))
neighbors = [i for i in a if i%2 != 0]
print('neighbours : ',neighbors)
print()

"""
ii. Use “cross_val_score” function and specify scoring='accuracy' to generate
accuracy from each 10-fold cross validation for the list of “neighbors”. Look at
sklearn.model_selection.cross_val_score to learn more about the required
parameters. 
"""
cv_scores = []
from sklearn.model_selection import cross_val_score
# perform 10-fold cross validation
for k in neighbors:
    knn = KNeighborsClassifier(n_neighbors=k)
    scores = cross_val_score(knn, X, y, cv=10, scoring='accuracy')
    cv_scores.append(scores.mean())
    
"""
Perform 10-fold cross validation and generate a list called “MSE”
(misclassification error) by using the equation, MSE = (1- accuracy). Note: Here
the accuracy is a list that contains the average accuracy of each 10-fold cross
validation (per each neighbors).
"""
# deriving misclassification error
MSE = [1 - x for x in cv_scores]
optimal_k = neighbors[MSE.index(min(MSE))]
error_k=min(MSE)
print( "The optimal 'k' is " + str(optimal_k) + " with misclassification error(MSE) of " + str(error_k))

"""
Generate a Plot “neighbors” vs “MSE” and also find and print the optimal K
using the “MSE” list. Include the plot as a figure in your pdf. 
"""
# plot misclassification error vs k
plt.plot(neighbors, MSE, marker='o')
plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error (MSE)')
plt.title('neighbors vs MSE')
plt.show()