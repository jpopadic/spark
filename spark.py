from random import randint
import json
import tracery
from tracery.modifiers import base_english

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('sparks', nargs='+', help="table(s) to reference")
args = parser.parse_args()
# print(args.sparks)

f = open('data.json')
data = json.load(f)

if not 'sparktables' in data:
  sys.exit("Invalid data...")

sparktables = data["sparktables"]

for spark in args.sparks:
  if not spark in sparktables:
    print("\"" + str(spark) + "\" not in spark tables!!!")
    continue
  rulestable = sparktables[spark]
  if 'origin' in rulestable:
    rules = {}
    for key in rulestable.keys():
      if rulestable[key][0] == '@':
        rules[key] = sparktables[rulestable[key].replace('@', '')]    
      else:
        rules[key] = rulestable[key]
    grammar = tracery.Grammar(rules)
    grammar.add_modifiers(base_english)
    print(grammar.flatten("#origin#"))  
  else:
    print(rulestable[randint(0, len(rulestable)-1)])
