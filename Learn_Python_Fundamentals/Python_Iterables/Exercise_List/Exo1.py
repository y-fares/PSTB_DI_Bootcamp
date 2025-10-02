
list1 = [1,2,3,4]
for i in list1:
    print(i) 

for i in list1:
    print(i*20)

list2 = ["Elie", "Tim", "Matt"]
list2A = [a[0] for a in list2]
print(list2A)

list3 = [1, 2, 3, 4, 5, 6]
list33 = [i for i in list3 if i%2==0]
print(list33)

list41 = [1,2,3,4]
list42 = [3,4,5,6]
list43 = [i for i in list41 if i in list42]
print(list43)

list5 = ["Elie", "Tim", "Matt"]
list51 = [i[::-1].lower() for i in list5]
print(list51)

s1 = "first"
s2 = "third"
s = list(set(s1) & set(s2))
print(s)

list6 = range(1,100)
list61 = [i for i in list6 if i%12==0]
print(list61)

str = "amazing"
str_consomn = [i for i in str if i not in 'aeiou']
print(str_consomn)

ll = [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
print(ll)

ll = range(0,9)
ll_list = [[i for i in ll] for j in ll]
print(ll_list)