from crewai import Agent, LLM
from crewai_tools import ScrapeWebsiteTool
from crewai.project import agent
from TTS.Service import ttsService

class agentService():
    def __init__(self, website_url, llm):
        self.website_scraper_tool = ScrapeWebsiteTool(website_url = website_url)
        self.llm = llm

    def website_scraper(self):
        website_scraper = Agent(
            role = "Website Content Scraper",
            goal = "Extract the main content of the specified website URL: {website_url}, ensuring the content is in English.",
            backstory = (
                "You're an expert in scraping and extracting meaningful information from web pages. "
                "You ensure the scraped content is clean, relevant, and easy to process, always ensuring it is in English."
            ),
            tools = [self.website_scraper_tool],
            llm = self.llm
        )

        return website_scraper

    def reporting_analyst(self):
        reporting_analyst = Agent(
            role = "Senior Reporting Analyst",
            goal = "Create detailed reports based on received content, analyzing data and findings, ensuring all content is in English.",
            backstory = (
                "You're a meticulous analyst with a keen eye for detail, especially when it comes to statistics and data. "
                "You are skilled in transforming complex information into structured reports, always in English. "
                "Concentrate only on the major topic and produce a detailed and in-depth report focusing on all relevant aspects. "
                "If there are multiple topics, generate a report that provides key insights and essential highlights for each one in numbered sections."
            ),
            llm = self.llm
        )

        return reporting_analyst

    def podcast_writer(self):
        podcast_writer = Agent(
            role = "Podcast Script Writer",
            goal = "Convert the processed content into a structured podcast conversation between two speakers in English.",
            backstory = (
                "You're a skilled content creator with experience in writing engaging and natural podcast dialogues in English."
            ),
            llm = self.llm
        )

        return podcast_writer

    def audio_generator(self):
        audio_generator = Agent(
            role = "Audio Producer",
            goal = "Generate an mp3 audio file from the podcast script in English.",
            backstory = (
                "You're an expert in text-to-speech synthesis and audio production. "
                "You ensure that the podcast narration is of high quality and is produced in English."
            ),
            tools = [ttsService()],
            llm = self.llm
        )

        return audio_generator