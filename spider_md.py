#! /usr/bin/env python
# coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import pymongo


def indexpage_generator():
    url = "http://paper.tuisec.win/search.jsp?keywords=&&search_by_html=title&&page="
    for i in range(30):
        yield url + str(i + 1)


def get_all_indexpages():
    url = "http://paper.tuisec.win/search.jsp?keywords=&&search_by_html=title&&page="
    url_list = []
    for i in range(30):
        url_list.append(url + str(i + 1))

    return url_list


def request_indexpages(url):
    # request indexpage
    cookie = "__jsluid=9534ddf58d60d6c49695bc1e850cba08; JSESSIONID=024021BD20BD320D67B19A858842707A"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
        "Cookie": cookie
    }
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    info = response.read()
    return info


def parse_indexpage(info):
    # parse indexpage
    soup = BeautifulSoup(info, "html.parser")
    all_tr = soup.findAll('tr')[1:]
    url = "http://paper.tuisec.win"
    item = []
    for i in all_tr:
        td = i.findAll('td')
        data = {"time": td[0].string,
                "name": td[1].string,
                "domain": td[2].string,
                "author": td[3].string,
                "link": url + td[1].a.get('href'),
                "hash": td[1].a.get('href')}
        item.append(data)
    return item


def mongodb(collection):
    client = pymongo.MongoClient('127.0.0.1', 27017)
    md_db = client['md_db']
    sheet_line = md_db[collection]
    return sheet_line


def get_latest():
    coll = mongodb('latest')
    return coll.find_one()['hash']


def get4():
    url_list = get_all_indexpages()[0:5]
    url_list.reverse()
    # sheet = mongodb('latestt')
    all_item = []
    for i in url_list:
        item = parse_indexpage(request_indexpages(i))
        item.reverse()
        all_item.extend(item)
    count = 0
    for j in all_item:
        print j['hash']
        if get_latest() == j['hash']:
            break
        count += 1
    # If we need 'everyday feed' , we can use the flowing code, the every day new info in the new_list
    new_list = all_item[count + 1:]
    # insert new_list in the public collection
    sheet = mongodb('md_sheet')
    sheet.insert(new_list)
    # update latest collection
    l_sheet = mongodb('latest')
    old = l_sheet.find_one()['hash']
    new = {'hash': new_list[-1]['hash']}
    l_sheet.find_one_and_replace({'hash': {'$eq': old}}, new)


def test():
    l_sheet = mongodb('latest')
    old = l_sheet.find_one()['hash']
    new = {'hash': '/detail/38d376bc0108499'}
    l_sheet.find_one_and_replace({'hash': {'$eq': old}}, new)


def main():
    url_list = get_all_indexpages()
    url_list.reverse()
    sheet = mongodb('test')
    for i in url_list:
        item = parse_indexpage(request_indexpages(i))
        item.reverse()
        sheet.insert(item)

    print item[14]


if __name__ == "__main__":
    # main()
    get4()
    # test()
