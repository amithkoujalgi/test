from razor import flow as rf

@rf.block
class SimpleAtomicPipeBlock:
    """
    Atomic input to output
    """
    source: str = None
    target: rf.Output[str]
        
    def run(self):
        self.logger.info(f'Piping atomic input {self.source} to atomic output.')
        self.target.put(self.source)


# atomic_pipe_block1 = SimpleAtomicPipeBlock(source = 'Hello')
# atomic_pipe_block2 = SimpleAtomicPipeBlock(source = atomic_pipe_block1.target)
# p = rf.Pipeline(targets = [atomic_pipe_block2])
# p.execute()