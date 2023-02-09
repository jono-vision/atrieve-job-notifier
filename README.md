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

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
