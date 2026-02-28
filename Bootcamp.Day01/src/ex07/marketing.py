import sys


def get_call_center_set(clients, recipients):
    return list(set(clients) - set(recipients))

def get_potential_clients_set(clients, participants):
    return list(set(participants) - set(clients))

def get_loyalty_program_set(clients, participants):
    return list(set(clients) - set(participants))


def main():
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    
    if len(sys.argv) != 2:
        return 
    
    task = sys.argv[1]
    
    if task == 'call_center':
        result = get_call_center_set(clients, recipients)
    elif task == 'potential_clients':
        result = get_potential_clients_set(clients, participants)
    elif task == 'loyalty_program':
        result = get_loyalty_program_set(clients, participants)
    else:
        raise Exception(f'Unknown task: {task}')
    
    print(result)
    


if __name__ == "__main__":
    main()