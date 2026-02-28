from timeit import timeit

def filter_emails_loop(emails: list) -> list:
    result_emails = []
    for email in emails:
        if "@gmail.com" in email:
            result_emails.append(email)
    return result_emails

def filter_emails_comprehension(emails: list) -> list:
    return [email for email in emails if "@gmail.com" in email]

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'] * 5

    # loop_time = timeit(lambda: filter_emails_loop(emails), number=90000000)
    # comprehension_time = timeit(lambda: filter_emails_comprehension(emails), number=90000000)
     
    # if comprehension_time <= loop_time:
    #     print("It is better to use a list comprehension")
    # else:
    #     print("It is better to use a loop")
        
    
        
    # times_sorted = sorted([loop_time, comprehension_time])
    # print(f"{times_sorted[0]} vs {times_sorted[1]}")
    print(filter_emails_loop(emails) == filter_emails_comprehension(emails))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Error: {error}")
