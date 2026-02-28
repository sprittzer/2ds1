import sys


def main():
    if len(sys.argv) != 2:
        return 
    search_email = sys.argv[1]
    
    with open('employees.tsv', 'r', encoding='utf-8') as file:
        data = [line.replace('\n', '').split('\t') for line in file.readlines()][1:]
        
    for name, surname, email in data:
        if search_email == email:
            print(f'Уважаемый {name}, добро пожаловать в нашу команду! '
                  'Мы уверены, что нам будет приятно с вами работать. '
                  'Это обязательное условие для специалистов, которых нанимает наша компания.')


if __name__ == "__main__":
    main()