import configparser
import os

class MyConfig:
    def __init__(self, path):
        if not path or not os.path.exists(path):
            raise ValueError('{} does not exist'.format(path))
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get(self, section, *args):
        if not args:
            return dict(self.config.items(section))

        result = {}
        for entry in [ {x: self.config.get(section, x)} for x in args ]:
            result.update(entry)
        return result
        
