#!/usr/local/bin/python3

import requests, sys, time
from bs4 import BeautifulSoup
from os import path

PATH = "https://www.auchandrive.fr/update-catalog/?categories="
headers = {"User-Agent":
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
cookies = {'auchanCook': '874|'}

def download_page(URL):
    retry_count = 5
    while (retry_count > 0):
        response = requests.get(URL, cookies=cookies, headers=headers)
        if (response.status_code != 200):
            print("[DEBUG] URL:", URL, "->", response, "[DEBUG]")
            print("Response code below:")
            print(response.content)
            print("[DEBUG] End of response")
            retry_count -= 1
            time.sleep(3)
            print("Trying ", retry_count, " more times...")
            if (retry_count == 0):
                return None
        else:
            retry_count = 0
            soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def read_file(file):
    file = open(file, "r").read()
    return file.split("\n")

def get_product(category, file):
    index = 0
    while True:
        page = download_page(category + str(index))
        if not 'body' in str(page) and page is not None:
            break
        all_a = page.find_all('a')
        for link in all_a:
            href = link.get('href')
            if not 'catalog' in href:
                print("Not a product: ", href)
            else:
                file.write("https://www.auchandrive.fr" + href)
                file.write('\n')
        index = index + 20
    return 0

def main():
    file = open("url.txt", "a")
    category_id = read_file('id.txt')
    for i in range(len(category_id)):
        print("Category ID: ", category_id[i])
        category_id[i] =  PATH + category_id[i] + "&startIndex="
        get_product(category_id[i], file)
    file.close()
    return 0

if not(path.exists("id.txt")):
    print("Please place id.txt in the same folder as "+sys.argv[0])
    exit()

if __name__ == "__main__":
    main()


