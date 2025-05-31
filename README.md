# Podcast Creator

An AI-powered podcast generation tool that scrapes content from websites, creates engaging podcast scripts, and generates audio using text-to-speech technology.

## Features

- **Content Scraping**: Extracts relevant content from any website
- **Script Generation**: Creates natural-sounding podcast scripts with host-guest dialogue
- **Audio Generation**: Converts scripts to high-quality audio using Bark TTS
- **Streamlit Interface**: User-friendly web interface for easy interaction

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended for faster TTS generation)
- LM Studio running locally with a compatible model

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/podcast-creator.git
cd podcast-creator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Download required NLTK data:
```bash
python -c "import nltk; nltk.download('punkt')"
```

## Configuration

1. Create a `.env` file in the project root:
```env
LLM_MODEL = 'model-name'
API_BASE = 'local-server-&-lm-studio-endpoint'
```

2. Start LM Studio:
   - Load your preferred model
   - Enable the API server
   - Make changes to env file accordingly

## Project Structure

podcast-creator/
├── Agents.py # Agent definitions for content processing
├── Crews.py # Crew configurations for task orchestration
├── Main.py # Main application and Streamlit interface
├── Tasks.py # Task definitions for the agents
├── TTS/
│ ├── Bark.py # Bark TTS implementation
│ └── Service.py # TTS service wrapper
├── Tools/
│ └── ReadScriptTool.py # JSON script processing tool
├── Logging/
│ └── Logger.py # Logging configuration
├── output/ # Generated content directory
│ ├── scraped_news.txt
│ └── podcast_script.json
│ └── Recordings/ # Generated audio files

## Usage

1. Start the Streamlit application:
```bash
streamlit run Main.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Enter a website URL in the input field

4. Click "Generate Podcast" to start the process:
   - Content scraping
   - Script generation
   - Audio generation

5. The generated podcast will be saved in `TTS/Recordings/podcast.wav`

## Workflow

1. **Content Scraping**:
   - Website content is scraped and processed
   - Content is saved to `output/scraped_news.txt`

2. **Script Generation**:
   - Content is converted into a podcast script
   - Script is saved as JSON in `output/podcast_script.json`

3. **Audio Generation**:
   - Script is converted to audio using Bark TTS
   - Audio is saved to `TTS/Recordings/podcast.wav`

## Dependencies

- `crewai`: For AI agent orchestration
- `streamlit`: For the web interface
- `soundfile`: For audio file handling
- `numpy`: For audio processing
- `torch`: For TTS model
- `transformers`: For Bark TTS model
- `nltk`: For text processing
- `python-dotenv`: For environment variable management
