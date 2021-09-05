import os
import re
import yaml


def add_front_matter(file_path: str, data) -> bool:
    """
    为MarkDown文件添加front matter配置
    :param file_path: md文件路径
    :param data: 添加的front matter内容，可以为字符串、字典
    :return: 布尔值，是否添加成功
    """
    if not os.path.exists(file_path):  # 文件不存在则抛出错误
        raise FileNotFoundError
    data_str = ''
    pt = re.compile('---([\s\S]*)---')
    if type(data) == str:  # 判断data的类型
        if not pt.match(data):
            data_str = '---\n' + data + '\n---\n'
        else:
            data_str = data + '\n'
    elif type(data) == dict:
        data_str = yaml.dump(data)
    with open(file_path, 'r', encoding='utf-8') as fp:
        content = fp.read()  # 读取文件内容
    with open(file_path, 'w') as ff:
        res = pt.match(content)
        if res:  # 判断原文件内容是否有front matter内容
            return False
        content = data_str + content
        ff.write(content)
        return True


if __name__ == '__main__':
    dt = {'title': 'w w h', 'ds': 'sd'}
    add_front_matter('test.md', dt)
    # modify_file().add_front_matter('test.md', 'title: dd')
