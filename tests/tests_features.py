from utils import INFILES, INDIR
from features import FGen
from expert import DataPageRecognizer


class TestFeatureExtractor:

    def setUp(self):
        self.f = FGen(INFILES[0])

    def test_simple(self):
        for feature in self.f.metadata(set(["page"]), elems=20):
            print(feature)


class TestDataPageRecognizer:

    def setUp(self):
        self.r = DataPageRecognizer(INFILES[0])

    def test_recognition(self):
        self.r.reset()
        self.r.run()
        print(self.r.facts)
