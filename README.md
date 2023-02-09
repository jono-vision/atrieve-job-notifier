# Job Board Automation

This is a code to automate the process of logging in and scraping job information from multiple job boards. The code uses Poetry as a package manager.

## Requirements

- geckodriver
- BeautifulSoup
- cryptography
- keyring
- selenium
- webdriver_manager

## Getting Started

Clone the repository and navigate to the project directory.

Install the required packages using poetry:

```
poetry install
```

Update the configuration file with the necessary information for each job board you want to scrape.

Run the main.py script to log in and scrape job information:

```
python main.py
```

How it Works
The code retrieves the login credentials and job board URLs from the configuration file.

It starts a virtual Firefox web browser and loads saved cookies if they exist. If cookies are not present or have expired, the code logs in using the credentials.

After logging in, the code scrapes the job information to send an email of the new jobs found using the email

The code continues this process for each job board specified in the configuration file.

## Use with Crontab

1. Create a virtual environment for your project using Poetry. Go to your project directory and run the following command:

```
poetry install
```

This will install all the dependencies for your project in a virtual environment.

2. Go to your project directory and activate the virtual environment.

```
poetry shell
```

3. Run the following command to display the path to your virtual environment's Python executable:
   `which python`
   The output of this command should be the path to the Python executable in your virtual environment.

4. Open the crontab file using the following command:
   `crontab -e`
5. Enter the following line in the crontab file, replacing /path/to/python with the path obtained in step 4 and replacing /path/to/main.py with the path to your main.py file.

`*/10 * * * * /path/to/python /path/to/main.py`
Save the crontab file and exit.

The script main.py will now run every 10 minutes, as specified by the crontab entry.

## Lessons Learned

I learned a lot from this program. I hate to admit that CHATGPT helped me out a lot as it acted as my mentor answering all my "stupid" questions which Ive never had access to before being a self taught.

1. Cryptography and Keychain library: I have never used these libraries before. Since this project deals with storing sensitive information like passwords and cookies which house credential information which would be best not to have those stored in a unsecure place. I encrypted the cookies using cryptography so that the cookies can be on the project directory but the key is stored on the computers keychain to encode and decode the cookies.
2. I learned you can run selenium headless! When i first made this program when I was two months into learning python, I didnt know this was a thing.
3. Used Poetry for the first time - seemed to be the most commonly used virtual environment manager. I have mainly used venv for virtual environment management. I still need to do some exploring as to which I prefer. Poetry seems like a black box as to whats going on which can be good and bad. I used it initially because of the popularity around it and it was to ease the installation process a bit.
4. Learned about the wheel package. I thought the wheel package was going to be this amazing one step installation but it turns out it doesn't transfer between PC - Mac - Linux. So I didn't really use it. Need to do some more exploration into this as well.
5. Virtual environments! Which i have been pretty bad at until lately. Early on in my python learning i feel this was a topic glossed over which Im not exactly sure why, maybe because a lot of my learning was done in the data science realm and I feel that anaconda is used heavily there and Im just following along not really knowing what Im doing. But the big thing about virtual environment was running a python script through the crontab while still accessing the virtual environment (See to do).
6. ChatGPT is both awesome and maybe terrible? I feel like Im using steroids and am kinda cheating. I guess this is what it felt like to be Jose Canseco

## To Do

1. So this program does not run on a Raspberry Pi with RAM of less than 2GB from what I've seen and this is because of the web browser being a RAM hog. I tried installing on a Pi with 1GB and I could not get it to work. Planning to upgrade my server soon and if Im still interested in this program Ill be able to see if it works on a linux distribution.
2. On Pi the keyring package didnt work because it was lacking a keyring backend. I found that keyring.cryptfile allowed me to successful save my passwords to the database. It had the annoying feature of asking to input your password to the backend everytime you accessed a password which wouldnt allow for complete automation. Further exploration into this is needed, but maybe running linux on something other than a Pi OS wouldnt have this issue.
3. Still need to verify that you can access virtual environment through the crontab. This was a topic i dont think I would have figured out with ChatGPT.
4. Need to get the config.toml up as this is currently not useable code without it.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
