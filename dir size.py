import os

total_dir_size = 0
d = os.path.dirname(os.path.realpath(__file__))
for root, dirs,files in os.walk(d):
    for f in files:
        file = os.path.join(root,f)
        total_dir_size+= os.path.getsize(file)

print(f"{total_dir_size/(1024**2):,.3f} MB")
input("press any key to exit")
