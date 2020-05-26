import requests
import argparse
from bs4 import BeautifulSoup

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('arg1', help='niconico channel URL')    # 必須の引数を追加
    args = parser.parse_args()
    list = videolist(args.arg1)

def videolist(channel_url):
    video_url = channel_url + "video"
    video_list = []

    next_link = '?&mode=&sort=f&order=d&type=&page=1'
    while(next_link != "javascript://最後のページです"):
        r = requests.get(video_url+next_link)
        soup = BeautifulSoup(r.text, 'lxml')
        items = soup.select(".item_left > a")
        for i in items:
            video_list.append(i.attrs["href"])
            print(i.attrs["href"])
        next_link = soup.select("li.next > a")[0].attrs["href"]
    return video_list

if __name__ == "__main__":
    main()