# OpenMRS Smart IA

<p align="center">
  <img src="https://openmrs.org/wp-content/uploads/2021/08/cropped-OpenMRSlogo-transparent.png" alt="OpenMRS Smart IA Logo" width="300">
</p>

<p align="center">
  <a href="https://github.com/eltonlaice/openmrs-smart-ia/stargazers"><img src="https://img.shields.io/github/stars/eltonlaice/openmrs-smart-ia" alt="Stars Badge"/></a>
  <a href="https://github.com/eltonlaice/openmrs-smart-ia/network/members"><img src="https://img.shields.io/github/forks/eltonlaice/openmrs-smart-ia" alt="Forks Badge"/></a>
  <a href="https://github.com/eltonlaice/openmrs-smart-ia/pulls"><img src="https://img.shields.io/github/issues-pr/eltonlaice/openmrs-smart-ia" alt="Pull Requests Badge"/></a>
  <a href="https://github.com/eltonlaice/openmrs-smart-ia/issues"><img src="https://img.shields.io/github/issues/eltonlaice/openmrs-smart-ia" alt="Issues Badge"/></a>
  <a href="https://github.com/eltonlaice/openmrs-smart-ia/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/eltonlaice/openmrs-smart-ia?color=2b9348"></a>
  <a href="https://github.com/eltonlaice/openmrs-smart-ia/blob/master/LICENSE"><img src="https://img.shields.io/github/license/eltonlaice/openmrs-smart-ia?color=2b9348" alt="License Badge"/></a>
</p>

<p align="center">
  <i>Artificial Intelligence for your OpenMRS (Open Medical Record System)</i>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#features">Features</a> •
  <a href="#how-it-works">How It Works</a> •
  <a href="#getting-started">Getting Started</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a> •
  <a href="#contact">Contact</a>
</p>

## Overview

OpenMRS Smart IA is an innovative Flask-based project that integrates OpenMRS (Open Medical Record System) with OpenAI to provide intelligent responses to medical-related questions based on OpenMRS data.

This project creates a bridge between OpenMRS, a widely used open-source medical record system, and OpenAI's powerful language models. By leveraging the vast amount of medical data stored in OpenMRS and the natural language processing capabilities of OpenAI, OpenMRS Smart IA enables users to ask medical-related questions and receive informed answers based on real patient data.

## Features

- 🔗 Seamless integration with OpenMRS for accessing medical record data
- 🧠 Utilization of OpenAI's language models for natural language processing
- 🖥️ User-friendly interface for asking medical-related questions
- 📊 Data-driven responses based on OpenMRS information
- 🌐 RESTful API for easy integration with other healthcare systems

## How It Works

1. Users input medical-related questions through the application interface.
2. The system processes the questions using OpenAI's language models.
3. Relevant data is retrieved from the OpenMRS database.
4. The AI generates informative responses based on the OpenMRS data and the user's query.
5. The answer is presented to the user in a clear and understandable format.

## Getting Started

### Prerequisites

- Python 3.8+
- Flask
- OpenMRS instance
- OpenAI API key

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/eltonlaice/openmrs-smart-ia.git
   cd openmrs-smart-ia
   ```

2. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```sh
   cp .env.example .env
   ```
   Edit the `.env` file with your OpenMRS and OpenAI credentials.

4. Run the application:
   ```sh
   flask run
   ```

## Usage

To use the OpenMRS Smart IA API, you can send a POST request to the `/api/query` endpoint with your medical-related question. Here's an example using Python:

```python
import requests

url = "http://localhost:5000/api/query"
payload = {"question": "What is the average blood pressure of patients with diabetes?"}
response = requests.post(url, json=payload)

print(response.json())
```

The API will process your question, retrieve relevant data from OpenMRS, and return an AI-generated response based on the available information.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Elton Laice - [@eltonlaice](https://www.linkedin.com/in/eltontlaice/) - meu@eltonlaice.com

Project Link: [https://github.com/eltonlaice/openmrs-smart-ia](https://github.com/eltonlaice/openmrs-smart-ia)

---

<p align="center">
  Developed with ❤️ by <a href="https://www.linkedin.com/in/eltontlaice/">Elton Laice</a>
</p>