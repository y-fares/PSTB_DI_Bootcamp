# Exercise 1 : Call History
# Instructions
# Create a class called Phone. This class takes a parameter called phone_number. 
# When instantiating an object create an attribute called call_history which value is an empty list.
class Phone:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.call_history = []
        self.messages = []
# Add a method called call that takes both self and other_phone (i.e another Phone object) as parameters.
# The method should print a string stating who called who, and add this string to the phone’s call_history.

    def call(self, other_phone):
        call_record = f"Number {self.phone_number} has called number {other_phone.phone_number}"
        print(call_record)
        self.call_history.append(call_record)
        other_phone.call_history.append(call_record)

# Add a method called show_call_history. This method should print the call_history.

    def show_call_history(self):
        print("Call History:")
        for call in self.call_history:
            print(call)
# Add another attribute called messages to your __init__() method which value is an empty list.
    # Added in __init__ function

# Create a method called send_message which is similar to the call method. Each message should be saved 
# as a dictionary with the following keys:
# to : the number of another Phone object
# from : your phone number (also a Phone object)
# content
    def send_message(self, other_phone, content):
        message = {
            "to": other_phone.phone_number,
            "from": self.phone_number,
            "content": content
        }
        self.messages.append(message)
        other_phone.messages.append(message)
        print(f"Message sent from {self.phone_number} to {other_phone.phone_number}: {content}")

# Create the following methods: show_outgoing_messages(self), show_incoming_messages(self), show_messages_from(self)
    def show_outgoing_messages(self):
        print(f"Outgoing messages from {self.phone_number}:")
        for message in self.messages:
            if message["from"] == self.phone_number:
                print(f"To {message['to']}: {message['content']}")

    def show_incoming_messages(self):
        print(f"Incoming messages to {self.phone_number}:")
        for message in self.messages:
            if message["to"] == self.phone_number:
                print(f"From {message['from']}: {message['content']}")

    def show_messages_from(self, other_phone):
        print(f"Messages from {other_phone.phone_number} to {self.phone_number}:")
        for message in self.messages:
            if message["from"] == other_phone.phone_number and message["to"] == self.phone_number:
                print(f"{message['content']}")
# Test your code !!!
phone1 = Phone("123-456-7890")
phone2 = Phone("098-765-4321")
phone1.call(phone2)
phone1.call(phone2) 
phone2.call(phone1)
phone1.show_call_history()
phone2.show_call_history()
phone1.send_message(phone2, "Hello, how are you?")
phone2.send_message(phone1, "I'm good, thanks!")
phone1.send_message(phone2, "What about you?")
phone1.show_outgoing_messages()
phone2.show_incoming_messages()
phone1.show_messages_from(phone2)
phone2.show_messages_from(phone1)