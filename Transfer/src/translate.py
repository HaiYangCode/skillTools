# -*- coding: UTF-8 -*-
# !/usr/bin/python3


import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ElementTree
import xlwt
import xlrd
import random


# 创建excel
def create_excel():
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet("测试表格")  # 新建sheet
    return workbook, sheet1


def read_string_xml(sheet):
    print("start read sourceStrings.xml file")
    root = ET.parse("sourceStrings2.xml")

    # sheet
    sheet.write(0, 0, "key")  # 第1行第1列数据
    sheet.write(0, 1, "中文")  # 第1行第2列数据
    sheet.write(0, 2, "英文")  # 第1行第3列数据
    sheet.write(0, 3, "高棉语")  # 第1行第4列数据
    i = 1
    total = 0
    for elem in root.iter("string"):
        sheet.write(i, 0, elem.get("name"))  # 第1行第1列数据
        sheet.write(i, 1, elem.text)  # 第1行第2列数据
        i += 1
        total += len(elem.text)
    # for item in root.iterfind("string"):
    #     print(item)
    print(total)


# 读取翻译后的目标文件转换成项目中使用的xml文件
def read_res_2_target_xml_file():
    workbook = xlrd.open_workbook("./translate.xlsx")
    sheet = workbook.sheet_names()
    workSheet = workbook.sheet_by_name(sheet[0])

    root = generate_root_element()
    for i in range(0, workSheet.nrows):
        row = workSheet.row(i)
        # print(workSheet.cell_value(i, j), "\t", end="\n")
        generate_sub_element(root, row[0].value, row[2].value);

    print("pase excel complete")

    tree = ElementTree(root)
    ri = random.randint(0, 100).__str__()
    tree.write("result" + ri + ".xml", encoding='utf-8')


def test_generate_xml():
    root = generate_root_element()
    tree = ElementTree(root)
    tree.write('result.xml', encoding='utf-8')


def generate_root_element():
    root = Element("resources")
    return root


def generate_sub_element(root, id, value):
    sub = SubElement(root, "string")
    sub.set("name", id)
    sub.text = value
    return sub


def main():
    # start 读取原始文件后生产指定名字的xlsx文件
    workbook, sheet = create_excel()
    read_string_xml(sheet)
    print("parse xml complete")
    workbook.save(r'./translate.xlsx')  # 保存
    # print("save translate.xlsx success")
    # del workbook
    # end 读取原始文件后生产指定名字的xlsx文件
    # readRes2TargetXmlFile()


if __name__ == '__main__':
    main()
