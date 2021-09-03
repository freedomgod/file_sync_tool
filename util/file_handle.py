import shutil
import os
import json


def get_path_file(path: str, lv: int = 0):
    """
    递归获取路径下的所有文件
    :param path: 文件夹路径
    :param lv: 默认为0，表示获取目录下所有文件，为1则表示只获取第一层级的文件
    :return: 文件名列表
    """
    res_file = []
    if os.path.isfile(path):
        res_file = [path.split('\\')[-1]]
        return res_file
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
        with open('../rule.json', 'r') as fp:  # 获取规则
            self.rules = json.load(fp)

    def sync_file_slot(self):
        """
        同步文件
        :return:
        """
        shutil.rmtree('../backup')  # 重新建立备份文件夹
        os.mkdir('../backup')

        for i, rule in zip(range(len(self.rules)), self.rules):
            file_path = rule['file_path']
            sync_path = rule['sync_path']
            backup_path = f'../backup/rule{i + 1}_backup'  # 在同步文件之前做好备份
            if os.path.isdir(sync_path):
                shutil.copytree(sync_path, backup_path)  # 复制整个目录内容
            else:
                os.mkdir(backup_path)
                shutil.copy2(sync_path, backup_path)
            if os.path.isdir(file_path):  # 规则为一个路径
                all_file = get_path_file(file_path, lv=1)
                for ff in all_file:
                    filepath = os.path.join(file_path, ff)
                    file2_path = sync_path + '/' + ff
                    if os.path.exists(file2_path):  # 同步文件需要目标文件夹下已存在文件
                        if os.stat(filepath).st_mtime > os.stat(file2_path).st_mtime:  # 要同步的文件最后修改时间应该要早于filepath的文件
                            shutil.copy2(filepath, file2_path)
            elif os.path.isfile(file_path):  # 规则为同步单个文件
                if os.path.exists(sync_path) and (os.stat(file_path).st_mtime > os.stat(sync_path).st_mtime):
                    shutil.copy2(file_path, sync_path)

    def undo_slot(self):
        """
        撤销同步操作，还原文件
        :return:
        """
        for i, rule in zip(range(len(self.rules)), self.rules):
            sync_path = rule['sync_path']
            backup_path = f'../backup/rule{i + 1}_backup'  # 在同步文件之前做好备份

            all_file = get_path_file(backup_path, lv=1)

            for ff in all_file:
                backpath = os.path.join(backup_path, ff)
                if os.path.isdir(sync_path):
                    orig_path = sync_path + '/' + ff
                else:
                    orig_path = sync_path
                if os.path.exists(orig_path):
                    if os.stat(backpath).st_mtime != os.stat(orig_path).st_mtime:
                        shutil.copy2(backpath, orig_path)