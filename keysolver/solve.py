from keysolver.ai import run_ai
from keysolver.io import write_data_to_output
from keysolver.post_treatment import get_all_possible_sequences
from keysolver.post_treatment import filter_keys

def solve(file_path, output_file_path=None):
    """
    Solve the key sequences contained in the file given as argument.

    Args:
        file_path:          The path of the file.
        output_file_path:   The file in which store the result.

    Returns:
        A list of possible key sequences.

    Examples:
        >>> solve("./given/pics_LOGINMDP.bin")
        ['CTRL SHIFT D SHIFT T SHIFT M SHIFT I H W C K A T O N 2 0 2 2 ENTER',
        'CTRL SHIFT D SHIFT T SHIFT M SHIFT I H W C K W G O N 3 0 2 4 ENTER'...]
    """

    # Get the prediction of the ai
    prediction = run_ai(file_path)
    # Filter the keys
    filtered_keys = filter_keys(prediction)
    # Get the possible sequences
    possible_sequences = get_all_possible_sequences(filtered_keys)

    # Write sequences in a file if requested
    if output_file_path != None:
        write_data_to_output(possible_sequences, output_file_path)

    return possible_sequences