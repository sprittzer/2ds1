#!/usr/bin/env python3
import os

def get_env():
    venv_path = os.environ.get('VIRTUAL_ENV')
    
    return venv_path
    
if __name__ == "__main__":
    current_venv = get_env()
    print(f"Your current virtual env is {current_venv}")