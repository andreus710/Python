# This code demonstrates the use of the range function in a for loop.
# It generates a sequence of numbers from 10 to 50 and prints each number.

for i in range(10, 50, 2):
    print(i)

print('----------------------------------------------------\n')
#list(range(5, 10))
#list(range(0, 10, 3))
#list(range(-10, -100, -30))

#La funcion len sirve para contar los elementos de una lista x , y los ejecuta en la funcion for
a = ['Mary', 'had', 'a', 'little', 'lamb']
for i in range(len(a)):
    print(i, a[i])
    
print('----------------------------------------------------\n')
  
sum(range(4))  
print(sum(range(4)))