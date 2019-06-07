# -*- coding: utf-8 -*-
import os
import time
import json
import shutil
import platform

BOOK_PATH = "/Users/shirukai/Nutstore/notebook"
HEXO_PATH = "/Users/shirukai/Desktop/hollysys/hexo"
BLOG_PATH = HEXO_PATH + "/" + "source/_posts"
TEMP_PATH = HEXO_PATH + "/" + "temp"


class HexoAutoUpdate:
    def __init__(self):
        self._init_dir()
        self.success_files = []
        self.error_files = []

    def run(self):
        files_info = self.find_markdown()
        # 清理
        os.chdir(HEXO_PATH)
        os.system("hexo clean")
        temp_files = []
        for book_info in files_info:
            dict_info = dict()
            if book_info:
                print(book_info['name'])
                self.edit_blog(book_info, BLOG_PATH)
                # 判断是否可以构建
                # result = self.generate()
                f_path = os.path.join(BLOG_PATH, book_info['name']) + ".md"
                t_path = os.path.join(TEMP_PATH, book_info['name']) + ".md"
                dict_info['path'] = f_path
                dict_info['info'] = book_info
                # if result is not 0:
                #     os.remove(f_path)
                #     self.error_files.append(dict_info)
                # else:
                temp_info = dict()
                shutil.move(f_path, t_path)
                temp_info['o_path'] = f_path
                temp_info['t_path'] = t_path
                self.success_files.append(dict_info)
                temp_files.append(temp_info)
        for t_info in temp_files:
            shutil.copy(t_info['t_path'], t_info['o_path'])
        self.generate()
        result_info_path = os.path.join(HEXO_PATH, 'result_info.json')
        with open(result_info_path, 'w') as f:
            f.write(
                json.dumps(self.error_files + self.success_files, indent=4))

    @staticmethod
    def find_markdown():
        book_info = []
        for dir_path, dir_names, file_names in os.walk(BOOK_PATH):
            dir_no_dp = dir_path[len(BOOK_PATH) + 1:]
            for fn in file_names:
                tmp_dict = dict()
                if '.md' in fn:
                    tmp_dict['path'] = dir_path
                    tmp_dict['name'] = os.path.splitext(fn)[0]
                    tmp_dict['tags'] = dir_no_dp.split('/')
                    # 获取创建时间
                    if platform.system() == "Windows":
                        tmp_dict['time'] = os.path.getctime(os.path.join(dir_path, fn))
                    else:
                        stat = os.stat(os.path.join(dir_path, fn))
                        try:
                            create_time = stat.st_birthtime
                        except Exception:
                            create_time = stat.st_mtime
                        tmp_dict['time'] = create_time
                book_info.append(tmp_dict)
        print(len(book_info))
        return book_info

    # 修改markdown
    def edit_blog(self, book_info, arm_path):
        book_title = book_info['name']
        book_data = self.timestamp_to_time(book_info['time'])
        tags = book_info['tags']
        categories = tags[0]
        book_tags = ""
        for tag in tags:
            book_tags += " - " + tag + "\n"
        header = "---\n" \
                 "title: " + book_title + "\n" \
                                          "date: " + book_data + "\n" \
                                                                 "categories: " + categories + "\n" \
                                                                                               "tags: " + "\n" + book_tags + \
                 "---"
        b_path = os.path.join(book_info['path'], book_info['name'] + '.md')
        with open(b_path, 'r') as f:
            read_content = f.read()
        rc = read_content.split('\n')
        # count = 0
        # index_nu = 0
        # for index, line in enumerate(rc):
        #     if count == 5:
        #         index_nu = index
        #         break
        #     if len(line) == 0:
        #         count += 1
        # more = "<!--more-->"
        # rc.insert(index_nu, more)
        rc.pop(0)
        rc.insert(0, header)

        wc = '\n'.join(rc)
        ap = os.path.join(arm_path, book_info['name'] + '.md')
        with open(ap, 'w') as f:
            f.write(wc)

    @staticmethod
    def generate():
        os.chdir(HEXO_PATH)
        return os.system("hexo g")

    @staticmethod
    def start_server():
        os.chdir(HEXO_PATH)
        return os.system("hexo s")

    @staticmethod
    def update_git():
        os.chdir(HEXO_PATH)
        return os.system("hexo d -g")

    @staticmethod
    def _init_dir():
        if os.path.exists(BLOG_PATH):
            shutil.rmtree(BLOG_PATH)
        if os.path.exists(TEMP_PATH):
            shutil.rmtree(TEMP_PATH)
        os.makedirs(BLOG_PATH)
        os.makedirs(TEMP_PATH)

    @staticmethod
    def timestamp_to_time(timestamp):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


if __name__ == '__main__':
    service = HexoAutoUpdate()
    service.run()
    service.generate()
    service.start_server()
    # service.update_git()
