#!/usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import time
from os import path

def download_page(URL):
    headers = {"User-Agent":
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
    cookies = {'auchanCook': '874|'}
    response = requests.get(URL, cookies=cookies, headers=headers)
    if (response.status_code != 200):
        print("[DEBUG] URL:", URL, "->", response, "[DEBUG]")
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def read_file(file):
    file = open(file, "r").read()
    return file.split("\n")

def get_product(category, file):   
    index = 0
    while 1:
        page = download_page(category + str(index))
        if not 'body' in str(page):
            break
        file.write("https://www.auchandrive.fr" + page.a.get('href'))
        file.write('\n')
        index = index + 1
        time.sleep(3)
    return 0

def main():
    file = open("url.txt", "a")
    category_id = read_file('id.txt')
    for i in range(len(category_id)):
        print("Category ID:", category_id[i])
        category_id[i] = "https://www.auchandrive.fr/update-catalog/?categories=" + category_id[i] + "&startIndex="
        get_product(category_id[i], file)
    return 0

if not(path.exists("id.txt")):
    print("Need id.txt")
    exit()

if __name__ == "__main__":
    main()


