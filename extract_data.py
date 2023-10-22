import time, csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd

def clear_data(name):
    with open(f"data/{name}", "w", newline="") as file:
        file.write('datetime,price,number,type\n')


def save_live_data(name):
    # Read the CSV file
    df = pd.read_csv(f'data/{name}')

    df = df[-20:]

    df.to_csv(f'live_data/{name}', index=False)



def flip_cnt_rm(name):
    # Read the CSV file
    df = pd.read_csv(f'data/{name}')

    # Find duplicates based on all columns
    duplicates = df[df.duplicated(keep=False)]  # `keep=False` keeps all duplicates

    num_duplicates = len(duplicates)

    print(f'Total number of duplicates: {num_duplicates}')

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Save the DataFrame back to a CSV file (optional)
    df.to_csv(f'data/{name}', index=False)
    print('duplicates removed for', f'{name}')

    # Find duplicates based on all columns
    duplicates = df[df.duplicated(keep=False)]  # `keep=False` keeps all duplicates

    num_duplicates = len(duplicates)

    print(f'Total number of duplicates: {num_duplicates}')

    # print(f'Line numbers of duplicates: {duplicate_indices}')

    # Step 2: Reverse the DataFrame
    df_reversed = df[::-1]

    # Step 3: Save the reversed DataFrame to a new CSV file
    df_reversed.to_csv(f'data/{name}', index=False)  # Replace 'reversed_file.csv' with your desired output file name
    print('\n\n')

def login(driver, number, password):
    my_element = driver.find_element(By.XPATH, "/html/body/div/div[5]/ul/li[4]")

    my_element.click()
    time.sleep(1)

    # Find the input element using XPath
    input_number = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[1]/input")
    input_password = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/input")
    submit_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[3]/button")

    # Input a value
    input_number.send_keys(number)
    input_password.send_keys(password)
    submit_button.click()
    time.sleep(1)

    win_element = driver.find_element(By.XPATH, "/html/body/div/div[4]/ul/li[3]")
    win_element.click()
    time.sleep(3)


def scrapToCsv(soup, file_name):

    # Find the table element by class, ID, or other attributes
    tables = soup.find_all('table')

    table = tables[1]

    rows = table.find_all('tr')

    with open(f"data/{file_name}", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        ls1 = []
        for row in rows:
            cells = row.find_all('td')
            ls = []
            for cell in cells:
                ls.append((cell.text).replace("\n", "").strip())
            # print(ls)
            ls1.append(ls)
        
        for x in ls1[2:]:
            writer.writerow(x)


# Launch the web browser
driver = webdriver.Chrome()  # Change this to the appropriate web driver

# Open the web page
driver.get('https://vespa.games/#/')
time.sleep(4)

login(driver, "8824655613", "Sarvesh@2000")
t = 3

# Get the page source
page_source = driver.page_source

file_names = ['sapre.csv', 'parity.csv', 'bcone.csv', 'emerd.csv']
xpaths = [
    "/html/body/div/div[2]/div[2]/div[2]/div/div[3]/ul/li[2]/i[2]", 
    "/html/body/div/div[2]/div[2]/div[1]/div/div[3]/ul/li[2]/i[2]", 
    "/html/body/div/div[2]/div[2]/div[3]/div/div[3]/ul/li[2]/i[2]", 
    "/html/body/div/div[2]/div[2]/div[4]/div/div[3]/ul/li[2]/i[2]"
    ]

sapre_tab = '/html/body/div/div[2]/ul/li[1]'
parity_tab = '/html/body/div/div[2]/ul/li[2]'
bcone_tab = '/html/body/div/div[2]/ul/li[3]'
emerd_tab = '/html/body/div/div[2]/ul/li[4]'
tabs = [sapre_tab, parity_tab, bcone_tab, emerd_tab]

element = driver.find_element(By.XPATH, xpaths[t])

clear_data(file_names[t])

tab_element = driver.find_element(By.XPATH, tabs[t])
tab_element.click()
time.sleep(3)

# Scroll down by 700 pixels
driver.execute_script("window.scrollBy(0, 700);")
time.sleep(1)

for i in range(70):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    try:
        scrapToCsv(soup, file_names[t])
        element.click()
        time.sleep(0.8)
    except:
        print("slept")
        time.sleep(0.7)

flip_cnt_rm(file_names[t])

save_live_data(file_names[t])

print("program finished")