#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import time
import argparse
import shutil


def main():
    # args analyze
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('-n', '--name', help="文件名(英文)，如：advice-for-ui",
                        type=str, default='template')
    parser.add_argument('-t', '--title', help="文章名(可中文)，如：关于用户界面编写的几点建议",
                        type=str, default='')
    parser.add_argument('-s', '--subtitle', help="副文章名(可中文)，如：过来人的建议",
                        type=str, default='')
    parser.add_argument('-d', '--date', help="文章日期，如：20191124",
                        type=str, default='')
    parser.add_argument('-c', '--categories', help="文章分类，如：[经验小结]",
                        type=str, default='')

    args = parser.parse_args()
    date = str(args.date)
    categories = str(args.categories)
    name = str(args.name)
    title = str(args.title)
    subtitle = str(args.subtitle)

    if date == '':
        date = str(time.strftime("%Y%m%d", time.localtime()))
    if title == '':
        title = name.replace('-', ' ')

    if not os.path.isfile('_posts/template.md'):
        print('\033[1;31m _posts目录下不存在模板文件template.md，请添加\033[0m')
        return
    else:
        new_file_name = '_posts/' + \
            date[0:4] + '-' + date[4:6] + '-' + \
            date[6:8] + '-' + name + '.md'

        old_file = open('_posts/template.md', 'r+')
        new_file = open(new_file_name, 'w')
        file_content = old_file.read()
        file_content = file_content.replace('tem_title', title)
        file_content = file_content.replace('tem_subtitle', subtitle)
        file_content = file_content.replace('tem_date', date[0:4] + '-' + date[4:6] + '-' +
                                            date[6:8])
        file_content = file_content.replace(
            'categories:', 'categories: ' + categories)
        file_content = file_content.replace('tem_link', 'https://haoqchen.site/' + date[0:4] + '/' + date[4:6] + '/' +
                                            date[6:8] + '/' + name + '/')
        new_file.write(file_content)
        new_file.close()
        old_file.close()


if __name__ == "__main__":
    main()
