from abc import ABC, abstractmethod


class ManageCodeMixin(ABC):
    """"""
    @abstractmethod
    def generate_code(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def _extract_code(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def execute_code(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def debug_code(self):
        """"""
        raise NotImplementedError


class FindRoleMixin(ABC):
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
            NotImplementedError: Select role method has not been implemented
        """
        raise NotImplementedError

    @abstractmethod
    def _extract_role(self, response: str, pattern: str) -> str:
        """
        Extract the role based on llm response

        Args:

        Raises:
            NotImplementedError: Select role method has not been implemented
        """
        raise NotImplementedError
