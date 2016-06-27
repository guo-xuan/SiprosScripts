'''
Created on Jun 16, 2016

@author: xgo
'''
import sys
#Import Library
from sklearn.ensemble import RandomForestClassifier #use RandomForestRegressor for regression problem
from sklearn.datasets import load_iris
import numpy as np


def main(argv=None):
    iris = load_iris()
    rf = RandomForestClassifier(max_depth = 4)
    idx = range(len(iris.target))
    np.random.shuffle(idx)
    rf.fit(iris.data[idx][:100], iris.target[idx][:100])
    
    instance = iris.data[idx][100:101]
    print rf.predict_proba(instance)


if __name__ == '__main__':
    sys.exit(main())