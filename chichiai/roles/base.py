from abc import ABC, abstractmethod


class MethodNotImplementedError(Exception):
    """
    Raised when a method is not implemented.

    Args:
        Exception (Exception): MethodNotImplementedError
    """


class BaseRoleFinder(ABC):
    """"""

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
    def _extract_role(self, response: str) -> str:
        """
        Extract the role based on llm response

        Args:

        Raises:
            MethodNotImplementedError: Select role method has not been implemented
        """
        raise MethodNotImplementedError("Select role method has not been implemented")
