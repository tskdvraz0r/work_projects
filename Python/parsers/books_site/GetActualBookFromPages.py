def get_actual_books():
    #by ts.kdv.raz0r >)
    
    import time

    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    
    # settings
    chrome_driver_path: str = 'path_to_driver_on_your_pc/chromedriver'
    login_url: str = 'https://certain_book_site.ru/login'

    web_driver_options = webdriver.ChromeOptions()
    web_driver_options.add_argument('--headless')
    web_driver_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(
        executable_path = chrome_driver_path,
        options = web_driver_options
    )
    
    # Get
    driver.get(url = login_url)

    # Enter login
    login_input = driver.find_element(by = By.ID, value = 'login')
    login_input.clear()
    login_input.send_keys('enter_your_login')
    print('Login entered successfully')

    driver.implicitly_wait(1)

    # Enter password
    password_input = driver.find_element(by = By.ID, value = 'password')
    password_input.clear()
    password_input.send_keys('enter_your_password')
    print('Password entered successfully')

    driver.implicitly_wait(1)

    # Pressing "ENTER"
    press_enter = password_input = driver.find_element(by = By.ID, value = 'password').send_keys(Keys.ENTER)
    print('ENTER-key pressed')

    driver.implicitly_wait(1)

    # Change page to "Catalog"
    catalog_url: str = 'https://certain_book_site.ru/catalog'
    driver.get(url = catalog_url)
    print(f'Page 1 was opened!')

    time.sleep(5)

    lst_good_links: list[str] = []
    lst_bad_links: list[str] = [
        'index',
        'cart',
        'order',
        'messages',
        'profile',
        'inventory',
        'purchases',
        'catalog',
        'news',
        'fpu',
        'docs',
        'contacts',
        'instructions',
        'service-agreement'
    ]

    # 1st page
    book_links_on_page = driver.find_elements(by = By.TAG_NAME , value = 'a')

    for book_link in book_links_on_page:
        if book_link.get_attribute('href').split('/')[-1] not in lst_bad_links:
            lst_good_links.append(book_link.get_attribute('href'))
            print(f"link: {book_link.get_attribute('href')} added to list")

    # 2nd page
    driver.find_element(by = By.XPATH, value = '/html/body/app-root/kz-page/kz-body/main/div/app-catalog/kz-section/div/div/div/div/div[2]/div/kz-lockable/div/div/div/kz-pagination[1]/div/div/div[6]/kz-btn/button').click()
    print(f'Page 2 was opened!')

    time.sleep(5)

    book_links_on_page = driver.find_elements(by = By.TAG_NAME , value = 'a')

    for book_link in book_links_on_page:
        if book_link.get_attribute('href') not in lst_bad_links:
            lst_good_links.append(book_link.get_attribute('href'))
            print(f"link: {book_link.get_attribute('href')} added to list")

    # Pages 3-788
    for i in range(3, 789):
        next_page_path: str = str('/html/body/app-root/kz-page/kz-body/main/div/app-catalog/kz-section/div/div/div/div/div[2]/div/kz-lockable/div/div/div/kz-pagination[1]/div/div/div[8]/kz-btn/button')

        driver.find_element(by = By.XPATH, value = next_page_path).click()
        print(f'Page {i} was opened!')
        time.sleep(2.5)

        book_links_on_page = driver.find_elements(by = By.TAG_NAME , value = 'a')
  
        for book_link in book_links_on_page:
            if book_link.get_attribute('href') not in lst_bad_links:
                lst_good_links.append(book_link.get_attribute('href'))
                print(f"link: {book_link.get_attribute('href')} added to list")

        #time.sleep(5)

    # Save dataframe
    df = pd.DataFrame(lst_good_links)
    df.to_csv('pages 1-788.csv', index = False, header = False)