import time, csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler
import tensorflow as tf
import numpy as np
import pandas as pd


def generate_sequence(file_name):
    # Step 1: Data Preparation
    path = "live_data/"
    path += file_name
    df = pd.read_csv(path)
    data = df['number'].to_list()
    data = data[-14:]
    print("last_point: ", data[-1])
    return data

def bet_on(num):
    refresh = '/html/body/div/div[1]/div/div/div[2]'
    element = driver.find_element(By.XPATH, refresh)
    element.click()
    time.sleep(2)
    
    buttons = {
        0: '/html/body/div/div[2]/div[1]/ul[2]/li[1]',
        1: '/html/body/div/div[2]/div[1]/ul[2]/li[2]',
        2: '/html/body/div/div[2]/div[1]/ul[2]/li[3]',
        3: '/html/body/div/div[2]/div[1]/ul[2]/li[4]',
        4: '/html/body/div/div[2]/div[1]/ul[2]/li[5]',
        5: '/html/body/div/div[2]/div[1]/ul[2]/li[6]',
        6: '/html/body/div/div[2]/div[1]/ul[2]/li[7]',
        7: '/html/body/div/div[2]/div[1]/ul[2]/li[8]',
        8: '/html/body/div/div[2]/div[1]/ul[2]/li[9]',
        9: '/html/body/div/div[2]/div[1]/ul[2]/li[10]',
        'plus': '/html/body/div/div[6]/div[1]/div/div/div[2]/div/button[2]',
        'minus': '/html/body/div/div[6]/div[1]/div/div/div[2]/div/button[1]',
        'confirm': '/html/body/div/div[6]/div[1]/div/div/div[4]/button[2]',
        'cancel': '/html/body/div/div[6]/div[1]/div/div/div[4]/button[1]',
    }
    
    element = driver.find_element(By.XPATH, buttons[num])
    element.click()
    time.sleep(2)

    element = driver.find_element(By.XPATH, buttons['confirm'])
    element.click()
    time.sleep(2)

def checkQuality(values):
    aa, bb, cc, dd = values
    global sapre_wins, sapre_loss, parity_wins, parity_loss, bcone_wins, bcone_loss, emerd_wins, emerd_loss
    print("quality func running....")
    df = pd.read_csv("bets.csv")
    a, b, c, d = df['sapre'].to_list()[-1], df['parity'].to_list()[-1], df['bcone'].to_list()[-1], df['emerd'].to_list()[-1]

    if a == aa:
        print("sapre won....")
        sapre_wins += 1
    else:
        print("sapre lost")
        sapre_loss += 1

    if b == bb:
        print("parity won....")
        parity_wins += 1
    else:
        print("parity lost")
        parity_loss += 1

    if c == cc:
        print("bcone won....")
        bcone_wins += 1
    else:
        print("bcone lost")
        bcone_loss += 1

    if d == dd:
        print("emerd won....")
        emerd_wins += 1
    else:
        print("emerd lost")
        emerd_loss += 1
    print([sapre_wins, sapre_loss], [parity_wins, parity_loss], [bcone_wins, bcone_loss], [emerd_wins, emerd_loss])
    return [[sapre_wins, sapre_loss], [parity_wins, parity_loss], [bcone_wins, bcone_loss], [emerd_wins, emerd_loss]]


def scrapToCsv(file_name, soup):

    # Find the table element by class, ID, or other attributes
    tables = soup.find_all('table')

    table = tables[1]

    rows = table.find_all('tr')

    with open("live_data/" + file_name, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        ls1 = []
        for row in rows:
            cells = row.find_all('td')
            ls = []
            for cell in cells:
                ls.append((cell.text).replace("\n", "").strip())
            # print(ls)
            ls1.append(ls)
        writer.writerow(ls1[2])
    
    with open("data/" + file_name, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        ls1 = []
        for row in rows:
            cells = row.find_all('td')
            ls = []
            for cell in cells:
                ls.append((cell.text).replace("\n", "").strip())
            # print(ls)
            ls1.append(ls)
        writer.writerow(ls1[2])

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

def main():
    global amount
    # Load the model
    model_sapre = tf.keras.models.load_model('model_sapre.h5')
    model_parity = tf.keras.models.load_model('model_parity.h5')
    model_emerd = tf.keras.models.load_model('model_emerd.h5')
    model_bcone = tf.keras.models.load_model('model_bcone.h5')

    print("\n\n\n program is running....")
    
    refresh = '/html/body/div/div[1]/div/div/div[2]'
    element = driver.find_element(By.XPATH, refresh)
    element.click()
    time.sleep(2)

    sapre_tab = '/html/body/div/div[2]/ul/li[1]'
    parity_tab = '/html/body/div/div[2]/ul/li[2]'
    bcone_tab = '/html/body/div/div[2]/ul/li[3]'
    emerd_tab = '/html/body/div/div[2]/ul/li[4]'

    tabs = [sapre_tab, parity_tab, bcone_tab, emerd_tab]
    models = [model_sapre, model_parity, model_bcone, model_emerd]
    names = ['sapre', 'parity', 'bcone', 'emerd']

    # for tab in tabs:
    #     # bet_on(tab, 1)
    #     print(tab)
    #     time.sleep(5)
    ls = []
    last_values = []
    for i in range(4):
        ##########################################################
        element = driver.find_element(By.XPATH, tabs[i])
        element.click()
        time.sleep(4)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        scrapToCsv(names[i] + ".csv" ,soup)
        ##########################################################

        # # Prepare input data
        seq_length = 14
        input_sequence = generate_sequence(names[i] + ".csv")
        print(f"input sequence for {names[i]}: ", input_sequence)
        last_values.append(input_sequence[-1])

        input_sequence = np.array([input_sequence])
        input_sequence = np.reshape(input_sequence, (input_sequence.shape[0], input_sequence.shape[1], 1))

        # Make a prediction
        model = models[i]
        predicted_probabilities = model.predict(input_sequence)[0]
        predicted_class = np.argmax(predicted_probabilities)

        # Get the predicted number
        predicted_number = predicted_class

        print(f"Predicted number for {names[i]}: {predicted_number}")
        ls.append(predicted_number)

        # if i != -1:
        #     bet_on(predicted_number)

    right_wrongs = checkQuality(last_values)
    amount += sum( [(right*85.5 - (right + wrong)*10) for right, wrong in right_wrongs] )
    print("balance:", amount)
    with open("bets.csv", "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ls)
    

# Launch the web browser
driver = webdriver.Chrome()  # Change this to the appropriate web driver

# Open the web page
driver.get('https://vespa.games/#/')
time.sleep(3)

sapre_wins = 0
parity_wins = 0
bcone_wins = 0
emerd_wins = 0

sapre_loss = -1
parity_loss = -1
bcone_loss = -1
emerd_loss = -1

amount = 1000

login(driver, "8824655613", "Sarvesh@2000")


scheduled_times = []

for i in range(24):
    for j in range(0, 60, 3):
        scheduled_times.append([i, j])

print( len(scheduled_times))

scheduler = BlockingScheduler()
for i in range(len(scheduled_times)):
    scheduler.add_job(main, 'cron', hour=scheduled_times[i][0], minute=scheduled_times[i][1], second=15)  # Set the time for execution
scheduler.start()

# main()


# if __name__ == '__main__':
#     main()

# checkQuality(1,1,1,1)