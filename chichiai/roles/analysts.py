from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
from .prompts import (
    SYSTEM_TASK_DF, USER_TASK_DF, SYSTEM_TASK_GENERIC, USER_TASK_GENERIC
)


class DataAnalystDataFrame:
    """
    DF means `DataFrame`
    """
    is_analyst = True
    agent = 'Planner'

    def __init__(self, eval_messages, code_messages):
        self.eval_messages = eval_messages
        self.eval_messages.append(HumanMessagePromptTemplate\
                             .from_template(USER_TASK_DF))
        self.code_messages = code_messages
        self.code_messages.append(SystemMessage(content=SYSTEM_TASK_DF))


class DataAnalystGeneric:
    """"""
    is_analyst = True
    agent = 'Planner'

    def __init__(self, eval_messages, code_messages):
        self.eval_messages = eval_messages
        self.eval_messages.append(HumanMessagePromptTemplate\
                             .from_template(USER_TASK_GENERIC))
        self.code_messages = code_messages
        self.code_messages.append(SystemMessage(content=SYSTEM_TASK_GENERIC))
