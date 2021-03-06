import re
import json
import requests
from bs4 import BeautifulSoup

#--personal loan scraper--
#setting webpage to scrap from using beautiful soup and empty array to receive all data and bank_list setup
personal_loan_page = requests.get('https://ringgitplus.com/en/personal-loan/')
personal_soup = BeautifulSoup(personal_loan_page.text, 'html.parser')
data_object=[]
bank_list=['affinbank', 'alliance', 'ambank', 'bankislam', 'bankrakyat', 'bsn', 'cimb', 'citibank', 'hongleong', 'hsbc', 'maybank', 'ocbc', 'public', 'rhb', 'standardchartered', 'uob']

#setting loop to cycle through website's loan and storing into empty array data_object
personal_loans = personal_soup.find_all('tr', class_="featured")
personal_loan_list=[]
for i, personal_loan in enumerate(personal_loans):
    bank_name = 'none'
    package_name = personal_loan.get('data-name')
    bank_name = package_name.lower().split()[0]
    if bank_name == "bank":
        bank_name = package_name.lower().split()[0] + package_name.lower().split()[1]
    elif bank_name in bank_list:
        bank_name = bank_name
    package_tag = 'personal'
    interest_rate = float(personal_loan.find('span', class_='data interest-rate').get_text())
    try:
        repayment = float(personal_loan.find('span', class_='data monthly-repayment').get_text())
    except:
        print('repayment not available')
    else:
        print(i, repayment)
        webpage = 'https://ringgitplus.com'
        apply_link = personal_loan.find('a').get('href')
        link = webpage + apply_link
        personal_loan_data = {"bank_name": bank_name, "package_name": package_name,"package_tag":package_tag, "interest_rate": interest_rate, "repayment": repayment, "link":link}
        personal_loan_list.append(personal_loan_data)

#--business loan scraper--
#setting webpage to scrap from using beautiful soup
business_loan_page = requests.get('https://ringgitplus.com/en/business-loan/')
business_soup = BeautifulSoup(business_loan_page.text, 'html.parser')

#setting loop to cycle through website's loan and storing into empty array data_object
business_loans = business_soup.find_all('tr', class_='loan')
business_loan_list = []
for business_loan in business_loans:
    bank_name = 'none'
    package_name = business_loan.get('data-name')
    bank_name = package_name.lower().split()[0]
    if bank_name == "bank":
        bank_name = package_name.lower().split()[0] + package_name.lower().split()[1]
    elif bank_name in bank_list:
        bank_name = bank_name
    package_tag = 'business'
    interest_rate = business_loan.find('span', class_='data interest-rate').get_text()
    if interest_rate == "":
        interest_rate = 0.00
    interest_rate = float(interest_rate)
    repayment = business_loan.find('span', class_='data monthly-repayment').get_text()
    try:
        repayment = float(personal_loan.find('span', class_='data monthly-repayment').get_text())
    except:
        print('repayment not available')
    else:
        print(i, repayment)
        webpage = 'https://ringgitplus.com'
        apply_link = business_loan.find('a').get('href')
        link = webpage + apply_link
        business_loan_data = {"bank_name": bank_name, "package_name": package_name, "package_tag": package_tag, "interest_rate": interest_rate, "repayment": repayment, "link":link}
        business_loan_list.append(business_loan_data)

#--car loan scraper--
#setting webpage to scrap from using beautiful soup
car_loan_page = requests.get('https://www.imoney.my/car-loan')
car_soup = BeautifulSoup(car_loan_page.text, 'html.parser')

#setting loop to cycle through website's loan and storing into empty array data_object
car_loans = car_soup.find_all('div', class_="columns list-item__info is-mobile is-multiline has-text-centered-mobile")
car_loan_list = []
for car_loan in car_loans:
    bank_name = 'none'
    package_name = car_loan.find('a').get_text()
    bank_name = package_name.lower().split()[0]
    if bank_name == "bank":
        bank_name = package_name.lower().split()[0] + package_name.lower().split()[1]
    elif bank_name in bank_list:
        bank_name = bank_name
    package_tag = 'car'
    interest_rate = car_loan.find_all('b')[0].get_text()
    for i in interest_rate:
        if i in "%":
            interest_rate = re.sub('%','', interest_rate)
    interest_rate = float(interest_rate)
    repayment = car_loan.find_all('b')[1].get_text()
    for i in repayment:
        if i in 'RM':
            repayment = re.sub('RM','', repayment)
    for i in repayment:
        if i in ' ':
            repayment = re.sub(' ','', repayment)
    repayment = float(repayment)
    apply_link = car_loan.find('a').get('href')
    car_loan_data = {"bank_name": bank_name, "package_name": package_name, "package_tag": package_tag, "interest_rate": interest_rate, "repayment": repayment, "link":apply_link}
    car_loan_list.append(car_loan_data)

#--home loan scraper--
#setting webpage to scrap from using beautiful soup
home_loan_page= requests.get('https://www.imoney.my/home-loan')
home_soup = BeautifulSoup(home_loan_page.text, 'html.parser')

#setting loop to cycle through website's loan and storing into empty array data_object
home_loans = home_soup.find_all('div', class_="table__product")
home_loan_list = []
for home_loan in home_loans:
    bank_name = 'none'
    package_name = home_loan.find_all('a')[2].get('data-value')
    bank_name = package_name.lower().split()[0]
    if bank_name == "bank":
        bank_name = package_name.lower().split()[0] + package_name.lower().split()[1]
    elif bank_name in bank_list:
        bank_name = bank_name
    package_tag = 'home'
    interest_rate = home_loan.find_all('span', class_='col-rate--item')[0].get_text()
    for i in interest_rate:
        if i in "%":
            interest_rate = re.sub('%','', interest_rate)
    interest_rate = float(interest_rate)
    repayment = home_loan.find_all('span', class_='col-rate--item')[2].get_text()
    for i in repayment:
        if i in 'RM':
            repayment = re.sub('RM','', repayment)
    for i in repayment:
        if i in ',':
            repayment = re.sub(',','',repayment)
    repayment = float(repayment)
    webpage = 'https://www.imoney.my'
    apply_link = home_loan.find('a').get('href')
    link = webpage + apply_link
    home_loan_data = {"bank_name": bank_name, "package_name": package_name, "package_tag": package_tag, "interest_rate": interest_rate, "repayment": repayment, "link":link}
    home_loan_list.append(home_loan_data)

#saving top 3 results from each list into the data_object for the data.json
data_object.append(personal_loan_list[0])
data_object.append(personal_loan_list[1])
data_object.append(personal_loan_list[2])
data_object.append(business_loan_list[0])
data_object.append(business_loan_list[1])
data_object.append(business_loan_list[2])
data_object.append(car_loan_list[0])
data_object.append(car_loan_list[1])
data_object.append(car_loan_list[2])
data_object.append(home_loan_list[0])
data_object.append(home_loan_list[1])
data_object.append(home_loan_list[2])

#using json module to save data_object into a json file
with open('data.json', 'w') as outfile:
    json.dump(data_object, outfile, indent=4)

print(data_object)
