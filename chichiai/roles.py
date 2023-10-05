from abc import ABC, abstractmethod
from exceptions import MethodNotImplementedError
from settings.config import *


class BaseRoleFinder(object):
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
    pass


class AnalystFinder(BaseRoleFinder):
    pass
