from threading import Thread
from scrape import ImageExtraction


def main():
    # Desired classes of images to download from the internet
    lists_of_objects = ["Desert", "Desert Biome", "sahara desert pictures africa", "the empty quarter desert",
                        "saudi arabia desert", "desert in night"]
    list_of_class = []
    list_of_threads = []
    # Creating Threads for each class 
    for obj in range(len(lists_of_objects)):
        list_of_class.append(ImageExtraction(r'/home/faisal/Downloads/chromedriver',
                                             lists_of_objects[obj]))
        list_of_threads.append(Thread(target=list_of_class[obj].get_images, args=(lists_of_objects[obj], 1000)))
    for threads in list_of_threads:
        threads.start()

    for threads in list_of_threads:
        threads.join()


if __name__ == '__main__':
    main()
