
class Git(object):

    def __init__(self, Github):
        self.Github = Github

    def getGithubUser(self, userName, password):
        return self.Github(userName, password)

    def sanitizeGitUrl( self, url ):
        gitPath = url.split('/')
        if url.count('blob') > 0 or url.count('tree') > 0:    
            del gitPath[2:4]
        return gitPath

    def extractUserRepoInfo(self, path ):
        result = {}
        gitPath = self.sanitizeGitUrl( path )
        result['user'] = gitPath[0]
        result['repository'] = gitPath[1]
        result['path'] = '/'.join(gitPath[2:])
        return result

    def getSearcUser(self,git, username ):
        git.legacy_search_users( username )
        try:
            searchUser = git.legacy_search_users( username )
            counter = 0
            for user in searchUser:
                if counter >= 2:
                    return False
                counter += 1
            return user
        except Exception:
            return False


    def getRepository(self, user, repositoryName):
        try:
            return user.get_repo( repositoryName )
        except Exception:
            return False

    def getDirContentFromRepository(self, repository, dirName):
        return repository.get_dir_contents( dirName )

    def getBranch(self, repository, branchName ):
        return repository.get_branch( branchName )

    def getTree(self, repository, shaCommit, isRecursive):
        fileList = []
        repoTree = repository.get_git_tree(shaCommit,isRecursive)
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

    def getFileContent(self, repository, path):
        return repository.get_file_contents( path )

    def getDirContentFromRepository(self, repository, dirName):
        return repository.get_dir_contents( dirName )

    def getContents(self, username,password, searchUser, searchRepo, branchName, ):
        git = Git.getGithubUser(username, password)
        user = Git.getSearcUser(git, searchUser )
        repository = Git.getRepository(user , searchRepo)
        branch = Git.getBranch( repository, branchName)
        tree = Git.getTree(repository, branch.commit.sha, True)
        fileDict = Git.extractFileListInfo(tree)
        flType = Git.checkFile(fileDict, urlParams['path'])

        if flType == 'blob':
            result = Git.getFileContent(repository, urlParams['path'])
        else:
            result = Git.getDirContentFromRepository(repository, urlParams['path'])
        return {'type':flType, 'file': result }