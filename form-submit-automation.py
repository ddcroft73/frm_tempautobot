
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
# the times for each element, but i find higher is more forgiving.
#
# delay:      The amount of time to wait for the element to load. Driver will wait this amount of time
#             for the element to load or will execute if it loads before. I keep them at  10. 
#             It seems to work better if I allow extra time before an action is executed.
# doing:      The action being sent to the find_element() method. More actions may be added to the 
#             switch case if needed and defined same as if you called the method directly. For my purposees:
#             "send" send keystroke to an element.
#             "click" sends a click event to the element.
#             "get"  calls find_element and returns an object so the properties may be accessed.
# by_target:  This is the string passed in referenced from the By object. FOr my purposes I'm  using
#             By.XPATH, and By.LINK_TEXT, but there are others you can use to access any element as well.
# elements_target:    This is that actual string data gotten from the webpage previous;y using inspect that
#                     identifies the element.
# send_data:  This is an otional argument that is only used when sending keystrokes to an element.
# 
# returns:    An object from find_element that can be used to get the elements text as well as other properties 
#             such as an attribute.               
#
def wait_and_find(delay: int, doing: str,  by_target: str, elements_target: str, send_data: str=None) -> str:
    result: str=None 
    WebDriverWait(drv, delay).until(EC.presence_of_element_located((by_target, elements_target)))
    # decide what is being done.
    match doing:
        case "send":
            drv.find_element(by_target, elements_target).send_keys(send_data)
        case "click":
            drv.find_element(by_target, elements_target).click()
        case "get":
            result = drv.find_element(by_target, elements_target)
    return result      


# load the data to run the site into a dictionary so the values can be accessed
# directly and easily updated all in one place.   
def get_userdata() -> dict:
    with open(PAYLOAD, "r") as infile:
        data = json.load(infile)
    return data


#
# FUNCTIONS TO SUBMIT AND\OR access FORM\PAGE DATA -
# 
#   This is just  example data to mimic what you way\should find when accessing page elements. 
#   THis script will not run as is. You must personalixe it to your needs. For a better
#   Description of how to obtain this data see readme.md
#   For this tutorial I am accessing the elements by XPATH, You can also access them by 
#   LINK_TEXT, TAG_NAME, CLASS_NAME, ID etc. 
# 
#    
def login() -> None:
    # this is the target of the element you copied form the inspect window in your browser.
    # name the variable appropriatly and paste the data to it.
    userid_xpath = '//*[@id="userid"]' # example of what XPATH data may look like
    user_pword_xpath = '//*[@id="password"]'
    page_data_xpath = 'target to page data'
    # XPATH data can also look like:
    submit_button_xpath = "/html/body/div/div/div/section/div[1]/div[2]/div/form/div[6]/div/button"
    
    # This function call is saying:
    # wait for X seconds before "action" by method, and send data if applicable
    # You eill access the data to send in the json like data['keyName')
    # 
    wait_and_find(10, 'send', By.XPATH, userid_xpath, data['userid'])   
    wait_and_find(10, 'send', By.XPATH, user_pword_xpath, data['password'])
    # you can also send an event by the text of the link to click a known link
    wait_and_find(10, 'click', By.LINK_TEXT, data['my_link_text'])

    # sends a clic event to the buttons target and submits the form
    # you can now move your focus to another function defined to handle 
    # another page or the data that is laoded after the submit
    wait_and_find(10, 'click', By.XPATH, submit_button_xpath)
    
    # YOu can be creative here and do more if you need
    # You can query an element for it's text using this syntax
    
    result = wait_and_find(3, 'get', By.XPATH, page_data_xpath)
    print(result.text)


# another exampl with out many comments and witht the element identifier
# above the method call
def submit_user_info() -> None:    
    # the target you use doesnt always have to be XPATH, but make sure
    # the method by which you identify matches the part of the element you want.
    address_xpath = '//*[@id="CustomerInfo_Address1"]'
    wait_and_find(10, 'send', By.XPATH, address_xpath, data['address'])  
    
    city_class_name = "city_class name"    
    wait_and_find(10, 'send', By.CLASS_NAME, city_class_name, data['city'])
    
    zip_tagname = "zipTagname"    
    wait_and_find(10, 'send', By.TAG_NAME, zip_tagname, data['zip'])
    
    phone_ID = "PhoneID"    
    wait_and_find(10, 'send', By.ID, phone_ID, data['phone'])
    
    state_xpath = '//*[@id="CustomerInfo_State"]'              
    wait_and_find(10, 'send', By.XPATH, state_xpath, data['state'])
    
    # clicking on link by link text
    link_text = "The text for a link..."
    wait_and_find(10, 'click', By.LINK_TEXT, link_text)    
    # clicking on link by The first word in the link textt
    wait_and_find(10, 'click', By.PARTIAL_LINK_TEXT, link_text.split()[0])         

    # return an atribute of an element by the link text
    link = wait_and_find(3, 'get', By.LINK_TEXT, link_text)
    the_link = link.get_attribute('href') 
    
    # click the button to submit the form.
    next_button_xpath = '//*[@id="bntNextCustomerInfo"]'
    wait_and_find(10, 'click', By.XPATH, next_button_xpath)   


#  Define more functions to get\access\manipulate dynamic data and then re submot it. 
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
