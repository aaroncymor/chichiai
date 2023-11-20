from langchain.prompts.chat import SystemMessage, AIMessage, HumanMessagePromptTemplate
from .prompts import USER_TASK_THEORIST, GOOGLE_SEARCH_QUERY_GENERATOR


class UnknownExpert:
    is_analyst = False
    agent = 'Unknown'

    def __init__(self, eval_messages):
        self.eval_messages = eval_messages
        self.eval_messages.append(HumanMessagePromptTemplate.from_template(
            USER_TASK_THEORIST))

class DataAnalysisTheorist:
    is_analyst = False
    agent = 'Theorist'

    def __init__(self, eval_messages):
        self.eval_messages = eval_messages
        self.eval_messages.append(HumanMessagePromptTemplate.from_template(
            USER_TASK_THEORIST))


class InternetResearchSpecialist:
    is_analyst = False
    agent = 'Theorist'

    def __init__(self, eval_messages, search_tool):
        self.eval_messages = eval_messages
        if search_tool:
            self.agent = 'Google Search Query Generator'
            self.eval_messages.append(HumanMessagePromptTemplate.from_template(
                                 GOOGLE_SEARCH_QUERY_GENERATOR))
        else:
            self.eval_messages.append(HumanMessagePromptTemplate.from_template(
                                USER_TASK_THEORIST))
