import subprocess
import pstats
from pstats import SortKey
import os

subprocess.run(['python', '-m', 'cProfile', '-o', 'stat.txt', 'financial_enhanced.py', 'MSFT', 'Total Revenue'])
stats = pstats.Stats('stat.txt')
stats.strip_dirs()
stats.sort_stats(SortKey.CUMULATIVE)

with open('pstats-cumulative.txt', 'w') as f:
    stats.stream = f
    stats.print_stats(5)
    
os.remove('stat.txt')
