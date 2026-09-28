import json
import subprocess
import random
import os

cacheFile = os.path.expanduser("~/.progressor_temp.txt")
try:
    with open(cacheFile, "r+") as cache:
        cache.seek(0)
        contents = cache.readlines()
        lastFilePath = contents[0] if len(contents) > 0 else None
except FileNotFoundError:
    with open(cacheFile, "w+") as cache:
        lastFilePath = None

print("~0----[Progressor]----0~")
print("v0.2 -> Early Access\n")

fn = None
while True:
    usrInp = input("> ")
    if usrInp == "":
        continue
    cmds = usrInp.split()
    if cmds[0][0] == "/":
        subprocess.run(usrInp[1:], shell=True)
    elif cmds[0] == ".exit":
        break
    else:
        cmd = cmds[0]
        args = cmds[1:]
        if cmd.lower() == "open":
            if args[0].lower() == "last":
                if input(f"Do you wish to open {lastFilePath}? (Y/n): ").lower() == "n":
                    continue
                try:
                    fn = open(lastFilePath, args[1] if len(args) > 1 else "r+")
                except TypeError:
                    print("ERROR: There is no file path stored in the memory. (Probably because you didn't open a file yet.)")
                    continue
                except FileNotFoundError:
                    print("ERROR: The last used path points to an unknown location!")
                    continue
            try:
                fn = open(args[0], args[1] if len(args) > 1 else "r+") if not fn else fn
                lastFilePath = os.path.abspath(fn.name)
                with open(cacheFile, "r+") as cache:
                    cache.seek(0)
                    cache.write(os.path.abspath(fn.name))
                    cache.truncate()
                while True:
                    try:
                        mObj = json.load(fn)
                        done = mObj["Done"]
                        revisit = mObj["Revisit"]
                        stuck = mObj["Stuck"]
                        break
                    except json.decoder.JSONDecodeError:
                        fn.seek(0)
                        json.dump({"Done": [], "Revisit": [], "Stuck": []}, fn, indent=4)
                        fn.truncate()
                        fn.flush()
                        fn.seek(0)
                last = 0 if len(done + revisit + stuck) == 0 else max(max(done, default=0), max(revisit, default=0), max(stuck, default=0))
                print("File loaded successfully.")
            except FileNotFoundError:
                print("ERROR: File not found! (Use 'w+' to auto-create.)")
            # except:
            #     print("FATAL: Fatal error occured! (Contact the dev(s)...I guess)")
        elif cmd.lower() == "wipe":
            if fn:
                if input(f"You sure, you wanna wipe ALL the records from {fn.name}? (y/N): ").lower() == "y":
                    try:
                        fn.seek(0)
                        json.dump({"Done": [], "Revisit": [], "Stuck": []}, fn, indent=4)
                        fn.truncate()
                        print(f"Successfully wiped {fn.name}")
                    except:
                        print("FATAL: Fatal error occured! (Contact the dev(s)...I guess)")
                else:
                    print("Did not wipe the records.")
            else:
                try:
                    with open(args[0], args[1] if len(args) > 1 else "r+") as fn:
                        if input(f"You sure, you wanna wipe ALL the records from {fn.name}? (y/N): ").lower() == "y":
                            try:
                                fn.seek(0)
                                json.dump({"Done": [], "Revisit": [], "Stuck": []}, fn, indent=4)
                                fn.truncate()
                                print(f"Successfully wiped {fn.name}")
                            except:
                                print("FATAL: Fatal error occured! (Contact the dev(s)...I guess)")
                        else:
                            print("Did not wipe the records.")
                except FileNotFoundError:
                    print(f"Error: File not found! ({fn.name})")
                except:
                    print("FATAL: Fatal error occured! (Contact the dev(s)...I guess)")
                    
                    
        elif cmd.lower() == "start":
            if fn:
                current = last + 1
                doneAdd = []
                revAdd = []
                stuckAdd = []
                while True:
                    usrInp = input(f"#{current}: ")
                    if usrInp.lower() in [".exit"]:
                        break
                    elif usrInp.lower() in ["done", "d"]:
                        doneAdd.append(current)
                        current += 1
                    elif usrInp.lower() in ["revisit", "r"]:
                        revAdd.append(current)
                        current += 1
                    elif usrInp.lower() in ["stuck", "s"]:
                        stuckAdd.append(current)
                        current += 1
                    elif usrInp.lower() in ["save"]:
                        try:
                            fn.seek(0)
                            json.dump({"Done": done+doneAdd, "Revisit": revisit+revAdd, "Stuck": stuck+stuckAdd}, fn, indent=4)
                            fn.truncate()
                            print(f"Saved {current-last-1} records successfully. (Upto #{current-1})")
                        except:
                            print("FATAL: Fatal error occured!")
                    elif usrInp.lower() in ["reset"]:
                        if input("You sure, you wanna discard the changes? (y/N): ").lower() == "y":
                            doneAdd = []
                            revAdd = []
                            stuckAdd = []
                            current = last + 1
                    else:
                        print("ERROR: Invalid Command!")
            else:
                print("ERROR: You must open a file first!")

        elif cmd.lower() == "fp?":
            print("Current File Pointer:", fn if fn else None)

        else:
            print("ERROR: Invalid Command!")

try:
    fn.close()
except:
    pass
print(random.choice(["REPL Disarmed.", "Mission Aborted.", "Ammo Unloaded.", "Shots Unfired.", "Ping Ponged.", "Lights Out.", "Have a good day.", "Chains Broken."]))