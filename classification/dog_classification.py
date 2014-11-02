from os import listdir
from os.path import isfile, join
from scipy.io import loadmat
import numpy as np
from sklearn import svm
import random

def read_data(directory):
    print "Reading in data"
    onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
    data = []
    labels = []
    for f in onlyfiles:
        if f.endswith(".mat"):
            mat = loadmat(join(directory,f))
            keys = mat.keys()
            name = keys[0]
            struct = mat.get(name)[0][0][0]
            if type(struct) == str:
                continue
            s = name.split('-')
            data_type = s[0]
            data.append(struct)
            labels.append(data_type)

    return data, labels

def get_features(data):
    print "Creating features"
    feats = []
    
    for d in data:
        f = []
        for i in xrange(len(d)):
            fft = np.fft.rfft(d[i])
            for val in fft:
                f.append(val * np.conjugate(val))
        feats.append(f)

    return feats

def cross_validation(data, label, k=5):
    A = zip(data, label)
    shuffled = random.shuffle(A)
    size = len(data)
    test_size = size / k
    for i in xrange(0, size - test_size, test_size):
        test = A[i:i + test_size]
        train = A[:i] + A[i + test_size:]

        yield train, test

if __name__=="__main__":
    data, labels = read_data("../../copy")
    feats = get_features(data)

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

        acc / len(test)
        accuracy += acc

    accuracy = accuracy / k
    print accuracy
