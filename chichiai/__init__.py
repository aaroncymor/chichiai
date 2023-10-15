import os
from contextlib import redirect_stdout
import io
import time
import warnings

import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage

from chichiai.roles import AnalystFinder, ExpertFinder
from chichiai.settings import OPENAI_API_KEY
from chichiai.output_manager import OutputManager
from chichiai.prompts import (
    EXAMPLE_OUTPUT_DF, SYSTEM_TASK_CLASSIFICATION, SYSTEM_ANALYST_SELECTION,
    USER_ANALYST_SELECTION, ANALYST_TASK_EVALUATION, SYSTEM_TASK_DF,
    USER_TASK_DF
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
                 llm: str = "gpt-3.5-turbo-0613",
                 df: pd.DataFrame = None,
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
        self.analyst_finder = AnalystFinder(llm)
        self.expert_finder = ExpertFinder(llm)
        self.output_manager = OutputManager()

        self.max_error_corrections = 5
        self.max_conversations = max_conversations

    def pd_csv_agent(self, question: str = None) -> str:
        pass
