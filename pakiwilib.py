import os
import time
import yaml
import pickle
import numpy as np


class UnimplementedMethod(Exception):
    pass


class Set(object):
    INPUT_FOLDER = 'inputs'
    INPUT_EXTENSION = '.txt'

    def __init__(self, setname):
        self.setname = setname
        self.filename = os.path.join(self.INPUT_FOLDER, '{}{}'.format(self.setname, self.INPUT_EXTENSION))
        self._load()

    def _load(self):
        if not os.path.exists(self.filename):
            raise Exception('The input dataset file {} does not exist'.format(self.filename))
        with open(self.filename) as f:
            content = f.readlines()
        self._processData(content)

    def _processData(self, data):
        raise UnimplementedMethod('Please implement _processData() in a subclass of Set')

    def score(self, result):
        raise UnimplementedMethod('Please implement score() in a subclass of Set')

    def raw_score(self, result):
        raise UnimplementedMethod('Please implement score() in a subclass of Set')


class Result(object):
    OUTPUT_FOLDER = 'outputs'
    OUTPUT_EXTENSION = '.out'
    OUTPUT_METADATA = 'meta.yml'
    OUTPUT_DATAFILE = 'data.pickle'

    def __init__(self, set_):
        self.set = set_
        self.date = time.time()
        self.foldername = None

    def score(self):
        return self.set.score(self)

    @classmethod
    def list(cls):
        if not os.path.exists(cls.OUTPUT_FOLDER):
            return []
        results = []
        for f in os.listdir(cls.OUTPUT_FOLDER):
            filename = os.path.join(cls.OUTPUT_FOLDER, f)
            if os.path.isdir(filename):
                with open(os.path.join(filename, cls.OUTPUT_METADATA), 'r') as stream:
                    meta = yaml.load(stream)
                score = meta.get('score', -1)
                date = meta.get('date', 0)
                results.append((f, score, date))
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
        self.datafilename = os.path.join(self.foldername, self.OUTPUT_DATAFILE)
        os.mkdir(self.foldername)

        # save metadata
        meta = {
            'score': self.score(),
            'date': self.date,
        }
        with open(os.path.join(self.foldername, self.OUTPUT_METADATA), 'w') as stream:
            yaml.dump(meta, stream, default_flow_style=False)

        self._save_data()

    @classmethod
    def load(cls, resultname, set_=None):
        foldername = os.path.join(cls.OUTPUT_FOLDER, resultname)
        with open(os.path.join(foldername, cls.OUTPUT_METADATA), 'r') as stream:
            meta = yaml.load(stream)
        score = meta.get('score', -1)
        date = meta.get('date', 0)

        datafilename = os.path.join(foldername, cls.OUTPUT_DATAFILE)

        result = cls._load_data(datafilename, set_)
        result.date = date
        result.foldername = foldername
        return result

    def _save_data(self):
        raise UnimplementedMethod('Please implement _save_data() in a subclass of Set')

    @classmethod
    def _load_data(cls, datafile, set_):
        raise UnimplementedMethod('Please implement _load_data() in a subclass of Set')


class SampleSet(Set):
    def _processData(self, data):
        self.data = data

    def score(self, result):
        return self.raw_score(result.data)

    def raw_score(self, data):
        return int(np.sum(data))


class SampleResult(Result):
    def __init__(self, set_, data):
        super(SampleResult, self).__init__(set_)
        self.data = data

    def _save_data(self):
        pickle.dump(self.data, open(self.datafilename, 'wb'))

    @classmethod
    def _load_data(cls, datafile, set_):
        data = pickle.load(open(datafile, 'rb'))
        result = cls(set_, data)
        return result


class Photoset(Set):
    HORIZONTAL = 0
    VERTICAL = 1

    def _processData(self, data):
        numbers = int(data[0])
        self.images = []
        for image_data in data[1:]:
            image_data = image_data.replace('\n', '').split(' ')
            vertical = (image_data[0] == 'V')
            tags = set(image_data[2:])
            id_ = len(self.images)
            self.images.append((id_, vertical, tags))

    def score(self, result):
        return self.raw_score(result.slides)

    def raw_score(self, data):
        return int(np.sum(data))


class Slideshow(Result):
    def __init__(self, set_, slides):
        """
        Args:
            slides ([(), (), ..., ()]): List of tuples
        """
        super(Slideshow, self).__init__(set_)
        self.slides = slides

    def _save_data(self):
        pickle.dump(self.slides, open(self.datafilename, 'wb'))

    @classmethod
    def _load_data(cls, datafile, set_):
        slides = pickle.load(open(datafile, 'rb'))
        result = cls(set_, slides)
        return result
