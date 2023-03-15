import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import pickle, json, time, toml
from pathlib import Path
from datetime import datetime
import email_sender

# Get the absolute path of the current file
current_file_path = Path(__file__).resolve()

# Get the parent directory of the current file
parent_directory = current_file_path.parent

# Get the parent directory of the parent directory
grand_parent_directory = parent_directory.parent

MIN_JOB_DURATION = 4  # Minimum job duration to be notified for
JOBS_TO_NOTIFY = {}
new_jobs_found = False

# Webdriver Options
system = platform.system()
options = Options()
options.add_argument("--window-size=768,1024")
options.add_argument("--headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-accelerated-2d-canvas")
options.add_argument("--disable-accelerated-jpeg-decoding")
options.add_argument("--disable-infobars")
options.add_argument("--disable-notifications")

# Get location of Chrome depending on OS
if system == "Windows":
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
elif system == "Darwin": # Mac
    # Chrome driver is in the environment variables
    pass
else: # Linux
    options.binary_location = "/usr/bin/google-chrome" # Untested
    pass

# Load in past jobs file or create file if none exists
past_jobs_filepath = parent_directory / 'past_jobs.json'

try:
    with open(past_jobs_filepath, 'r') as file:
        past_jobs_data = json.load(file)
except FileNotFoundError:
    past_jobs_data = {}
    with open(past_jobs_filepath, 'w') as file:
        json.dump(past_jobs_data, file)


# Join the grand parent directory and the config file name
config_file_path = grand_parent_directory / "config.toml"

# Load school board information
with open(config_file_path, "r") as file:
    config_data = toml.load(file)

# Function for determining the duration of a job in hours
def get_duration_in_hours(start_time, end_time):
    start_time = datetime.strptime(start_time, '%H:%M')
    end_time = datetime.strptime(end_time, '%H:%M')
    duration = end_time - start_time
    return round(duration.total_seconds() / 3600,1) 

chromedriver_path = ChromeDriverManager().install()

for board_name, board_info in config_data['boards'].items():
    # Initialize variables for board
    username = board_info[0]['username']
    board_login_name = f"atrieve_{board_name}"
    login_web_address = board_info[0]['login']
    jobboard_web_address = board_info[0]['jobboard']
    password = board_info[0]['password']

    # Catch empty passwords prompting the user to enter a password
    if password is None:
        print("Please run the password_init.py file to set your passwords as they are currently empty")
        break

    # Load cookies if they exist
    cookies_file_path = parent_directory / (f"cookies_{board_name}.pkl")
    try:
        with open(cookies_file_path, "rb") as f:
            cookies = pickle.load(f)
    except (EOFError, FileNotFoundError):
        cookies = {}

    service = Service(executable_path=chromedriver_path)
    service.start()
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.get(jobboard_web_address) # Needed or else get an error trying to load cookies
        if cookies != {}:
            for cookie in cookies:
                driver.add_cookie(cookie)
            # With cookies attempt at opening job page
            driver.get(jobboard_web_address)

        # If login present means we got denied access using the cookies
        if "login" in driver.current_url.lower():
            print('cookies didnt work')
            driver.delete_all_cookies() # Causes error or fails without
            driver.get(login_web_address)
            
            # Enter Username
            userElem = driver.find_element("id","Username")
            userElem.send_keys(username) # Input username

            # Enter Password
            passElem = driver.find_element('name','Password')
            passElem.send_keys(password) # Input Password
            time.sleep(0.1)
            
            # Click login button
            login = driver.find_element('id', "SsoLogin_Btn")
            login.click()
            time.sleep(1)
            
            if "login" not in driver.current_url.lower(): # Login success and save cookies
                with open(cookies_file_path, "wb") as f:
                    pickle.dump(driver.get_cookies(), f)
                driver.get(jobboard_web_address)
                time.sleep(1)

        else:
            print('Cookies were successful')
            pass
        job_board_image_path = parent_directory / (f"jobs_{board_name}.png")
        driver.get_screenshot_as_file(job_board_image_path)

        # Failed login skip to next school board
        if "login" in driver.current_url.lower():
            continue

        # Generate the HTML of the page
        rawcontent = driver.page_source
        soup = BeautifulSoup(rawcontent,'lxml')
        jobs_body = soup.find('tbody') # Find tag where jobs are found

        if jobs_body: # if there are jobs
            jobs_html_list = jobs_body.select('tr')
            for job_row in jobs_html_list:
                job_information = job_row.select('td')
                job_id = job_information[0].getText().strip()
                # print(job_id)
                if job_id not in past_jobs_data.keys():
                    new_jobs_found = True
                    job_dictionary = {
                        'board': board_name,
                        'starttime': job_information[6].getText().split("-")[0],
                        'endtime': job_information[6].getText().split("-")[1],
                        'startdate': job_information[1].getText(),
                        'enddate': job_information[2].getText(),
                        'subject': job_information[3].getText(),
                        'location': job_information[5].getText(),
                        'duration_in_hours': '',
                        'link': jobboard_web_address,
                    }
                    
                    # Get duration of single job
                    job_dictionary['duration_in_hours'] = get_duration_in_hours(job_dictionary['starttime'], job_dictionary['endtime'])
                    
                    # Only Notify if job is longer than threshold
                    if job_dictionary['duration_in_hours'] >= MIN_JOB_DURATION:
                        JOBS_TO_NOTIFY[job_id] = job_dictionary
                    
                    # Add job to dump into JSON
                    past_jobs_data[job_id] = job_dictionary
    service.stop()

if new_jobs_found:
    # Write the updated data to the file
    with open(past_jobs_filepath, 'w') as file:
        json.dump(past_jobs_data, file, indent=4)


if JOBS_TO_NOTIFY != {}:
    print('New Jobs Found')
    # print(email_to, email_from, email_cc)
    email_sender.send_email(
        jobs=JOBS_TO_NOTIFY
        )
else:
    print("No new jobs found")