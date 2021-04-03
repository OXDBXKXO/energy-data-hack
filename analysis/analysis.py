import numpy as np
import matplotlib.pyplot as plt

import os, math

import plot


def read_int(f):
    ba = bytearray(4)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)
    return prm[0]


def read_double(f):
    ba = bytearray(8)
    f.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)
    return prm[0]


def read_double_tab(f, n):
    ba = bytearray(8 * n)
    nr = f.readinto(ba)
    if nr != len(ba):
        return []
    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm


def try_read_double_tab(file, dest):
    tmp = read_double_tab(file, len(dest))
    if len(tmp) == 0:
        return False
    for i in range(len(dest)):
        dest[i] = tmp[i]
    return True


class CaptureInfo:
    def __init__(self, file):
        self.__spike_count_per_frame = read_int(file)
        self.__freq_sampling_khz = read_double(file)
        self.__freq_trame_hz = read_double(file)
        self.__freq_pic_khz = read_double(file)
        self.__norm_fact = read_double(file)

    def printInfo(self):
        print(f"Nb pics par trame : {self.__spike_count_per_frame}")
        print(f"Frequence d'echantillonnage : {self.__freq_sampling_khz} kHz")
        print(f"Frequence trame: {self.__freq_trame_hz} Hz")
        print(f"Frequence pic: {self.__freq_pic_khz} kHz")
        print(f"Facteur de normalisation: {self.__norm_fact}")

    @property
    def spike_count_per_frame(self):
        return self.__spike_count_per_frame


class Capture:
    def __init__(self, file):
        self.__meta = CaptureInfo(file)
        self.__frames = []
        frame_spikes = [None] * self.spike_count_per_frame
        while try_read_double_tab(file, frame_spikes):
            self.__frames.append([x for x in frame_spikes])

    @staticmethod
    def load_from_file(filename: str):
        with open(filename, "rb") as file:
            return Capture(file)

    @property
    def spike_count_per_frame(self):
        return self.__meta.spike_count_per_frame

    @property
    def frames(self):
        return self.__frames


class Mean:
    def __init__(self, data):
        self.frames = Capture.load_from_file(os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "given" + os.path.sep + "data" + os.path.sep + "{}".format(data)).frames

    def get(self):
        means = []
        for i in range(17):
            mean = []
            for frame in self.frames:
                mean.append(frame[i])
            means.append(np.mean(mean))

        return means


def differenceFactor(frames_mean_1, frames_mean_2):
    factor = 0
    for i in range(17):
        factor += math.pow(abs(frames_mean_1[i] - frames_mean_2[i]), 2)
    return factor

# ['CTRL', '0', 'SUPPR']
# ['I', 'SHIFT']
# ['U', 'B', 'H']
# ['W', 'A', 'Q']
# ['C']
# ['K']
# ['W', 'Q', 'A']
# ['G', 'T']
# ['O']
# ['N']
# ['1', '3', '2']
# ['SUPPR', '0']
# ['4', '3', '1', '2']
# ['4', '1', '2', '3']
# ['1', '3', '4', 'ENTER']

def buildWordsTree(likelyLetters):

    if not len(likelyLetters):
        print("buildWordsTree: Invalid input")
        return

    special = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]

    # Cleaning list
    for letters in likelyLetters:
        for index, letter in enumerate(letters):
            if letter in special:
                letters.pop(index)

    previous_stack = []
    next_stack = []

    for stackFill in likelyLetters[0]:
        previous_stack.append(stackFill)

    for i in range(1, len(likelyLetters)):
        likelyLetter = likelyLetters[i]

        while len(previous_stack) != 0:
            word = previous_stack.pop()

            for letter in likelyLetter:
                next_stack.append(word + letter)
        
        previous_stack = next_stack
        next_stack = []
    
    return previous_stack




def main():
    # pics_pad0 = Fingerprint("pics_1.bin")
    # pics_pad0.mean()
    # print(Mean("pics_0.bin").get())

    # return

    test = [['CTRL', '0', 'SUPPR'], ['I', 'SHIFT'], ['U', 'B', 'H'], ['W', 'A', 'Q'], ['C'], ['K'], ['W', 'Q', 'A'], ['G', 'T'], ['O'], ['N'], ['1', '3', '2'], ['SUPPR', '0'], ['4', '3', '1', '2'], ['4', '1', '2', '3'], ['1', '3', '4', 'ENTER']]

    words = buildWordsTree(test)

    f = open("words.txt", "w")
    for word in words:
        f.write(word + '\n')
    f.close()

    return

    keys_means = {}
    
    alphanum = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    special = ["CTRL", "ENTER", "NOKEY", "SHIFT", "SPACE", "SUPPR"]
    
    for c in alphanum:
        keys_means[c] = Mean("pics_" + c + ".bin").get()
    for c in special:
        keys_means[c] = Mean("pics_" + c + ".bin").get()

    login_frames = Capture.load_from_file(os.path.dirname(__file__) + os.path.sep + ".." + os.path.sep + "given" + os.path.sep + "data" + os.path.sep + "{}".format("pics_LOGINMDP.bin")).frames

    password = []
    for login_frame in login_frames:
        lowest_factor = math.inf
        letter = ""
        for key in keys_means:
            factor = differenceFactor(login_frame, keys_means[key])
            if factor < lowest_factor:
                lowest_factor = factor
                letter = key

        likely_match = {}
        likely_match[letter] = lowest_factor
        password.append(likely_match)
    
    last_letter = ""
    for letter in password:
        for l in letter:
            if l == last_letter:
                continue
            print(l)
            last_letter = l
    # plt.figure(1)
    # # NO KEY
    # for i in range(10):
    #     plot.frame(pics_nokey.frames[i], 211, "Sans touches")

    # # PAD-0
    # plot.frame(pics_pad0.frames[0], 212, "Touche 0")
    # #
    # plt.show()


if __name__ == "__main__":
    main()
