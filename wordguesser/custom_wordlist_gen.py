import argparse

def combos(lines, iters, writefile=None, prevlines=None):
    """
    Create combinations of words.

    Args:
        lines:          The word to search in the list.

        iters:          The number of words to concatenate.

        writefile:      The file to write the words combos into.

        prevlines:      --Used by recursion mechanism-- Holds all generated combos

    Returns:
        Return nothing but write generated word combos in writefile.

    Example:
        >>> f = open("output.txt", "w")
        >>> combos(["word1", "word2"], 2, f)
    """
    if (iters >= 1):

        nextlines = []

        if (prevlines is None):
            for line in lines:
                nextlines.append(line.strip() + "\n")
                if (writefile is not None):
                    writefile.write(line.strip() + "\n")
        else:
            
            for prevline in prevlines:
                combo = prevline.strip() + "\n"
                nextlines.append(combo)

            for line in lines:
                for prevline in prevlines:
                    combo = line.strip() + prevline.strip() + "\n"

                    if (combo not in nextlines):
                        nextlines.append(combo)
                        if (writefile is not None):
                            writefile.write(combo)
                        elif (writefile is not None and iters == 1):
                            writefile.write(combo)

        return combos(lines, iters-1, writefile, nextlines)

def main():
    """ 
    Create combinations of words from command-line.

    Args:
        iterations:     The number of words to concatenate.

        --words:        Path to the words file. One word per line. Optional parameter (default="words.txt").

        --output:      Path to the output file. Optional parameter (default="output.txt").

    Returns:
        Return nothing but write generated word combos in output file.

    Example:
        >>> python custom_wordlist_gen.py 3 --output wordlist_hackaton.txt
    """
    parser = argparse.ArgumentParser("Generate custom wordlist")

    parser.add_argument("iterations", type=int, help="Maximum words to combine.")
    parser.add_argument("--words", default="words.txt", type=str, help="Path to the words file. One word per line.")
    parser.add_argument("--output",default="output.txt", type=str, help="Path to the output file.")

    args = parser.parse_args()

    wordlist = open(args.words, 'r')
    wordlistlines = []
    for line in wordlist.readlines():
        wordlistlines.append(line)

    global iterations
    iterations = args.iterations

    output = open(args.output, 'w')

    combos(wordlistlines, iterations, output)


if __name__ == "__main__":
    main()