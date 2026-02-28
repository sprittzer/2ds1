import sys


def main():
    if len(sys.argv) != 2:
        return
     
    with open(sys.argv[1], 'r', encoding='utf-8') as file:
        data = file.read().split('\n')
        
    table = ['Name\tSurname\tE-mail']
    
    for email in data:
        name, surname = list(map(lambda x: x.capitalize(), email.split('@')[0].split('.')))
        table.append('\t'.join([name, surname, email]))
    
    with open('employees.tsv', 'w', encoding='utf-8') as f:
        f.write('\n'.join(table))


if __name__ == "__main__":
    main()