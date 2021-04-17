import numpy as np
from matplotlib.image import imsave
import matplotlib.pyplot as plt

Image = np.array


def show_image(img: Image, gamma_correction=False) -> None:
    """Display an image in matplotlib."""
    if gamma_correction:
        # this is an approximate gamma correction because imshow expects non-linear intensities
        img = img * img

    #   This is a hack to fix some dodgy rendering breaking the expected pixel interval of [0,1].
    img[img < 0.0] = 0.0
    img[img > 1.0] = 1.0

    plt.imshow(img)
    plt.axis('off')
    plt.show()


def save_image(img: Image, filename: str, gamma_correction=False) -> None:
    """Save image to the specified filename (extension will auto-select the output format)."""
    if gamma_correction:
        # this is an approximate gamma correction because imshow expects non-linear intensities
        img = img * img

    #   This is a hack to fix some dodgy rendering breaking the expected pixel interval of [0,1].
    img[img < 0.0] = 0.0
    img[img > 1.0] = 1.0

    imsave(filename, img)
