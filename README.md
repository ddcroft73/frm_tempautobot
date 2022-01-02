# Template for login\form submissions using Selenium.

I have three bills I need to pay each months and for these blls, I'm unable to setup auto pay  with the debtor or auto draft from my bank account for one reason or another. So i decided I'd automate it with Selenium. Turns out it was easier than i thought but seeing how I needed to do it thrice I made an easy to use and modify template for just that. I am not an expert on Selenium this is just something I put together to keep my code clean, simple, readable, organized and easily reusable. Maybe it will be useful to others as well. 

I wrote the script on Windows10 using Python 3.10. If you change the match case conditional statements with if\else it will run on earlier versions.

To use this code you will need to install:

    
    pip install webdriver_manager

    pip install selenium

Some websites use code to sense if you are using automation. I've implemented some code to try and get around this, but It's not 100%. If you can access the page and submit data manually but the page either abruptly shuts down or refuses to return data, then its blocked. The other way to interact is by using the requests, urlib, urlib2 or other HTTP modules. 

I've also done away with calls to 2 depreciated methods of the webdriver module, find_elemnt_by_() and the need to define the location of the actual Selenium webdriver executable used to control the browser. Fomerlly you'd set up your driver by assigning a path as an argument;

    driver = webdriver.Chrome("path to executable")
or 

    driver = webdriver.Chrome(executable_path="path to executable") 
Instead I use webdiver_manager and pass in a reference to the Chrome Service Object.
    
    srv=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=srv, options=chrome_options) 
It will still work using the path but if nothing more this will stop the depreciation messages you'll get doing it with the path.


## Inspecting the webpage
In order to get the XPATH I use to identify the elements to the methods in the script, you need to open the inspect window on your browser and copy the path from within.
1. Navigate to the webpage you wish to automate.
2. Right click on the element you want to identify. *(Button, link anythng on the page.)*
3. Click Inspect.
4. When the window opens, repeat steps 2 and 3.
5. Right click on the highlighted code in the window.
6. Select Copy -> Copy Xpath.
Use this information to identify the element in the code as I've demonstrated.

It can be any acceptable way to link to the element. XPATH, ID, LINK_TEXT etc. However you will have to dissect these from the code as needed.

## Data to be used in the form submission
I've notice most scrapers\form submission scripts etc keep all the user data on the page, *(Maybe not all I only looked at a few examples)* I use a json file to store the data and then access it via a dictionary. This will make it easier and cleaner to use and aid in any updates you may need to make. I believe the code is self explanatory, But if you need help you can get more info [here](https://www.tutorialspoint.com/python/python_dictionary.htm) about dictionaries, and [here](https://realpython.com/python-json/) about json in Python.

## Headless Operation
In addition to the anti-automation options utilized in start_bot(), you can also run this script with the headless option. This means you won't see anything via a browser window. It will just execute in the background. Just change the code that calls the bot.

    drv = start_bot(headless=True) 
Change headless to True. If you use this option you should add logging or print the results of certain actions to the terminal window if you want to stay aprised of what the bot is doing. Alternately the script can easily be modified so that it can be called with options from the command line,  and ultimatley launched via a script by using cron or Windows Task Scheduler.
