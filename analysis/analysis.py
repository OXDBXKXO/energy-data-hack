import numpy as np
import matplotlib.pyplot as plt

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

class Fingerprint:
    def __init__(self, data):
        self.nokey = Capture.load_from_file("../../given/data/pics_NOKEY.bin").frames
        self.file = Capture.load_from_file("../../given/data/{}".format(data)).frames

        self.diffs = []
        for i in range(len(self.file)):
            if i >= len(self.nokey):
                break

            diff = []
            exit_for = False
            for j in range(len(self.nokey[i])):
                if j >= len(self.file[i]):
                    exit_for = True
                    break

                diff.append(self.file[i][j] - self.nokey[i][j])

            if exit_for:
                break

            self.diffs.append(diff)

    def mean(self):
        means = []
        for diff in self.diffs:
            means.append(np.mean(diff))

        return np.mean(means)


def main():
    pics_pad0 = Fingerprint("pics_1.bin")
    print(pics_pad0.mean())
    # pics_nokey = Capture.load_from_file("../../given/data/pics_NOKEY.bin")
    # pics_pad0 = Capture.load_from_file("../../given/data/pics_0.bin")

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
