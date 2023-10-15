import os
from contextlib import redirect_stdout
import io
import time
import pandas as pd
import warnings

from chichiai.roles import AnalystFinder, ExpertFinder
from chichiai.settings import OPENAI_API_KEY
from chichiai.output_manager import OutputManager

warnings.filterwarnings('ignore')


class ChiChiAI(object):
    pass
