import sys
import resource

def read_lines_generator(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            yield line

if __name__ == '__main__':
    file_name = sys.argv[1]
    for line in read_lines_generator(file_name):
        pass
    
    usage = resource.getrusage(resource.RUSAGE_SELF)
    peak_mem_gb = usage.ru_maxrss / (1024 ** 3)
    cpu_time = usage.ru_utime + usage.ru_stime
    
    print(f"Peak Memory Usage = {peak_mem_gb:.3f} GB")
    print(f"User Mode Time + System Mode Time = {cpu_time:.2f}s")
