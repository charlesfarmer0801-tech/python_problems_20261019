def dis(price, discount):
  discount = price * ((100 - discount) / 100)
  return round(discount, 2)
