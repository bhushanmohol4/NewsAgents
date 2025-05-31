from Agents import *
from crewai import Task

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
                "If there are multiple different topics, generate a report that provides key insights and essential highlights for each one."
            ),
            expected_output = "A detailed report in English with around 6 paragraphs.",
            agent = self.AgentService.reporting_analyst(),
            output_file = "output/scraped_news.txt"
        )

        return reporting_task

    def fetch_script_task(self):
        script_task = Task(
            description=(
                "Write a podcast script based on the processed content: {content}. "
                "Structure the script as a conversation between two speakers: 'Host' and 'Guest'. "
                "The 'Host' is a host of a news podcast and the 'Guest' is a guest who will be talking about the news. "
                "Ensure the script is structured as a natural dialogue in English where the 'Host' is asking relevant questions to the 'Guest' and the 'Guest' is answering the questions. "
                "Always start the script saying the name of the podcast: 'Welcome to Daily News'. "
                "If there are multiple topics, produce a smaller script for each. "
                "The output should be a clean JSON list where each item has 'speaker' and 'text' fields. "
                "Example format: [{\"speaker\": \"Host\", \"text\": \"Welcome to Daily News.\"}, {\"speaker\": \"Guest\", \"text\": \"Thank you for having me.\"}]"
            ),
            expected_output = "A clean JSON array containing the podcast script with speaker and text fields.",
            agent = self.AgentService.podcast_writer(),
            output_file = "output/podcast_script_raw.json"
        )

        return script_task
    
    
    def fetch_clean_script_task(self):
        clean_script_task = Task(
            description = (
                "Clean and validate the podcast script JSON file. "
                "Read the podcast script from output/podcast_script_raw.json. "
                "Use the ReadScriptTool to clean the json file and save it to output/podcast_script.json. "
                "The format for the clean JSON list should include a 'speaker' and 'text' fields for each item. "
                "Example format: [{\"speaker\": \"Host\", \"text\": \"Welcome to Daily News.\"}, {\"speaker\": \"Guest\", \"text\": \"Thank you for having me.\"}]"
            ),
            expected_output = "A clean JSON array containing the podcast script with speaker and text fields.",
            agent = self.AgentService.podcast_cleaner(),
            output_file = "output/podcast_script.json"
        )

        return clean_script_task