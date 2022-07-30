from dotenv import load_dotenv # pip install -U python-dotenv
from pathlib import Path
import os
from distutils.util import strtobool

def load_environment_variables():
    env = os.getenv('ENV')
    if not env:
        env = 'development'
        # os.putenv('ENV', env)
        os.environ['ENV'] = env # update os.environ instead of os.putenv() beacuse of... https://docs.python.org/3/library/os.html#os.putenv

    currentPath = Path(__file__) / '..'

    envPaths = [
        f'.env',
        f'.env.local',
        f'.env.{env}',
        f'.env.{env}.local',
    ]
    envPaths = list(filter(lambda path: path != False, envPaths))
    envPaths = list(map(lambda path: (currentPath / path).resolve(), envPaths))
    
    for envPath in envPaths:
        load_dotenv(dotenv_path=envPath, override=True)
    

def to_bool(value):
    if type(value) == str:
        return bool(strtobool(value))
    return bool(value)

if __name__ == '__main__':
    load_environment_variables()