import numpy as np


def read_int(file):
    ba = bytearray(4)
    file.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)

    return prm[0]


def read_double(file):
    ba = bytearray(8)
    file.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)

    return prm[0]


def read_double_tab(file, n):
    ba = bytearray(8 * n)
    nr = file.readinto(ba)

    if nr != len(ba):
        return []

    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm


class Capture:

    def __init__(self, file_path):
        with open(file_path, "rb") as file:
            self.__spikes_per_frame = read_int(file)
            self.__freq_sampling_khz = read_double(file)
            self.__freq_frame_hz = read_double(file)
            self.__freq_spike_khz = read_double(file)
            self.__norm_fact = read_double(file)

            self.__frames = []

            frame = read_double_tab(file, self.__spikes_per_frame)

            while len(frame) != 0:
                self.__frames.append(frame)
                frame = read_double_tab(file, self.__spikes_per_frame)

    def print_info(self):
        print(f"Spikes per frames: {self.spikes_per_frame}")
        print(f"Sampling frequence: {self.__freq_sampling_khz} kHz")
        print(f"Frame frequence: {self.__freq_frame_hz} Hz")
        print(f"Spike frequence: {self.__freq_spike_khz} kHz")
        print(f"Normalization factor: {self.__norm_fact}")

    @property
    def spikes_per_frame(self):
        return self.__.spikes_per_frame

    @property
    def frames(self):
        return self.__frames

    @property
    def nb_frames(self):
        return len(self.__frames)