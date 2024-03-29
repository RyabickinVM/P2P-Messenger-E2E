import os
import time

import pyautogui
import pytest
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_chat_text_message(driver):
    driver.get("http://localhost:3000/login")

    register_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Регистрация')]")
    register_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/login"))
    assert "http://localhost:3000/registration" in driver.current_url

    email = driver.find_element(By.NAME, "email")
    username = driver.find_element(By.NAME, "uname")
    password = driver.find_element(By.NAME, "psw")
    email.send_keys("testuser1@yandex.com")
    username.send_keys("first1")
    password.send_keys("first1!")

    register_submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]")
    register_submit_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/registration"))
    assert "http://localhost:3000/home" in driver.current_url

    room_name_str = "First Room"
    room_name = driver.find_element(By.XPATH, "//div[@class='css-96r7gq']//input[@id='messageText']")
    room_name.send_keys(room_name_str)

    create_room_button = driver.find_element(By.XPATH, "//button[@class='css-1hy3zlq']")
    create_room_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/home"))
    assert f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}' in driver.current_url

    time.sleep(1)
    message_str = "1234lox"
    message_field = driver.find_element(By.XPATH, "//input[@id='messageText']")
    message_field.send_keys(message_str)

    message_send_button = driver.find_element(By.XPATH, "//button[@class='css-17iq27n']")
    message_send_button.click()
    time.sleep(1)

    home_button = driver.find_element(By.XPATH, "//a[contains(text(),'Домашняя страница')]")
    home_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}'))
    assert "http://localhost:3000/home" in driver.current_url
    time.sleep(2)

    room_buttom = driver.find_element(By.XPATH, "//div[@id='First Room']")
    room_buttom.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/home"))
    assert f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}' in driver.current_url
    time.sleep(1)

    user_in_list = driver.find_element(By.XPATH, "//*[contains(text(), 'first1')]")
    assert user_in_list.is_displayed()
    message_in_history = driver.find_element(By.XPATH, "//*[contains(text(), '1234lox')]")
    assert message_in_history.is_displayed()
    time.sleep(1)

    logout_button = driver.find_element(By.XPATH, "//a[contains(text(),'Выйти из системы')]")
    logout_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}'))
    assert "http://localhost:3000/login" in driver.current_url


def test_chat_media_file(driver):
    driver.get("http://localhost:3000/login")

    register_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Регистрация')]")
    register_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/login"))
    assert "http://localhost:3000/registration" in driver.current_url

    email = driver.find_element(By.NAME, "email")
    username = driver.find_element(By.NAME, "uname")
    password = driver.find_element(By.NAME, "psw")
    email.send_keys("testuser2@yandex.com")
    username.send_keys("second2")
    password.send_keys("second2!")

    register_submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]")
    register_submit_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/registration"))
    assert "http://localhost:3000/home" in driver.current_url

    room_name_str = "Second Room"
    room_name = driver.find_element(By.XPATH, "//div[@class='css-96r7gq']//input[@id='messageText']")
    room_name.send_keys(room_name_str)

    create_room_button = driver.find_element(By.XPATH, "//button[@class='css-1hy3zlq']")
    create_room_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/home"))
    assert f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}' in driver.current_url
    time.sleep(1)

    upload_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..", "selenium_mediafile.png"))
    media_file_attach = driver.find_element(By.XPATH, "//button[@class='css-p14d8s']")
    media_file_attach.click()
    time.sleep(1)

    pyautogui.write(upload_file)
    pyautogui.press('enter')
    time.sleep(1)

    message_send_button = driver.find_element(By.XPATH, "//button[@class='css-17iq27n']")
    message_send_button.click()
    time.sleep(5)

    home_button = driver.find_element(By.XPATH, "//a[contains(text(),'Домашняя страница')]")
    home_button.click()
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.url_changes(f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}'))
    assert "http://localhost:3000/home" in driver.current_url
    time.sleep(1)

    room_buttom = driver.find_element(By.XPATH, "//div[@id='Second Room']")
    room_buttom.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/home"))
    assert f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}' in driver.current_url
    time.sleep(1)

    user_in_list = driver.find_element(By.XPATH, "//*[contains(text(), 'second2')]")
    assert user_in_list.is_displayed()
    media_in_history = driver.find_element(By.XPATH, "//img[@alt='uploaded file']")
    assert media_in_history.is_displayed()
    time.sleep(1)

    logout_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Выйти из системы')]")
    logout_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}'))
    assert "http://localhost:3000/login" in driver.current_url


def test_chat_text_message_and_media_file(driver):
    driver.get("http://localhost:3000/login")

    register_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Регистрация')]")
    register_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/login"))
    assert "http://localhost:3000/registration" in driver.current_url

    email = driver.find_element(By.NAME, "email")
    username = driver.find_element(By.NAME, "uname")
    password = driver.find_element(By.NAME, "psw")
    email.send_keys("testuser3@yandex.com")
    username.send_keys("third3")
    password.send_keys("second3!")

    register_submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Зарегистрироваться')]")
    register_submit_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/registration"))
    assert "http://localhost:3000/home" in driver.current_url

    room_name_str = "Third Room"
    room_name = driver.find_element(By.XPATH, "//div[@class='css-96r7gq']//input[@id='messageText']")
    room_name.send_keys(room_name_str)

    create_room_button = driver.find_element(By.XPATH, "//button[@class='css-1hy3zlq']")
    create_room_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/home"))
    assert f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}' in driver.current_url
    time.sleep(1)

    message_str = "4321xol"
    message_field = driver.find_element(By.XPATH, "//input[@id='messageText']")
    message_field.send_keys(message_str)
    time.sleep(1)

    upload_file = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..", "selenium_mediafile.png"))
    media_file_attach = driver.find_element(By.XPATH, "//button[@class='css-p14d8s']")
    media_file_attach.click()
    time.sleep(1)

    pyautogui.write(upload_file)
    pyautogui.press('enter')
    time.sleep(1)

    message_send_button = driver.find_element(By.XPATH, "//button[@class='css-17iq27n']")
    message_send_button.click()
    time.sleep(5)

    home_button = driver.find_element(By.XPATH, "//a[contains(text(),'Домашняя страница')]")
    home_button.click()
    time.sleep(1)

    WebDriverWait(driver, 10).until(EC.url_changes(f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}'))
    assert "http://localhost:3000/home" in driver.current_url
    time.sleep(1)

    room_buttom = driver.find_element(By.XPATH, "//div[@id='Second Room']")
    room_buttom.click()

    WebDriverWait(driver, 10).until(EC.url_changes("http://localhost:3000/home"))
    assert f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}' in driver.current_url
    time.sleep(1)

    user_in_list = driver.find_element(By.XPATH, "//*[contains(text(), 'second2')]")
    assert user_in_list.is_displayed()
    media_in_history = driver.find_element(By.XPATH, "//img[@alt='uploaded file']")
    assert media_in_history.is_displayed()
    time.sleep(1)

    logout_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Выйти из системы')]")
    logout_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(f'http://localhost:3000/dashboard/{room_name_str.replace(" ", "%20")}'))
    assert "http://localhost:3000/login" in driver.current_url