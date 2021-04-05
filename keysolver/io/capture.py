import numpy as np


def read_int(file):
    """
    Read an int from a file.

    Args:
        file:       The file in which read the int.

    Returns:
        The int read.

    Examples:
        >>> with open("example", "rb") as file:
        >>>     read_int(file)
        42
    """

    ba = bytearray(4)
    file.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.int32)

    return prm[0]


def read_double(file):
    """
    Read a double from a file.

    Args:
        file:       The file in which read the double.

    Returns:
        The double read.

    Examples:
        >>> with open("example", "rb") as file:
        >>>     read_double(file)
        42
    """

    ba = bytearray(8)
    file.readinto(ba)
    prm = np.frombuffer(ba, dtype=np.double)

    return prm[0]


def read_double_arr(file, n):
    """
    Read a double array from a file.

    Args:
        file:       The file in which read the double array.

    Returns:
        The numpy double array read.

    Examples:
        >>> with open("example", "rb") as file:
        >>>     read_double_tab(file, 3)
        numpy.array([42, 42, 42])
    """

    ba = bytearray(8 * n)
    nr = file.readinto(ba)

    if nr != len(ba):
        return []

    else:
        prm = np.frombuffer(ba, dtype=np.double)
        return prm


class Capture:
    """
    Capture class.

    Attributes:
        spikes_per_frame:   The number of spikes per frame.
        freq_sampling_khz:  The frequence of a sampling (in kHz).
        freq_frame_hz:      The frequence of a frame (in Hz).
        freq_spike_khz:     The frequence of a spike (in kHz).
        norm_fact:          The normalization factor.
        frames:             List of numpy arrays of the frames.
    """

    def __init__(self, file_path):
        with open(file_path, "rb") as file:
            self.__spikes_per_frame = read_int(file)
            self.__freq_sampling_khz = read_double(file)
            self.__freq_frame_hz = read_double(file)
            self.__freq_spike_khz = read_double(file)
            self.__norm_fact = read_double(file)

            self.__frames = []

            frame = read_double_arr(file, self.__spikes_per_frame)

            while len(frame) != 0:
                self.__frames.append(frame)
                frame = read_double_arr(file, self.__spikes_per_frame)

    def print_info(self):
        """
        Print the info a a Capture object.
        """
        print(f"Spikes per frames: {self.spikes_per_frame}")
        print(f"Sampling frequence: {self.__freq_sampling_khz} kHz")
        print(f"Frame frequence: {self.__freq_frame_hz} Hz")
        print(f"Spike frequence: {self.__freq_spike_khz} kHz")
        print(f"Normalization factor: {self.__norm_fact}")

    @property
    def spikes_per_frame(self):
        """
        Get the number of spikes per frame of a Capture object.
        """
        return self.__.spikes_per_frame

    @property
    def frames(self):
        """
        Get the list of the numpy arrays of the frames of a Capture object.
        """
        return self.__frames

    @property
    def nb_frames(self):
        """
        Get the number of frames of a Capture object.
        """
        return len(self.__frames)