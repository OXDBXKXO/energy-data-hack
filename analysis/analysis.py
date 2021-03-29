"""
Script python pour ouvrir les fichiers de traces de clavier

"""

import matplotlib.pyplot as plt
import numpy as np


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

    def print(self):
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


def plot_frame(frame, title="Sans titre"):
    plt.plot(range(1, len(frame) + 1), frame, 'ko')
    plt.xlabel('numéro de pic')
    plt.ylabel('valeur du pic')
    plt.title(title)
    plt.ylim(0, 1.5)
    plt.grid(b=True, which='both')


def main():
    pics_nokey = Capture.load_from_file("../Hackaton/data/pics_NOKEY.bin")
    pics_pad0 = Capture.load_from_file("../Hackaton/data/pics_0.bin")

    ######### Pics ############
    plt.figure(1)
    # NO KEY
    plt.subplot(211)
    plot_frame(pics_nokey.frames[0], "Sans touches")
    # PAD-0
    plt.subplot(212)
    plot_frame(pics_pad0.frames[0], "Touche 0")
    #
    plt.show()


if __name__ == "__main__":
    main()
