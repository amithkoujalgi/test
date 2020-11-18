from razor_core import ContainerExecutorBase, ClusterExecutorBase


class DaskClusterExecutor(ClusterExecutorBase):
  def __init__(
    self,
    master_cores: int = 2,
    master_memory: int = 2,
    nworkers: int = 0,
    worker_cores: int = 1,
    worker_memory: int = 2
  ):
    master_container = ContainerExecutorBase(
      name='dask-master',
      image='dask-core',
      cores=master_cores,
      master_memory=master_memory,
      entrypoint='bash /etc/dask/master.sh'
    )
    worker_containers = [
      ContainerExecutorBase(
        name=f'dask-worker-{w_id}',
        image='dask-core',
        cores=worker_cores,
        master_memory=worker_memory,
        entrypoint='bash /etc/dask/worker.sh'
      )
      for w_id in range(nworkers)
    ]
    dask_cluster = ClusterExecutorBase(
      containers=[master_container, worker_containers],
      network_type='host',
      ...
    )

    dask_cluster.start()