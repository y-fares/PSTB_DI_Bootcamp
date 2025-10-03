def my_pow(a:int, b:int, c:int):
    return (a**b)*c
a = int(input("a = "))
b = int(input("b = "))
c = int(input("c = "))

print(f"({a}^{b})*{c} = {my_pow(a,b,c)}")
