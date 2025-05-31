from Crews import *
from crewai import LLM
import os
import json
import streamlit as st
from dotenv import load_dotenv
from Logging.Logger import logger

load_dotenv()

def ensure_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/Recordings", exist_ok=True)
    os.makedirs("Tools", exist_ok=True)

def cleanup_old_files():
    """Clean up old output files to prevent confusion."""
    try:
        if os.path.exists("output/podcast_script.json"):
            os.remove("output/podcast_script.json")
            if os.path.exists("output/scraped_news.txt"):
                os.remove("output/scraped_news.txt")
            if os.path.exists("output/podcast_script_raw.json"):
                os.remove("output/podcast_script_raw.json")
            if os.path.exists("output/Recordings/podcast.wav"):
                os.remove("output/Recordings/podcast.wav")
    except Exception as e:
        st.warning(f"Could not clean up old files: {e}")

st.set_page_config(page_title="Podcast Creator", layout="centered")
st.title("Podcast Creator")

# Initialize session state for progress
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# User inputs
llm_model = os.getenv("LLM_MODEL")
llm_url = os.getenv("API_BASE")
website_url = st.text_input("Enter Website URL to scrape content:")

# button to start the process
if st.button("Generate Podcast"):
    logger.info("------Starting podcast generation process------")
    if not llm_model or not website_url:
        st.error("Please provide both the LLM model and the website URL.")
    else:
        try:
            # Setup
            ensure_directories()
            cleanup_old_files()
            progress_bar = st.progress(0)
            
            llm = LLM(model = llm_model, base_url = llm_url, api_key = "not-needed")
            CrewService = crewService(website_url, llm)

            # Website scraping
            with st.spinner("Scraping the website. Please wait..."):
                logger.info("Scraping the website")
                content_crew = CrewService.fetch_content_crew()
                content_result = content_crew.kickoff(inputs={"website_url": website_url})
                st.session_state.progress = 30
                progress_bar.progress(st.session_state.progress)
                
                if not os.path.exists("output/scraped_news.txt"):
                    logger.error("Failed to generate scraped news file")
                    raise FileNotFoundError("Failed to generate scraped news file")
                
                st.success("News content successfully scraped and processed.")
                logger.info("News content successfully scraped and processed.")

            # Podcast script generation
            with st.spinner("Generating podcast script..."):
                logger.info("Generating podcast script")
                podcast_script_crew = CrewService.fetch_podcast_script_crew()
                podcast_script_result = podcast_script_crew.kickoff(inputs={"content": str(content_result)})
                st.session_state.progress = 60
                progress_bar.progress(st.session_state.progress)

                # Verify JSON script was created
                if not os.path.exists("output/podcast_script.json"):
                    logger.error("Failed to generate podcast script")
                    raise FileNotFoundError("Failed to generate podcast script")
                
                # Validate JSON format
                with open("output/podcast_script.json", 'r', encoding='utf-8') as f:
                    script_data = json.load(f)
                    if not isinstance(script_data, list) or not all(isinstance(item, dict) and 'speaker' in item and 'text' in item for item in script_data):
                        logger.error("Invalid podcast script format")
                        raise ValueError("Invalid podcast script format")

                st.success("Podcast script generated successfully.")

            # Podcast audio generation
            with st.spinner("Generating podcast audio..."):
                logger.info("Generating podcast audio")
                podcast_audio_crew = CrewService.fetch_podcast_audio_crew()
                podcast_audio_result = podcast_audio_crew.kickoff(inputs={"script": str(podcast_script_result)})
                st.session_state.progress = 90
                progress_bar.progress(st.session_state.progress)
                
            # Audio file handling
            with st.spinner("Processing audio file..."):
                podcast_dir = "output/Recordings"
                latest_podcast_file = max(
                    (os.path.join(podcast_dir, f) for f in os.listdir(podcast_dir) if f.endswith(".wav")),
                    key=os.path.getmtime,
                    default=None
                )

                if latest_podcast_file and os.path.exists(latest_podcast_file):
                    st.session_state.progress = 100
                    progress_bar.progress(st.session_state.progress)
                    
                    # Display audio player
                    st.audio(latest_podcast_file, format="audio/wav")
                    
                    # Add download button
                    with open(latest_podcast_file, "rb") as f:
                        st.download_button(
                            label="Download Podcast",
                            data=f.read(),
                            file_name=os.path.basename(latest_podcast_file),
                            mime="audio/wav"
                        )
                    
                    # Display script preview
                    with st.expander("View Podcast Script"):
                        for line in script_data:
                            st.markdown(f"**{line['speaker']}**: {line['text']}")
                else:
                    raise FileNotFoundError("No podcast file found. Please ensure the podcast generation was successful.")

        except FileNotFoundError as e:
            st.error(f"File Error: {str(e)}")
        except json.JSONDecodeError:
            st.error("Error: Invalid JSON format in podcast script")
        except ValueError as e:
            st.error(f"Validation Error: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Reset progress if there was an error
            if st.session_state.progress != 100:
                st.session_state.progress = 0
                progress_bar.progress(st.session_state.progress)