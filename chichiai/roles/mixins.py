from abc import ABC, abstractmethod


class EvaluateTaskMixin(ABC):
    """"""
    pass


class ManageCodeMixin(ABC):
    """"""

    @abstractmethod
    def generate_code(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def extract_code(self):
        """"""
        raise NotImplementedError

    @abstractmethod
    def execute_code(self):
        """"""
        raise NotImplementedError


class FinderMixin(ABC):
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
        raise NotImplementedError

    @abstractmethod
    def _extract_role(self, response: str, pattern: str) -> str:
        """
        Extract the role based on llm response

        Args:

        Raises:
            MethodNotImplementedError: Select role method has not been implemented
        """
        raise NotImplementedError
