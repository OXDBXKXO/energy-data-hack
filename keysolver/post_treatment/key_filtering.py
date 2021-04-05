
__SLIDING_WINDOW = 80
__SHIFT_RADIUS = 50


class KeyPress:
    """
    Represent a key presses. Instances of this class are immutable.

    Attributes:
        key:        A tring representing the key (e.g. "A", "SHIFT" or "NOKEY")
        count:      The number of consecuting repetitions.
        has_shift:  True if the SHIFT modifier is applied.
    """

    def __init__(self, key, count=1, has_shift=False):
        self.__key = key
        self.__count = count
        self.__has_shift = has_shift
    
    @property
    def key(self):
        return self.__key
    
    @property
    def count(self):
        return self.__count
    
    @property
    def has_shift(self):
        return self.__has_shift


def __detect_modifiers(keys, radius):
    """
    Try to detect keys with a SHIFT modifier.

    Args:
        keys:     A list of KeyPress.
        radius:  How far back and ahead the algorithm will look for SHIFT frames.

    Returns:
        The "key" array is modified in place and returned.
    """
    
    # for each key : a greater score means more SHIFT frames in the neighborhood,
    # a smaller score means more NOKEY frames.
    score = [0] * len(keys)
    
    for i in range(len(keys)):
    
        # will the score be increased or decreased in this neighborhood? 
        mod = 0
        if keys[i].key == "NOKEY":
            mod = -1
        elif keys[i].key == "SHIFT":
            mod = 1
        else:
            continue
    
        # applying the score
        neighborhood_begin = max(0, i - radius)
        neighborhood_end = min(len(keys), i + radius)
        for j in range(neighborhood_begin, i):
            score[j] += mod
        for j in range(i, neighborhood_end):
            score[j] += mod

        # applying the SHIFT modifier where the score is strictly positive
    for i in range(len(keys)):
        if score[i] > 0:
            keys[i] = KeyPress(keys[i].key, keys[i].count, True)

    return keys


def __has_mostly_shift(keys):
    """
    Detect whether a list of keys contains more keys with or without the SHIFT modifier.

    Args:
        keys:     A list of KeyPress.

    Returns:
        True if there are more key presses with the SHIFT modifier, False otherwise.
    """

    return sum([(1 if key.has_shift else -1) for key in keys]) > 0


def __get_histo(keys):
    """
    Compute the frequency of every key in a set of key presses.

    Args:
        keys:     A list of KeyPress.
      
    Returns:
        A dictionary whose keys are key strings, and whose elements are occurence counts.
    """

    histo = dict()

    for key in keys:
        if key.key in histo:
            histo[key.key] += key.count
        else:
            histo[key.key] = key.count

    return histo


def __get_most_frequent(keys):
    """
    Get the key with the most occurences in a list.

    Args:
        keys:     A list of KeyPress.
    
    Returns:
        A KeyPress corresponding to the most represented key.
    """ 

    histo = __get_histo(keys)

    most_frequent = ""
    max_count = 0

    for element, count in histo.items():
        if count > max_count:
            most_frequent = element
            max_count = count

    return KeyPress(most_frequent, 1, __has_mostly_shift(keys))


def __sliding_most(keys, window_size):
    """
    Computes, using a sliding window, the most represented key in each window.

    Args:
        keys:     A list of KeyPress.
    
    Returns:
        A list of KeyPress, corresponding to the "keys" argument but keeping only maximum values.
    """

    result = []
    window = keys[0:window_size]

    for key in keys[window_size - 1:]:
        window = window[1:] + [key]
        most_frequent = __get_most_frequent(window)
        result.append(most_frequent)

    return result


def __dedup(keys):
    """
    Merge duplicate adjacent keys.

    Args:
        keys:     A list of KeyPress.
    
    Returns:
        A list of KeyPress, corresponding to the "keys" argument but with duplicate adjacent keys merged.
    """

    len_keys = len(keys)

    if len_keys == 0:
        return []

    result = [keys[0]]

    for i in range(1, len_keys):
        key = keys[i]

        last_key_press = result[-1]

        if last_key_press.key == key.key:
            # for simplicity, the SHIFT modifier always win 
            result[-1] = KeyPress(key.key, last_key_press.count + key.count, key.has_shift or last_key_press.has_shift) 
        else:
            result.append(key)

    return result


def __filter(keys):
    """
    Remove isolated key occurences.

    Args:
        keys:     A list of KeyPress.
    
    Returns:
        A list of KeyPress, corresponding to the "keys" argument but with non-repeated keys removed.
    """

    return __dedup([
        key
        for key in keys
        if key.count > 1
    ])


def __split_keys(keys):
    """
    Split a list of keys according to actual key strokes.

    Args:
        keys:     A list of KeyPress.
        
    Returns:
        A list of keys. Every key is itself represented by a list of KeyPress, which are candidates for the actual key.
    """

    result = []
    buff = []

    for key in keys:
        if key.key == "NOKEY":
            result.append(buff)
            buff = []
        else:
            buff.append(key)

    result.append(buff)

    # returning only non-empty parts
    return [part for part in result if len(part) != 0]


def __get_sorted_histo(keys):
    """
    Compute the frequency of every key in a set of key presses.

    Args:
        keys:     A list of KeyPress.
      
    Returns:
        A list of (KeyPress, occurence count) pairs. The list is sorted by descending occurence count.
    """

    # the shift modifier is applied uniformly to every element
    has_shift = __has_mostly_shift(keys)
    items = sorted(__get_histo(keys).items(), key = lambda e : e[1])
    return [(KeyPress(item[0], 1, has_shift), item[1]) for item in items]


def filter_keys(keys):
    """
    Turn a raw list of tagged frames into a list of key presses.

    Args:
        keys: A list representing, for each frame, the detected key as a string.

    Returns:
        A list of key presses, in chronological order. Each key press is represented by an array
        of key strings, sorted from the most likely to the least likely.
        The "SHIFT" modifier is represented as a standalone key, just before the affected key press.

    Examples:
        >>> filter_keys(keys)
        [
            ['0', 'SUPPR', 'CTRL'], 
            ['SHIFT'],
            ['D'],
            ['SHIFT'],
            ['T'],
            ['SHIFT'],
            ['A'],
            ['SHIFT'],
            ['M'],
            ['SHIFT'],
            ['I'],
            ['H', 'U'],
            ['A', 'W'],
            ['C'],
            ['K'],
            ['A', 'W'],
            ['T'],
            ['O'],
            ['N'],
            ['2'],
            ['0'],
            ['2'],
            ['2', '3', '4'],
            ['ENTER']
        ]
    """  

    prob_keys = []

    # applying filters

    key_presses = [KeyPress(key) for key in keys]
    key_presses = __detect_modifiers(key_presses, __SHIFT_RADIUS)
    key_presses = [(key if key.key != "SHIFT" else KeyPress("NOKEY", key.count, True)) for key in key_presses]
    key_presses = __sliding_most(key_presses, __SLIDING_WINDOW)
    key_presses = __dedup(key_presses)
    key_presses = __filter(key_presses)
    processed = __split_keys(key_presses)

    # building the resulting list

    for part in  processed:
        sorted_histo = __get_sorted_histo(part)
        sorted_part = [e[0] for e in sorted_histo if e[1] > 0]

        # representing the SHIFT modifier as a standalone key
        if __has_mostly_shift(sorted_part):
            prob_keys.append(["SHIFT"])

        prob_keys.append([key.key for key in sorted_part])

    return prob_keys
