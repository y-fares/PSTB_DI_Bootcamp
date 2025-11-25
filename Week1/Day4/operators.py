def addOperator(x, y):
    return x + y

def divideOperator(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
