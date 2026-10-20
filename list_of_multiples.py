def list_of_multiples (num, length):
  multiples = []

  for i in range(1, length+1):
    multiples.append(num * i)
  
  return multiples  
