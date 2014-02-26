import itertools
import numpy as np
from sklearn import svm, linear_model, cross_validation

def preProcess(filename):
    X=[]
    y=[]
    with open(filename) as f:
        for line in f:
            xx=[]
            row=line.split()
            y.append((row[0],row[1].split(':')[1]))
            for i in range(2,len(row)):
                xx.append(row[i].split(':')[1])
            X.append(xx)
    f.close()
    return X,y


def pairwise(X, y):

    X_new = []
    y_new = []
    X=np.asfarray(X) 
    y = np.asfarray(y)
    if y.ndim == 1:
        y = np.c_[y, np.ones(y.shape[0])]
    comb = itertools.combinations(range(X.shape[0]), 2)
    for k, (i, j) in enumerate(comb):
        if y[i, 0] == y[j, 0] or y[i, 1] != y[j, 1]:
            continue
        X_new.append(X[i] - X[j])
        y_new.append(np.sign(y[i, 0] - y[j, 0]))
        if y_new[-1] != (-1) ** k:
            y_new[-1] = - y_new[-1]
            X_new[-1] = - X_new[-1]
    return np.asarray(X_new), np.asarray(y_new).ravel()

def SVM(train,test):
    X,y=preProcess(train)
    Xtrans,ytrans=pairwise(X,y)
   

    Xt,yt=preProcess(test)
    Xtrain,ytrain=pairwise(Xt,yt)

    
    clf=svm.SVC(kernel="linear",C=0.2)
    fit=clf.fit(Xtrans,ytrans)
    print "Accuracy:", np.mean(fit.predict(Xtrain)==ytrain)
    print "\n"
    feature=[]
    for i in range(len(clf.coef_[0])):
        feature.append(["Feature "+ str((i+1)),clf.coef_[0][i]])
    feature=sorted(feature,key=lambda x:abs(x[1]))
    feature.reverse()
    for i in range(10):
        print feature[i]
 
    
    
def getSVM():
    for i in range(3):
        train="fold"+str(i+1)+"/train.txt"
        test="fold"+str(i+1)+"/test.txt"
        print "Fold "+str(i+1)
        print "\n"
        SVM(train,test)
    
    
