from crewai import Agent
from crewai_tools import ScrapeWebsiteTool
from TTS.Service import ttsService
from Tools.ReadScriptTool import ReadScriptTool

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
            llm = self.llm,
            verbose = True
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
            llm = self.llm,
            verbose = True
        )

        return reporting_analyst

    def podcast_writer(self):
        podcast_writer = Agent(
            role = "Podcast Script Writer",
            goal = "Convert the processed content into a structured podcast conversation between two speakers in English.",
            backstory = (
                "You're a skilled content creator with experience in writing engaging and natural podcast dialogues in English. "
                "You excel at creating natural-sounding conversations that maintain the original content's meaning while being engaging for listeners."
            ),
            llm = self.llm,
            verbose = True
        )

        return podcast_writer
    
    def podcast_cleaner(self):
        podcast_cleaner = Agent(
            role = "Podcast Script Cleaner",
            goal = "Clean the json file to ensure it is in the correct format.",
            backstory = "A data processing expert who ensures JSON files are properly formatted.",
            tools = [ReadScriptTool()],
            llm = None,
            function_calling_llm = self.llm,
            verbose = True
        )

        return podcast_cleaner

    def audio_generator(self):
        audio_generator = Agent(
            role = "Audio Producer",
            goal = "Generate a high-quality audio file from the podcast script in English.",
            backstory = "An audio processing expert who converts text to speech.",
            tools = [ttsService()],
            llm = None,
            function_calling_llm = self.llm,
            verbose = True
        )

        return audio_generator