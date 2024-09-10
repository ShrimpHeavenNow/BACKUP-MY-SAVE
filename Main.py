import shutil
import os

path  = "//SCENIC-EXPRESS/Public/2024/"
backupPath = "C:/Users/wrigh/OneDrive/Documents/Dean Server backup/"
deanWalk =[]
def dean_walk(_path):
    deanFilesLatest = {}
    for (root,dirs,files) in os.walk(_path,topdown=True): #Finds every file with "dean" in it within the path.
      for x in files:
          if "dean" in x.lower():
              deanWalk.append(root+"/"+x) #adds the filepath+filename to a list.

    for x in deanWalk:
        deanFilesLatest[x] = str(os.path.getmtime(x)) #Makes a dictionary with file names and date modified times.
    return (deanFilesLatest)

def write_file(name, toWrite):
    title = name+".txt"
    f = open(title, "w")
    for x in toWrite:
        f.write(x + "," + toWrite[x] + "\n") #Writes this to a file.
    f.close()

def move_to_backup(walkdict): #Backup all these files locally with correct directories.
    progress = 0
    for x in walkdict:
        newdir = ""
        y= x.split("/")
        for z in y:
            if z != "" and z != "SCENIC-EXPRESS" and z != "Public":
                if "." not in z:
                    newdir += z + "/"
        os.makedirs(os.path.dirname(backupPath+ newdir), exist_ok=True)
        shutil.copy(x, (backupPath+ newdir))
        print("Moved: ",x)
        progress +=1
        print(progress, " / ", str(len(walkdict)))

walk = dean_walk(path)
write_file("latest", walk)
move_to_backup(walk)


#TODO: Initial check to see if file is there at all. add if not.
#TODO: Do the check again after x amount of time. If there is a newer version, back that up with a number appended.
#TODO: keep only the latest 3 changes. delete the older.

#wait for a bit

newWalk = dean_walk(path)







