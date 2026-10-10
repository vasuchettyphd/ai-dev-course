# 📦 Requirements
* Docker 20.10+
* Docker Compose v2 (comes with Docker Desktop)
* NVIDIA GPU (e.g., RTX 2070) with 8GB+ VRAM
* NVIDIA Container Toolkit

# 🚀 Quickstart
```bash
# Clone the repo
git clone https://github.com/vasuchettyphd/ai-dev-course.git
cd ai-dev-course/02-local-llm-docker

# Build and start the containers
docker compose up --build
```

This will:

* Start the model server at http://localhost:5000
* Start the Jupyter notebook at http://localhost:8888

# 📁 Project Structure
```bash
02-local-llm-docker/
├── docker-compose.yml                    # Top-level Compose config
├── model_server/                         # LLaMA model server container
│   ├── app.py                            # Flask app exposing the /generate endpoint
│   ├── Dockerfile                        # Builds the model server container
│   └── requirements.txt                  # All Python dependencies (torch, transformers, etc.)
├── jupyter/                              # Jupyter Notebook environment
│   ├── Dockerfile                        # Builds the Jupyter container
│   └── requirements.txt                  # Jupyter, requests, numpy, pandas, etc.
├── notebooks/                            # The location of the notebooks
│   └── test_model.ipynb                  # A sample notebook that uses the model server
```

# ✨ Jupyter Notebook Example
Once running, open notebooks/test_model.ipynb and run:

```python
import requests

res = requests.post("http://model:5000/generate", json={
    "prompt": "What is the capital of France?"
})
print(res.json()["response"])
```

# 🔧 Updating Dependencies
```bash
cd jupyter
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt  # After installing new packages

cd ../model_server
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt  # After installing new packages
```

⚠️ The requirements.txt files are now the single source of truth for dependency versions. Remember to re-export them with pip freeze > requirements.txt after adding or upgrading any package.

# 🧹 Stopping Containers
```bash
docker compose down
```

📬 Questions?
Feel free to open an issue or PR!