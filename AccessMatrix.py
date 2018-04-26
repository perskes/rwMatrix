import subprocess
import os
import glob


from subprocess import Popen, PIPE
#print("Root-Verzeichnis ist zum Beispiel P:\\")
print("Examples for the Root-Folder: C:\ or a mapped network share Z:\\")
print("")
#path = input("Root-Verzeichnis für Matrix:")
path = input("Root-Folder for the Matrix:")
path = path+"\\"
#maxDepth = input("Maximale Ordner-Tiefe:")
maxDepth = input("Maximum recursiveness:")

#print("Suche in "+path)
print("Searching ... "+path)


groupsArray = ["administrator","Jeder","otherADGroups","Sales","CEO","..."]

file = open("accessMatrix-Ausgabe.txt","w")

def getPermissions(path):
    with subprocess.Popen(["powershell.exe",
                  "Get-Acl '"+path+"' | Select-Object -Expand Access | Select-Object AccessControlType,IdentityReference | format-list"],
                  stdout=subprocess.PIPE, stdin=subprocess.PIPE) as p:
        output, errors = p.communicate()

    lines = output.decode('iso-8859-15').splitlines()
    lines = list(filter(None, lines))


    accessControll = []


    for x in lines:
        x = x.replace("AccessControlType : ","")
        x = x.replace("IdentityReference : ","")
        accessControll.append(x)


    users =[]
    rights =[]

    foo = {}

    for i,k in zip(accessControll[0::2], accessControll[1::2]):
        k = str(k.split("\\")[-1])
        i = str(i)
        foo[k] = i

    currentFolderRights = []
    for group in groupsArray:
        try:
            currentFolderRights.append(foo[group]+";")
        except KeyError:
            currentFolderRights.append("-"+";")


    currentFolderRightsString = ''.join(currentFolderRights)
    print(path + ";" + currentFolderRightsString)
    file.write(path + ";" + currentFolderRightsString+"\n")
    p.kill()

#print(foo)



def glob_list(start, max_depth=0, min_depth=0):
    # start out at least `min_depth` levels deep
    current_dir = os.path.join(start, *"*" * min_depth)
    for depth in range(min_depth, max_depth+1):
        # go one level deeper
        current_dir = os.path.join(current_dir, "*")
        # print(current_dir)
        yield from filter(os.path.isdir, glob.iglob(current_dir))

print("Folder" + ";" + ';'.join(groupsArray))
file.write("Folder" + ";" + ';'.join(groupsArray)+"\n")


if __name__ == "__main__":
    for folder in glob_list(path, max_depth=int(maxDepth), min_depth=1):
        if not folder.startswith('.'):
          if not folder.endswith('.lnk'):
            if not folder.endswith('.bat'):
                 getPermissions(folder)

file.close()