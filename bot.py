import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# TODO:
#3: Make sure account has CC details and all info needed for speedy checkout

# Vars for different products
ryzen9_5900x = r"https://www.bestbuy.com/site/amd-ryzen-9-5900x-4th-gen-12-core-24-threads-unlocked-desktop-processor-without-cooler/6438942.p?skuId=6438942"
nvidia_rtx3060ti = r"https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-ti-ftw3-gaming-8gb-gddr6-pci-express-4-0-graphics-card/6444444.p?skuId=6444444"
test_product_in_stock = r"https://www.bestbuy.com/site/customer/lists/manage/saveditems"

browser = webdriver.Chrome(r"C:\Users\Main\Documents\Projects\ChromeDriver/chromedriver")
browser.maximize_window()

# hit the site
#browser.get("https://www.bestbuy.com")
# look for amd ryzen 9 product, fuck scalpers
browser.get(test_product_in_stock)

time.sleep(2)

part1 = False
while not part1:
    try:
        #finds account button
        acctBtn = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Account" ))
        )
        
        #Clicks account button
        acctBtn.click()
        part1 = True
    except:
            #if accnt button doesnt work
            print("this did not work. ")
            browser.quit()
            part1 = True

# Sign in as a user, this needs real credentials
email_field = browser.find_element_by_id("fld-e")
email_field.send_keys("EMAIL HERE")
password_field = browser.find_element_by_id("fld-p1")
password_field.send_keys("PASSWORD HERE")

#sign in button method
part2 = False
while not part2:
    try:
        sign_in_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "btn-secondary"))
        )
        sign_in_button.click() 
        time.sleep(10)   
    except:
        part2 = True
       

#find add to cart button
isComplete = False
while not isComplete:
    # find add to cart button
    try:
        atcBtn = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[2]/div/div/div[3]/div[2]/ul/li[1]/div/div[3]/div[4]/div/div/div/div/div/button"))
        )
        
    except:
        time.sleep(2)
        print("no button found")
        continue

    print("Add to cart button found")
     
    try:
       
        # add to cart
        atcBtn.click()

        finalAdd = False
        while not finalAdd:
            # find add to cart button #2
            try:
                atcBtn = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/main/div[2]/div/div/div[3]/div[2]/ul/li[1]/div/div[3]/div[4]/div/div/div/div/div/button"))
                )
        
            except:
                time.sleep(2)
                print("no button found")
                continue

        print("Add to cart button found")

        time.sleep(60)
        browser.quit()

        # go to cart and begin checkout
        browser.get("https://www.bestbuy.com/cart")
        
        checkoutBtn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/main/div/div[2]/div[1]/div/div[1]/div[1]/section[2]/div/div/div[4]/div/div[1]/button"))
        )
        checkoutBtn.click()

        # fill in card cvv
        cvvField = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "credit-card-cvv"))
        )
        cvvField.send_keys("513")       

         # place order
        placeOrderBtn = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[2]/div[1]/div[1]/main/div[2]/div[2]/div/div[4]/div[3]/div/button"))
        )
        placeOrderBtn.click()
        print("order is complete")
        isComplete = True
       
    
    except:
        # make sure this link is the same as the link passed to driver.get() before looping
        browser.get("https://www.bestbuy.com/site/customer/lists/manage/saveditems")
        print("Error - restarting bot")
        continue

time.sleep(300)
browser.quit()


