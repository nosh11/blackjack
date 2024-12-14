import time
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup

output_folder = Path('いらすとや')
output_folder.mkdir(exist_ok=True)

url = "https://www.irasutoya.com/search?q=%E3%83%88%E3%83%A9%E3%83%B3%E3%83%97+%E7%B5%B5%E6%9C%AD"
linklist = []

html = requests.get(url).text
# ②-②.検索結果ページのオブジェクトを作成
soup = BeautifulSoup(html, 'lxml')
# ②-③.画像リンクのタグをすべて取得
a_list =soup.select('div.boxmeta.clearfix > h2 > a')
# ②-④.画像リンクを1つずつ取り出す
for a in a_list:
# ②-⑤.画像ページのURLを抽出
    link_url = a.attrs['href']
# ②-⑥.画像ページのURLをリストに追加
    linklist.append(link_url)
    time.sleep(1.0)
    
# ●各画像ページから画像ファイルのURLを特定  
# ③-①.画像ページのURLを1つずつ取り出す
for page_url in linklist:
# ③-②.画像ページのhtmlを取得
    page_html = requests.get(page_url).text
# ③-③.画像ページのオブジェクトを作成
    page_soup = BeautifulSoup(page_html, "lxml")
# ③-④.画像ファイルのタグをすべて取得
    img_list = page_soup.select('div.entry > div > a > img')
# ③-⑤.imgタグを1つずつ取り出す
    for img in img_list:
# ③-⑥.画像ファイルのURLを抽出
        img_url = (img.attrs['src'])
# ③-⑦.画像ファイルの名前を抽出
        filename = re.search(".*\/(.*png|.*jpg)$",img_url)
# ③-⑧.保存先のファイルパスを生成
        save_path = output_folder.joinpath(filename.group(1))
        time.sleep(1.0)
# ●画像ファイルのURLからデータをダウンロード
        try:
# ④-①.画像ファイルのURLからデータを取得
            image = requests.get(img_url)
            open(save_path, 'wb').write(image.content)
            print(save_path)
            time.sleep(1.0)
        except ValueError:
            print("ValueError!")