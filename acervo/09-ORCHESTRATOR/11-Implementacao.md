# Implementação

```python
from engine.volumes import ORCHESTRATOR
result = ORCHESTRATOR.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
