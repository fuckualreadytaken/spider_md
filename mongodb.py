#! /usr/bin/env python
# coding=utf-8

import pymongo

host = '127.0.0.1'
port = 27017
db_name = 'md_db'
table_name = 'sheet_line'
data = {}
client = pymongo.MongoClient(host, port)
md_db = client[db_name]
sheet_line = md_db[table_name]
sheet_line.insert_one(data)