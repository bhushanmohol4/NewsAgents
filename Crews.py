from crewai import Crew, Process
from crewai.project import crew
from Agents import *
from Tasks import *

class crewService():
    def __init__(self, website_url, llm):
        self.llm = llm
        self.AgentService = agentService(website_url, llm)
        self.TaskService = taskService(website_url, llm)

    def fetch_content_crew(self):
        content_crew = Crew(
            agents = [self.AgentService.website_scraper(), self.AgentService.reporting_analyst()],
            model = self.llm,
            tasks = [self.TaskService.fetch_content_task(), self.TaskService.fetch_reporting_task()],
            cache = True,
            verbose = True,
            process = Process.sequential,
            planning = True,
            planning_llm = self.llm
        )

        return content_crew

    def fetch_podcast_crew(self):
        podcast_crew = Crew(
            agents = [self.AgentService.podcast_writer(), self.AgentService.audio_generator()],
            model = self.llm,
            tasks = [self.TaskService.fetch_script_task(), self.TaskService.fetch_audio_task()],
            cache = True,
            verbose = True,
            process = Process.sequential,
            planning = True,
            planning_llm = self.llm
        )

        return podcast_crew