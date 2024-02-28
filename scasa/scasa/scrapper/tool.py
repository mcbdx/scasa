## QUICK Test to selenium webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as keys
from time import sleep
from collections import defaultdict
import pandas as pd
import os


# options = Options()
# firefox_binary =  options.binary_location = '/Applications/Firefox D      eveloper Edition.app/Contents/MacOS/firefox-bin'


# # Set up the Firefox WebDriver with the custom binary
# driver = webdriver.Firefox(options=options)

chrome_options = Options()
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument("--headless")
user_agent = '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Safari/537.36"'
chrome_options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(options=chrome_options)

def get_info(apartment_url):
    # FETCH WEBPAGE
    driver.get(apartment_url)

    # WAIT FOR PAGE TO LOAD
    wait = WebDriverWait(driver, 5)

    # INFO DICTS

    dog_fees = defaultdict(list)
    parking = defaultdict(list)
    application_fee = defaultdict(list)

    # FETCH INFO
    name = driver.find_element(By.ID, "propertyName").text
    phone_number = driver.find_element(By.CLASS_NAME, "phoneNumber")
    rent_info = driver.find_element(By.CLASS_NAME, "priceBedRangeInfoContainer")
    rent_info_label = [label.text for label in rent_info.find_elements(By.CLASS_NAME, "rentInfoLabel")]
    rent_info_detail = [detail.text for detail in rent_info.find_elements(By.CLASS_NAME, "rentInfoDetail")]
    address = driver.find_element(By.CLASS_NAME, "propertyAddressContainer").text
    city = driver.find_element(By.CLASS_NAME, "neighborhood").text
    try:
        link_element = driver.find_element(By.CSS_SELECTOR, 'a[title="View Property Website"]')
        property_url = link_element.get_attribute('href')
    except:
        property_url = 'No url'
    rent_details = dict(zip(rent_info_label, rent_info_detail))
    fee_policies = driver.find_elements(By.CLASS_NAME, "feespolicies")
    fees = [fee.text for fee in fee_policies]

    # FETCH FEES
    for i in fees:
        lines = i.strip().split('\n')

        for j in range(len(lines)):
            key = lines[j]
            try:
                value = lines[j+ 1]
            except IndexError:
                value = 'No info'
            
            if key == 'Dogs Allowed':
                dog_fees[key] = value
            elif key in ['Pet deposit','Monthly pet rent']:
                dog_fees[key] = value
            elif key == 'Parking':
                parking[key] = value
            elif key == 'Application Fee':
                application_fee[key] = value
    
    # GOOGLE RATINGS
    driver.get(f"https://google.com/search?q={name}+apartments")

    try:
        google_rating = driver.find_element(By.CLASS_NAME, "Aq14fc").text
    except:
        google_rating = "tbd"
    
    # print(name)
    # print(address)
    # print(city)
    # print(rent_details)
    # print(f'Dog Fees: {dog_fees}')
    # print(parking)
    # print(application_fee)
    # print(property_url)
    # print(google_rating)

    data = {
        'Name': name,
        'Address': address,
        'City': city,
        **rent_details,
        **dog_fees,
        **parking,
        **application_fee,
        'Property Url': property_url,
        'Google Rating': google_rating
    }

    cols = [
    "Name",
    "Address",
    "City",
    "Monthly Rent",
    "Bedrooms",
    "Bathrooms",
    "Square Feet",
    "Dogs Allowed",
    "Pet deposit",
    "Monthly pet rent",
    "Parking",
    "Property Url",
    "Google Rating"]

    df = pd.DataFrame(data, index=[0], columns=cols)

    path = '/Users/mcbdx/OneDrive/Office Documents/San Diego/apartments.xlsx'  # Specify the Excel file path

    # Check if the Excel file already exists
    if not os.path.exists(path):
        # If it doesn't exist, create a new Excel file
        df.to_excel(path, index=False, header=True)
        print("created excel file for you")
    else:
        # If it exists, open the existing Excel file and append the DataFrame to it
        existing_df = pd.read_excel(path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_excel(path, index=False, header=True, engine='openpyxl')
        print(f"succesfully appended data to existing excel file for {name}")
    driver.quit()

if __name__ == '__main__':
    # usr_input = input('Enter URL: ')
    # get_info(usr_input)
    urls = [
        #"https://www.apartments.com/valentina-san-diego-ca/hh8dgy3/",
        #"https://www.apartments.com/the-seaton-apartments-san-diego-ca/lx70jhg/",
        #"https://www.apartments.com/vora-mission-valley-san-diego-ca/sbk32d7/",
        #"https://www.apartments.com/one-paseo-living-san-diego-ca/djmcwtk/",
        #"https://www.apartments.com/diega-san-diego-ca/f6fslxs/",
        #"https://www.apartments.com/ruby-at-the-society-san-diego-ca/b9zgw08/",
        #"https://www.apartments.com/margo-at-the-society-san-diego-ca/8522y62/",
        #"https://www.apartments.com/alexan-gallerie-san-diego-ca/tjtsle9/",
        #"https://www.apartments.com/winslow-san-diego-ca/vxhvh8f/",
        #"https://www.apartments.com/bradbury-at-the-society-san-diego-ca/hzh0jd1/"
    ]
    
    for url in urls:
        get_info(url)
        
    
        
