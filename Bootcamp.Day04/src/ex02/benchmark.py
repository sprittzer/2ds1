from timeit import timeit
import sys

def filter_emails_loop(emails: list) -> list:
    result_emails = []
    for email in emails:
        if "@gmail.com" in email:
            result_emails.append(email)
    return result_emails

def filter_emails_comprehension(emails: list) -> list:
    return [email for email in emails if "@gmail.com" in email]

def filter_emails_by_map(emails: list) -> list:
    return map(lambda x: x if "@gmail.com" in x else None, emails)
    
def filter_emails_by_filter(emails: list) -> list:
    return filter(lambda x: "@gmail.com" in x, emails)
    
def main():
    if len(sys.argv) != 3:
        raise Exception("Not enough arguments, you need to enter the method name and the number of calls")
    
    method = sys.argv[1]
    calls_num = int(sys.argv[2])
    
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5
    if method == 'loop':
        time = timeit(lambda: filter_emails_loop(emails), number=calls_num)
    elif method == 'list_comprehension':
        time = timeit(lambda: filter_emails_comprehension(emails), number=calls_num)
    elif method == 'map':
        time = timeit(lambda: filter_emails_by_map(emails), number=calls_num)
    elif method == 'filter':
        time = timeit(lambda: filter_emails_by_filter(emails), number=calls_num)
    else:
        raise Exception("Invalid method entered")
    print(list(filter_emails_by_filter(emails)) == filter_emails_comprehension(emails))
    print(time)

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
