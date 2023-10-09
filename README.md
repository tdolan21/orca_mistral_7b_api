# Mistral-7B-OpenOrca API

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![NVIDIA](https://img.shields.io/badge/NVIDIA-76B900?style=for-the-badge&logo=nvidia&logoColor=white)

![orca](assets\imgs\majestic-orca.png)

## Overview

This is a FastAPI project that exposes a text generation API powered by the Mistral-7B-OpenOrca model. The API runs in a Docker container and is optimized for NVIDIA GPUs using PyTorch. This model requires ~16GB of VRAM to host for inference. With this API you can have one machine on your network host the model and provide inference through api calls to other machines without the need for AWS in the development phase.

## Installation

The only prerequisite install needed for this API to run in docker

### Requirements

- Docker
- NVIDIA GPU 

### Build Docker Image

```bash
docker build -t orca_api:latest .
```

### Run Docker Container

The API must run with gpu support:

```bash
docker run --gpus all -p 8001:8001 orca_api:latest
```

### API Endpoints

- `GET /`: Welcome message
- `POST /orca/`: Text generation
- `POST /orca/codegen`: Python code generation

Visit `/docs` for API documentation and testing.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details.

Feel free to add or remove sections based on the specifics of your project.



