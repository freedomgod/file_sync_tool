import shutil
import os
import json
import re



operate_path = os.getcwd()


def get_path_file(path: str, lv: int = 0):
    """
    递归获取路径下的所有文件
    :param path: 文件夹路径
    :param lv: 默认为0，表示获取目录下所有文件，为1则表示只获取第一层级的文件
    :return: 文件名列表
    """
    res_file = []
    if os.path.isfile(path):
        return os.path.basename(path)
    allfilelist = os.listdir(path)
    # 遍历该文件夹下的所有目录或者文件
    for file in allfilelist:
        filepath = os.path.join(path, file)
        # 如果是文件夹，递归调用函数
        if os.path.isdir(filepath) and (lv == 0):
            res_file += get_path_file(filepath)
        # 如果不是文件夹，保存文件路径及文件名
        elif os.path.isfile(filepath):
            res_file.append(file)
    return res_file


class file_handle:
    def __init__(self):
        with open(os.path.join(operate_path, 'rule.json'), 'r') as fp:  # 获取规则
            self.rules = json.load(fp)

    def sync_file(self) -> dict:
        """
        同步文件
        :return: 返回字典，表示各个规则同步的文件有哪些
        """
        shutil.rmtree(os.path.join(operate_path, 'backup'))  # 重新建立备份文件夹
        os.mkdir(os.path.join(operate_path, 'backup'))
        sync_res = {}
        for i, rule in zip(range(len(self.rules)), self.rules):
            file_lis = []
            file_path = rule['file_path']
            sync_path = rule['sync_path']
            backup_path = os.path.join(operate_path, 'backup', f'rule{i + 1}_backup')  # 在同步文件之前做好备份
            if os.path.isdir(sync_path):
                shutil.copytree(sync_path, backup_path)  # 复制整个目录内容
            else:
                os.mkdir(backup_path)
                shutil.copy2(sync_path, backup_path)
            if os.path.isdir(file_path):  # 规则为一个路径
                all_file = get_path_file(file_path, lv=1)  # 只获取第一层级的文件，如果要更进一层的文件需要更改规则
                for ff in all_file:
                    filepath = os.path.join(file_path, ff)
                    syncpath = os.path.join(sync_path, ff)
                    if os.path.exists(syncpath):  # 同步文件需要目标文件夹下已存在文件
                        if os.stat(filepath).st_mtime > os.stat(syncpath).st_mtime:  # 要同步的文件最后修改时间应该要早于filepath的文件
                            shutil.copy2(filepath, syncpath)
                            file_lis.append(ff)
            elif os.path.isfile(file_path):  # 规则为同步单个文件
                if os.stat(file_path).st_mtime > os.stat(sync_path).st_mtime:
                    shutil.copy2(file_path, sync_path)
                    file_lis.append(os.path.basename(sync_path))
            sync_res[rule['rule_name']] = file_lis
        return sync_res

    def undo(self):
        """
        撤销同步操作，还原文件
        :return:
        """
        for i, rule in zip(range(len(self.rules)), self.rules):
            sync_path = rule['sync_path']
            backup_path = os.path.join(operate_path, 'backup', f'rule{i + 1}_backup')

            all_file = get_path_file(backup_path, lv=1)

            for ff in all_file:
                backpath = os.path.join(backup_path, ff)
                if os.path.isdir(sync_path):
                    orig_path = os.path.join(sync_path, ff)
                else:
                    orig_path = sync_path
                if os.path.exists(orig_path):
                    if os.stat(backpath).st_mtime != os.stat(orig_path).st_mtime:
                        shutil.copy2(backpath, orig_path)


class modify_file:
    def __init__(self):
        pass

    def add_front_matter(self, file_path: str, data) -> bool:
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
            for k, v in data.items():
                data_str += str(k) + ': ' + str(v) + '\n'
            data_str = '---\n' + data_str + '---\n'
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
    modify_file().add_front_matter('test.md', dt)
    # modify_file().add_front_matter('test.md', 'title: dd')
