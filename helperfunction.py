import os
import random
import string


# Creating the necessary directories for images to be downloaded in.
def does_folder_exist(filename):
    if not os.path.exists(filename):
        os.mkdir(filename)


# Creating random names for the images
def create_random_name():
    x = "".join([string.ascii_letters[random.randint(0, len(string.ascii_letters) - 1)] + str(x) for x in range(10)])
    random.shuffle(list(x))
    return x
