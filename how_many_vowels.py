def count_vowels(txt):
  vowels = "aeiou"
  count = 0
  
  for letter in txt.lower():
    if letter in vowels:
      count += 1
      
  return count
