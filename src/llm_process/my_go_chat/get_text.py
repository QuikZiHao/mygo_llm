
from promptflow import tool
from typing import List, Dict
import re

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def get_text(speechs_list: List[str]) -> List[str]:
    results = []
    pattern = r"<(.*?)>(.*?)</\1>"
    for line in speechs_list:
        matches = re.findall(pattern, line)
        for _ ,content in matches:
            results.append(content.strip())
    return results
