import requests
import urllib.request
import argparse
import chromedriver_binary
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import os
import glob

driver = None

def main():
    # 引数
    parser = argparse.ArgumentParser()
    parser.add_argument('arg1', help='niconico channel URL')  # 必須の引数を追加
    parser.add_argument('-i', help='id')  # 必須の引数を追加
    parser.add_argument('-p', help='password')  # 必須の引数を追加
    args = parser.parse_args()
    channel_url = args.arg1
    nico_id = args.i
    nico_pass = args.p

    # selenium起動
    selenium_init()

    # ニコニコログイン
    driver.get('https://account.nicovideo.jp/login')
    driver.find_element_by_id('input__mailtel').send_keys(nico_id)
    driver.find_element_by_id('input__password').send_keys(nico_pass)
    driver.find_element_by_id('login__submit').click()

    video_urls = videolist(channel_url)

    started = False
    while video_urls:
        url = video_urls.pop()
        video_id = re.search(r"(sm)?[0-9]*$", url).group(0)
        # DL済ならスキップ
        if glob.glob("dl/" + video_id + "*"):
            continue
        driver.get(url)
        # 初回のみhls→httpに手動切替を待つ
        if started is False:
            time.sleep(10)
        title = driver.find_element_by_xpath('//h1').text
        raw_video_url = driver.find_element_by_xpath('//*[@id="MainVideoPlayer"]/video').get_attribute("src")
        filename = "dl/" + video_id + "_" + title + ".mp4"
        urllib.request.urlretrieve(raw_video_url, filename)
        started = True


def videolist(channel_url):
    video_url = channel_url + "/video"
    video_list = []

    next_link = '?&mode=&sort=f&order=d&type=&page=1'
    while True:
        r = requests.get(video_url + next_link)
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.select(".item_left > a")
        for i in items:
            video_list.append(i.attrs["href"])
            print(i.attrs["href"])
        next_link = soup.select("li.next > a")[0].attrs["href"]
        if next_link != "javascript://最後のページです":
            break;
    return video_list


def video_download():
    pass


def selenium_init():
    # Chrome のオプションを設定する
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        'download.default_directory': r'./',
        'profile.default_content_settings.popups': 0,
        'download.prompt_for_download': False,
        'download.directory_upgrade': True,
        'safebrowsing.enabled': True
    })
    # driver = webdriver.Remote(
    #     command_executor='http://localhost:4444/wd/hub',
    #     desired_capabilities=options.to_capabilities(),
    #     options=options,
    # )
    driver = webdriver.Chrome(options=options)


if __name__ == "__main__":
    main()
