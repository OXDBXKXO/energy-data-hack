from keysolver.io.output_writing import write_data_to_output
from keysolver.io.capture import Capture
from keysolver.ia.run import run_ai

def solve(file_path, output_file_path=None):
    pred = run_ai(file_path)
    # TODO: ia process

    # TODO: post treatment

    # TODO: write results