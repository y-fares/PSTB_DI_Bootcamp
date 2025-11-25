def say_hello(username = "", language = "FR"):
    if language == "FR":
        print(f"Bonjour {username}")
    elif language == "EN":
        print(f"Hello {username}")
    else:
        print(" euuuh ok")

say_hello("TEST", language = "EN")
say_hello(language = "EN", username = "TEST2")