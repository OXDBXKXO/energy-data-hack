import matplotlib.pyplot as plt


def frame(frame, position, title="Sans titre"):
    plt.subplot(position)
    plt.plot(range(1, len(frame) + 1), frame, 'ko')
    plt.xlabel('numéro de pic')
    plt.ylabel('valeur du pic')
    plt.title(title)
    plt.ylim(0, 1.5)
    plt.grid(b=True, which='both')
