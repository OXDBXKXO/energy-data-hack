def get_all_possible_sequences(possible_letters_seq):

    previous_stack = []
    next_stack = []

    for letter in possible_letters_seq[0]:
        previous_stack.append(letter)

    for i in range(1, len(possible_letters_seq)):
        possible_letters = possible_letters_seq[i]

        while len(previous_stack) != 0:
            word = previous_stack.pop()

            for letter in possible_letters:
                next_stack.append(word + letter)

        previous_stack = next_stack
        next_stack = []

    return previous_stack