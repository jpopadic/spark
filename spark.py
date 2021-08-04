import sys
from random import randint
import json
import tracery
from tracery.modifiers import base_english

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('sparks', nargs='*', help="table(s) to reference")
parser.add_argument("-c", "--chargen", help="run character generator", action="store_true")
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


if args.chargen:

  careeridx = 10000
  careerslist = data["careerslist"]

  print("WARNING: Careerslist is not complete. Only failed careers 1.." + str(len(careerslist)-1) + " are available")
  
  while careeridx >= len(careerslist):
    STR = randint(1, 6) + randint(1, 6) + randint(1, 6)
    DEX = randint(1, 6) + randint(1, 6) + randint(1, 6)
    CHA = randint(1, 6) + randint(1, 6) + randint(1, 6)
    HP = randint(1, 6)
    POUNDS = randint(1, 6)

    maxstat = max(STR, DEX, CHA)
    minstat = min(STR, DEX, CHA)

    maxidx = max(min(18, maxstat), 9) - 9
    minidx = max(min(12, minstat), 3) - 3

    careeridx = data["careerstable"][maxidx][minidx]
    print(careeridx)

  career = careerslist[careeridx - 1]
  if(type(career) == list):
    print("Choose from:")
    index = 0
    for c in career:
      print("\t" + str(index) + ": " + c["careername"])
      index += 1
    found = 0
    while(found == 0):
      careerchoice = input("...")
      if(careerchoice.isdigit()):
        if(int(careerchoice) < len(career)):
          career = career[int(careerchoice)]
          found = 1

  name = ""
  if("names" in career):
    nameidx = randint(0, len(career["names"]) - 1)
    name = career["names"][nameidx]
    print("\n" + name + ", " + career["careername"] + "(" + str(careeridx) + ")")
  else:
    print("\n" + career["careername"] + "(" + str(careeridx) + ")")
   
  print("\n" + career["tagline1"])
  print(career["tagline2"])

  print("\nSTR: " + str(STR) + " DEX: " + str(DEX) + " CHA: " + str(CHA) + " " + str(HP) + "hp £" + str(POUNDS))

  if ("debtor" in career):
    print("\nDebtor:")
    print("\t" + career["debtor"])
    
  if ("equipment" in career):
    print("\nEquipment:")
    for equipment in career["equipment"]:
      print("\t" + equipment)

  if ("attr1name" in career):
    print("\n" + career["attr1name"])
    print("\t" + career["attr1"][POUNDS-1])
   
  if ("attr2name" in career):
    print("\n" + career["attr2name"])
    print("\t" + career["attr2"][HP-1] + "\n")
      
      