
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#  WebDriver Setup
chrome_service = Service("C:\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_service)

# Task 1: Login Validation

def login(username, password):
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


# Validating login with invalid credentials
def validate_invalid_login():
    login("invalid_user", "wrong_password")
    time.sleep(5)  # Wait for 5 seconds to observe the result
    
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".error-message-container"))
        )
        assert "Username and password do not match any user in this applicatio ." in error_message.text
        print("Invalid login test passed.")
    except AssertionError:
        print("Assertion failed: Error message not found.")
    except Exception as e:
        print(f"An error occurred while validating invalid login: {e}")
    
    clear_and_login("standard_user", "secret_sauce")
    
def clear_and_login(username, password):
    try:
        # Clear username and password fields before entering valid credentials
        username_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "user-name"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        
        print("Clearing username and password fields...")
        username_field.click()  # Focus on username field
        username_field.send_keys(Keys.CONTROL, 'a')  # Select all
        username_field.send_keys(Keys.DELETE)  # Delete
        
        password_field.click()  # Focus on password field
        password_field.send_keys(Keys.CONTROL, 'a')  # Select all
        password_field.send_keys(Keys.DELETE)  # Delete
        
        #.clear() did not worked here in password_field as the field retained it's old password value after clearing
        
        time.sleep(2)
        
        print(f"Entering username: {username}")
        username_field.send_keys(username)
        
        
        print(f"Entering password: {password}")
        password_field.send_keys(password)
        
        
        #driver.execute_script("arguments[0].setAttribute('type', 'text')", password_field)
        # to see the password without in *** form (converting to text) for debugging
        
        
        time.sleep(1)
        
        driver.find_element(By.ID, "login-button").click()
        time.sleep(1)
        
        #I introduced a lot of time.sleep() so that we can see atleast what is happening in the video 
        
        # Wait for successful login and verify redirection
        WebDriverWait(driver, 10).until(
            EC.url_contains("inventory.html")
        )
        print("Valid login test passed.")
    except Exception as e:
        print(f"An error occurred during clearing and logging in: {e}")

# Task 2: Add Items to Cart from Inventory Page
def add_items_to_cart():
    # Filter products by "Price (low to high)"
    filter_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "product_sort_container"))
    )
    time.sleep(1)
    filter_dropdown.click()
    time.sleep(1)
    filter_dropdown.find_element(By.XPATH, "//option[text()='Price (low to high)']").click()

    # Add items to cart
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    time.sleep(1)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-bike-light").click()
    time.sleep(1)

    # Verify cart count
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == "2"
    print("Added two items to cart.")

# Task 3: Add Items to Cart from Inventory Item Page
def add_item_from_details_page():
    driver.find_element(By.LINK_TEXT, "Sauce Labs Onesie").click()
    time.sleep(1)
    
    add_to_cart_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart"))
    )
    add_to_cart_button.click()
    
    # Verify cart count after adding third item
    time.sleep(2)  # Wait for a short duration before checking cart count
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == "3"
    print("Added third item to cart.")

# Task 4: Remove Items from Cart
# def remove_item_from_cart():
#     driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
#     time.sleep(1)
    
#     # Wait for items to be visible in the cart and remove one item priced between $8 and $10
#     WebDriverWait(driver, 10).until(
#         EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Remove')]"))
#     )
    
#     time.sleep(1)
#     # Remove an item (assuming it's the first item)
#     driver.find_element(By.XPATH, "//button[contains(text(),'Remove')]").click()
    
#     # Verify cart count updates accordingly
#     time.sleep(2)  # Wait for a short duration before checking cart count
#     cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
#     assert cart_count == "2"
#     print("Removed one item from cart.")


def remove_item_from_cart():
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Wait for items to be visible in the cart
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='cart_item']"))
    )
    
    # Find all items in the cart
    cart_items = driver.find_elements(By.XPATH, "//div[@class='cart_item']")
    
    # Loop through items to find one priced between $8 and $10
    for item in cart_items:
        # Get the price element for each item
        price_element = item.find_element(By.CLASS_NAME, "inventory_item_price")
        price_text = price_element.text.strip('$')  # Remove dollar sign
        price = float(price_text)  # Convert price to float
        
        # Check if the price is between 8 and 10
        if 8 < price < 10:
            print(f"Removing item priced at ${price:.2f}")
            remove_button = item.find_element(By.XPATH, ".//button[contains(text(),'Remove')]")
            remove_button.click()
            break  # Exit loop after removing the item

    # Verify cart count updates accordingly
    time.sleep(2)  # Wait for a short duration before checking cart count
    cart_count = driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == "2"  # Assuming you started with 3 items
    print("Removed one item from cart.")
    

# Task 5: Checkout Workflow
def checkout():
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(1)
    
    driver.find_element(By.ID, "checkout").click()
    time.sleep(1)
    
    # Fill in checkout information with delays for visibility
    driver.find_element(By.ID, "first-name").send_keys("John")
    time.sleep(1)
    
    driver.find_element(By.ID, "last-name").send_keys("Doe")
    time.sleep(1)
    
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    
    time.sleep(1)  # Wait before clicking continue
    driver.find_element(By.ID, "continue").click()

    # Wait for checkout overview page and print total amount
    total_amount = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "summary_total_label"))
    ).text
    
    print(f"Total amount: {total_amount}")
    
    time.sleep(1)  # Wait before finishing purchase
    driver.find_element(By.ID, "finish").click()

# Task 6: Logout Functionality
def logout():
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    
    time.sleep(1)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))
    )
    
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    
    time.sleep(1)
   # Verify redirection back to login page 
    WebDriverWait(driver, 10).until(
       EC.url_contains("/")
    )
    print("Logged out successfully.")



# Main execution block with error handling
try:
   validate_invalid_login()  # First test invalid login credentials and wait for observation.
   time.sleep(5)             # Wait before proceeding to valid login.
   
#    login("standard_user", "secret_sauce")  # Now test valid credentials.
#    time.sleep(5)             # Wait for successful login.

   add_items_to_cart()
   time.sleep(5)

   add_item_from_details_page()
   time.sleep(5)

   remove_item_from_cart()
   time.sleep(5)

   checkout()
   time.sleep(5)
finally:
    if driver.current_url == "https://www.saucedemo.com/":
        print("Already on login page; no logout needed.")
    else:
        print(f"Current URL before logout: {driver.current_url}")
        logout()                 

