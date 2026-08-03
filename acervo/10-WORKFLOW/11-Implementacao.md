# Implementação

```python
from engine.volumes import WORKFLOW
result = WORKFLOW.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
