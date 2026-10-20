def profit(info):
  profit = info.get("sell_price") - info.get("cost_price")
  return round(profit * info.get("inventory"))
