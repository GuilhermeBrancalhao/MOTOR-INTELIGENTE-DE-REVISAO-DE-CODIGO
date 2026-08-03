# Implementação

```python
from engine.volumes import PLUGINS
result = PLUGINS.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
