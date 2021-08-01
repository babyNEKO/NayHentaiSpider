from time import sleep
from lxml import etree
import requests
from sys import platform
from rich import print
from re import findall
from os.path import exists
from os import mkdir
from urllib3 import disable_warnings


class NyaHentai:
    def __init__(self):
        self.download_count = 0
        self.download_delay = 1
        self.main_url = 'https://zha.eehentai.com/g/{}/'
        self.image_url = 'https://zha.eehentai.com/g/{gid}/list/1/'
        self.jpg_url = 'https://i1.mspcdn7.xyz/galleries/{gid}/{image_number}.jpg'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        }

    def get_images_id(self, gid):
        disable_warnings()
        response = requests.get(url=self.image_url.format(gid=gid), headers=self.headers)
        response.encoding = 'utf-8'
        e = etree.HTML(response.text)
        images_id = e.xpath('//*[@id="image-container"]/a/img/@src')[0]
        images_id = images_id.replace('https://i1.mspcdn7.xyz/galleries/', '').replace('/1.jpg', '')
        return images_id

    def spider(self, gid=None):
        images_id = self.get_images_id(gid=gid)
        if gid is None:
            print('[bold red]缺少关键参数：Gallery ID[/bold red]')
            exit(0)
        disable_warnings()
        response = requests.get(url=self.main_url.format(str(gid)), headers=self.headers)
        response.encoding = 'utf-8'
        e = etree.HTML(response.text)
        gallery_total_image = e.xpath('//*[@id="info"]/div[1]/text()')[0]
        gallery_total_image_number = findall(r'\d+', gallery_total_image)[0]
        gallery_title = e.xpath('//*[@id="info"]/h1/text()')[0]
        gallery_author = e.xpath('//*[@id="tags"]/div[2]//a/text()')[0]
        print('页数：' + str(findall(r'\d+', gallery_total_image)[0]))
        print('标题：' + gallery_title)
        print('作者：' + gallery_author)

        if not exists('.\\' + gallery_title.replace(' ', '') + '\\'):
            mkdir('.\\' + gallery_title.replace(' ', '') + '\\')
            with open('.\\' + gallery_title.replace(' ', '') + '\\' + 'info.txt', 'w') as save_info:
                save_info.writelines('URL - ' + response.url + '\n')
                save_info.writelines('标题 - ' + gallery_title + '\n')
                save_info.writelines('作者 - ' + gallery_author + '\n')
                save_info.writelines('页数 - ' + gallery_total_image_number)

        for i in range(1, int(gallery_total_image_number), 1):
            sleep(self.download_delay)
            disable_warnings()
            resp = requests.get(url=self.jpg_url.format(gid=str(images_id), image_number=str(i)))
            print(resp.url)
            with open('.\\' + gallery_title.replace(' ', '') + '\\' + str(i) + '.jpg', 'wb') as save_jpg:
                save_jpg.write(resp.content)
            self.download_count += 1
            print('[bold green]已下载' + str(self.download_count) + '张[/bold green]')
        print('[bold green]All Done.[/bold green]')


if __name__ == '__main__':
    try:
        assert ('win' in platform), 'only windows platform'.title()
        NyaHentai().spider(gid=252771)
    except AssertionError as AE:
        print(AE)
    except KeyboardInterrupt as KI:
        print(KI)
        exit(0)
