from random import randint

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb   

def random_exclude(*exclude):
  exclude = set(exclude)
  randInt = randint(0,9)
  return random_exclude(*exclude) if randInt in exclude else randInt 

def chance(probability: float):
   return randint(1, 10) <= probability * 10
   