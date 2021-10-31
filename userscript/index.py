from selenium import webdriver
from selenium.webdriver.common.keys import Keys
##from password import username
#from password import password
import time
import string
import random
import csv

grouptitle=''
grouptags=''
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def pwd_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def csv_randrow():
    global grouptitle
    global grouptags
    r =random.randint(1,910)
    print(r)
    with open('oftd.csv', newline='') as f:
        reader = csv.reader(f)
        i=0
        for row in reader:
            if r == i:
                print('this row')
                grouptitle=row[0]
                grouptags=row[1]
                #groupname = '"'+groupname+'"'
                #grouptags = '"'+grouptags+'"'
                print(grouptitle)
                print(grouptags)
            i=i+1

driver = webdriver.Firefox()
driver.get("http://localhost:3000")
time.sleep(5)

#DELETE FROM users WHERE username = 'admin'
while True:
    signup_button = driver.find_elements_by_xpath('/html/body/div/div/div/nav/div/ul[2]/li[2]/a')[0]
    signup_button.click()

    #time.sleep(3)

    #
    #GENERATE USER LOGIN INFO
    #
    name = id_generator(6)
    print(name)

    passwd = pwd_generator(6)
    print(passwd)
    userinfo =name+' , '+passwd+'\n'

    f = open("userdata.txt", "a")
    f.write(userinfo)
    f.close()

    #
    #SIGNUP AS NEW USER
    #
    elem = driver.find_element_by_name("firstName")
    elem.send_keys("ad")

    lname = driver.find_elements_by_name("lastName")[0]
    lname.send_keys("min")

    uname = driver.find_elements_by_name("userName")[0]
    uname.send_keys(name)#AUTO GEN

    email =driver.find_elements_by_name("email")[0]
    email.send_keys("e@e.e")

    pwd = driver.find_elements_by_name("password")[0]
    pwd.send_keys(passwd)#AUTO GEN

    cpwd = driver.find_elements_by_name("confirmPassword")[0]
    cpwd.send_keys(passwd)#AUTO GEN

    signup_button = driver.find_elements_by_xpath('/html/body/div/div/div/section/div/form/button')[0]
    signup_button.click()

    time.sleep(1)#Wait for new user page to load


    #
    #CREATE GROUP FOR NEW USER
    #
    createGroup = driver.find_elements_by_xpath('/html/body/div/div/div/div[3]/div/div[1]/div/div[1]/div/button[1]')[0]
    createGroup.click()

    #
    #GENERATE GROUP DATA
    #
    csv_randrow()
    time.sleep(1)
    #
    #APPEND GENERATED INFO
    #
    groupname = driver.find_element_by_name("groupName")
    print("GT: "+grouptitle)
    groupname.send_keys(grouptitle)#AUTO GEN

    groupdesc = driver.find_element_by_name("groupDescription")
    groupdesc.send_keys(grouptags)#AUTO GEN

    subgroup = driver.find_elements_by_xpath('/html/body/div/div/div/div[3]/div/div[1]/div[1]/div[2]/div[2]/form/button')[0]
    subgroup.click()

    #
    #LOGOUT OF CURRENT USER
    #

    logoutbtn = driver.find_elements_by_xpath('/html/body/div/div/div/div[1]/div/div[2]/button[5]')[0]
    logoutbtn.click()
