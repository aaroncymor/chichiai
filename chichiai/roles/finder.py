import re

from .base import BaseRoleFinder


class ExpertFinder(BaseRoleFinder):
    """"""

    def find_role(self):
        return "find_role"

    def _extract_role(response: str) -> str:
        # Create a pattern to match any of the substrings
        pattern = r'Data Analyst|Data Analysis Theorist|Internet Research Specialist'

        # Use re.search to find the first match in the input string
        match = re.search(pattern, response)

        if match:
            # If a match is found, return it
            return match.group()
        else:
            # If no match is found, return None
            return None


class AnalystFinder(BaseRoleFinder):
    """"""

    def find_role(self):
        return "find_role"

    def _extract_role(response: str) -> str:
        # Create a pattern to match any of the substrings
        pattern = r'Data Analyst DF|Data Analyst Generic'

        # Use re.search to find the first match in the input string
        match = re.search(pattern, response)

        if match:
            # If a match is found, return it
            return match.group()
        else:
            # If no match is found, return None
            return None


if __name__ == "__main__":
    ef = ExpertFinder("test")
