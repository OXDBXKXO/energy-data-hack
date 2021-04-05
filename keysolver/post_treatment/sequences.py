def get_all_possible_sequences(possible_keys_seq):
    """
    Get all possible sequences from a list of possible keys list.

    Arguments:
        possible_keys_seq:   A list of possible keys list.

    Returns:
        A list containing all the possible sequences.

    Examples:
        >>> ks.get_all_possible_sequences([['A'], ['B', 'C'], ['D']])
        ['A C D', 'A B D']

        >>> ks.get_all_possible_sequences([['A'], ['B', 'C'], ['D', 'E']])
        ['A C D', 'A C E', 'A B D', 'A B E']
    """

    previous_stack = []
    next_stack = []

    for key in possible_keys_seq[0]:
        previous_stack.append(key)

    for i in range(1, len(possible_keys_seq)):
        possible_keys = possible_keys_seq[i]

        while len(previous_stack) != 0:
            keys = previous_stack.pop()

            for key in possible_keys:
                next_stack.append(keys + " " + key)

        previous_stack = next_stack
        next_stack = []

    return previous_stack