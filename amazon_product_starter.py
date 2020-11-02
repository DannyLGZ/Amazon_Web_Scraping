from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
import time
import pandas as pd

# Windows users need to specify the path to chrome driver you just downloaded.
# You need to unzip the zipfile first and move the .exe file to any folder you want.
# driver = webdriver.Chrome(r'path\to\the\chromedriver.exe')
driver = webdriver.Chrome(r'C:\Users\lingg\Desktop\chromedriver.exe')
# Go to the page that we want to scrape
csv_file1 = open('amazon_product.csv', 'w', encoding='utf-8', newline='')
csv_file2 = open('amazon_product_review.csv', 'w', encoding='utf-8', newline='')
writer1 = csv.writer(csv_file1)
writer2 = csv.writer(csv_file2)

urls = pd.read_csv(r'C:\Users\lingg\Desktop\NYC Data Science\Boot Camp\Python\Web_Scraping_project\amazon_product\amazon_product_url.csv')
for url in urls.url:
    driver.get(url)
    time.sleep(2)
#driver.get("https://www.amazon.com/AILUN-Protector-Compatible-Tempered-Anti-Scratch/dp/B07H2V5YLH/ref=zg_bs_wireless_1?_encoding=UTF8&psc=1&refRID=VCGXP5P2KSNA6BD7QG02")
# driver.get("https://www.amazon.com/Temdan-Designed-Protection-Anti-Yellowing-Protective/dp/B08K3ZB12Y/ref=zg_bs_wireless_13?_encoding=UTF8&psc=1&refRID=F1CF60DPT8GW7NC2ZMTF")
#driver.get("https://www.amazon.com/Protector-Compatible-iPhone-12-Anti-Scratch-Case-friendly/dp/B08JCFXGC6/ref=zg_bs_wireless_64?_encoding=UTF8&psc=1&refRID=VB49VNZV3FE15YEMJVDZ")

    try:
        product_info = {}

        product_title = driver.find_element_by_xpath('//span[@class="a-size-large product-title-word-break"]').text
        asin = driver.find_element_by_xpath('.//table[@id="productDetails_detailBullets_sections1"]/tbody/tr[3]/td').text
        #price = float('.'.join(re.findall('\d+',driver.find_element_by_xpath('//span[@class="a-size-medium a-color-price priceBlockBuyingPriceString"]').text)))
        try:
            price =  float('.'.join(re.findall('\d+',driver.find_element_by_xpath('//span[@class="a-size-medium a-color-price priceBlockBuyingPriceString"]').text)))
        except:
            price =  float('.'.join(re.findall('\d+',driver.find_elements_by_xpath('//span[@class="a-size-medium a-color-price priceBlockSalePriceString"]')[0].text)))

        about_item = driver.find_element_by_xpath('.//ul[@class="a-unordered-list a-vertical a-spacing-mini"]').text
        try:
            answer_qs = int(''.join(re.findall('\d+', driver.find_element_by_xpath('.//a[@class="a-link-normal askATFLink"]').text)))
        except:
            answer_qs = 'None'
        rating_number = int(''.join(re.findall('\d+', driver.find_element_by_xpath('.//span[@id="acrCustomerReviewText"]').text)))
        rating_star = '.'.join(re.findall('\d+', driver.find_element_by_xpath('.//span[@id="acrPopover"]').get_attribute('title'))[:-1])
        try:
            ranking = int(re.findall('\d+', driver.find_element_by_xpath('.//table[@id="productDetails_detailBullets_sections1"]/tbody/tr[6]/td/span/span').text)[0])
        except:
            ranking = 'None'
        try:
            date_available = driver.find_element_by_xpath('.//table[@id="productDetails_detailBullets_sections1"]/tbody/tr[7]/td').text
        except:
            date_available = 'None'
        # print('='*20)
        # print('Product = {}'.format(product_title))
        # print('Price = {}'.format(price))
        # print('answer_qs = {}'.format(answer_qs))
        # print('About_Item = {}'.format(about_item))
        # print('Rating_Number = {}'.format(rating_number))
        # print('Rating_Star = {}'.format(rating_star))
        # print('Ranking = {}'.format(ranking))
        # print('Date_Available = {}'.format(date_available))
        # print('='*20)

        product_info['product_title'] = product_title
        product_info['asin'] = asin
        product_info['price'] = price
        product_info['answer_question'] = answer_qs
        product_info['about'] = about_item
        product_info['rating_number'] = rating_number
        product_info['rating'] = rating_star
        product_info['date_available'] = date_available
        product_info['ranking'] = ranking

        writer1.writerow(product_info.values())



        # Click review button to go to the review section
        review_button = driver.find_element_by_xpath('//a[@class="a-link-emphasis a-text-bold"]')
        review_button.click()
        # driver.find_element_by_xpath('//span[@class="a-dropdown-prompt"]/text()=\'Most recent\'').click()
        time.sleep(1)

        driver.find_element_by_xpath('//span[@id="a-autoid-4-announce"]').click()
        driver.find_element_by_xpath('//li[@aria-labelledby="sort-order-dropdown_1"]/a').click()

        # Select mostrecentSort = new Select(driver.find_elements_by_xpath('//span[@class="a-dropdown-prompt"]')
        # mostrecentSort.selectByVisibleText("Most recent")

        time.sleep(1)

        # Page index used to keep track of where we are.
        index = 0
        # We want to start the first two pages.
        # If everything works, we will change it to while True
        while index < 1000:
            index = index + 1
            try:
                #print("Scraping Page number " + str(index+1))
                
                # Find all the reviews. The find_elements function will return a list of selenium select elements.
                # Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
                reviews = driver.find_elements_by_xpath('//div[@class="a-section review aok-relative"]')
                #print(len(reviews))
                #print('='*20)
                # Iterate through the list and find the details of each review.
                for review in reviews:
                    # Initialize an empty dictionary for each review
                    review_dict = {}
                    # Use try and except to skip the review elements that are empty. 
                    # Use relative xpath to locate the title.
                    # Once you locate the element, you can use 'element.text' to return its string.
                    # To get the attribute instead of the text of each element, use 'element.get_attribute()'
                        
                    # read_more_exists = False
                    # try:
                    #     read_more = review.find_element_by_xpath('.//span[@class="a-expander-prompt"]')
                    #     read_more.click()
                    #     read_more_exists = True
                    #     # Slows down the text expansion so the text can be scraped
                    #     time.sleep(.5)
                    # except:
                    #     pass
                    
                    
                    try:
                        title = review.find_element_by_xpath('.//a[@class="a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold"]').text
                        user_name = review.find_element_by_xpath('.//span[@class="a-profile-name"]').text
                        #rating = float('.'.join(re.findall('\d+', review.find_element_by_xpath('.//a[@class="a-link-normal"]/i/span').get_attribute('textContent'))[:-1]))
                        #rating = review.find_element_by_xpath('.//span[@class="a-icon-alt"]').text[3:]
                        rating = float('.'.join(re.findall('\d+', review.find_element_by_xpath('.//a[@class="a-link-normal"]').get_attribute('title'))[:-1]))
                        date = review.find_element_by_xpath('.//span[@class="a-size-base a-color-secondary review-date"]').text
                        txt = review.find_element_by_xpath('.//span[@class="a-size-base review-text review-text-content"]').text
                    except:
                        continue

                    # print('='*20)
                    # print('Title = {}'.format(title))
                    # print('User_name = {}'.format(user_name))
                    # print('Rating = {}'.format(rating))
                    # print('Date = {}'.format(date))
                    # print('Text = {}'.format(txt))
                    # print('='*20)


                    # OPTIONAL: How can we deal with the "read more" button?
                    
                    # Use relative xpath to locate text, username, date_published, rating.
                    # Your code here

                    # Uncomment the following lines once you verified the xpath of different fields
                    review_dict['product_title'] = product_title
                    review_dict['asin'] = asin
                    review_dict['title'] = title
                    review_dict['text'] = txt
                    review_dict['username'] = user_name
                    review_dict['date'] = date
                    review_dict['rating'] = rating

                    writer2.writerow(review_dict.values())

                # We need to scroll to the bottom of the page because the button is not in the current view yet.
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Locate the next button element on the page and then call `button.click()` to click it.
                #button = driver.find_element_by_xpath('//li[@class="a-last"]')
                wait_button = WebDriverWait(driver, 10)
                next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//li[@class="a-last"]')))
                next_button.click()
                time.sleep(1)

            except Exception as e:
                break
                driver.close()
    except:
        continue
        driver.close()
        
        
csv_file1.close()
csv_file2.close()
