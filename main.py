from selenium import webdriver
import parseLot as parse
import csv
from multiprocessing import Pool
from datetime import datetime
import logging

URL = 'https://www.telderi.ru/ru/search/index/page/9#page=3&user_id=&website_type%5B0%5D=website&website_type'

logging.basicConfig(filename="parse.log", level=logging.ERROR, filemode="w")
logging = logging.getLogger()


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x935')
try:
    DRIVER = webdriver.Chrome(options=options)
except:
    pass

def get_total_pages(webdriver):
    pages = webdriver.find_element_by_id('yw0').find_element_by_class_name('last').find_element_by_tag_name('a').get_attribute('href')
    total_pages = pages.split('/')[-1]
    return int(total_pages)

def get_page_links(webdriver):
    links = webdriver.find_elements_by_class_name('click')

    result = list()
    for link in links:
        try:
            result.append(link.get_attribute('href'))
        except:
            logging.ERROR("Error adding link in page")

    return result

def get_data_page(links):
    data = {}
    listData = list()

    for link in links:
        DRIVER.get(link)

        name = parse.get_name(DRIVER)
        opPrice = parse.get_optimalPrice(DRIVER)
        sqi = parse.get_sqi(DRIVER)
        profit = parse.get_profit(DRIVER)
        costs = parse.get_costs(DRIVER)
        visit = parse.get_visit(DRIVER)
        views = parse.get_views(DRIVER)
        topic = parse.get_topic(DRIVER)

        data = {'name': name,
                'topic': topic,
                'opPrice': opPrice,
                'sqi': sqi,
                'profit': profit,
                'costs': costs,
                'visit': visit,
                'views': views,
                'link': link
                }
        listData.append(data)

    return listData

def create_csv():
    with open("telderiSiteData.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(('Название', 'Тема', 'Оптимальная цена', 'ИКС', 'Расходы', 'Доходы', 'Просмотры в дн.',
                         'Посетители в дн.', 'Ссылка'))

def write_csv(data):
  with open("telderiSiteData.csv", 'a') as f:
      writer = csv.writer(f)
      for i in data:
          writer.writerow((i['name'],
                           i['topic'],
                           i['opPrice'],
                           i['sqi'],
                           i['costs'],
                           i['profit'],
                           i['views'],
                           i['visit'],
                           i['link']))


def make_all(url):

    DRIVER.get(url)
    links = get_page_links(DRIVER)
    data = get_data_page(links)
    write_csv(data)
    print("\nСтраница добавлена: " + url)

def generated_URL(total_pages):
    base_url = 'https://www.telderi.ru/ru/search/index/page/'
    page_part = '#page='
    query_part = '&user_id=&website_type%5B0%5D=website&website_type'

    url_gen = list()

    for i in range(1, total_pages):
        url_gen.append(base_url + str(i) + page_part + str(i) + query_part)

    return url_gen

def main():
    start = datetime.now()
    DRIVER.get(URL)
    total_pages = get_total_pages(DRIVER)

    create_csv()
    DRIVER.close()

    links = generated_URL(total_pages)
    size_links = len(links)
    print("Последняя стр: " + links[size_links - 1])
    with Pool(15) as p:
        p.map(make_all, links)

    # for i in range(1, total_pages):
    #     base_url = 'https://www.telderi.ru/ru/search/index/page/'
    #     page_part = '#page='
    #     query_part = '&user_id=&website_type%5B0%5D=website&website_type'
    #
    #     link = base_url + base_url + str(i) + page_part + str(i) + query_part
    #     DRIVER.get(link)
    #     links_lots = get_page_links(DRIVER)
    #     data = get_data_page(links_lots)
    #     write_csv(data)
    #     print('Добавлены лоты со страницы: ' + link)

    end = datetime.now()
    time_result = end - start
    print('\nВремя выполнения: ' + time_result.__str__())

if __name__ == '__main__':
    main()