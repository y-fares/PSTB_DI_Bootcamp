from googletrans import Translator

# Instructions :
# Consider this list

# french_words= ["Bonjour", "Au revoir", "Bienvenue", "A bientôt"] 
# Look at this result :
# {"Bonjour": "Hello", "Au revoir": "Goodbye", "Bienvenue": "Welcome", "A bientôt": "See you soon"}
# You have to recreate the result using a translator module. Take a look at the googletrans module

# Liste de mots français
french_words = ["Bonjour", "Au revoir", "Bienvenue", "A bientôt"]

# Crée le traducteur
translator = Translator()

# Traduit chaque mot du français vers l’anglais
translations = {word: translator.translate(word, src='fr', dest='en').text for word in french_words}

# Affiche le dictionnaire résultat
print(translations)
