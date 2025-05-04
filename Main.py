from Crews import *
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Podcast Creator", layout="centered")
st.title("Podcast Creator")

# User inputs
llm_model = os.getenv("LLM_MODEL")
website_url = st.text_input("Enter Website URL to scrape content:")

# button to start the process
if st.button("Generate Podcast"):
    if not llm_model or not website_url:
        st.error("Please provide both the LLM model and the website URL.")
    else:
        llm = LLM(model = llm_model, base_url = "http://localhost:11434")
        
        CrewService = crewService(website_url, llm)
        try:
            # Website scraping
            st.info("Scraping the website. Please wait...")
            content_crew = CrewService.fetch_content_crew()
            content_result = content_crew.kickoff(inputs = {"website_url": website_url})

            # dump textual scraped news
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            scraped_file = os.path.join(output_dir, "scraped_news.txt")
            with open(scraped_file, "w", encoding="utf-8") as file:
                file.write(str(content_result))
            st.success("News content successfully scraped and processed.")

            # Podcast generation
            st.info("Starting the podcast generation process. Please wait...")
            podcast_crew = CrewService.fetch_podcast_crew()
            podcast_result = podcast_crew.kickoff(inputs = {"content": str(content_result)})
            st.success("Podcast generated successfully.")

            # audio download link in the UI
            podcast_dir = "TTS/Recordings"
            latest_podcast_file = max(
                (os.path.join(podcast_dir, f) for f in os.listdir(podcast_dir) if f.endswith(".wav")),
                key=os.path.getmtime,
                default=None 
            )
            if latest_podcast_file and os.path.exists(latest_podcast_file):
                st.audio(latest_podcast_file, format="audio/wav")
                st.download_button(
                    label = "Download Podcast",
                    data = open(latest_podcast_file, "rb").read(),
                    file_name = os.path.basename(latest_podcast_file),
                    mime = "audio/wav"
                )
            else:
                st.error("No podcast file found. Please ensure the podcast generation was successful.")

        except Exception as e:
            st.error(f"An error occurred: {e}")