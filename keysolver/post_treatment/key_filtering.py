def __get_histo(array):
    histo = dict()

    for element in array:
        if element in histo:
            histo[element] += 1
        else:
            histo[element] = 1

    return histo


def __get_most_frequent(array):
    histo = __get_histo(array)

    most_frequent = ""
    max_count = 0

    for element, count in histo.items():
        if count > max_count:
            most_frequent = element
            max_count = count

    return most_frequent


def __sliding_most(keys, window_size):
    result = []
    window = keys[0:window_size]

    for key in keys[window_size - 1:]:
        window = window[1:] + [key]
        result.append(__get_most_frequent(window))

    return result


def __dedup(keys):
    len_keys = len(keys)

    if len_keys == 0:
        return []

    entries = [(keys[0], 1)]

    for i in range(1, len_keys):
        key = keys[i]

        last_key, last_count = entries[-1]

        if last_key != key:
            entries.append((key, 1))
        else:
            entries[-1] = (key, last_count + 1)

    return entries


def __filter(entries):
    return __dedup([
        key
        for key, count in entries
        if count > 1
    ])


def __split_keys(entries):
    result = []
    buff = []

    for key, _ in entries:
        if key == "NOKEY":
            result.append(buff)
            buff = []
        else:
            buff.append(key)

    result.append(buff)

    return [part for part in result if len(part) != 0]


def __get_sorted_histo(array):
    return sorted(__get_histo(array).items(), key = lambda e : e[1])

def filter_keys(keys):
    prob_keys = []

    for part in (__split_keys(__filter(__dedup(__sliding_most(keys, 15))))):
        sorted_histo = __get_sorted_histo(part)
        prob_keys.append([e[0] for e in sorted_histo if e[1] > 0])

    return prob_keys