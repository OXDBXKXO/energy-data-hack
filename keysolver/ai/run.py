from joblib import load
import os

import keysolver.io.capture as capture

def run_ai(file_path, model_file_path = \
            os.path.join(os.path.dirname(__file__), "ai_model.joblib")):
    """
    Run the AI that is used to solve the keys in a file.

    Args:
        file_path:              The path of the file from which the keys should be
                                solved.

        model_file_path:        The path of the file from which the AI training
                                should be loaded. By default, the file
                                'ai_model.joblib', in the same directory of this
                                file.

    Returns:
        A list containing the solved key for each frame of the file.

    Examples:
        >>> # The file containing the frames of the key A is named pics_A.bin
        >>> run_ai("./data/pics_A.bin")
        ['A', 'A', 'A', 'Q', 'A', ... 'A']
    """

    # Open and read the file
    c = capture.Capture(file_path)
    # Load the AI
    clf = load(model_file_path)

    # Return the list prediction
    return clf.predict(c.frames).tolist()
