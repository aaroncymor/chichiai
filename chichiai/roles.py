from abc import ABC, abstractmethod

# custom
from exceptions import MethodNotImplementedError
from settings.config import OPENAI_API_KEY
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
    def _extract_role(self):
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

    def _extract_role(self):
        return "_extract_role"


class AnalystFinder(BaseRoleFinder):
    """"""

    def find_role(self):
        return "find_role"

    def _extract_role(self):
        return "_extract_role"


if __name__ == "__main__":
    ef = ExpertFinder()
