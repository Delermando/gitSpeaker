import json
with open('ignorelist.json') as data_file:    
        ignorelist = json.load(data_file)



def getListFilesToRemove( filename, fileRemove):
    for fr in fileRemove:
        if filename.count(fr) >= 1:
            return True
    return False

def getListFilesToRemoveByFolderName( filename, folderRemove):
    for fr in folderRemove:
        if filename.count(fr) >= 1:
            return True
    return False

def removeFilesFromList(filelist, listFilesToRemove):
    for fl in listFilesToRemove:
        del filelist[fl]
    return fl

filelist = {
    'teste.py':'blob',
    'teste.pdf':'blob',
    'teste.pyc':'blob',
    '.gitignore':'blob',
    'vendor/':'tree',
    'vendor/teste.html':'blob',
}

for key, value in filelist.iteritems():
    if value == 'blob':
        remove = getListFilesToRemove(key, ignorelist['files'] + ignorelist['extensions']+ignorelist['folders'])
    elif value == 'tree':
        remove = getListFilesToRemoveByFolderName(key, ignorelist['folders'])

    if remove:
        removelist.append(key)

removeFilesFromList(filelist, removelist)
