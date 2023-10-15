import re

from .base import BaseRoleFinder
from .patterns import EXPERT_FINDER_PATTERN, ANALYST_FINDER_PATTERN


class ExpertFinder(BaseRoleFinder):
    """"""
    def _extract_role(response: str, pattern: str) -> str:

        # Create a pattern to match any of the substrings
        # Use re.search to find the first match in the input string
        match = re.search(pattern, response)

        if match:
            # If a match is found, return it
            return match.group()
        else:
            # If no match is found, return None
            return None

    def find_role(self, response: str) -> str:
        return self._extract_role(response, EXPERT_FINDER_PATTERN)


class AnalystFinder(BaseRoleFinder):
    """"""
    def _extract_role(response: str, pattern: str) -> str:
        # Create a pattern to match any of the substrings
        # Use re.search to find the first match in the input string
        match = re.search(pattern, response)

        if match:
            # If a match is found, return it
            return match.group()
        else:
            # If no match is found, return None
            return None

    def find_role(self, response: str) -> str:
        return self._extract_role(response, ANALYST_FINDER_PATTERN)


if __name__ == "__main__":
    ef = ExpertFinder("test")
