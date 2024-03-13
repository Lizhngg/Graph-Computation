<div align="center">
    <h1 align="center">Serving SDXL Turbo with BentoML</h1>
</div>

[Stable Diffusion XL Turbo](https://huggingface.co/stabilityai/sdxl-turbo) is a real-time text-to-image generation model utilizing a novel distillation technique called Adversarial Diffusion Distillation (ADD). This technology enables SDXL Turbo to generate images in a single step, significantly enhancing performance and reducing computational requirements without sacrificing image quality.

This is a BentoML example project, demonstrating how to build an image generation inference API server, using the SDXL Turbo model. See [here](https://github.com/bentoml/BentoML?tab=readme-ov-file#%EF%B8%8F-what-you-can-build-with-bentoml) for a full list of BentoML example projects.

## Prerequisites

- You have installed Python 3.8+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/1.2/get-started/quickstart.html) first.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or the [Python documentation](https://docs.python.org/3/library/venv.html) for details.
- To run the Service locally, you need a Nvidia GPU with at least 12G VRAM.

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