import sys
import json
import os

def write_to_json(dict1):
  with open("database.json", "w") as f:
    json.dump(dict1, f)

def read_from_json():
  with open("database.json") as f:
    _dict = json.load(f)
    return _dict

def sort(dict1):
  pending = dict1["Pending"]
  lst = len(pending) 
  for i in range(0, lst):  
      for j in range(0, lst-i-1): 
          if (int(pending[j][1]) > int(pending[j + 1][1])): 
              temp = pending[j] 
              pending[j]= pending[j + 1] 
              pending[j + 1]= temp
  dict1["Pending"] = pending
  return dict1

def add(dict1, list1):
  pending = dict1["Pending"]
  pending.append([list1[1], list1[0]])
  dict1["Pending"] = pending
  sort(dict1)
  sys.stdout.buffer.write(('Added task: "' + list1[1] + '" with priority '+list1[0]).encode('utf8'))
  return dict1

def ls(dict1):
  pending = dict1["Pending"]
  if len(pending)==0:
    print("There are no pending tasks!")
  else:
    j = 1
    for i in pending:
      sys.stdout.buffer.write((str(j)+". "+i[0]+" ["+i[1]+"]\n").encode('utf-8'))
      j+=1

def delete(dict1, list1):
  pending = dict1["Pending"]
  if len(pending)==0:
    print("Error: task with index #0 does not exist. Nothing deleted.")
  else:
    del pending[int(list1[0])-1]
    sys.stdout.buffer.write(("Deleted task #"+list1[0]).encode('utf-8'))
  return dict1

def done(dict1, list1):
  pending = dict1["Pending"]
  if len(pending)==0:
    print("Error: no incomplete item with index #0 exists.")
  else:
    completed = dict1["Completed"]
    index = int(list1[0])-1
    completed.append(pending[index][0])
    del pending[index]
    sys.stdout.buffer.write(("Marked item as done.").encode('utf-8'))
  return dict1

def help():
  sys.stdout.buffer.write(("Usage :-\n$ ./task add 2 hello world    # Add a new item with priority 2 and text \"hello world\" to the list\n$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order\n$ ./task del INDEX            # Delete the incomplete item with the given index\n$ ./task done INDEX           # Mark the incomplete item with the given index as complete\n$ ./task help                 # Show usage\n$ ./task report               # Statistics").encode('utf-8'))

def report(dict1):
  pending = dict1["Pending"]
  completed = dict1["Completed"]
  sys.stdout.buffer.write(("Pending : "+ str(len(pending))+"\n").encode('utf-8'))

  j = 1
  for i in pending:
    sys.stdout.buffer.write((str(j)+". "+i[0]+" ["+i[1]+"]\n").encode('utf-8'))
    j+=1
  sys.stdout.buffer.write(("\nCompleted : "+ str(len(completed))+"\n").encode('utf-8'))
  j = 1
  for i in completed:
    sys.stdout.buffer.write((str(j)+". "+i).encode('utf-8'))
    print("\n")
    j+=1

arguments = list(sys.argv)
del arguments[0]

if (os.path.exists("database.json")==False) or (os.path.getsize("database.json")==0):
  data = {"Pending":[], "Completed": []}
  write_to_json(data)

data = read_from_json()


if (len(arguments)==0) or (arguments[0]=="help"):
  help()

elif arguments[0]=="add":
  del arguments[0]
  if len(arguments)<2:
    print('Error: Missing tasks string. Nothing added!')
  
  else:
    data = add(data, arguments)
    write_to_json(data)

elif arguments[0]=="ls":
  ls(data)

elif arguments[0]=="del":
  del arguments[0]
  if len(arguments)==0:
    print("Error: Missing NUMBER for deleting tasks.")
  else:
    data = delete(data, arguments)
    write_to_json(data)

elif arguments[0]=="done":
  del arguments[0]
  if len(arguments)==0:
    print("Error: Missing NUMBER for marking tasks as done.")
  else:
    data = done(data, arguments)
    write_to_json(data)

elif arguments[0]=="report":
  report(data)