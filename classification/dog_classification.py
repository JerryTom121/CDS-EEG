import os
from scipy.io import loadmat
import numpy as np
from sklearn import svm
import random

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
    #READ IN DATA
    data, labels = read_data("../../copy")

    #EXTRACT FEATURES
    #feats = fft(data)
    feats = flatten(data)

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
    k = 5
    #train 1 vs. 1 SVM
    print "Training"
    for train, test in cross_validation(train_data, train_label, k):
        clf = svm.SVC()
        f_train, l_train = zip(*train)
        clf.fit(f_train, l_train)
        acc = 0.0
        for f, l in test:
            prediction = clf.predict(f)
            if prediction == l:
                acc += 1.0

        acc = acc / len(test)
        print acc
        accuracy += acc

    accuracy = accuracy / k
    print accuracy
