import sys
import os
from src.subtitle_process.implement.get_result import get_result

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))


get_result((1, 13))

