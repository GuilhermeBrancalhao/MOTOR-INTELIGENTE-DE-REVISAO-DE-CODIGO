# Implementação

```python
from engine.volumes import RAG
result = RAG.process(input_data, request_id="uuid")
if result.status == "SUCCESS":
    print(result.payload)
```
