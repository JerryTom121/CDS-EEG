import os
from scipy.io import loadmat
import numpy as np
from sklearn import svm, decomposition, neighbors
import random
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Train and test Kaggle EEG dog data")
    parser.add_argument('--path', dest="path", type=str, help="Path to tagged data. REQUIRED", required=True)
    parser.add_argument('--features', dest="features", type=str, help="Type of features to use", choices=["raw", "fft", "cpa"], default="raw")
    parser.add_argument('--classifier', dest="classifier", type=str, help="Type of classifier to use", choices=["svm"], default="svm")
    parser.add_argument('--k', dest="k", type=int, default=5, help="k for cross validation")
    parser.add_argument('--pca', dest="pca", action='store_true', help="Apply pca")

    args = parser.parse_args()
    return args

def read_data(directory):
    print "Reading in data"
    data = []
    labels = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".mat"):
                mat = loadmat(os.path.join(directory,f))
                keys = mat.keys()
                name = keys[0]
                struct = mat.get(name)[0][0][0]
                if type(struct) == str:
                    continue
                s = name.split('_')
                l = s[0]
                data.append(struct)
                labels.append(l)

    return data, labels

#FEATURE EXTRACTORS
def fit_pca(data):
    print "PCA"
    pca = decomposition.PCA(n_components=0.5)
    X = []
    for d in data:
        for i in xrange(len(d)):
            X.append(d[i])

    pca.fit(X)

    return pca

def pca(data, pca_trained):
    feats = []
    for d in data:
        f = []
        for i in xrange(len(d)):
            if f==[]:
                f = pca_trained.transform(d[i])
            else:
                f = f + pca_trained.transform(d[i])
        feats.append(f.flatten())

    return feats
    
def flatten(data):
    print "Flatten"
    feats = []
    
    for d in data:
        feats.append(d.flatten())

    return feats

def fft(data):
    print "FFT"
    feats = []
    
    for d in data:
        f = []
        for i in xrange(len(d)):
            fft = np.fft.rfft(d[i])
            for val in fft:
                f.append((val * np.conjugate(val)).astype(np.int64))
        feats.append(f)

    return feats

def cpa(data):
    feats = []

    return feats

def cross_validation(data, label, k=5):
    A = zip(data, label)
    random.shuffle(A)
    size = len(data)
    test_size = size / k
    for i in xrange(0, size - test_size + 1, test_size):
        test = A[i:i + test_size]
        train = A[:i] + A[i + test_size:]

        yield train, test

if __name__=="__main__":
    args = parse_args()
    #READ IN DATA
    data, labels = read_data(args.path)

    #EXTRACT FEATURES
    if args.features == "raw":
        feats = flatten(data)
    elif args.features == "fft":
        feats = fft(data)
    elif args.features == "cpa":
        feats = cpa(data)

    train_data = []
    train_label = []
    test_data = []

    for f, l in zip(feats, labels):
        if l == 'test':
            test_data.append(f)
        else:
            train_data.append(f)
            train_label.append(l)

    #TRAIN CLASSIFIER
    accuracy = 0.0
    k = args.k
    #train 1 vs. 1 SVM
    print "Training"
    for train, test in cross_validation(train_data, train_label, k):
        if args.classifier == "svm":
            clf = svm.SVC()

        f_train, l_train = zip(*train)
        f_test, l_test = zip(*test)

        #Apply PCA
        if args.pca:
            pca_trained = fit_pca(f_train)
            f_train = pca(f_train, pca_trained)
            f_test = pca(f_test, pca_trained)

        clf.fit(f_train, l_train)
        acc = 0.0
        for f, l in zip(f_test, l_test):
            prediction = clf.predict(f)
            if prediction == l:
                acc += 1.0

        acc = acc / len(test)
        print acc
        accuracy += acc

    accuracy = accuracy / k
    print accuracy
