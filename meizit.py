import requests
import re
import random
import os
import time

main_url = 'https://www.mzitu.com/'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'referer': main_url
}
mzitu_home_response = requests.get(main_url, headers=header)


# print(mzitu_home_response.text)

def category_list():
    category_re = '<li><a title="(.*?)" href="'
    category_list = re.findall(category_re, mzitu_home_response.text)[0:4]
    category_url_list = []
    category_name_list = []
    for category in category_list:
        # os.makedirs(f'mzitu/{category}')
        category_url_re = f'<li><a title="{category}" href="(.*?)/">{category}</a></li>'
        category_url = re.findall(category_url_re, mzitu_home_response.text)[0]
        category_url_list.append(category_url)
        category_name_list.append(category)
    return {'url': category_url_list, 'name': category_name_list}


def img_number(category_ulr):
    category_response = requests.get(category_ulr, headers=header)
    img_number_re = '<li><a href="https://www.mzitu.com/(.*?)" target="_blank"><img class='
    img_number_list = re.findall(img_number_re, category_response.text)
    return img_number_list


def crawl_img(img_n_list, category_name):
    choice_num = random.choice(img_n_list)

    base_url = main_url + choice_num

    base_url_response = requests.get(base_url, headers=header)
    title_rule = '<h2 class="main-title">(.*?)</h2>'
    title = re.findall(title_rule, base_url_response.text)[0]
    os.makedirs(f'mzitu/{category_name}/{title}/')
    num = 1
    while choice_num in base_url:
        base_url_response = requests.get(base_url, headers=header)
        next_url_rule = '<div class="main-image"><p><a href="(.*?)" >'
        next_url = re.findall(next_url_rule, base_url_response.text)[0]
        girl_img_url_rule = '<img class="blur" src="(.*?)"'
        girl_img_url = re.findall(girl_img_url_rule, base_url_response.text)[0]
        girl_img_name = girl_img_url.rsplit('/')[-1]

        girl_img_response = requests.get(girl_img_url, headers=header)
        with open(f'mzitu/{category_name}/{title}/{num}.jpg', 'wb') as f:
            for line in girl_img_response.iter_content():
                f.write(line)
        print('图片%s爬取成功。' % girl_img_name)
        base_url = next_url
        num += 1
        # print(base_url)


if __name__ == '__main__':
    category_list = category_list()
    category_name_list = category_list.get('name')
    category_url_list = category_list.get('url')
    category_count = (len(category_url_list))
    for i in range(category_count):
        person_img_number_list = img_number(category_url_list[i])
        crawl_img(person_img_number_list, category_name_list[i])
    print('程序结束')
