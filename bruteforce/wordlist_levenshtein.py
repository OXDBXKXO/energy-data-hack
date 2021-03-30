import os, argparse, math
from Levenshtein import distance as lev

def getCloserMatch(word, wordlist):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Find closer Levenshtein distance in given wordlist")

    parser.add_argument("word", type=str, help="The word to look for")
    parser.add_argument("--wordlist", type=str, help="Path of the wordlist to use", required=True)

    args = parser.parse_args()

    matches, distance = getCloserMatch(args.word, args.wordlist)

    if distance > 3:
        print("WARNING: Levenshtein distance exceeds 3, result may not be accurate")
    
    print("Levenshtein distance: {}\n".format(distance))
    for match in matches:
        print("Match: {}".format(match))