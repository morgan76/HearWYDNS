import numpy as np
from skimage.filters.rank import entropy
from skimage import data
from skimage.util import img_as_ubyte
from skimage.morphology import disk
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage import io
from matplotlib.pyplot import plot, ion, show


def moving_mask(image, mask_size):
    """
    Sub-regions extraction function

    :param image: input image
    :param mask_size: the size of the mask
    :return: a list of sub-regions and the total number of sub-regions
    """
    num_rows, num_columns = image.shape
    list_regions = []
    num_steps_rows = num_rows//mask_size
    num_steps_columns = num_columns//mask_size
    for i in range(num_steps_rows-1):
        for j in range(num_steps_columns-1):
            list_regions.append(image[i*mask_size:(i+1)*mask_size,j*mask_size:(j+1)*mask_size])
    return list_regions, len(list_regions)
    

def extract_from_mask(list_regions):
    """
    Feature extraction function

    :param list_regions: List of sub-regions
    :return: a list of average entropy value for each sub-region
    """
    information = []
    for i in list_regions:
        information.append(np.mean(entropy(i, disk(10))))
    information = np.array(information)
    for i in range(len(information)):
        information[i] = (information[i]-np.min(information))/(np.max(information))
    return information
    
def pre_process(image_path):
    """
    Image loading function

    :param image_path: Path of the image to load
    :return: Grayscale version of the image
    """
    image = io.imread(image_path)
    image = rgb2gray(image)
    return image

def test_print(image):
    """
    Image printing function

    :param image: Image to load
    :return: Displays the original and the entropy version of the image
    """
    fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(12, 4),
                                   sharex=True, sharey=True)

    img0 = ax0.imshow(image, cmap=plt.cm.gray)
    ax0.set_title("Image")
    ax0.axis("off")
    fig.colorbar(img0, ax=ax0)

    img1 = ax1.imshow(entropy(image, disk(10)), cmap='gray')
    ax1.set_title("Entropy")
    ax1.axis("off")
    fig.colorbar(img1, ax=ax1)

    fig.tight_layout()
    plot(block=False)
    show()


