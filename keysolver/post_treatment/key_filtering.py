
__SLIDING_WINDOW = 80
__SHIFT_RADIUS = 50


class KeyPress:
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
	score = [0] * len(keys)
	for i in range(len(keys)):

		mod = 0
		if keys[i].key == "NOKEY":
			mod = -1
		elif keys[i].key == "SHIFT":
			mod = 1
		else:
			continue

		window_begin = max(0, i - radius)
		window_end = min(len(keys), i + radius)
		for j in range(window_begin, i):
			score[j] += mod
		for j in range(i, window_end):
			score[j] += mod

	for i in range(len(keys)):
		if score[i] > 0:
			keys[i] = KeyPress(keys[i].key, keys[i].count, True)

	return keys


def __has_mostly_shift(keys):
    return sum([(1 if key.has_shift else -1) for key in keys]) > 0


def __get_histo(keys):
    histo = dict()

    for key in keys:
        if key.key in histo:
            histo[key.key] += key.count
        else:
            histo[key.key] = key.count

    return histo


def __get_most_frequent(keys):
    histo = __get_histo(keys)

    most_frequent = ""
    max_count = 0

    for element, count in histo.items():
        if count > max_count:
            most_frequent = element
            max_count = count

    return KeyPress(most_frequent, 1, __has_mostly_shift(keys))


def __sliding_most(keys, window_size):
    result = []
    window = keys[0:window_size]

    for key in keys[window_size - 1:]:
        window = window[1:] + [key]
        most_frequent = __get_most_frequent(window)
        result.append(most_frequent)

    return result


def __dedup(keys):
    len_keys = len(keys)

    if len_keys == 0:
        return []

    result = [keys[0]]

    for i in range(1, len_keys):
        key = keys[i]

        last_key_press = result[-1]

        if last_key_press.key == key.key:
            result[-1] = KeyPress(key.key, last_key_press.count + key.count, key.has_shift or last_key_press.has_shift) 
        else:
            result.append(key)

    return result


def __filter(keys):
    return __dedup([
        key
        for key in keys
        if key.count > 1
    ])


def __split_keys(keys):
    result = []
    buff = []

    for key in keys:
        if key.key == "NOKEY":
            result.append(buff)
            buff = []
        else:
            buff.append(key)

    result.append(buff)

    return [part for part in result if len(part) != 0]


def __get_sorted_histo(keys):
    has_shift = __has_mostly_shift(keys)
    items = sorted(__get_histo(keys).items(), key = lambda e : e[1])
    return [(KeyPress(item[0], 1, has_shift), item[1]) for item in items]


def filter_keys(keys):
    prob_keys = []

    key_presses = [KeyPress(key) for key in keys]
    key_presses = __detect_modifiers(key_presses, __SHIFT_RADIUS)
    key_presses = [(key if key.key != "SHIFT" else KeyPress("NOKEY", key.count, True)) for key in key_presses]
    key_presses = __sliding_most(key_presses, __SLIDING_WINDOW)
    key_presses = __dedup(key_presses)
    processed = __split_keys(__filter(key_presses))

    for part in  processed:
        sorted_histo = __get_sorted_histo(part)
        sorted_part = [e[0] for e in sorted_histo if e[1] > 0]
        if __has_mostly_shift(sorted_part):
        	prob_keys.append(["SHIFT"])
        prob_keys.append([key.key for key in sorted_part])

    return prob_keys
