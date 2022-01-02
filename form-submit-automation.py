
import json
from selenium import webdriver                                     
from webdriver_manager.chrome import ChromeDriverManager           # ChromeDriverManager oddwers a better way to access
                                                                   # the webdriver other than execution_path="path to web driver"
from selenium.webdriver.chrome.service import Service              # Service that invokes ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait            # Waits for the page elements to load to ensure they can accept input 
from selenium.webdriver.support import expected_conditions as EC   # the condition the driver is set to wait for.
from selenium.webdriver.common.by import By                        # a string object that issues the type of element being accessed

PAYLOAD = "./bot-payload.jsonc"                                    # The file that contains all the data used to for the form submisssion(s)


# THis function initializes and sets up the options for the webdriver
# then returns the a criver object used to run the aoutomation
def start_bot(headless: bool=False) -> None:
    # all of thes options are "optional" if you elect not to use them, you may but on the initalizing of the 
    # web driver below delete out the options argument.
    chrome_options = webdriver.ChromeOptions()     
    if headless: chrome_options.add_argument("--headless")
    # attempts to mask the automation, But noting gets them all. 
    # TO remain even more incognito use requests, urlip, urlib2, cookielib, and don't use Selenium
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    srv=Service(ChromeDriverManager().install())
    # delete options=chrome_options to not use any of the automation, and headless options
    driver = webdriver.Chrome(service=srv, options=chrome_options) 
    # try to keep the webdriver from setting off automation alarms. Doesnt always work.
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd(
        'Network.setUserAgentOverride', {
         "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
         })

    driver.refresh()        
    # using the dictiionary data returned for the payload.json file 
    # access the URL designated as the start page
    driver.get(data["start_url"])     
     # return the intiialized driver object.
    return driver
    
# wait_and_find() function attmepts to wait for each element passed in before acessing it, you can adjust 
# the times for some timeouts. Some my stil time out but compared to not using WebDriverWait()
# before sending or clicking it seems to work much better.
#
# delay:      The amount of time to wait for the element to load. Driver will wait this amount of time
#             fore the element to load or will execute if it loads before. I keep them at  10. 
#             It seems to work better if I allow extra time before an action is executed.
# doing:      The action being sent to the find_element() method. These actions can be added to the 
#             match case if needed and defined as if youd call the method directly. FoOr our purposees:
#             "send" send skeystroke to an element.
#             "click" sends a click event to the element.
#             "query"  calls find_element and returns an object.
# by_target:  This is the string passed in referenced fFrom the By object. FOr our purposes we are using
#             By.XPATH, and By.LINK_TEXT, but there are others you can utilize to access the element as well.
# elements_target:    This is that actual string data gotten from the webpage previous;y using inspect that
#                     identifies the element.
# send_data:  This is an otiona argument that is aonly used when sendinf keys to an element.
# 
# returns:    An object from find_element that can be used to get the elements text as well as other things 
#             such as an attribute.               
#
def wait_and_find(delay: int, doing: str,  by_target: str, elements_target: str, send_data: str=None) -> str:
    result: str=None 
    WebDriverWait(drv, delay).until(EC.presence_of_element_located((by_target, elements_target)))

    match doing:
        case "send":
            drv.find_element(by_target, elements_target).send_keys(send_data)
        case "click":
            result = drv.find_element(by_target, elements_target).click()
        case "query":
            result = drv.find_element(by_target, elements_target)
    return result      


# load the data to run the site into a dictionary so the values can be accessed
# directly and easily  updated all in one place.   
def get_userdata() -> dict:
    with open(PAYLOAD, "r") as infile:
        data = json.load(infile)
    return data


#
# FUNCTIONS TO SUBMIT AND\OR QUERY FORM DATA -
# 
#   This is just examole data to mimic what you way\should find when accessing page elements. For a better
#   Description of how to obtain this data see readme.md
#   For this tutorial I am accessing the elements by XPATH, You can also access them by 
#   LINK_TEXT, TAG_NAME, CLASS, ID etc. Examples of each are given.
# 
#    
def login() -> str:
    # this is the target of the element you cpoioed form the inspect window in your browser.
    # name the variable appropriatly and paste the data to it.
    userid_xpath = '//*[@id="userid"]'
    user_pword = '//*[@id="password"]'
    page_data = 'target to page data'
    submit_xpath = "/html/body/div/div/div/section/div[1]/div[2]/div/form/div[6]/div/button"
    
    # This function call is saying:
    # wait for X seconds before "action" by method, data to send if applicable
    # 
    #  send the User Id name By."method" to the element
    wait_and_find(10, 'send', By.XPATH, userid_xpath, data['userid'])   
    wait_and_find(10, 'send', By.XPATH, user_pword, data['password'])
    # you can also send an event by the text of the link to click a known link
    wait_and_find(10, 'click', By.LINK_TEXT, data['my_link_text'])

    # sends a clic event to the buttons target and submits the data
    wait_and_find(10, 'click', By.XPATH, submit_xpath)
    
    # YOu can be creative here and do more if you need
    # You can query an element for an attribute using this syntax to get
    # the text that comes back    
    result = wait_and_find(3, 'query', By.XPATH, page_data)
    print(result.text)


# another exampl with out any comments
def submit_user_info() -> None:
    address_xpath = '//*[@id="CustomerInfo_Address1"]'
    city_xpath = '//*[@id="CustomerInfo_City"]'
    state_xpath = '//*[@id="CustomerInfo_State"]'
    zip_xpath = '//*[@id="CustomerInfo_Zip"]'
    phone_xpath = '//*[@id="Phone"]'
    email_xpath = '//*[@id="Email"]'
    link_text = "The text for a link..."
    next_button_xpath = '//*[@id="bntNextCustomerInfo"]'
    
    # the target you use doesnt always have to be XPATH, but make sure
    # the method by which you identify mathes the part of the element you want.
    wait_and_find(10, 'send', By.XPATH, address_xpath, data['address'])  
    wait_and_find(10, 'send', By.CLASS_NAME, city_xpath, data['city'])
    wait_and_find(10, 'send', By.TAG_NAME, zip_xpath, data['zip'])
    wait_and_find(10, 'send', By.ID, phone_xpath, data['phone'])
    wait_and_find(10, 'send', By.LINK_TEXT, email_xpath, data['email'])
    wait_and_find(10, 'send', By.XPATH, state_xpath, data['state']) 

    # return an atribute of an element
    link = wait_and_find(3, 'query', By.LINK_TEXT, link_text)
    the_link = link.get_attribute('href') 

    wait_and_find(10, 'click', By.XPATH, next_button_xpath)   


#  Define more functions to get\access\manipulate dynamic data and then re  submot it 
#  more data as needed... You can acces links and crawl them\request data and parse\scrape it as well.





# With a few modifications you could employ command line arguemts to control how the bot launches,
# quiclly change things like the amount you're paying this time, or anything else you would to change
# about the data being submitted
if __name__ == '__main__':

    # load your dat to be used in a ditionary throughout the script
    # all the data you have designated for the foem can now be accesses eith
    #  key value pairs like:
    #  data['key name here']
    data = get_userdata()
    # init the webdriver, set the options, and load the start page.
    drv = start_bot(headless=False)     

    # call individual functions to take care of each page breaking  tasks into 
    # individual functions to make code simple and readable. Thesse fumctions 
    # will vary depending on how the pages are served. There could be one or two
    # or could be 5 or 10. Wlll have to edit these functioins to suit your needs.
    login()      
    submit_user_info()
    # sumbit_paymemt_info()
    # data = get_data_from_page()
    # sumbit_data_to_differentpage(data)
    # etc, etc.
