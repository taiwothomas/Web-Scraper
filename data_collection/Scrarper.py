from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from random import randint

driver = webdriver.Chrome()
URL = 'https://www.goodreads.com/'

class Scraper:

    '''
    A web scraper class that collects data from Goodreads website
    It starts with an empty dictionary of lists and populates that with data from the web scraper

    Parameters:
    ------------
    URL: str
        The starting URL for scraping data
    URL_list: List
        A list of URLs for each data point (book)
    
    Attributes:
    ------------
    title: str
        The book title from each data point
    author: str
        The author of the book from each data point
    rating: str
        The average rating plus the number of ratings for each book
    book_summary: str
        The summary of the book for each data point
    book_dict: dict
        A dictionary of the data of one data point
    book_list: list
        A list of dictionaries of all the points
    
    Methods:
    ---------
    get_url()
    Gets the URLs for all 199 data points
    
    get_book_data(driver)
    Gets the title, author and rating for each data point

    get_summary(driver)
    Gets the book summary for each data point

    '''

    def __init__(self):
        self.URL_list = []
        # self.genre = (input("Choose one genre from biography, history, fiction, horror, romance, science: - ")).lower
        self.book_dict = {'Title': "", 'Author': "", 'Rating': "", 'Summary': ""}
        self.book_list = []
        
    def get_book(self):
                 
        container = driver.find_element(By.XPATH, "//div[@class='bigBoxContent containerWithHeaderContent']")
        book_list = container.find_elements(By.TAG_NAME, "a")
        for book in book_list:
            b_link = book.get_attribute('href')
            self.URL_list.append(b_link)
        self.URL_list.pop(-1)
    
    def get_genre(self, genre):
        driver.get(URL)
        genre_xpath = f'//*[@href="/genres/{genre}"]'
        genre_container = driver.find_element(By.XPATH, genre_xpath)
        print(f"New {genre_container.text} books.")
        genre_container.click()

        try:
            button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div/div[1]/button")))
            button.click()
        except:
            pass
    
    def fill_dict(self):
        
        pass

    def get_book_data(self):

        for link in self.URL_list:
            driver.get(link)
            book_title = driver.find_element(By.XPATH, "//h1[@id='bookTitle']").text
            full_description = driver.find_element(By.XPATH, "//div[@id='descriptionContainer']")
            full_description.find_element(By.TAG_NAME, 'a').click()
            # book_description = driver.find_element(By.XPATH, "//div[@id='descriptionContainer']").text
            book_description = full_description.find_element(By.XPATH, "//span[@style='display:none']").text
            rating = driver.find_element(By.XPATH, "//span[@itemprop='ratingValue']").text
            authors = driver.find_element(By.XPATH, "//div[@id='bookAuthors']").text
            self.book_dict['Title'] = book_title
            self.book_dict['Author'] = authors
            self.book_dict['Rating'] = rating
            self.book_dict['Summary'] = book_description

            self.book_list.append(self.book_dict)


    
if __name__ == '__main__':
    Horror = Scraper()
    Horror.get_genre("horror")
    Horror.get_book()
    print(Horror.URL_list)
    Horror.get_book_data()
    print(Horror.book_list[randint(0,10)])
