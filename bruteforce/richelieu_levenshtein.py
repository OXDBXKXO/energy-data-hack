import os, argparse, math
from Levenshtein import distance as lev

def getCloserMatch(word, wordlist):
    try:
        f = open(wordlist, 'r')
        passwords = f.readlines()
        f.close()
    except:
        print("Could not find required file")
        exit(1)

    min_distance = math.inf
    match = ""
    for password in passwords:
        distance = lev(word, password)
        if distance < min_distance:
            min_distance = distance
            match = password

    return match, min_distance


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Find closer Levenshtein distance in given wordlist")

    parser.add_argument("word", type=str, help="The word to look for", required=True)
    parser.add_argument("--wordlist", type=str, help="Path of the wordlist to use", required=True)

    parser.parse_args()

    match, distance = getCloserMatch(parser.word, parser.wordlist)

    if distance > 3:
        print("WARNING: Levenshtein distance exceeds 3, result may not be accurate")
    
    print("Levenshtein distance: {}\nMatch: {}".format(distance, match))