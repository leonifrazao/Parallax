<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![Unlicense License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Parallax</h3>

  <p align="center">
    An AI-powered news aggregator utilizing local LLMs to deduplicate, analyze context, and extract narratives!
    <br />
    <a href="https://github.com/leonifrazao/Parallax"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/leonifrazao/Parallax">View Demo</a>
    &middot;
    <a href="https://github.com/leonifrazao/Parallax/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/leonifrazao/Parallax/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#architecture">Architecture</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Parallax is a complete AI-driven pipeline designed for fetching news, extracting headlines, intelligently deduplicating similar coverage, and leveraging local LLMs (via Ollama) to output coherent, analyzed "Narratives".

The system doesn't just display news links; it deeply reads their headlines and metadata to:
1. **Scrape**: Gathers headlines across the web via provider integrations like NewsAPI based on a targeted query.
2. **Deduplicate**: Uses advanced string metrics (`RapidFuzz`) to remove duplicate headlines covering the exact same event across different outlets.
3. **Analyze**: Routes the curated list through an LLM via Ollama to determine each news item's `stance`, `emotional_tone`, `key_entities`, and `motives`.
4. **Export**: Yields structured JSON endpoints in a RESTful format for easy downstream integration or direct saving to the filesystem.

The application is built heavily on Dependency Injection principles and runs within a microservices-inspired architecture via Docker Compose.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.org]][Python-url] (Python >= 3.12)
* [![FastAPI][FastAPI.tiangolo]][FastAPI-url]
* [![Docker][Docker.com]][Docker-url]
* [![Ollama][Ollama.com]][Ollama-url]
* **UV**: Ultra-fast Python package installer and resolver.
* **RapidFuzz**: High-speed string matching library to handle deduplication.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Architecture

Parallax separates concerns into three primary microservices deployed using Docker Compose:

1. **Pipeline Service (Port `8000`)**
   - **Role**: The core orchestrator and the primary API gateway for users.
   - **Workflow**: Receives queries -> Calls Scraper Service -> Deduplicates headlines (`HeadlineDeduplicator`) -> Limits responses -> Calls Analysis Service -> Returns final `Narratives`.

2. **Scraper Service (Port `8001`)**
   - **Role**: Specialized in fetching unstructured or semi-structured data.
   - **Workflow**: Safely manages external API tokens and queries platforms (like NewsAPI) to return raw headlines and URLs.

3. **Analysis Service (Port `8002`)**
   - **Role**: LLM Handler.
   - **Workflow**: Ingests limited, deduplicated headlines and interfaces directly with `OLLAMA_HOST` to convert raw text into a rich analytical structure.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Follow these simple steps to configure your environment and run Parallax locally.

### Prerequisites

You need Docker, Docker Compose, and a local instance of Ollama to run the text analysis models. 

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop).
2. Install [Ollama](https://ollama.com/) locally and pull your preferred model (by default, models like `llama3` or `mistral` are recommended):
   ```sh
   ollama run llama3
   ```
3. Get a free API Key at [NewsAPI](https://newsapi.org/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/leonifrazao/Parallax.git
   cd parallax
   ```
2. Create your `.env` configuration file in the project's root based on your actual local environment setup.
   ```sh
   cp .env.example .env
   ```
3. Configure the secrets internally in your `.env` file:
   ```env
   NEWSAPI_KEY='your_newsapi_key_here'
   # Use host.docker.internal to allow Docker containers to access your local Ollama port
   OLLAMA_HOST='http://host.docker.internal:11434'
   ```
4. Build and launch all services using Docker Compose
   ```sh
   docker compose up --build
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Once up and running, you can interact with the Pipeline Service at `http://localhost:8000/pipeline`. 

### 1. Running a Pipeline Analysis
To trigger a pipeline run to aggregate, deduplicate, and analyze narratives, send a `POST` request.

**Endpoint**: `POST http://localhost:8000/pipeline`

**Request Payload**:
```json
{
  "query": "Artificial Intelligence",
  "limit": 5,
  "tojson": true
}
```

* `query`: The search term you wish to aggregate news on.
* `limit` (default: 10): Maximum narratives to analyze (keeps LLM fast).
* `tojson` (default: false): Automatically dumps analysis to the disk `output/` folder.

**cURL Example**:
```sh
curl -X 'POST' \
  'http://localhost:8000/pipeline' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "SpaceX",
  "limit": 3,
  "tojson": true
}'
```

### 2. Expected Response Model
The response will be an array of `Narrative` objects. Each parsed event will look like this:

```json
[
  {
    "id": "uuid-1234",
    "headline": "SpaceX Successfully Launches New Satellite",
    "stance": "Positive",
    "emotional_tone": "Triumphant",
    "emotional_intensity": 0.8,
    "key_entities": ["SpaceX", "Elon Musk", "NASA"],
    "narrative_summary": "Details the successful deployment of... ",
    "motives": ["Technological Advancement", "Commercial Expansion"],
    "url": "https://example.com/spacex-launch",
    "source": "TechCrunch"
  }
]
```

_For detailed interactive testing, visit the Swagger UI docs automatically generated by FastAPI:_
* **Pipeline Service Docs**: `http://localhost:8000/docs`
* **Scraper Service Docs**: `http://localhost:8001/docs`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Integrate NewsAPI Scraper
- [x] Deduplication heuristics (`RapidFuzz`)
- [x] Ollama local model analysis
- [ ] Add more content scrapers (e.g. Reddit, Twitter via unofficial APIs)
- [ ] UI for Dashboard Analysis (Next.js / React)
- [ ] Multi-language Support (prompts & extraction)
    - [ ] Spanish
    - [ ] Portuguese

See the [open issues](https://github.com/leonifrazao/Parallax) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the Unlicense License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Leoni Frazão - leoni.frazao.oliveira@gmail.com

Project Link: [https://github.com/leonifrazao/Parallax](https://github.com/leonifrazao/Parallax)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com/)
* [Loguru](https://github.com/Delgan/loguru)
* [UV](https://github.com/astral-sh/uv)
* [RapidFuzz](https://github.com/maxbachmann/RapidFuzz)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/leonifrazao/Parallax.svg?style=for-the-badge
[contributors-url]: https://github.com/leonifrazao/Parallax/graphs/contributors
[forks-shield]: https://github.com/leonifrazao/Parallax.svg?style=for-the-badge
[forks-url]: https://github.com/leonifrazao/Parallax/network/members
[stars-shield]: https://img.shields.io/github/stars/leonifrazao/Parallax.svg?style=for-the-badge
[stars-url]: https://github.com/leonifrazao/Parallax/stargazers
[issues-shield]: https://img.shields.io/github/issues/leonifrazao/Parallax.svg?style=for-the-badge
[issues-url]: https://github.com/leonifrazao/Parallax/issues
[license-shield]: https://img.shields.io/github/license/leonifrazao/Parallax.svg?style=for-the-badge
[license-url]: https://github.com/leonifrazao/Parallax/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/leonifrazao
[product-screenshot]: images/screenshot.png

[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org
[FastAPI.tiangolo]: https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white
[FastAPI-url]: https://fastapi.tiangolo.com
[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://docker.com
[Ollama.com]: https://img.shields.io/badge/Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white
[Ollama-url]: https://ollama.com/
