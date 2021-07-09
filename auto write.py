with open('check.txt', 'w') as f:
    i=0
    while True:
        f.write("This a text file\n")
        i= i+1
        if i==100000:
            break