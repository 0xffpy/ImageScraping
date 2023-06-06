from threading import Thread
from scrape import ImageExtraction

# Class For image scraping in the internet

# image_extract_object = ImageExtraction(r'C:\Users\Faisal Eid alharbi\Downloads\chromedriver.exe', "Faisal")
# image_extract_object.get_images('Forest', 200)


def main():
    # lists_of_objects = ["aquatic biome", "grassland biome", "Tropical Rainforest", "Temperate Forest",
    #                     "Desert", "tundra", "Sahara", "Antarctica", "savanna", "taiga"]
    #
    lists_of_objects = ["Desert", "Desert Biome", "sahara desert pictures africa", "the empty quarter desert",
                        "saudi arabia desert", "desert in night"]
    list_of_class = []
    list_of_threads = []
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