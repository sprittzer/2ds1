import sys
import resource

def read_all_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

if __name__ == '__main__':
    file_name = sys.argv[1]
    
    lines = read_all_lines(file_name)
    for line in lines:
        pass
    
    usage = resource.getrusage(resource.RUSAGE_SELF)
    
    peak_mem_gb = usage.ru_maxrss / (1024 ** 3)
    cpu_time = usage.ru_utime + usage.ru_stime
    
    print(f"Peak Memory Usage = {peak_mem_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
