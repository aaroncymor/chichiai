from abc import ABC, abstractmethod

from ..exceptions import MethodNotImplementedError


class BaseRoleFinder(ABC):
    """"""

    def __init__(self, llm):
        self.llm = llm

    @abstractmethod
    def find_role(self, question: str, *args, **kwargs) -> str:
        """
        Select the role based on llm response

        Args:
            messages (list): List of messages accepted by langchain
        Raises:
            MethodNotImplementedError: Select role method has not been implemented
        """
        raise MethodNotImplementedError(
            "Select role method has not been implemented")

    @abstractmethod
    def _extract_role(self, response: str, pattern: str) -> str:
        """
        Extract the role based on llm response

        Args:

        Raises:
            MethodNotImplementedError: Select role method has not been implemented
        """
        raise MethodNotImplementedError(
            "Select role method has not been implemented")
