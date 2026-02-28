from timeit import timeit
import sys
from functools import reduce

def sum_loop(num: int) -> int:
    result_num = 0
    for i in range(1, num + 1):
        result_num += i ** 2
    return result_num

def sum_reduce(num: int) -> int:
    return reduce(lambda x, y: x + y**2, range(1, num + 1))

def main():
    if len(sys.argv) != 4:
        raise Exception("Incorrect number of arguments")
    
    method = sys.argv[1]
    calls_num = int(sys.argv[2])
    sum_num = int(sys.argv[3])
    if method == 'loop':
        time = timeit(stmt=lambda: sum_loop(sum_num), number=calls_num, globals=globals())
    elif method == 'reduce':
        time = timeit(stmt=lambda: sum_reduce(sum_num), number=calls_num, globals=globals())
    else:
        raise Exception("Invalid method entered")
    print(sum_loop(sum_num) == sum_reduce(sum_num))
    print(time)
        
if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")