import json
from typing import Optional


def format_comment(comment, indent: Optional[int] = 0) -> str:
    snippet = comment["snippet"]

    prefix = "".join([" " for _ in range(indent)])
    author = snippet["authorDisplayName"]
    text = snippet["textOriginal"]

    text_lines = text.split("\n")
    indented_text = text_lines[0]
    if len(text_lines) > 1:
        for line in text_lines[1:]:
            indented_text += f"\n{prefix}  {line}"

    return f"{prefix}{author}: {indented_text}"


def format_thread(thread) -> str:
    result = ""

    thread_snippet = thread["snippet"]
    top_level_comment = thread_snippet["topLevelComment"]
    result += format_comment(top_level_comment)
    result += "\n\n"

    if thread_snippet["totalReplyCount"] > 0:
        for reply in thread["replies"]["comments"]:
            result += f"{format_comment(reply, indent=2)}"
            result += "\n\n"

    return result
