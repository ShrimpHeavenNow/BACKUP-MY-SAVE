import shutil
import os

path  = "//SCENIC-EXPRESS/Public/2024/EMMYS" #The older we want to backup from
backupPath = "C:/Users/wrigh/OneDrive/Documents/Dean Server backup/"  #The Folder we cant to backup to.
deanWalk =[]

def dean_walk(_path): #Walks through the path finding files with "dean" in the filename
    deanFilesLatest = {}
    for (root,dirs,files) in os.walk(_path,topdown=True):
      for x in files:
          if "dean" in x.lower():
              deanWalk.append(root+"/"+x) #adds the filepath+filename to a list.

    for x in deanWalk:
        deanFilesLatest[x] = str(os.path.getmtime(x)) #Makes a dictionary with file names and date modified times.
    return (deanFilesLatest)

def write_file(name, toWrite): #Creates text document of whatever is fed to it
    title = name+".txt"
    f = open(title, "w")
    for x in toWrite:
        f.write(x + "," + toWrite[x] + "\n") #Writes this to a file.
    f.close()

def move_to_backup(walkdict): #Backup all these files locally with correct directories
    progress = 0
    backupFilePaths = {}
    for x in walkdict:
        newdir = ""
        y= x.split("/")
        for z in y:
            if z != "" and z != "SCENIC-EXPRESS" and z != "Public": #This gets rid of some layers to keep ther backup cleaner. Not fully needed.
                if "." in z: #Finds the File name
                    _fileName = z 

                if "." not in z: #makes new new filepath
                    newdir += z + "/"

        newFilePath = backupPath + newdir
        new_name = version_check(_fileName, newFilePath, walkdict[x]) #adds modification time, purges oldest versions.

        os.makedirs(os.path.dirname(newFilePath), exist_ok=True)
        if not os.path.isfile(newFilePath + new_name): #Checks if this same file and name is already there.
            shutil.copy(x, newFilePath)
            os.renames(newFilePath + _fileName, newFilePath + new_name)

        backupFilePaths[newFilePath+ (os.path.basename(x))] = walkdict[x] #TODO: This is probably also now wrong.
        print("Moved: ",x)
        progress +=1
        print(progress, " / ", str(len(walkdict)))
        
    return backupFilePaths

def check_for_updates(oldWalk):  #TODO: This is probably totally wrong now.
    newWalk = dean_walk(path)
    updates = {}
    for x in newWalk:
        if x not in oldWalk:
            updates[x] = newWalk[x]
            print("New File: ",x,newWalk[x])
        elif float(newWalk[x]) > float(oldWalk[x]):
            print(x, "new walk ", newWalk[x], " old walk ", oldWalk[x])
            #Add to list of update to be copied
            updates[x]= newWalk[x]
    return updates

def version_check(file,_path,modified): #TODO: Should this be two functions? rename and purge versions?
    versions = []
    newName=file.split(".")
    fileName = newName[0]
    newName = str((newName[0] + '-' + modified.split('.')[0])+ "." + newName[1])


    for x in os.listdir(_path):   #if there are now more than three backups, get rid of the oldest.
        if fileName in x:
            versions.append(x)

    vers_modified = []
    if len(versions) > 3:
        print ('Time to kill')  #Destroy oldest version.
        for x in  versions: #get file names of every version.
            x.split('-')  #TODO: check if there is more than one hyphen and use the last one.
            vers_modified.append(x[1])
        vers_modified.sort(reverse = True)
        to_delete = file+'-'+vers_modified[0]
        os.remove(_path + to_delete)
        #get rid of oldest.

    return newName





walk = dean_walk(path)
write_file("latest", walk)
newPaths = move_to_backup(walk)
print(newPaths)



#wait for a bit
input()

newVersions = check_for_updates(walk)
move_to_backup(newVersions)












