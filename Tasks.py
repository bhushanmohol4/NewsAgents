from Agents import *
from crewai import Task
from crewai.project import CrewBase, agent, task, crew, before_kickoff, after_kickoff


class taskService():
    def __init__(self, website_url, llm):
        self.website_url = website_url
        self.AgentService = agentService(website_url, llm)
    
    def fetch_content_task(self):
        content_task = Task(
                    description = (
                        "Scrape and clean content from the specified website URL: {website_url}. "
                        "Extract all relevant details and maintain the context. The language MUST be English."
                    ),
                    expected_output = "A full report with the main topics, in English.",
                    agent = self.AgentService.website_scraper()
                )
        
        return content_task
    
    def fetch_reporting_task(self):
        reporting_task = Task(
            description=(
                "Review the scraped content and expand each topic into a full section. "
                "Produce a detailed and in-depth report focusing on all relevant aspects on the main topic. "
                "you must avoid using titles or subtitles, just use a plain text."
                "If there are multiple different topics, generate a report that provides key insights and essential highlights for each one."
            ),
            expected_output="A detailed report in English with around 6 paragraphs.",
            agent = self.AgentService.reporting_analyst()
        )

        return reporting_task

    def fetch_script_task(self):
        script_task = Task(
            description=(
                "Write a podcast script based on the processed content: {content}. "
                "Structure the script as a conversation between two speakers: 'Host' and 'Guest'"
                "Ensure the script is structured as a natural dialogue and is in English. You must avoid using titles or subtitles. "
                "Always start the script saying the name of the podcast: 'Welcome to Daily News'. "
                "If there are multiple topics, produce a smaller script for each. "
                "Output the conversation as a JSON list, where each item has 'speaker' and 'text' fields. "
                "For example: [{\"speaker\": \"Host\", \"text\": \"Welcome to Daily News.\"}, {\"speaker\": \"Guest\", \"text\": \"Thank you for having me.\"}]"
            ),
            expected_output = "A structured podcast script with a single speaker in English.",
            agent = self.AgentService.podcast_writer(),
            output_file = "output/podcast_script.txt"
        )

        return script_task

    def fetch_audio_task(self):
        audio_task = Task(
            description=(
                "Generate an mp3 audio file from the podcast script using text-to-speech synthesis. "
                "Assume two speakers. Produce an audio file in English."
            ),
            expected_output = "TTS/Recordings/podcast.mp3",
            agent = self.AgentService.audio_generator()
        )

        return audio_task