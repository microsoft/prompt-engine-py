import os
import sys
PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(
    PROJECT_PATH,"..","src", "prompt_engine"
)
sys.path.append(SOURCE_PATH)