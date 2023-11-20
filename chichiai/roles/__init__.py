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
        self.llm = llm
        self.search_tool = search_tool

    def _find_expert(self, question: str):
        # declare pre_eval_messages
        pre_eval_messages = [
            SystemMessage(content=SYSTEM_TASK_CLASSIFICATION)
        ]

        expert, pre_eval_messages = self.expert_finder.find_role(
            question, pre_eval_messages)

        # assign updated pre_eval_messages
        self.pre_eval_messages = pre_eval_messages

        # declare eval_messages
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
        analyst, select_analyst_messages = self.analyst_finder.find_role(
            question, select_analyst_messages, self.df)

        # assign updated select_analyst_messages
        self.select_analyst_messages = select_analyst_messages
        return analyst

    def evaluate_task(self, question: str):
        """"""
        expert = self._find_expert(question)

        # get eval messages from expert
        eval_messages = expert.eval_messages
        print("Eval messages", eval_messages)
        template = ChatPromptTemplate.from_messages(eval_messages)

        tasks = None
        print("Evaluating tasks")
        if expert.is_analyst:
            print("Evaluating analyst task")
            response = self.llm(template.format_messages(
                question=question,
                dataframe=self.df.head(1)
            ))
            tasks = response.content
            eval_messages.append(AIMessage(content=response.content))

            # assign new code_messages
            self.code_messages = expert.code_messages
        else:
            print("Evaluating expert task")
            response = self.llm(template.format(question=question))
            eval_messages.append(AIMessage(content=response.content))

        # assign updated eval_messages
        self.eval_messages = eval_messages
        return tasks
