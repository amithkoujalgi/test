import razor.flow as rf 
from custom_executors import DaskClusterExecutor


@rf.block(executor=DaskClusterExecutor(
  master_cores=2,
  master_memory=2,
  nworkers=10,
  worker_cores=1,
  worker_memory=2
))
class DistributedSplit:
  inputs: type
  outputs: rf.Output[type]
  def run(self):
    ...

@rf.block(executor=DaskClusterExecutor(
  master_cores=2,
  master_memory=2,
  nworkers=10,
  worker_cores=1,
  worker_memory=2
))
class DistributedCombine:
  inputs: type
  outputs: rf.Output[type]
  def run(self):
    ...