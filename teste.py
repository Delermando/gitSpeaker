from app import *
var = Tools.getEnviromentVar()

user = 'delermando'
repositoryName = 'gitSpeaker'
branchName = 'master'
filePath = 'app/__init__.py'

git = Git.getGithubUser(var['GITSPEAKER_GH_USERNAME'], var['GITSPEAKER_GH_PASSWORD'])
user = Git.getSearcUser(git, user )
repository = Git.getRepository(user , repositoryName)
branch = Git.getBranch( repository, branchName)
tree = Git.getTree(repository, branch.commit.sha, True)
fileDict = Git.extractFileListInfo(tree)
fl = Git.checkFile(fileDict, filePath)

if fl == 'blob':
    fileContent = Git.getFileContent(repository, filePath)
    print(fileContent.name)
elif fl == 'tree':
    dirContent = Git.getDirContentFromRepository(repository, filePath)
    print(dirContent)
else:
    print('Nao existe')


#if user:
#    print(user.name)
#    repository = getRepository(user , 'flask-sandboxe')
#    if repository:
#        print(repository.name)
#        getDirContentFromRepository()
#    else:
#        print('Repositorio nao encontrado')    
#else:
#    print('Usuario nao encontrado')
