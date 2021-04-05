from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import os

import keysolver.io.capture as capture

def train_ai(dataset_path, dataset_filename_model, save_file = \
            os.path.join(os.path.dirname(__file__), "ai_model.joblib"), \
            keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', \
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', \
            'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', \
            'CTRL', 'ENTER', 'NOKEY', 'SHIFT', 'SPACE', 'SUPPR']):

    X = []
    y = []

    for key in keys:
        file_name = dataset_filename_model.replace("@", key)
        c = capture.Capture(os.path.join(dataset_path, file_name))

        for i in range(c.nb_frames):
            frame = c.frames[i]
            X.append(frame)
            y.append(key)

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    training_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)

    if save_file != None and save_file != "":
        dump(clf, save_file)

    return training_accuracy, test_accuracy