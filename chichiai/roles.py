from abc import ABC, abstractmethod

# custom
from exceptions import MethodNotImplementedError
from settings.config import OPENAI_API_KEY
from utils import reg_ex as regex
from prompts import *


class BaseRoleFinder(ABC):

    def __init__(self, llm):
        self.llm = llm

    @abstractmethod
    def find_role(self):
        """
        Select the role based on llm response

        Args:

        Raises:
            MethodNotImplementedError: Select role method has not been implemented
        """
        raise MethodNotImplementedError("Select role method has not been implemented")

    @abstractmethod
    def _extract_role(self, response:str) -> str:
        """
        Extract the role based on llm response

        Args:

        Raises:
            MethodNotImplementedError: Select role method has not been implemented
        """
        raise MethodNotImplementedError("Select role method has not been implemented")


class ExpertFinder(BaseRoleFinder):
    """"""

    def find_role(self):
        return "find_role"

    def _extract_role(self, response:str) -> str:
        return regex._extract_expert(response)


class AnalystFinder(BaseRoleFinder):
    """"""

    def find_role(self):
        return "find_role"

    def _extract_role(self, response):
        return regex._extract_analyst(response)


if __name__ == "__main__":
    ef = ExpertFinder("test")
