def main():
    with open("ds.csv", encoding='utf-8') as f:
        data = f.readlines()
        
    new_lines = []
    
    for line in data:
        new_line = ''
        in_el = False
        
        for el in line:
            if el == '"':
                in_el = not in_el
            elif el == ',' and not in_el:
                el = '\t'
            new_line += el
        new_lines.append(new_line)
        
    with open('ds.tsv', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
                
    
if __name__ == "__main__":
    main()
