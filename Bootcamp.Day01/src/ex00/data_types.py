def data_types():
    n = 1
    s = "sprittzer"
    n_f = 1.1
    b = True
    l = [1, 2, 3]
    d = {1: 0, 2: 1}
    t = (1, 2, 3)
    st = {1, 2, 3}
    
    print(f'[{', '.join([type(i).__name__ for i in [n, s, n_f, b, l, d, t, st]])}]')
    
    
if __name__ == "__main__":
    data_types()
