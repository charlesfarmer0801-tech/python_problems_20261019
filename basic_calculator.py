def calculator(num1, operator, num2):
  if operator == "+":
    return num1 + num2
  if operator == "-":
    return num1 - num2
  if operator == "*":
    return num1 * num2
  if operator == "/":
    return "Can't divide by 0!" if num2 == 0 else num1 / num2
