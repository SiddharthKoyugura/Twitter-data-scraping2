###### Importing the modules
# Selenium section
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
# Database imports
from database import insert_twitter_data


# Set the path to the ChromeDriver executable
chrome_driver_path = "D:\Apps\chromedriver.exe"

# Configure Chrome options
chrome_options = Options()

# Code runs in the background without browser open
chrome_options.add_argument("--headless")

# Set up the ChromeDriver service
service = Service(chrome_driver_path)

# Function to scrape the data
def get_twitter_profile_data(url):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    # Open a webpage
    driver.get(url)
    sleep(2)
    # Scrape the required data
    try:
        name = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div/span/span[1]').text
        # Error handling with optional data
        try:
            website = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div/div[4]/div/a/span').text
        except:
            website = ''
        try:
            bio = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div/div[3]/div').text
            bio = bio.replace("\n", " ")
            following_count = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div/div[5]/div[1]/a/span[1]/span').text
            followers_count = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div/div[5]/div[2]/a/span[1]/span').text
            location = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div/div[4]/div/span[1]/span/span').text
        except:
            bio = ''
            location = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div[2]/div[3]/div/span[1]/span/span').text
            followers_count = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div[2]/div[4]/div[1]/a/span[1]/span').text
            following_count = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div[2]/div[4]/div[2]/a/span[1]/span').text
            try:
                website = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div/div/div/div[2]/div[3]/div/a/span').text
            except:
                website = ''
        
    except:
        # Close the driver
        driver.close()
        return
    
    # Close the driver
    driver.close()
    return [name, bio, following_count, followers_count, location, website]



# Required scrape data 
names_list, bio_list, following_list, followers_list, location_list, website_list = [], [], [], [], [], []
total_data_list = [ names_list, bio_list, following_list, followers_list, location_list, website_list ]

# Read the twitter_links.csv file
with open("csv/twitter_links.csv", "r") as file:
    contents = file.read()
    links = contents.split("\n")[:-1]

for link in links:
    # Removing error making content ("")
    link = link[1:-1]
    # Call scrape data function
    scraped_data = get_twitter_profile_data(link)
    if scraped_data:
        for i in range(6):
            total_data_list[i].append(scraped_data[i])
    

# Insert the values into database
n = len(names_list)
for i in range(n):
    insert_twitter_data(
        names_list[i],
        bio_list[i],
        following_list[i],
        followers_list[i],
        location_list[i],
        website_list[i]
    )