import subprocess
import sys
import pytest

def run_script(args):
    result = subprocess.run([sys.executable, '../ex03/financial.py'] + args, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def test_total_revenue_output():
    stdout, return_code = run_script(['MSFT', 'Total Revenue'])
    assert return_code == 0
    assert stdout.startswith('(') and stdout.endswith(')')
    assert any(char.isdigit() for char in stdout)

def test_return_type_is_tuple():
    stdout, return_code = run_script(['MSFT', 'Total Revenue'])
    assert return_code == 0
    assert stdout.startswith('(') and stdout.endswith(')')

def test_invalid_ticker_raises():
    stdout, return_code = run_script(['MEOWMEOWMEOW', 'Total Revenue'])
    
    assert 'Error' in stdout or return_code != 0


if __name__ == "__main__":
    pytest.main()
