import json
import datetime
import urllib
import git
import re
import shutil

import pandas
import requests
import time
import numpy as np

apiURL = 'https://api.github.com'
tokenFile = '../token.txt'
orgName = 'Computational-Content-Analysis-2018'


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
