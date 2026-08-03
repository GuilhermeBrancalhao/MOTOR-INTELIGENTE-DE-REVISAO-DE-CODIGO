# Implementação

```python
from engine.volumes import KNOWLEDGE
result = KNOWLEDGE.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
