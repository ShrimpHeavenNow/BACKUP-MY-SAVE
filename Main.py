import shutil
import os
import time
import datetime

path  = "//SCENIC-EXPRESS/Public/2024/" #The older we want to back up from
backupPath = "C:/Users/wrigh/OneDrive/Documents/Dean Server backup/"  #The Folder we cant to back up to.
deanWalk =[]
backupLog = "latest.txt"

def dean_walk(_path): #Walks through the path finding files with "dean" in the filename
    dean_files_latest = {}
    for (root,dirs,files) in os.walk(_path,topdown=True):
      for x in files:
          if "dean" in x.lower():
              deanWalk.append(root+"/"+x) #adds the filepath+filename to a list.

    for x in deanWalk:
        dean_files_latest[x] = str(os.path.getmtime(x)) #Makes a dictionary with file names and date modified times.
    return dean_files_latest

def write_file(name, to_write): #Creates text document of whatever is fed to it
    f = open(name, "w")
    for x in to_write:
        f.write(x + "," + to_write[x] + "\n") #Writes this to a file.
    f.close()

def walk_from_file(name):
    file_dict = {}
    with open(name) as f:
        to_dict = [line.rstrip().split("\n") for line in f]
        for x in to_dict:
            x = x[0].split(",")
            file_dict[x[0]] = x[1]
    return file_dict

def move_to_backup(walkdict): #Backup all these files locally with correct directories
    print ("Backing up", str(len(walkdict)), "files.")
    progress = 0
    for x in walkdict:
        new_dir = ""
        y= x.split("/")
        for z in y:
            if z != "" and z != "SCENIC-EXPRESS" and z != "Public": #This gets rid of some layers to keep the backup cleaner. Not fully needed.
                if "." in z: #Finds the File name
                    _fileName = z 

                if "." not in z: #makes new  filepath
                    new_dir += z + "/"

        new_file_path = backupPath + new_dir
        new_name = modified_name(_fileName, new_file_path, walkdict[x]) #adds modification time, purges oldest versions.

        os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
        if not os.path.isfile(new_file_path + new_name): #Checks if this same file and name is already there.
            shutil.copy(x, new_file_path)
            os.renames(new_file_path + _fileName, new_file_path + new_name)
            print("Backed up: ", x, " as: ", new_file_path + new_name)
        else:
            print('No changes: ',x)

        version_check(_fileName, new_file_path)
        progress += 1
        print(progress, " / ", str(len(walkdict)))

def check_for_updates(old_walk):
    new_walk = dean_walk(path)
    updates = {}
    for x in new_walk:
        if x not in old_walk:
            updates[x] = new_walk[x]
            print("New File: ",x,new_walk[x])
        elif float(new_walk[x]) > float(old_walk[x]):
            print('Newer Version: ',x)
            updates[x]= new_walk[x] #Add to list of update to be copied
    return updates

def modified_name(file,_path,modified):
    extension = file.split(".")[1]
    file_name = file.split(".")[0]
    new_name = file_name + '-' + modified.split('.')[0]+ "." + extension
    return new_name


def version_check(file,_path):
    versions = []
    extension = file.split(".")[1]
    file_name = file.split(".")[0]

    for x in os.listdir(_path):   #if there are now more than three backups, get rid of the oldest.
        y = hyphen_checker3000(x)
        z = y[1].split('.')
        if file_name == y[0] and extension == z[1]:
            versions.append(x)

    vers_modified = []
    while len(versions) > 3:
        for x in  versions: #get file names of every version.
            x = hyphen_checker3000(x)
            vers_modified.append(x[1])
        vers_modified.sort()
        to_delete = file_name+'-'+vers_modified[0]
        print ('Murdering old version: ', _path ,to_delete)
        os.remove(_path + to_delete)
        versions.pop()

def hyphen_checker3000(file):
    hyphens = file.count('-')
    if  hyphens <= 1: #there is only one hyphen
        file = file.split('-')
        return file
    else:
        file = file.split('-')
        x=0
        add = ""
        while x <hyphens:
            add += file[x] + '-'
            x +=1
        file_split = add, file[-1:][0]
        return file_split


while True:
    print("Checking for Updates", datetime.datetime.now())
    if walk_from_file(backupLog) == dean_walk(path):
        print("No changes.")
    else:
        newVersions = walk_from_file(backupLog)
        newVersions = check_for_updates(newVersions)
        move_to_backup(newVersions)
        write_file(backupLog, dean_walk(path))
    time.sleep(420)












