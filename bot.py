import time
import colorama
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from colorama import Fore, Back, Style, init
colorama.init()

#Must use path to your own geckodriver file
geckodriver = r'C:\Geckodriver\geckodriver.exe'
 
#This option allows you to run this script in headless mode which allows it to run with no browser being opened
#To enable uncomment line 19
options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
 
browser = webdriver.Firefox(executable_path=geckodriver, options=options)
 
login_page = r"https://www.bestbuy.com/signin"
                
test_product_in_stock = r"https://www.bestbuy.com/site/google-fi-sim-card-kit/6325631.p?skuId=6325631"
out_of_stock_product = r"https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-ti-ftw3-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444444.p?skuId=6444444"

store_page = r"https://www.bestbuy.com/site/store-locator/"

pay_page = r"https://www.bestbuy.com/checkout/r/payment"

saved_parts = r"https://www.bestbuy.com/site/customer/lists/manage/saveditems"

#timer to being counting how long the program takes to run
begin = time.time()

#first page that loads
browser.get(login_page)

#fill in your email and password creds "your email" "your pass"
email_field = browser.find_element_by_id("fld-e")
email_field.send_keys("EMAIL HERE")
password_field = browser.find_element_by_id("fld-p1")
password_field.send_keys("PASSWORD HERE")
print("account creds filled")

#sign in button
part2 = False
while not part2:
    #After creds are filled finds Sign In Button and clicks it
    try:
        sign_in_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-secondary"))
        )
        sign_in_button.click()

        #added sleep for stability
        time.sleep(5) 
        print("sign in button clicked")
       
    except:
        part2 = True

        #Directs user to one of the product options above
        browser.get(test_product_in_stock)
        time.sleep(5)

#begins try except block to start checking if the add to cart button is available
isComplete = False
while not isComplete:
    #Tries to find add to cart on specific product, if the condition is not met the page reloads until the button is found
    try:
        atcBtn = WebDriverWait(browser, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
        #Used coloram library so when user sees the color red the user knows nothing was clicked, if condition is met the print line turns green.
        print(Back.RED + "No Good")
        browser.refresh()
        continue

    try: 
        # Clicks add to cart button when found
        atcBtn.click()
        time.sleep(2)
        browser.get(out_of_stock_product)
        # browser.get(test_product_in_stock)
        print(Back.GREEN + Fore.WHITE + "added")
          
        #begins checkout process
        browser.get("https://www.bestbuy.com/cart")
           
        checkoutBtn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button"))
            )
        checkoutBtn.click()

        #directs user to payment page
        browser.get(pay_page)

        # fill in card cvv assuming user has credit card already connected to account
        cvvField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "credit-card-cvv"))
        )
        cvvField.send_keys("CVV")       

         # place order
        placeOrderBtn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/div/div[4]/div[3]/div/button"))
        )
        #place order button is commented out for safety reasons, uncomment if user is ready to go through whole process.
        #placeOrderBtn.click()
        print("order is complete")
        isComplete = True

        #delete comment on next line with your own path to save a screen shot of the page after item is bought!
        browser.save_screenshot('C:\\Users\\Main\\Downloads\\Headless_test.png')
        
        # total time taken 
        end = time.time() 
        print(f"Total runtime of the program is {end - begin}") 
        time.sleep(12)
        browser.quit()  
        isComplete = True

    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        browser.get(test_product_in_stock)
        print("Error - restarting bot")
        continue

 
browser.quit()