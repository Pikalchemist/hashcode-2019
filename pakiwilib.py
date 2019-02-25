import os
import time
import yaml


class UnimplementedMethod(Exception):
    pass


class Set(object):
    INPUT_FOLDER = 'inputs'
    INPUT_EXTENSION = '.in'

    def __init__(self, setname, input_folder='inputs', input_extension='in'):
        self.setname = setname
        self.filename = os.path.join(self.INPUT_FOLDER, '{}{}'.format(self.setname, self.INPUT_EXTENSION))
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            raise Exception('The input dataset file {} does not exist'.format(self.filename))
        with open(path) as f:
            content = f.readlines()
        self._processData(content)

    def _processData(self, data):
        raise UnimplementedMethod('Please implement _processData() in a subclass of Set')

    def score(self, result):
        raise UnimplementedMethod('Please implement score() in a subclass of Set')


class Result(object):
    OUTPUT_FOLDER = 'outputs'
    OUTPUT_EXTENSION = '.out'
    OUTPUT_METADATA = 'meta.yml'

    def __init__(self, set):
        self.set = set
        self.date = time.time()
        self.foldername = None

    def score(self):
        return self.set.score(self)

    @classmethod
    def list():
        if not os.path.exists(cls.OUTPUT_FOLDER):
            return []
        reults = []
        for f in os.listdir(cls.OUTPUT_FOLDER):
            if os.path.isdir(f):
                with open(os.path.join(f, cls.OUTPUT_METADATA), 'r') as stream:
                    meta = yaml.load(stream)
                score = meta.get('score', -1)
                results.append((f, score))
        return results

    def save(self):
        # create the outputs folder
        if not os.path.exists(self.OUTPUT_FOLDER):
            os.mkdir(self.OUTPUT_FOLDER)

        # search an available name
        def foldername(index):
            return os.path.join(self.OUTPUT_FOLDER, '{}_{}'.format(self.set.setname, index))

        index = 0
        while os.path.exists(foldername(index)):
            index += 1

        # create the output folder for this results
        self.foldername = foldername(index)
        os.mkdir(self.fodlername)

        # save metadata
        meta = {
            'score': self.score(),
            'date': self.date,
        }
        with open(os.path.join(self.foldername, self.OUTPUT_METADATA), 'w') as stream:
            yaml.dump(meta, stream, default_flow_style=False)
