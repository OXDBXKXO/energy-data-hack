from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from joblib import dump
import os

import keysolver.io.capture as capture

def train_ai(dataset_path, dataset_filename_model, save_file_path = \
            os.path.join(os.path.dirname(__file__), "ai_model.joblib"), \
            keys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', \
            'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', \
            'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', \
            'CTRL', 'ENTER', 'NOKEY', 'SHIFT', 'SPACE', 'SUPPR']):
    """
    Train the AI that will be used to solve the keys in a file.

    Args:
        dataset_path:           The path to the directory of the dataset used
                                to train the AI.

        dataset_filename_model: The model of a filename in a directory. It
                                contains a symbol '@' that will be replaced by
                                the characters contained in 'keys' argument.

        save_file_path:         The path of the file in which the AI training
                                is saved. By default, it is saved in a file
                                'ai_model.joblib', in the same directory of this
                                file.

        keys:                   The name of the keys to train the AI with. They
                                are used to build the name of the training
                                files. By default, alphanum keys and some
                                special keys.

    Returns:
        A tuple holding the training accuracy and the test accuracy.

    Examples:
        >>> # Files are located in './data/'
        >>> # The file containing the frames of the key A is named pics_A.bin
        >>> # The file containing the frames of the key B is named pics_B.bin
        >>> # etc
        >>> train_ai("./data/", "pics_@.bin")
        (0.99, 0.57)
    """

    # The list containing each of the frames
    X = []
    # The list containing the key associated to each frame
    y = []

    for key in keys:
        # Build the file name according to the key
        file_name = dataset_filename_model.replace("@", key)
        # Open and read the file of the key
        c = capture.Capture(os.path.join(dataset_path, file_name))

        # For each frame, add it in X and add the key in y
        for i in range(c.nb_frames):
            frame = c.frames[i]
            X.append(frame)
            y.append(key)

    # Train the AI
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)

    # Get the training accuracy and the test accuracy
    training_accuracy = clf.score(X_train, y_train)
    test_accuracy = clf.score(X_test, y_test)

    # Save the AI in the file if valid save_file
    if save_file_path != None and save_file_path != "":
        dump(clf, save_file_path)

    return training_accuracy, test_accuracy