# Selenium Automation Assignment | SYFE

This is a Syfe QA Intern assignment where I automate the e-commerce process of logging in 
by incorrect and correct credentials and then sorting items based on price and adding them 
in my cart, then removing a specific item from my cart based on it's price and then
adding my personal details for the checkout order and placing the order after finally
I logout.

## Set Up the Script
The required tools for running this python file are:-

1.) go to cmd and type -> pip install selenium
2.) go to a new tab on chrome and type -> chrome://version and checkout your version
3.) I used chromedriver for selinium for automation on chrome so for that install the relevant chromedriver 
    (keep in mind that both the chromedriver and chrome should be of same version so either update the chrome by going on about on help after clicking three dots in the top right
     or install the relevant version chromedriver )
4.) paste your path where you have installed chromedriver on line no. 12
5.) run the python file using -> python file_name.py
6.) sit back and watch the show 


## Observation & Assumption
1.) password.clear() did not worked for the password_field, assumption is that the password id retained it's old value
    so had to use delete
2.) The process was too fast for capturing on video so adding time.sleep() wherever needed.
3.) Removing element made the first item to be removed which was the highest dollar amount and not withing the limits informed on the instruction. (fixed)


