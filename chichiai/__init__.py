import os
from contextlib import redirect_stdout
import io
import time
import warnings

import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessage, AIMessage, HumanMessagePromptTemplate

from chichiai.roles import AnalystFinder, ExpertFinder
from chichiai.settings import OPENAI_API_KEY
from chichiai.output_manager import OutputManager
from chichiai.prompts import (
    EXAMPLE_OUTPUT_DF, SYSTEM_TASK_EVALUATION, ANALYST_TASK_EVALUATION_DF,
    SYSTEM_TASK_DF, USER_TASK_DF
)
from chichiai.exceptions import EnvironmentError, UnsupportedModelError

warnings.filterwarnings('ignore')

SUPPORTED_MODELS = {}

SUPPORTED_CHAT_MODELS = {
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-16k',
    'gpt-4-0613',
}


class ChiChiAI(object):
    """"""

    def __init__(self,
                 df: pd.DataFrame = None,
                 llm: str = "gpt-3.5-turbo-0613",
                 max_conversations: int = 4,
                 exploratory: bool = True):

        self.df = df

        # chat model only supported at the moment
        all_supported_models = SUPPORTED_CHAT_MODELS
        if SUPPORTED_MODELS:
            all_supported_models.update(SUPPORTED_MODELS)

        if llm not in all_supported_models:
            raise UnsupportedModelError(llm)

        if not OPENAI_API_KEY:
            raise EnvironmentError((
                "Error: Environment variable OPENAI_API_KEY is not set"))

        if llm in SUPPORTED_CHAT_MODELS:
            # use chat completion
            self.llm = ChatOpenAI(
                temperature=0,
                openai_api_key=OPENAI_API_KEY,
                model=llm
            )

        # instantiate classes
        self.analyst_finder = AnalystFinder(self.llm)
        self.expert_finder = ExpertFinder(self.llm)
        self.output_manager = OutputManager()

        self.max_error_corrections = 5
        self.max_conversations = max_conversations

    def pd_csv_agent_converse(self, question: str = None) -> str:
        dataframe_head = self.df.head(1)
        print("DF HEAD 1", dataframe_head)

        expert, pre_eval_messages = self.expert_finder.find_role(question)
        print("EXPERT", expert)
        print("PRE EVAL MESSAGES", pre_eval_messages)
        if expert == "Data Analyst":
            analyst, system_analyst_messages = self.analyst_finder.find_role(
                question, self.df)
            print("ANALYST", analyst)
            print("SYSTEM ANALYST MESSAGES", system_analyst_messages)
            if analyst == "Data Analyst DF":
                eval_messages = [
                    SystemMessage(content=SYSTEM_TASK_EVALUATION),
                    HumanMessagePromptTemplate.from_template(
                        ANALYST_TASK_EVALUATION_DF)
                ]
                template = ChatPromptTemplate.from_messages(eval_messages)
                response = self.llm(template.format_messages(
                    question=question,
                    dataframe=dataframe_head
                ))
                print("RESPONSE CONTENT TASKS", response.content)
