from selenium.webdriver import Chrome
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
    StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from time import sleep
from helperfunction import create_random_name, does_folder_exist
from urllib.error import HTTPError, URLError
import urllib.request


# Exception raised when the object is not an image
class NotImageError(Exception):
    def __init__(self):
        super().__init__("It is a decoy")


class ImageExtraction(Chrome):
    iteration: int = 1
    num_of_dev: int = 0
    folder_name: str

    def __init__(self, path='', folder_name='imgs'):
        self.folder_name = "".join(folder_name.split())
        does_folder_exist(self.folder_name)
        super().__init__(path)

    # Method responsible for searching the images wanted to download.
    def __search_images(self, images_download):
        self.get('https://www.google.com/')
        element = self.find_element_by_xpath('/html/body/div[1]/div[1]/div/div/div/div[1]/div/div[2]/a')
        element.click()
        search_bar = self.find_element_by_name('q')
        search_bar.send_keys(images_download)
        sleep(1)
        search_bar.send_keys(Keys.ENTER)
        sleep(0.5)
        self.scroll_down()

    # Method responsible for determining weather the html object is an image or not
    def is_valid(self, current_img):
        html_img_obj = self.find_element_by_xpath(current_img)
        sleep(0.5)
        if 'عمليات' in html_img_obj.text or 'الشائعة' in html_img_obj.text or 'شائعة' in html_img_obj.text:
            return "decoy"

    # Method responsible for loading all the images in html page.
    def scroll_down(self):
        last_height = self.execute_script("return document.body.scrollHeight")
        while True:
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(1.5)
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # Method responsible for determining the location of the next object in html
    def __img_loc(self):
        if self.iteration < 50 and self.num_of_dev == 0:
            return '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]' + \
                f'/div[1]/span/div[1]/div[1]/div[{str(self.iteration)}]'
        elif self.num_of_dev == 0:
            self.iteration, self.num_of_dev = 1, 1

        elif self.iteration > 54:
            self.iteration = 1
            self.num_of_dev += 1

        return '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]' + \
            f'/div[1]/span/div[1]/div[1]/div[{str(50 + self.num_of_dev)}]/div[{str(self.iteration)}]'

    # Method responsible for downloading the image
    def downloading_file(self):
        image = self.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]" +
                                           "/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]")
        src = image.get_attribute('src')
        print(src)
        with open(f'{self.folder_name}\{create_random_name()}.png', 'wb') as f:
            print(src)
            x = urllib.request.urlopen(src).read()
            print(len(x))
            f.write(x)

    # Method responsible of getting the url of the current image to be downloaded.
    def __get_single_image(self, current_img):
        try:
            sleep(1)
            html_img_obj = self.find_element_by_xpath(current_img)
            if 'عمليات' in html_img_obj.text or 'الشائعة' in html_img_obj.text or 'شائعة' in html_img_obj.text:
                raise NotImageError
            sleep(1)
            html_img_obj.click()
            sleep(2)
            print(current_img)
            self.downloading_file()
        except ElementClickInterceptedException:
            self.refresh()
            sleep(1)
            print("Element not click exception")
            return False

        except NoSuchElementException:
            sleep(1)
            print("No such element exception")
            return False

        except StaleElementReferenceException:
            print("Stale Element Refrence Exception")
            self.refresh()
            sleep(1)

        return True

    # Method responsible for going back to the main page to traverse to the next object
    def back_page(self):
        try:
            self.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]" +
                                       "/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[2]" +
                                       "/div/div/div[2]/div[3]/a/div").click()
        except NoSuchElementException:
            pass

    # Method responsible for downloading specific number of images.
    def get_images(self, images_download, num_of_images):
        self.__search_images(images_download)

        for image in range(num_of_images):
            current_img = self.__img_loc()
            self.iteration += 1
            tries, patience = 0, 5
            try:
                while not self.__get_single_image(current_img) and tries < patience:
                    tries += 1
                    print(tries)

                else:
                    self.back_page()

                if tries == patience:
                    self.back_page()
                    self.scroll_down()
                    sleep(2)
                    print("I am scrolling down")

            except NotImageError as e:
                print(e)

            except HTTPError as e:
                print(e)

            except URLError as e:
                print(e)
