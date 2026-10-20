def damage(damage, speed, time):
  if damage < 0 or speed < 0:
    return  "invalid"
    
  mult_dict = {
  "second": 1,
  "minute": 60,
  "hour": 3600,
  }
  
  return damage * speed * mult_dict.get(time)
