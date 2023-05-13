import re

GPT_SYSTEM_INSTRUCTIONS = """Write Manim scripts for animations in Python. Generate code, not text. Never explain code. Never add functions. Never add comments. Never infinte loops. Never use other library than Manim/math. Only complete the code block. Use variables with length of maximum 2 characters. At the end use 'self.play'.

```
from manim import *
from math import *

class GenScene(Scene):
    def construct(self):
        # Write here
```"""

def wrap_prompt(prompt: str) -> str:
  """
    Wraps the prompt in the GPT-3.5 instructions
  """
  return f"Animation Request: {prompt}"

def extract_code(text: str) -> str:
  """
    Extracts the code from the text generated by GPT-3.5 from the ``` ``` blocks
  """
  pattern = re.compile(r"```(.*?)```", re.DOTALL)
  match = pattern.search(text)
  if match:
    return match.group(1).strip()
  else:
    return text

def extract_construct_code(code_str: str) -> str:
  """
    Extracts the code from the construct method
  """
  pattern = r"def construct\(self\):([\s\S]*)"
  match = re.search(pattern, code_str)
  if match:
    return match.group(1)
  else:
    return ""

def code_static_corrector(code_response: str) -> str:
  """
    Corrects some static errors in the code
    GPT only has information until 2021, so it ocasionally generates code
    that is not compatible with the latest version of Manim
  """
  # Replace ShowCreation with Create
  # Solution: https://www.reddit.com/r/manim/comments/qcosuj/nameerror_name_showcreation_is_not_defined/
  code_response = code_response.replace("ShowCreation", "Create")

  return code_response

def create_file_content(code_response: str) -> str:
  """
    Creates the content of the file to be written
  """
  return f"""# Manim code generated with OpenAI GPT
# Command to generate animation: manim GenScene.py GenScene --format=mp4 --media_dir . --custom_folders video_dir

from manim import *
from math import *

class GenScene(Scene):
    def construct(self):
{code_static_corrector(code_response)}"""