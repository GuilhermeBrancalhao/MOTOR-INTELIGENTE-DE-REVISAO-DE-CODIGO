# Implementação

```python
from engine.volumes import REQUIREMENTS
result = REQUIREMENTS.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
