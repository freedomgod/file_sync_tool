import yaml


def add_items(file_path: str, data):
    with open(file_path, 'r') as fp:
        con = yaml.load(fp, Loader=yaml.FullLoader)
        print(con)
        ss = yaml.dump(con)
        print(type(ss))

def del_items():
    pass


if __name__ == '__main__':
    add_items('test.yml', 's')
