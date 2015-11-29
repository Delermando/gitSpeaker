class Git(object):

    def __init__(self, Github):
        self.Github = Github

    def getGithubUser(self, userName, password):
        return self.Github(userName, password)

    def sanitizeGitUrl(self, url):
        gitPath = url.split('/')

        if gitPath[-1] == '':
            del gitPath[-1]

        if url.count('blob') > 0 or url.count('tree') > 0:
            del gitPath[2:4]
        return gitPath

    def extractUserRepoInfo(self, path):
        result = {}
        gitPath = self.sanitizeGitUrl(path)
        result['user'] = gitPath[0]
        result['repository'] = gitPath[1]
        result['path'] = '/'.join(gitPath[2:])
        return result

    def getSearcUser(self, git, username):
        try:
            searchUser = git.legacy_search_users(username)
            for user in searchUser:
                if user.login == username:
                    return user
        except Exception:
            return False

    def getRepository(self, user, repositoryName):
        try:
            return user.get_repo(repositoryName)
        except Exception:
            return False

    def getDirContentFromRepository(self, repository, dirName):
        return repository.get_dir_contents(dirName)

    def getBranch(self, repository, branchName):
        return repository.get_branch(branchName)

    def getTree(self, repository, shaCommit, isRecursive):
        fileList = []
        repoTree = repository.get_git_tree(shaCommit, isRecursive)
        for fl in repoTree.tree:
            fileList.append(fl)
        return fileList

    def extractFileListInfo(self, tree):
        fileDict = {}
        for fl in tree:
            fileDict[fl.path] = fl.type
        return fileDict

    def checkFile(self, fileDict, filePath):
        if fileDict.has_key(filePath):
            return fileDict[filePath]
        else:
            return False

    def getFileContentsByList(self, repository, listfile):
        files = []
        for key, value in listfile.iteritems():
            files.append(self.getFileContent(repository, key))
        return files

    def getFileContent(self, repository, path):
        return repository.get_file_contents(path)

    def getFileList(self, username, password, searchUser, searchRepo, path, branchName, ignoreList):
        git = self.getGithubUser(username, password)
        user = self.getSearcUser(git, searchUser)
        repository = self.getRepository(user, searchRepo)
        print(username, password)
        branch = self.getBranch(repository, branchName)
        treeFiles = self.getTree(repository, branch.commit.sha, True)
        fileDict = self.extractFileListInfo(treeFiles)
        fileDictRemovedFolders = self.removeFolderFromList(fileDict)
        filesFromPath = self.getFilesFromPath(fileDictRemovedFolders, path)
        return self.removeFilesInIgnoreList(filesFromPath, ignoreList)
        # return self.getFileContentsByList(repository, clearDict)

    def removeFolderFromList(self, filelist):
        result = {}
        for key, value in filelist.iteritems():
            if value != 'tree':
                result[key] = value
        return result

    def getFilesFromPath(self, filelist, path):
        filesInFolder = {}
        if path == '' or path == '/':
            return filelist
        else:
            if path in filelist.keys():
                result = {path: filelist[path]}
            else:
                for key, value in filelist.iteritems():
                    if key.count(path+'/') >= 1:
                        filesInFolder[key] = value
                print(filesInFolder)
                if len(filesInFolder) >= 1:
                    result = filesInFolder
                else:
                    result = False
        return result

    def removeFilesInIgnoreList(self, filelist, ignorelist):
        removelist = []
        for key, value in filelist.iteritems():
            if value == 'blob':
                remove = self.getListFilesToRemove(key, ignorelist['files'] + ignorelist['extensions'] + ignorelist['folders'])

            if remove:
                removelist.append(key)
        return self.removeFilesFromList(filelist, removelist)

    def getListFilesToRemove(self, filename, fileRemove):
        for fr in fileRemove:
            if filename.count(fr) >= 1:
                return True
        return False

    def getListFilesToRemoveByFolderName(self, filename, folderRemove):
        for fr in folderRemove:
            if filename.count(fr) >= 1:
                return True
        return False

    def removeFilesFromList(self, filelist, listFilesToRemove):
        for fl in listFilesToRemove:
            del filelist[fl]
        return filelist
