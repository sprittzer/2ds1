from timeit import timeit
from random import randint
from collections import Counter

def count_values_dict(nums: list) -> dict:
    result_dict = dict()
    for num in range(0, 101):
        result_dict[num] = nums.count(num)
    return result_dict

def top_ten(nums: list) -> dict:
    top_items = sorted(count_values_dict(nums).items(), key=lambda x: x[1], reverse=True)[:10]
    return dict(top_items)

def main():
    nums = [randint(0, 100) for _ in range(1000000)]
    
    print(count_values_dict(nums) == Counter(nums))
    time_my_count = timeit(lambda: count_values_dict(nums), number=1)
    print(f'my function: {time_my_count}')

    time_counter_count = timeit(lambda: Counter(nums), number=1)
    print(f'Counter: {time_counter_count}')

    time_my_top = timeit(lambda: top_ten(nums), number=1)
    print(f'my top: {time_my_top}')

    time_counter_top = timeit(lambda: dict(Counter(nums).most_common(10)), number=1)
    print(f"Counter's top: {time_counter_top}")

if __name__ == "__main__":
    main()
