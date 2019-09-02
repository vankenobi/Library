from datetime import datetime



x = datetime.now()
x = datetime.strftime(x,"%x")
print(x)
a = "09.02.18"
datetime.strptime(a,a)
if a < x:
    print("gecikmedi")
else:
    print("gecikti")




