import os
import json

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from dotenv import load_dotenv
load_dotenv()

class SchemaConverter:
    @staticmethod
    def build(json_schema):
        # Implementation of schema conversion
        return json_schema

@CrewBase
class TextResponseAutomationCrew:
    """TextResponseAutomation crew"""

    @agent
    def text_response_assistant(self) -> Agent:
        return Agent(
            config=self.agents_config["text_response_assistant"],
            tools=[],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gemini/gemini-2.5-flash-lite",
                temperature=0.7,
            ),
        )

    @task
    def process_user_text_input(self) -> Task:
        return Task(
            config=self.tasks_config["process_user_text_input"],
            markdown=False,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the TextResponseAutomation crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
