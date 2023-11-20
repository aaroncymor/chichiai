import re
import pandas as pd

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import AIMessage, HumanMessagePromptTemplate

from .mixins import FindRoleMixin
from .patterns import EXPERT_FINDER_PATTERN, ANALYST_FINDER_PATTERN
from .prompts import USER_ANALYST_SELECTION

from ..utils import OutputManager


class ExpertFinder(FindRoleMixin):
    """"""
    agent = "Expert Selector"

    def _extract_role(self, response: str, pattern: str) -> str:
        # Create a pattern to match any of the substrings
        # Use re.search to find the first match in the input string
        match = re.search(pattern, response)

        if match:
            # If a match is found, return it
            return match.group()
        # If no match is found, return None
        return None

    def find_role(self, question: str, pre_eval_messages: list) -> str:
        pre_eval_messages.append(HumanMessagePromptTemplate\
                                      .from_template("{question}"))
        template = ChatPromptTemplate.from_messages(pre_eval_messages)
        response = self.llm(template.format_messages(question=question))
        expert = self._extract_role(response.content, EXPERT_FINDER_PATTERN)
        pre_eval_messages.append(AIMessage(content=expert))
        return (expert, pre_eval_messages)


class AnalystFinder(FindRoleMixin):
    """"""
    agent = "Analyst Selector"

    def _extract_role(self, response: str, pattern: str) -> str:
        # Create a pattern to match any of the substrings
        # Use re.search to find the first match in the input string
        match = re.search(pattern, response)

        if match:
            # If a match is found, return it
            return match.group()
        # If no match is found, return None
        return None

    def find_role(self,
                  question: str,
                  select_analyst_messages: list,
                  dataframe: pd.DataFrame) -> str:
        columns = dataframe.columns.tolist()
        select_analyst_messages.append(HumanMessagePromptTemplate\
                                            .from_template(USER_ANALYST_SELECTION))
        template = ChatPromptTemplate.from_messages(select_analyst_messages)
        response = self.llm(template.format_messages(question=question,
                                                     dataframe=columns))
        analyst = self._extract_role(response.content, ANALYST_FINDER_PATTERN)
        select_analyst_messages.append(AIMessage(content=analyst))
        return (analyst, select_analyst_messages)
