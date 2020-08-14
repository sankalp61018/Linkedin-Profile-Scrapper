import csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from getpass import getpass


username = input('Enter your linkedin username ')
password = getpass('Enter your linkedin password ')


job_profile = input('Enter required Job_profile ')
location = input('Enter required Location/Organization ')


query = 'site:linkedin.com/in/ AND "'+job_profile+'" AND "'+location+'"'
required_count = int(input('Enter the number of Profiles Required (between 1 to 300) '))
if(required_count>300 or required_count<1):
    print("Required number of profiles is out of range")
    exit()


connection_request= False
c=input('Enter Y if you want to send connection request to all profiles else enter N. [Y/N] ')
if(c=='Y' or c=='y'):
    connection_request = True
elif(c=='N' or c=='n'):
    connection_request = False
else:
    exit()


output_file = input('Enter name of your output file ')
output_file=output_file+'.csv'
writer = csv.writer(open(output_file, 'w'))
writer.writerow(['Name', 'Job_title', 'Schools', 'Location', 'Image_url', 'Linkedin_url'])


# Enter correct location of chromedriver.exe 
driver = webdriver.Chrome('/webdrivers/chromedriver.exe')


# To open linkedin.com
driver.get('https://www.linkedin.com/')
sleep(2)


# To click on Sign in button
driver.find_element_by_xpath('//a[text()="Sign in"]').click()
sleep(2)


# Finding username input bar and entering username 
username_input = driver.find_element_by_name('session_key')
username_input.send_keys(username)
sleep(1)


# Finding password input bar and entering password 
password_input = driver.find_element_by_name('session_password')
password_input.send_keys(password)
sleep(1)


# To click on the sign in button
driver.find_element_by_xpath('//button[text()="Sign in"]').click()
sleep(3)


# To open google.com
driver.get('https://www.google.com/')
sleep(2)


#Finding search bar and entring query
google_search = driver.find_element_by_name('q')
google_search.send_keys(query)
sleep(1)
google_search.send_keys(Keys.RETURN)
sleep(2)
google_search_url=driver.current_url
count=0


# A boolean variable to check if username or password are invalid
Isvalid = False


while 1:
    #Getting list of all profiles of current page
    profiles = driver.find_elements_by_xpath('//*[@class="r"]/a[1]')
    profiles = [profile.get_attribute('href') for profile in profiles]

    
    for profile in profiles:
        driver.get(profile)
        sleep(2)

        sel = Selector(text=driver.page_source)


        # To check if provided username or password is invalid
        if Isvalid == False:
            if(len(sel.xpath('//*[text()="Sign in"]'))>0):
                print("Provided username or password is invalid")
                driver.quit()
                exit()
            else:
                Isvalid=True


        # To move on next profile if current profile is unavilable
        if len(sel.xpath('//div[@class="profile-unavailable"]').extract())>0:
            continue


        #To increase profile count 
        count+=1


        # To Scrape all required information of current profile
        name = sel.xpath('//title/text()').extract_first().split(' | ')[0]
        if name[0]=='(':
            name = name.split(')')[1].strip()
        job_title = sel.xpath('//h2[@class="mt1 t-18 t-black t-normal break-words"]/text()').extract_first().strip()
        schools = ', '.join(sel.xpath('//*[contains(@class, "pv-entity__school-name")]/text()').extract())
        location = sel.xpath('//*[@class="t-16 t-black t-normal inline-block"]/text()').extract_first().strip()
        image_url=sel.xpath('//img[@title="'+name+'"]/@src').extract_first()
        ln_url = driver.current_url


        # To Print all informations
        print('\n')
        print(name)
        print(job_title)
        print(schools)
        print(location)
        print(ln_url)
        print(image_url)
        print('\n')
        

        # To send connection request if required
        if connection_request==True:
            try:
                driver.find_element_by_xpath('//*[text()="More…"]').click()
                sleep(1)

                driver.find_element_by_xpath('//*[text()="Connect"]').click()
                sleep(1)

                driver.find_element_by_xpath('//*[text()="Send now"]').click()
                sleep(1)
            except:
                pass


        # To add information of current profile to output file
        writer.writerow([name, job_title, schools, location, image_url, ln_url])


        if count==required_count:
            break

    if count==required_count:
        break


    # To open next page
    driver.get(google_search_url)
    next_page = driver.find_elements_by_xpath('//span[text()="Next"]')
    if len(next_page)>0:
        next_page[0].click()
        sleep(2)
        google_search_url=driver.current_url
    else:
        print('Required number of profiles are not avilable')
        break


driver.quit()
