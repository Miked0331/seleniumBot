import time
import colorama
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from colorama import Fore, Back, Style, init
colorama.init()

###

#Must use path to your own geckodriver file
geckodriver = r'C:\Geckodriver\geckodriver.exe'
 
options = webdriver.FirefoxOptions()
# options.add_argument('-headless')
 
browser = webdriver.Firefox(executable_path=geckodriver, options=options)
 
login_page = r"https://www.bestbuy.com/signin"
                
test_product_in_stock = r"https://www.bestbuy.com/site/nvidia-geforce-rtx-3060-ti-8gb-gddr6-pci-express-4-0-graphics-card-steel-and-black/6439402.p?skuId=6439402"
out_of_stock_product = r"https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-ti-ftw3-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444444.p?skuId=6444444"

store_page = r"https://www.bestbuy.com/site/store-locator/"

pay_page = r"https://www.bestbuy.com/checkout/r/payment"

saved_parts = r"https://www.bestbuy.com/site/customer/lists/manage/saveditems"

begin = time.time()

browser.get(login_page)

email_field = browser.find_element_by_id("fld-e")
email_field.send_keys("Your Email Here")
password_field = browser.find_element_by_id("fld-p1")
password_field.send_keys("Your Password Here")
print("account creds filled")



#sign in button
part2 = False
while not part2:
    try:
        sign_in_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-secondary"))
        )
        sign_in_button.click()
        time.sleep(15) 
        print("sign in button clicked")
       
    except:
        part2 = True
        browser.get(test_product_in_stock)
        time.sleep(5)


isComplete = False
while not isComplete:

    try:
        atcBtn = WebDriverWait(browser, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-button"))
        )
    except:
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