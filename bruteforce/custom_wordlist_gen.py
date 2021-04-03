import argparse

def combos(lines, iters, writefile=None, prevlines=None):

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

#the main function
def main():

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


#execute the main function
if __name__ == "__main__":
    main()