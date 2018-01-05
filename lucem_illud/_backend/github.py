import json
import datetime
import urllib
import git
import re
import shutil

import pandas
import requests
import time
import getpass
import os.path
import numpy as np

apiURL = 'https://api.github.com'
tokenFile = '../token.txt'
orgName = 'Computational-Content-Analysis-2018'
repoName = 'content-analysis-2018'

def makeStudentRepo(targetDir = '.', name = repoName):
    repoDir = os.path.abspath(os.path.join(os.path.expanduser(targetDir), name))
    print("Creating your repo at: {}".format(repoDir))
    if os.path.isdir(repoDir):
        print("Repo already exists at: {}".format(repoDir))
        print("Exiting")
        return
    print("A repo will be created on your GitHub account, to do this you will need to input your GitHub username and password")
    while True:
        username = input("GitHub Username: ")
        password = getpass.getpass()
        auth = (username, password)
        try:
            getGithubURL('', auth = auth)
        except RuntimeError:
            print("Your username or password was incorrect, please try again. Make sure you are using your GitHub username and password")
        else:
            break

    data = {
        "name": name,
        "description": 'Assignments for Computational Content Analysis 2018',
        "homepage": "https://github.com/Computational-Content-Analysis-2018",
        "private": False,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
        "auto_init" : False,
    }
    print("Creating a new repo")
    try:
        d = makeNewRepo(data, auth=auth)
        print("Repo created at: {}".format(d['html_url']))
    except RuntimeError:
        print("Repo already exists, cloning")
        d = getGithubURL('/repos/{}/{}'.format(username, name), auth = auth)
    print("Adding the notebooks")
    repo = git.Repo.clone_from(d['clone_url'], repoDir)
    base = repo.create_remote('base', url='https://github.com/Computational-Content-Analysis-2018/Content-Analysis.git')
    base.pull('master')
    print("Pushing to GitHub, you may have to enter your login details again")
    while True:
        try:
            repo.remotes.origin.push('master')
        except:
            print("Your username or password was incorrect, please try again. Make sure you are using your GitHub username and password")
        else:
            break
    print("Done")

def getGithubURL(target, auth = None):
    if auth is None:
        try:
            with open(tokenFile) as f:
                username, token = f.readline().strip().split()
                auth = (username, token)
        except FileNotFoundError:
            auth = None
    if target.startswith('http'):
        url = target
    else:
        url = urllib.parse.urljoin(apiURL, target)
    r = requests.get(url, auth = auth)
    if not r.ok:
        raise RuntimeError('Invalid request: {}\n{}'.format(url, r.text))
    try:
        return json.loads(r.text)
    except json.JSONDecodeError:
        return []

def postGithubURL(target, data, auth = None):
    if auth is None:
        try:
            with open(tokenFile) as f:
                username, token = f.readline().strip().split()
                auth = (username, token)
        except FileNotFoundError:
            auth = None
    if target.startswith('http'):
        url = target
    else:
        url = urllib.parse.urljoin(apiURL, target)
    r = requests.post(url, data = json.dumps(data), auth = auth)
    if not r.ok:
        raise RuntimeError('Invalid request: {}\n{}'.format(url, r.text))
    try:
        return json.loads(r.text)
    except json.JSONDecodeError:
        return []

def getLogin(username, password):
    s = requests.session()

def makeNewRepo(data, auth, org = None):
    if org is None:
        target = 'user/repos'
    else:
        target = 'orgs/{}/repos'.format(org)
    return postGithubURL(target, data, auth = auth)


def makeCommentsRepo(classTime, articleCite, articleURL, auth, org = orgName):
    articleName = re.search(r'“(.+?)\.?”', articleCite).group(1)
    repoName = "{}-{}".format(classTime, articleName)[:100]
    data = {
        "name": repoName,
        "description": articleCite,
        "homepage": "https://github.com/Computational-Content-Analysis-2018",
        "private": False,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
        "auto_init" : False,
    }
    d = makeNewRepo(data, auth, org = org)
    target = d['clone_url']
    try:
        repo = git.Repo.clone_from(target, 'temp')
    except git.GitCommandError:
        print("Waiting")
        time.sleep(2)
        repo = git.Repo.clone_from(target, 'temp')
    with open('temp/README.md', 'w') as f:
        f.write("# Comments on: {}\n[{}]({})".format(articleName, articleCite, articleURL))
    repo.index.add(['README.md'])
    repo.index.commit("Create README.md")
    repo.remotes[0].push()
    shutil.rmtree('temp')
    return d['html_url'] + r'/issues'
