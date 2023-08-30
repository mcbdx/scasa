## QUICK Test to selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from time import sleep

# options = Options()
# firefox_binary =  options.binary_location = '/Applications/Firefox D      eveloper Edition.app/Contents/MacOS/firefox-bin'


# # Set up the Firefox WebDriver with the custom binary
# driver = webdriver.Firefox(options=options)

chrome_options = Options()
chrome_options.add_argument("window-size=1920,1080")
#chrome_options.add_argument("--headless")
#user_agent = '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"'
#chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_options)


# the get method 
driver.get('https://www.apartments.com/casas-by-the-sea-san-diego-ca/wpqr1wh/')


name = driver.find_element(By.ID, "propertyName")
rent_info = driver.find_element(By.CLASS_NAME, "priceBedRangeInfoContainer")
rent_info_label = [label.text for label in rent_info.find_elements(By.CLASS_NAME, "rentInfoLabel")]
rent_info_detail = [detail.text for detail in rent_info.find_elements(By.CLASS_NAME, "rentInfoDetail")]
rent_details = dict(zip(rent_info_label, rent_info_detail))
fee_policies = driver.find_elements(By.CLASS_NAME, "feespolicies")
fees = [fee.text for fee in fee_policies[:2]]

### NEED TO ADD if statements for fees to get specific elements based on page 
## examples if 'Pet' in fees:
## then get the pet fees else skip 
## if 'Parking' in fees:
## then get the parking fees else skip
## If application fee in fees:
## then get the application fee else skip

## fruits = driver.find_element(By.ID, "fruits")
##fruit = fruits.find_element(By.CLASS_NAME,"tomatoes") - do this to get headers/ details
  
address = driver.find_element(By.CLASS_NAME, "propertyAddressContainer")

apartment_name = name.text
print(apartment_name)
print(address.text)
print(rent_details)
print(fees)


# # Find the link element based on the href attribute
link_element = driver.find_element(By.CSS_SELECTOR, 'a[title="View Property Website"]')

# Get the URL from the href attribute
property_url = link_element.get_attribute('href')

driver.get(property_url)


driver.get(f"https://google.com/search?q={apartment_name}+apartments")


try:
    google_rating = driver.find_element(By.CLASS_NAME, "Aq14fc").text
    print(google_rating)
except:
    google_rating = "tbd"
    


# search_element = driver.find_element(By.ID, "searchBarLookup")

# # search_element.send_keys('San Francisco, CA')
# # search_element.send_keys(keys.RETURN)
driver.quit()