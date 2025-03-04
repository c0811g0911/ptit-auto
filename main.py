#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import platform
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from utilities import load_driver
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
import random



def login(driver, web_url,u, p):
    driver.get(web_url)
    time.sleep(.5)
    user = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, 'username')))
    user.send_keys(u)
    password = WebDriverWait(driver, 5).until(ec.visibility_of_element_located((By.ID, 'password')))
    password.send_keys(p)
    time.sleep(.5)
    login = WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.ID, 'loginbtn')))
    login.click()

def is_pass(driver):
    try:
        driver.find_element(by=By.XPATH, value="//div[contains(@class, 'badge rounded-pill alert-success icon-no-margin')]/strong[text()='Hoàn thành:']")
        return True
    except NoSuchElementException:
        return False

def by_pass_dialog(driver):
    try:
        dialog = driver.find_element(By.XPATH, value="//div[@role='dialog']")
        dialog.find_element(By.XPATH, value="//input[@value='Bắt đầu làm bài']").click()
    except NoSuchElementException:
        return



def do_homework(driver):
    print("start do_homework")
    values = ["Thực hiện lại đề thi", "Bắt đầu kiểm tra", "Tiếp tục làm bài"]
    xpath_expression = "//button[" + " or ".join([f"contains(text(), '{value}')" for value in values]) + "]"

    WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.XPATH, xpath_expression))).click()
    time.sleep(.5)
    by_pass_dialog(driver)
    time.sleep(.5)
    
    questions = driver.find_elements(by=By.XPATH, value="//div[starts-with(@id, 'question-')]")    
    for q in questions:
        try:            
            random_value = random.randint(0, 3)
            radio_button = q.find_element(by=By.XPATH, value=f".//input[@type='radio' and @value='{random_value}']")
            radio_button.click()
        except Exception as e:
            print(f"Could not click the radio button in div {q.get_attribute('id')}: {e}")

    time.sleep(.5)
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.XPATH, f"//input[@value='Hoàn thành bài thi...']"))).click()

    time.sleep(.5)

    values = ["Nộp Bài Và Kết Thúc", "Nộp bài và kết thúc"]
    xpath_expression = "//button[" + " or ".join([f"contains(text(), '{value}')" for value in values]) + "]"

    WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.XPATH, xpath_expression))).click()

    time.sleep(.5)
    dialog = driver.find_element(By.XPATH, value="//div[@role='document']")

    xpath_expression = "//button[@data-action='save']"
    submit_button = dialog.find_element(By.XPATH, xpath_expression)
    submit_button.click()


    time.sleep(.5)
    driver.find_element(By.XPATH, value="//a[text()='Dừng xem lại']").click()

if __name__ == '__main__':
    load_dotenv()    
    # Clear screen and instructions on terminal window
    if 'windows' in platform.system().lower():
        os.system('cls')
    else:
        os.system('clear')
    try:
        print('start load driver')
        driver = load_driver()    
        driver.maximize_window()
        print('start login')
        username = os.getenv("username")
        password = os.getenv("password")
        homework_link = os.getenv("homework_link")
        login(driver, homework_link, username, password)
        
        isPass = is_pass(driver)
        while isPass is False:
            do_homework(driver)
            isPass = is_pass(driver)
            print('isPass:', isPass)
    finally:
        driver.close()
    