from crewai import Crew, Process
from crewai.project import crew
from Agents import *
from Tasks import *
import os
from datetime import datetime

class crewService():
    def __init__(self, website_url, llm):
        self.llm = llm
        self.AgentService = agentService(website_url, llm)
        self.TaskService = taskService(website_url, llm)
        today = datetime.now().strftime('%Y-%m-%d')
        self.crewaiLogDir = os.path.join("Logging/Logs", f'crewai_{today}')

        # Ensure output directories exist
        os.makedirs("output", exist_ok = True)
        os.makedirs("output/Recordings", exist_ok = True)

    def fetch_content_crew(self):
        content_crew = Crew(
            agents = [self.AgentService.website_scraper(), 
                      self.AgentService.reporting_analyst()],
            tasks = [self.TaskService.fetch_content_task(), 
                     self.TaskService.fetch_reporting_task()],
            cache = True,
            verbose = True,
            process = Process.sequential,
            planning = True,
            planning_llm = self.llm,
            max_rpm = 10,

        )

        return content_crew

    def fetch_podcast_script_crew(self):
        # Ensure directories exist before starting the crew
        os.makedirs("output", exist_ok=True)
        os.makedirs("TTS/Recordings", exist_ok=True)
        
        podcast_script_crew = Crew(
            agents = [self.AgentService.podcast_writer(), 
                      self.AgentService.podcast_cleaner()],
            tasks = [self.TaskService.fetch_script_task(), 
                     self.TaskService.fetch_clean_script_task()],
            cache = True,
            verbose = True,
            process = Process.sequential,
            planning = True,
            planning_llm = self.llm,
            max_rpm = 10,
            output_log_file = self.crewaiLogDir
        )

        return podcast_script_crew
