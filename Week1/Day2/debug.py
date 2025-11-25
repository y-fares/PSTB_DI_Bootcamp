people = ["Rick", "Morty", "Beth", "Jerry", "Snowball"]

for i in people:
    if len(i) <= 4:
        print(f"Hello {i}")

short_names = filter(lambda name: len(name) <= 4, people)
greetings = map(lambda name: f"Hello {name}", short_names)

for greeting in greetings:
    print(greeting)