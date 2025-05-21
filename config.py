from configparser import ConfigParser


def load_config(filename: str = 'database.ini', section: str = 'postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    # get section, default to postgresql
    contents = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            contents[param[0]] = param[1]
    return contents


if __name__ == '__main__':
    config = load_config()
    print(config)
