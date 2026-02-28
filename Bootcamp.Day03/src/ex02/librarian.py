import sys
import subprocess
import os

def check_env():
    venv_path = os.environ.get('VIRTUAL_ENV')
    if not venv_path:
        raise Exception(f"Activate the virtual environment")
    if 'marianbe' not in venv_path:
        raise Exception(f'The script is not in the correct virtual environment. Expected "marianbe", but received: "{sys.prefix}"')
    
def make_requiremenets():
    libs = ['beautifulsoup4', 'pytest']
    
    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            f.writelines('\n'.join(libs))

def install_libraries():
    subprocess.call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

def list_installed_libs():
    subprocess.run([sys.executable, '-m', 'pip', 'freeze'])
    with open('requirements.txt', 'w') as f:
        subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=f)

def main():
    check_env()
    make_requiremenets()
    install_libraries()
    list_installed_libs()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
