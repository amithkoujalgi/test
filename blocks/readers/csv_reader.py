from razor import flow as rf
from readers.utils.my_util import MyUtil

@rf.block
class CSVReader:

    source: rf.Input[str] = None
    content: rf.Output[str] = None

    def run(self):
        self.content.put(self.source)
