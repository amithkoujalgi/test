from razor import flow as rf

@rf.block
class SimpleSeriesPipeBlock:
    """
    Series input to output
    """
    source: list = []
    target: rf.SeriesOutput[str]
        
    def run(self):
        for data in self.source:
            self.logger.info(f'Piping steaming input {data} to streaming output.')
            self.target.put(data)

# series_pipe_block1 = SimpleSeriesPipeBlock(source = ['a', 'b', 'c'])
# series_pipe_block2 = SimpleSeriesPipeBlock(source = series_pipe_block1.target)
# p = rf.Pipeline(targets = [atomic_pipe_block2])
# p.execute()