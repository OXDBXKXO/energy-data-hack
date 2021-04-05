import os, argparse, math
from Levenshtein import distance as lev

def getCloserMatch(word, wordlist):
    """
    Search closest match (using Levenshtein distance)

    Args:
        word:           The word to search in the list.

        wordlist:       Path to the wordlist to perform the search into.

    Returns:
        A tuple holding the matches array and Levenshtein distance between the
        word variable and these matches.

    Example:
        >>> getCloserMatch("azerto", "wordlists/french_top1000.txt")
        Levenshtein distance: 1

        Match: azerty
        Match: azert
    """

    try:
        f = open(wordlist, 'r')
        passwords = f.read().splitlines()
        f.close()
    except:
        print("Could not find required file")
        exit(1)

    min_distance = math.inf
    matches = []
    for password in passwords:
        distance = lev(word, password)
        if distance < min_distance:
            min_distance = distance
            matches = [ password ]
            
        elif distance == min_distance:
            matches.append(password)

    return matches, min_distance


def main():
    """ 
    Create combinations of words from command-line.

    Args:
        --word:             The word to look for.

        --words             The words to look for

        wordlist:           The path of the wordlist to use.

    Returns:
        Find closer Levenshtein distance in given wordlist.

    Example:
        >>> python wordlist_levenshtein.py azerty --output wordlists/french_top1000.txt
    """

    parser = argparse.ArgumentParser("Find closer Levenshtein distance in given wordlist")

    parser.add_argument("--word", type=str, help="The word to look for")
    parser.add_argument("--words", type=str, help="The words to look for")
    parser.add_argument("wordlist", type=str, help="The path of the wordlist to use")

    args = parser.parse_args()

    if not args.word and not args.words:
        print("You must set --word or --words")
        exit(1)

    if not (args.words):
        matches, distance = getCloserMatch(args.word, args.wordlist)

        if distance > 3:
            print("WARNING: Levenshtein distance exceeds 3, result may not be accurate")
        
        print("Levenshtein distance: {}\n".format(distance))
        for match in matches:
            print("Match: {}".format(match))
    else:
        try:
            f = open(args.words, 'r')
            passwords = f.read().splitlines()
            f.close()
        except:
            print("Could not find required file")
            exit(1)

        final_matches = []
        min_distance = math.inf
        for word in passwords:
            matches, distance = getCloserMatch(word, args.wordlist)
            if distance < min_distance:
                min_distance = distance
                final_matches = []
                for match in matches:
                    final_matches.append(match)
            
            elif distance == min_distance:
                for match in matches:
                    final_matches.append(match)

        print("Levenshtein distance: {}\n".format(min_distance))
        for match in final_matches:
            print("Match: {}".format(match))


if __name__ == "__main__":
    main()