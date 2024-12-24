import re
from typing import List
from ..entity.sub import Sub


def time_to_ms(time_str: str) -> int:
    hours, minutes, seconds = map(float, time_str.split(":"))
    seconds, centiseconds = divmod(seconds, 1)
    centiseconds = int(centiseconds * 100) 
    return int((hours * 3600 + minutes * 60 + seconds) * 1000 + centiseconds * 10)

def remove_effects(text: str) -> str:
    cleaned_text = re.sub(r"{[^}]*}", "", text, flags=re.DOTALL)
    return cleaned_text.strip()


def solve_sub( input_filepath:str) -> List[Sub]:
    subtitles = []
    with open(input_filepath, "r", encoding="utf-8") as file:
        for line in file:
            if line.startswith("Dialogue:"):
                parts = line.split(",", 9) 
                if len(parts) > 9:
                    start_time = time_to_ms(parts[1]) 
                    end_time = time_to_ms(parts[2])   
                    text = parts[-1].strip() 
                    clean_text = remove_effects(text)
                    subtitles.append(Sub(start_time, end_time, clean_text))
    subtitles.sort(key=lambda sub: sub.start_time)
    return subtitles
