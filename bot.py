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
                
test_product_in_stock = r"https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402"
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
email_field.send_keys("Your Email Here")
password_field = browser.find_element_by_id("fld-p1")
password_field.send_keys("Your Password Here")
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
         # add to cart
        atcBtn.click()
        time.sleep(500)
        browser.get(out_of_stock_product)
        # browser.get(test_product_in_stock)
        print(Back.GREEN + Fore.WHITE + "added")
        try:
            atcBtn2 = WebDriverWait(browser, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
            )
        except:
            print(Back.LIGHTMAGENTA_EX + "No Good")
            browser.refresh()
            continue

            #begins checkout process
        atcBtn2.click()
        print(Back.LIGHTYELLOW_EX + Fore.BLACK + "added")
        browser.get("https://www.bestbuy.com/cart")

            # shippingBtn = WebDriverWait(browser,5).until(
            #     EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[1]/div[4]/ul/li/section/div[2]/div[2]/form/div[2]/fieldset/div[2]/div[1]/div/div/div/input"))
            # )
            # shippingBtn.click()
            
        checkoutBtn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[3]/div/div[1]/button"))
            )
        checkoutBtn.click()

        time.sleep(3)

        browser.get(pay_page)
        browser.save_screenshot('C:\\Users\\Main\\Downloads\\Headless_test.png')
            # total time taken 
            # select = Select(browser.find_element_by_css_selector('#consolidatedAddresses\.ui_address_2\.state'))
        end = time.time() 
        print(f"Total runtime of the program is {end - begin}") 
        time.sleep(12)
        browser.quit()  
        isComplete = True

    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        browser.get(saved_parts)
        print("Error - restarting bot")
        continue

  
#browser.save_screenshot('C:\\Users\\Main\\Downloads\\headless_firefox_test.png')
 
browser.quit()