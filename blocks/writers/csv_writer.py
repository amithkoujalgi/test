from razor import flow as rf
from writers.utils.my_util import MyUtil

@rf.block
class CSVWriter:

    content: rf.SeriesInput[str] = None
    target: rf.Output[str] = None

    def run(self):
        self.target.put(self.content)
