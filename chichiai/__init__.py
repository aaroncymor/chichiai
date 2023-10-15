import os
from contextlib import redirect_stdout
import io
import time
import pandas as pd
import warnings

from chichiai.roles import AnalystFinder, ExpertFinder
from chichiai.settings import OPENAI_API_KEY
from chichiai.output_manager import OutputManager
from chichiai.prompts import (
    EXAMPLE_OUTPUT_DF, SYSTEM_TASK_CLASSIFICATION, SYSTEM_ANALYST_SELECTION,
    USER_ANALYST_SELECTION, ANALYST_TASK_EVALUATION, SYSTEM_TASK_DF,
    USER_TASK_DF
)

warnings.filterwarnings('ignore')

SUPPORTED_MODELS = {
    'llm_gpt4': "gpt-4-0613",
    'llm_16k': "gpt-3.5-turbo-16k",
    'llm_func': "gpt-3.5-turbo-0613"
}


class EnvironmentError(Exception):
    """
    Raised when a environment variable is not set.

    Args:
        Exception (Exception): EnvironmentError
    """
    pass


class ChiChiAI(object):
    def __init__(self,
                 llm: str = "gpt-3.5-turbo-0613",
                 df: pd.DataFrame = None,
                 max_conversations: int = 4,
                 exploratory: bool = True):
        self.analyst_finder = AnalystFinder()
        self.expert_finder = ExpertFinder()
        self.max_error_corrections = 5
        self.max_conversations = max_conversations
        self.df = df
        self.model_dict = SUPPORTED_MODELS.update({'llm': llm})
        self.output_manager = OutputManager()

    def pd_csv_agent(self, question: str = None) -> str:
        if not OPENAI_API_KEY:
            raise EnvironmentError((
                "Error: Environment variable OPENAI_API_KEY is not set"))
