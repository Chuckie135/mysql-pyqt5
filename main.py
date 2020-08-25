import pymysql
import sys
from PyQt5 import QtWidgets
from lib import Ui_MainWindow
import prettytable as pt
import pandas as pd
import re

class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.new = Ui_MainWindow()
        self.new.setupUi(self)

        # 链接数据库library
        self.db = pymysql.connect("localhost", "root", "password", "library")
        # 获取光标
        self.cursor = self.db.cursor()

        self.table = ''
        self.whe =''

        self.new.change_button.setEnabled(False)
        self.new.del_button.setEnabled(False)

    def insert(self):
        #text显示
        book_num = self.new.num_cheline.text()
        if not book_num:
            book_num = 0
        book_num = int(book_num)

        book_name = str(self.new.name_cheline.text())
        if len(book_name) == 0 :
            book_name = "null"

        author = str(self.new.author_cheline.text())
        if len(author) == 0:
            author = "null"

        price = self.new.price_cheline.text()
        if not price:
            price = 0.00
        price = float(price)
        # "insert into library(Book_num, Book_name, Author, Price)"
        sql = "insert into library values({}, '{}', '{}', {});".format(book_num,book_name,author,price)
        self.new.Sql_text.clear()
        self.new.Sql_text.setText(sql)
        try:
            #写入表
            self.cursor.execute(sql)
            self.db.commit()

            self.new.dbviewer.append("写入成功\n")

        except:
            #写入失败
            self.db.rollback()
            self.new.dbviewer.append("写入失败！\n")

    def search(self):
        whe = []
        if self.new.num_checkBox.isChecked():
            book_num = self.new.num_cheline.text().strip()
            if not book_num:
                book_num = 0
                nu = 'Book_num = %d' % book_num
            else:
                # book_num = int(book_num)
                if book_num.isalnum():
                    nu = 'Book_num = %s' % book_num
                else:
                    nu = 'Book_num%s' % book_num
            whe.append(nu)

        if self.new.name_checkBox.isChecked():
            book_name = self.new.name_cheline.text().strip()
            if len(book_name) == 0:
                book_name = "null"
            na = 'Book_name = \'%s\'' % book_name
            whe.append(na)

        if self.new.author_checkBox.isChecked():
            author = self.new.author_cheline.text().strip()
            if len(author) == 0:
                author = "null"
            au = 'Author = \'%s\'' % author
            whe.append(au)

        if self.new.price_checkBox.isChecked():
            prices = self.new.price_cheline.text().strip().split(",")
            try:
                for price in prices:
                    if not price:
                        pr = ''
                    else:
                        if price[0].isdigit():
                            price = float(price)
                            pr = 'Price = %0.2f' % price
                        else:
                            dig = r'\d+\.?\d*'
                            priced = re.findall(dig, price)[0]
                            optre = r'[^\d]'
                            opt = ''.join(re.findall(optre, price))
                            print(opt)
                            priced = float(priced)
                            pr = 'Price {} {:.2f}'.format(opt, priced)
                    whe.append(pr)
            except:
                self.new.dbviewer.append("输入有误！\n")
                return 0
        self.whe = ' and '.join(whe)
        if self.whe == '':
            sql = "select * from library"
        else:
            sql = "select * from library where {}".format(self.whe)
        self.new.Sql_text.clear()
        self.new.Sql_text.setText(sql)

        try:
            self.table = pd.read_sql(sql, self.db)
            tb = pt.PrettyTable()
            tb.add_column('Book_num', self.table['Book_num'])
            tb.add_column('Book_name', self.table['Book_name'])
            tb.add_column('Author', self.table['Author'])
            tb.add_column('Price', self.table['Price'])

            text_data = str(tb)
            # self.new.dbviewer.clear()
            self.new.dbviewer.append("查找结果:\n")
            self.new.dbviewer.insertPlainText(text_data)
            if self.whe != '':
                self.new.change_button.setEnabled(True)
                self.new.del_button.setEnabled(True)

        except:
            # self.new.dbviewer.clear()
            self.new.dbviewer.append("操作失败！\n")

    def deleted(self):
        sql = "delete from library where {}".format(self.whe)
        self.new.Sql_text.clear()
        self.new.Sql_text.setText(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            # self.new.dbviewer.clear()
            self.new.dbviewer.append("已成功删除记录！\n")

        except:
            # self.new.dbviewer.clear()
            self.new.dbviewer.append("操作失败！\n")

    def edit(self):
        whe = []
        if self.new.num_checkBox.isChecked():
            book_num = self.new.num_cheline.text().strip()
            if not book_num:
                book_num = 0
                nu = 'Book_num=%d' % book_num
            else:
                if book_num.isalnum():
                    nu = 'Book_num=%s' % book_num
                else:
                    nu = 'Book_num%s' % book_num
            whe.append(nu)

        if self.new.name_checkBox.isChecked():
            book_name = self.new.name_cheline.text().strip()
            if len(book_name) == 0:
                book_name = "null"
            na = 'Book_name=\'%s\'' % book_name
            whe.append(na)

        if self.new.author_checkBox.isChecked():
            author = self.new.author_cheline.text().strip()
            if len(author) == 0:
                author = "null"
            au = 'Author=\'%s\'' % author
            whe.append(au)

        if self.new.price_checkBox.isChecked():
            prices = self.new.price_cheline.text().strip().split(",")
            try:
                for price in prices:
                    if not price:
                        pr = ''
                    else:
                        if price[0].isdigit():
                            price = float(price)
                            pr = 'Price=%0.2f' % price
                        else:
                            dig = r'\d+\.?\d*'
                            priced = re.findall(dig, price)[0]
                            opt = ''.join(list(set(price).difference(set(priced))))
                            priced = float(priced)
                            pr = 'Price {} {:.2f}'.format(opt, priced)
                    whe.append(pr)
            except:
                self.new.dbviewer.append("输入有误！\n")
                return 0
        whe = ",".join(whe)
        sql = "update library set {} where {}".format(whe, self.whe)
        self.new.Sql_text.clear()
        self.new.Sql_text.setText(sql)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            # self.new.dbviewer.clear()
            self.new.dbviewer.append("已成功更新记录！\n")

        except:
            # self.new.dbviewer.clear()
            self.new.dbviewer.append("操作失败！\n")

    def sql_edit(self):
        sql = str(self.new.Sql_text.toPlainText())
        if sql.split()[0].lower() == 'select':
            try:
                # self.cursor.execute(sql)
                # self.db.commit()
                table = pd.read_sql(sql, self.db)
                tb = pt.PrettyTable()
                regex = r"select (.+?) from"
                res = " ".join(re.findall(regex, sql)).split(",")
                if res ==['*']:
                    tb.add_column('Book_num', table['Book_num'])
                    tb.add_column('Book_name', table['Book_name'])
                    tb.add_column('Author', table['Author'])
                    tb.add_column('Price', table['Price'])

                else:
                    for i in res:
                        m = i[:1].upper() + i[1:].lower()
                        tb.add_column('%s' %m, table['%s' %m])

                text_data = str(tb)
                # self.new.dbviewer.clear()
                self.new.dbviewer.append("操作结果:\n")
                self.new.dbviewer.insertPlainText(text_data)

            except:
                # self.new.dbviewer.clear()
                self.new.dbviewer.append("操作失败！\n")

        elif sql.split()[0].lower() == 'delete':
            try:
                self.cursor.execute(sql)
                self.db.commit()
                self.new.dbviewer.append("已成功删除记录！\n")
                table = pd.read_sql('select * from library', self.db)
                tb = pt.PrettyTable()
                # regex = r"select (.+?) from"
                # res = " ".join(re.findall(regex, sql)).split(",")
                # if res == ['*']:
                tb.add_column('Book_num', table['Book_num'])
                tb.add_column('Book_name', table['Book_name'])
                tb.add_column('Author', table['Author'])
                tb.add_column('Price', table['Price'])
                text_data = str(tb)
                # self.new.dbviewer.clear()
                # self.new.dbviewer.append("操作结果:\n")
                self.new.dbviewer.insertPlainText(text_data)

            except:
                self.new.dbviewer.append("操作失败！\n")

        elif sql.split()[0].lower() == 'update':
            try:
                self.cursor.execute(sql)
                self.db.commit()
                self.new.dbviewer.append("已成功更改记录！\n")
                table = pd.read_sql('select * from library', self.db)
                tb = pt.PrettyTable()
                # regex = r"select (.+?) from"
                # res = " ".join(re.findall(regex, sql)).split(",")
                # if res == ['*']:
                tb.add_column('Book_num', table['Book_num'])
                tb.add_column('Book_name', table['Book_name'])
                tb.add_column('Author', table['Author'])
                tb.add_column('Price', table['Price'])
                text_data = str(tb)
                # self.new.dbviewer.clear()
                # self.new.dbviewer.append("操作结果:\n")
                self.new.dbviewer.insertPlainText(text_data)

            except:
                self.new.dbviewer.append("操作失败！\n")

        elif sql.split()[0].lower() == 'insert':
            try:
                self.cursor.execute(sql)
                self.db.commit()
                self.new.dbviewer.append("已成功插入记录！\n")
                table = pd.read_sql('select * from library', self.db)
                tb = pt.PrettyTable()
                # regex = r"select (.+?) from"
                # res = " ".join(re.findall(regex, sql)).split(",")
                # if res == ['*']:
                tb.add_column('Book_num', table['Book_num'])
                tb.add_column('Book_name', table['Book_name'])
                tb.add_column('Author', table['Author'])
                tb.add_column('Price', table['Price'])
                text_data = str(tb)
                # self.new.dbviewer.clear()
                # self.new.dbviewer.append("操作结果:\n")
                self.new.dbviewer.insertPlainText(text_data)

            except:
                self.new.dbviewer.append("操作失败！\n")

        else:
            self.new.dbviewer.append("暂不支持其他命令\n")

    def showtable(self):
        sql = "select * from library"
        table = pd.read_sql(sql, self.db)

        tb = pt.PrettyTable()
        tb.add_column('Book_num',table['Book_num'])
        tb.add_column('Book_name', table['Book_name'])
        tb.add_column('Author', table['Author'])
        tb.add_column('Price', table['Price'])

        text_data = str(tb)
        # self.new.dbviewer.clear()
        self.new.dbviewer.append("系统数据如下:\n")
        self.new.dbviewer.insertPlainText(text_data)

    def exit(self):
        self.db.close()
        sys.exit(app.exec_())

    def clear(self):
        self.new.dbviewer.clear()
        self.new.Sql_text.clear()
        self.new.change_button.setEnabled(False)
        self.new.del_button.setEnabled(False)
        self.new.num_cheline.clear()
        # self.new.num_checkBox.setChecked(False)
        self.new.name_cheline.clear()
        # self.new.name_checkBox.setChecked(False)
        self.new.author_cheline.clear()
        # self.new.author_checkBox.setChecked(False)
        self.new.price_cheline.clear()
        # self.new.price_checkBox.setChecked(False)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = myWindow()
    myshow.show()
    sys.exit(app.exec_())
