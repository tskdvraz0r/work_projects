def download_data(start: int, stop: int) -> None:
    #by ts.kdv.raz0r >)
    
    import datetime
    import os
    import random
    import time

    import pandas as pd
    import requests
    from fake_useragent import UserAgent
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys

    # settings
    chrome_driver_path: str = 'path_to_driver/chromedriver'
    login_url: str = 'https://some_books_site.ru/login'
    download_path: str = 'path_to_folder/imgs'
    
    prefs = {'download.default_directory' : f'{download_path}'}

    web_driver_options = webdriver.ChromeOptions()
    web_driver_options.add_argument('--headless')
    web_driver_options.add_experimental_option('prefs', prefs)
    web_driver_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        executable_path = chrome_driver_path,
        options = web_driver_options
    )

    # Get
    driver.get(url = login_url)
    
    time.sleep(1)


    # Enter login
    login_input = driver.find_element(by = By.ID, value = 'login')
    login_input.clear()
    login_input.send_keys('some_login')  # enter your login

    time.sleep(1)


    # Enter password
    password_input = driver.find_element(by = By.ID, value = 'password')
    password_input.clear()
    password_input.send_keys('some_password')  # enter your password

    time.sleep(1)


    # Pressing "ENTER"
    press_enter = password_input = driver.find_element(by = By.ID, value = 'password').send_keys(Keys.ENTER)

    time.sleep(1)


    books_info: dict = {
        'Издательство' : [],
        'Полное название' : [],
        'Год издания' : [],
        'Класс' : [],
        'Цена' : [],
        'УМК' : [],
        'Уникальный код' : [],
        'Код по ФП' : [],
        'Изображение' : []
    }

    lst_headers: list[str] = ['Издательство', 'Полное название', 'Год издания', 'Класс', 'Цена', 'УМК', 'Уникальный код', 'Код по ФП']
    #page_not_found = []


    for i in range(start, stop):  # 21339
    
        #fake_user_agent = UserAgent(random)
        #web_driver_options.add_argument(f'user-agent = {fake_user_agent}')
    
        print(f'{datetime.datetime.now()} opened page-{i}: https://some_books_site.ru/catalog/{i}! {21339 - i} remain!')
        driver.get(url = f'https://some_books_site.ru/catalog/{i}')
        time.sleep(random.randrange(5, 10))
        
        page_headers = [i.text[:-1] for i in driver.find_elements(by = By.CLASS_NAME, value = 'kz-catalog-item__prop-key')]
        page_values = [i.text for i in driver.find_elements(by = By.CLASS_NAME, value = 'kz-catalog-item__prop-value')]
    
        for j in range(len(page_headers)):
            try:
                books_info[page_headers[j]].append(page_values[j])
            
            except KeyError:
                continue
            
        try:
            os.chdir(download_path)
            img = driver.find_element(by = By.XPATH, value = '//div[@class="kz-catalog-item__med-image"]/img').get_attribute('src')
            p = requests.get(img)

            out = open(f'{i}.jpg', 'wb')
            out.write(p.content)
            out.close()
        
            books_info['Изображение'].append(f'{i}.jpg')
    
        except Exception as ex:
            books_info['Изображение'].append(f'{i} - НЕТ ИЗОБРАЖЕНИЯ!')
        
        for header in lst_headers:
            if header == 'Описание':
                continue

            if header not in page_headers:
                books_info[header].append('НЕТ ДАННЫХ')
    
        os.chdir('path_to_folder/data')
    
        df_books = pd.DataFrame(books_info)
        df_books.to_csv(f'{start} - {stop}.csv', index = True, header = True)