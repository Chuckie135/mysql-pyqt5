# import prettytable as pt
#
# tb = pt.PrettyTable()
# tb.field_names = ["dcd","cdcdc","d2d"]
# tb.add_row(["dc",20,20])
# print(tb)
#
# uh = "dded"
# con = """INSERT INTO LIBRARY(BOOK_NUM, BOOK_NAME, AUTHOR, PRICE) VALUE(%(num)d, %(name)s, %(auth)s, %(pri)0.2f)"""
# print(uh)
# book_num = 155
#
# book_name = uh
#
# author = "cdcd"
#
# price = 155.00
#
# print ( con % dict(num=book_num, name=book_name, auth=author, pri=price) )
#
# sql = "INSERT INTO LIBRARY(BOOK_NUM, BOOK_NAME, AUTHOR, PRICE) VALUE({}, {}, {}, {})".format(book_num,book_name,author,price)
# print(sql)
#
import re
# sql = 'select cdnc,cd from lib'
# regex = r"select (.+?) from"
# # res = re.findall(regex, sql)
# res = " ".join(re.findall(regex, sql)).split(",")
# print(res)
# for i in res:
#     tu = i[:1].upper() + i[1:].lower()
#     print('%s' %tu)

# price = '=12.00'
# regex = r"\d+\.?\d*"
# price = re.findall(regex, price)[0]
# print(price)

# whe = []
# whe.append('dd')
# whe.append('aa')
# whe.append(52)
# print(whe)
# redd = ' and '.join(whe)
# print(redd)
price = '>15,<2596'.split(",")
print(price)
dig = r'\d+\.?\d*'

ri = '>14'
ie = '14'
print(''.join(list(set(ri).difference(set(ie)))))
# priced = re.findall(dig, price)
# print(priced)
#
# pr = 'Price {} {:.2f}'.format(price[0], priced)
# print(pr)
res = r'[^\d]'
pre = '>=123'
ru = ''.join(re.findall(res, pre))
print(ru)

# pe = 15
# pre = '='
# pr = 'pruice {:.2f} {}'.format(pe, pre)
# print(pr)

# he = ''
# m='dhk'
# he+='Book=%s' %m
# print(he)





