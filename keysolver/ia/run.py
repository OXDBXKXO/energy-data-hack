from joblib import load
import os, sys

import keysolver.io.capture as capture

def run_ai(file_path, model_file_path = \
            os.path.join(os.path.dirname(__file__), "ai_model.joblib")):
    c = capture.Capture(file_path)
    clf = load(model_file_path)
    return clf.predict(c.frames)
