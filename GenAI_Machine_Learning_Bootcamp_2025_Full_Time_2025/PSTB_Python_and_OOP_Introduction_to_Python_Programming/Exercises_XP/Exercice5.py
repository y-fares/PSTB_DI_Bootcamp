my_fav_numbers = set()

my_fav_numbers.add(1)
print(my_fav_numbers)
my_fav_numbers.add(2)
my_fav_numbers.add(3)

print(my_fav_numbers)
my_fav_numbers.discard(3)

print(my_fav_numbers)

friend_fav_numbers = set()
friend_fav_numbers.add(int(input("Enter your friend's favorite number: ")))

our_fav_numbers = my_fav_numbers.union(friend_fav_numbers)

print(our_fav_numbers)
