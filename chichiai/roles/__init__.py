import pandas as pd
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, AIMessage, HumanMessagePromptTemplate

from .mixins import ManageCodeMixin
from .finders import AnalystFinder, ExpertFinder
from .experts import (
    DataAnalysisTheorist, InternetResearchSpecialist, UnknownExpert
)
from .analysts import DataAnalystDataFrame, DataAnalystGeneric
from .prompts import (
    SYSTEM_TASK_EVALUATION, SYSTEM_TASK_CLASSIFICATION,
    SYSTEM_ANALYST_SELECTION
)


class DataAnalystCodeManager(ManageCodeMixin):

    def __init__(self, analyst):
        self.analyst = analyst

    def generate_code(self):
        pass

    def _extract_code(self):
        pass

    def execute_code(self):
        pass

    def debug_code(self):
        pass


class TaskMaster:

    def __init__(self, llm, df: pd.DataFrame, search_tool: bool):
        self.df = df
        self.expert_finder = ExpertFinder(llm)
        self.analyst_finder = AnalystFinder(llm)
        self.search_tool = search_tool

    def _find_expert(self, question: str):
        pre_eval_messages = [
            SystemMessage(content=SYSTEM_TASK_CLASSIFICATION)
        ]

        expert, messages = self.expert_finder.find_role(
            question, pre_eval_messages)

        # updated pre_eval_messages from expert finder
        self.pre_eval_messages = messages

        eval_messages = [
            SystemMessage(content=SYSTEM_TASK_EVALUATION),
        ]

        if expert == "Data Analyst":
            print("Expert is Data Analyst")
            code_messages = []
            analyst = self._find_analyst(question)

            print("Finding Analyst")
            if analyst == "Data Analyst DF":
                print("Analyst is Data Analyst DF")
                return DataAnalystDataFrame(eval_messages, code_messages)

            if analyst == "Data Analyst Generic":
                print("Analyst is Data Analyst Generic")
                return DataAnalystDataFrame(eval_messages, code_messages)
                return DataAnalystGeneric(eval_messages, code_messages)

        if expert == "Data Analysis Theorist":
            print("Expert is Data Analysis Theorist")
            return DataAnalysisTheorist(eval_messages)

        if expert == "Internet Research Specialist":
            print("Expert Internet Research Specialist")
            return InternetResearchSpecialist(eval_messages, self.search_tool)

        print("Expert is Unknown")
        return UnknownExpert(eval_messages)

    def _find_analyst(self, question: str):
        select_analyst_messages = [
            SystemMessage(content=SYSTEM_ANALYST_SELECTION)
        ]
        analyst, messages = self.analyst_finder.find_role(
            question, select_analyst_messages, self.df)
        # updated select_analyst_messages
        self.select_analyst_messages = messages
        return analyst

    def evaluate_task(self, question: str):
        """"""
        expert = self._find_expert(question)
        # get eval messages from expert
        self.eval_messages = expert.eval_messages
        print("Expert eval messages", self.eval_messages)
        agent = expert.agent
        print("Expert agent", agent)

        # if expert is analyst, get code messages
        if expert.is_analyst:
            self.code_messages = expert.code_messages
            print("Expert code messages", self.code_messages)
