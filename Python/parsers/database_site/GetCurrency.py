def download_data(date, path):
    #by ts.kdv.raz0r >)
    
    from datetime import datetime
    import time

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    
    start_time = datetime.datetime.now()
    
    # settings
    cd_path: str = 'path_to_driver/chromedriver'
    login_url: str = 'http://some_database_ip/'
    
    prefs = {'download.default_directory' : f'{path}/{date[6:]}/{date[3:5]}'}

    wd_options = webdriver.ChromeOptions()
    wd_options.add_experimental_option('prefs', prefs)
    wd_options.add_argument('--headless')
    wd_options.add_argument('--disable-gpu')
    
    
    driver = webdriver.Chrome(executable_path = cd_path, options= wd_options)
    
    # Get
    driver.get(url = login_url)

    # Enter login
    login_input = driver.find_element(by = By.NAME, value = 'login')
    login_input.clear()
    login_input.send_keys('enter_your_login')
    print(f'[{datetime.now()}][INFO!] Login entered successfully')
    
    # Enter password
    password_input = driver.find_element(by = By.NAME, value = 'password')
    password_input.clear()
    password_input.send_keys('enter_your_password')
    print(f'[{datetime.now()}][INFO!] Password entered successfully')
    
    # Pressing "ENTER"-button
    driver.find_element(by = By.NAME, value = 'submit').click()
    print(f'[{datetime.now()}][INFO!] Successful login')
    
    # Navigate
    driver.find_element(by = By.CSS_SELECTOR, value = '#ПЛАНФИН').click()
    time.sleep(1)

    currency = driver.find_element(by = By.CSS_SELECTOR, value = '#Заработная_плата').click()
    time.sleep(1)
    
    # Transform date to xpath
    temp_date = f'//*[@id="{date}00001802"]/x'
    
    # ...
    date = driver.find_element(by = By.XPATH, value = temp_date).click()
    time.sleep(5)  # need wait to be opened!
        
    lst_good_links: list[str] = []

    src_href = driver.find_elements(by = By.XPATH , value = '//a[@href]')
        
    for link in src_href:
        if len(link.text) == 56:
            lst_good_links.append(f'//*[@id="{link.text.split()[0]}"]/x/a')

    for i in range(len(lst_good_links)):
        driver.find_element(by = By.XPATH, value = lst_good_links[i]).click()
        print(f'[{datetime.now()}][INFO!] {i} Page was opened')
        time.sleep(1)

        # pages names
        page_name = driver.window_handles

        # switch to download page
        driver.switch_to.window(page_name[1])
        print(f'[{datetime.now()}][INFO!] Page was switched to {page_name[1]}')
        time.sleep(1)

        # press "print" button
        driver.find_element(by = By.XPATH, value = '//*[@id="footer"]/input[10]').click()
        print(f'[{datetime.now()}][INFO!] "PRINT"-button was pressed')
        time.sleep(1)

        # press "inn form" button
        driver.find_element(by = By.XPATH, value = '//*[@id="maxwin"]/tbody/tr[5]/td[1]/x/b').click()
        print(f'[{datetime.now()}][INFO!] "Int-form"-button was pressed')
        time.sleep(1)
        
        # press "OK" to start downloading file
        try:
            driver.find_element(by = By.CLASS_NAME)
            print(f'[{datetime.now()}][INFO!] "ENTER" button pressed')
            time.sleep(1)

        except:
            print(f'[{datetime.now()}][EXCEPTION ERROR!] "ENTER"-button was not pressed')
            time.sleep(8)

        driver.close()
        print(f'[{datetime.now()}][INFO!] Page {page_name[1]} was closed')

        # switch to main page
        driver.switch_to.window(page_name[0])
        print(f'[{datetime.now()}][INFO!] Page was switched to main')
    
        print('')

    finish_time = datetime.now()
    print(f'[{datetime.now()}][INFO!] Spent time: {finish_time - start_time}')
    
    driver.quit()