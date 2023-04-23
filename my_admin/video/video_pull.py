import logging
import os
import re
import time
# from pyecharts import options as opts
# from pyecharts.charts import Bar
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from utils.LoggerUtil import LogUtil

# from matplotlib import pyplot as plt
# from matplotlib.font_manager import FontProperties
log = LogUtil(log_level=logging.DEBUG).getLogger()

headers = {"User-Agent": UserAgent().random}


# 获取数据
def url_parse():
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E8%B1%86%E7%93%A3%E9%AB%98%E5%88%86&sort=rank&page_limit=200&page_start=0"
    response = requests.get(url=url, headers=headers).json()
    # print(response)
    return response


# 处理内容
def content_parse(res):
    vedio_name = []
    vedio_rate = []
    content = res["subjects"]
    for i in content:
        name = i["title"]
        rate = i["rate"]
        vedio_name.append(name)
        vedio_rate.append(float(rate))
        get_film_info(i["url"], headers)
    return vedio_name, vedio_rate


def get_film_info(url, headers):
    # film_info = []
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    # 片名
    name = soup.find(attrs={'property': 'v:itemreviewed'}).text.split(' ')[0]
    # 上映年份
    year = soup.find(attrs={'class': 'year'}).text.replace('(', '').replace(')', '')
    # 评分
    score = soup.find(attrs={'property': 'v:average'}).text
    # 评价人数
    votes = soup.find(attrs={'property': 'v:votes'}).text
    infos = soup.find(attrs={'id': 'info'}).text.split('\n')[1:11]
    # 导演
    director = infos[0].split(': ')[1]
    # 编剧
    scriptwriter = infos[1].split(': ')[1]
    # 主演
    actor = infos[2].split(': ')[1]
    # 类型
    film_type = infos[3].split(': ')[1]
    # 国家/地区
    area = infos[4].split(': ')[1]

    if '.' in area:
        area = infos[5].split(': ')[1].split(' / ')[0]
        # 语言
        language = infos[6].split(': ')[1].split(' / ')[0]
    else:
        area = infos[4].split(': ')[1].split(' / ')[0]
        # 语言
        language = infos[5].split(': ')[1].split(' / ')[0]

    if '大陆' in area or '香港' in area or '台湾' in area:
        area = '中国'
    if '戛纳' in area:
        area = '法国'
        # 时长
    times0 = soup.find(attrs={'property': 'v:runtime'}).text
    times = re.findall('\d+', times0)[0]
    log.critical(
        '电影名称：【%s】 上映年份:[%s] 评分：[%s] 导演：[%s] 编剧：[%s] 国家/地区：[%s] 语言：[%s] 类型：[%s] 主演：[%s] 时长：[%s]' % (
            name, year, score, director, scriptwriter, area, language, film_type, actor, times))

    # film_info.append(name)
    # film_info.append(year)
    # film_info.append(score)
    # film_info.append(votes)
    # film_info.append(director)
    # film_info.append(scriptwriter)
    # film_info.append(actor)
    # film_info.append(film_type)
    # film_info.append(area)
    # film_info.append(language)
    # film_info.append(times)
    # filepath = 'TOP250.xlsx'
    # insert2excel(filepath, film_info)

# def insert2excel(filepath,film_info):
#     try:
#         if not os.path.exists(filepath):
#             tableTitle = ['片名','上映年份','评分','评价人数','导演','编剧','主演','类型','国家/地区','语言','时长(分钟)']
#             wb = Workbook()
#             ws = wb.active
#             ws.title = 'sheet1'
#             ws.append(tableTitle)
#             wb.save(filepath)
#             time.sleep(3)
#             wb = load_workbook(filepath)
#             ws = wb.active
#             ws.title = 'sheet1'
#             ws.append(film_info)
#             wb.save(filepath)
#      return True
#     except:
#         return False
# 制作图表
# def make_pic(name,rate):
#     fig=plt.figure(figsize=(15,8),dpi=80)
#     font=FontProperties(fname=r"STZHONGS.TTF",size=12)
#     plt.barh(name[::-1],rate[::-1],color="red")
#     plt.xticks(fontproperties=font)
#     plt.yticks(name,fontproperties=font)
#     plt.savefig("豆瓣.png")
#     plt.show()

# 主函数
def main():
    data = url_parse()
    content_parse(data)
    # make_pic(name,rate)


if __name__ == '__main__':
    main()
