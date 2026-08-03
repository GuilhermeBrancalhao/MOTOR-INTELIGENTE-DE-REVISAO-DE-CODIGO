# Implementação

```python
from engine.volumes import TEMPLATES
result = TEMPLATES.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
