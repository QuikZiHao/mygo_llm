from jinja2 import Template
from ..constants import LLM_CONFIG


def get_systemprompt_template() ->Template:
    with open(LLM_CONFIG.get("system_prompts"), "r", encoding="utf-8") as file:
        template_str = file.read()
    return Template(template_str)
