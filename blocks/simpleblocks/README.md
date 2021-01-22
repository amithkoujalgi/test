## Sample Blocks with new razorflow


### Initialise the bundle

Note: This creates/updates the `package.yaml` with the latest changes of the block code. 

```bash
from razor import api

api.blocks.init_bundle('/path/to/simpleblocks')

```

#### Publish the bundle


```bash
from razor import api

api.blocks.publish(bundle='./blocks')
```