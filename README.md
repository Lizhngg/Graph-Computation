<div align="center">
    <h1 align="center">Serving Graph Model with BentoML</h1>
</div>

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py`. Run `bentoml serve` in your project directory to start the Service.

```python
$ bentoml serve .

```

The server is now active at [http://localhost:3000](http://localhost:3000/). You can interact with it using the POSTMAN or in other different ways.

POST

URL: 
```bash
'http://localhost:3000/alert_subgraph_mining'
```
Headers:
```bash
  add
   'accept: text/plain' 
   'Content-Type: application/json' 
   ```
Body:
```bash
{
    "task": "new_task",
    "model": "subgraph_mining",
    "path": "alert_node_subgraph_mining",
    "input_params":{  
                "table": "neo4j",
                "node_type": "alert_information_id",
                "node_id": 5,
                "edge_type": "alert_service_edge",
                "directed": "undirected"
                },
    "response": "default"
}
```

Expected response

```python
import bentoml

with bentoml.SyncHTTPClient("http://localhost:3000") as client:
        result = client.txt2img(
            prompt="A cinematic shot of a baby racoon wearing an intricate italian priest robe.",
            num_inference_steps=1,
            guidance_scale=0.0
        )
```