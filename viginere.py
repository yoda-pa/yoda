from itertools import cycle
pt=""
ct=input("Please enter the cipher text: ")
k=input("Please enter the key: ")
for i,j in zip(ct,cycle(k)):
	if(i.islower()):		
		x=(ord(i)-ord(j))%26
		pt+=chr(ord("a")+x)
	else:
		pt+=i
print(pt)
