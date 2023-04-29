class SimpleCalculator:
    def __init__(self):
        pass

    def evaluate(self, expression):
        try:
            result = eval(expression)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    # Usage example
    calc = SimpleCalculator()
    expression = "5 * (2 + 3)"
    result = calc.evaluate(expression)
    print(f"The result of the expression '{expression}' is: {result}")