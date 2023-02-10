DISCLAIMER: Does not currently work as the project sits right now. It is missing a config.toml file

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

- I gained knowledge in the Cryptography and Keychain libraries, which I hadn't used before. The project deals with sensitive information, such as passwords and cookies, which need to be stored securely.
- I learned about running Selenium in headless mode, which was a new discovery for me.
- Using Poetry for virtual environment management was a first for me and I still need to determine which I prefer between Poetry and venv.
- I discovered the wheel package, but found that it doesn't transfer between different operating systems.
- My understanding of virtual environments improved and I'm still investigating running a Python script through crontab while accessing the virtual environment.
- Firefox webdriver did not work on windows when running from task scheduler. Would only run from command prompt when using "Run As Administrator" running the program through task scheduler and using the option to run with highest privileges didn't solve it either. Simply replacing firefox with Chrome solved the issue.

## To-Do:

- Upgrade the server to test the program on a Linux distribution with more than 2GB of RAM, as the current web browser usage requires more RAM than a 1GB Raspberry Pi can provide.
- Investigate the keyring.cryptfile as a solution for saving passwords in the database on a Raspberry Pi, as the standard keyring package lacked a keyring backend.
- Verify if virtual environments can be accessed through crontab.
- Set up the config.toml for the program to be usable, as it is currently not functional without it.

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
