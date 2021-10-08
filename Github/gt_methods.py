import requests
from github import Github
import os

g = Github(os.getenv('GITHUB_ACCESS'))  #using pygithub to authenticate


#This header authorises the app using Personal access token
header = { 'Authorization': f"token {os.getenv('GITHUB_ACCESS')}"}


#get profile with username
def getbyusername(username):
    url = f'https://api.github.com/users/{username}'

    url2 = f'https://api.github.com/users/{username}/followers'
    url3 = f'https://api.github.com/users/{username}/following'
    r = requests.get(url,headers=header)
    followers_data = requests.get(url2,headers=header).json()
    following_data = requests.get(url3,headers=header).json()
    followers,following = [],[]

    for dic in followers_data:
        followers.append(dic['login'])

    for dic in following_data:
        following.append(dic['login'])

    if r.status_code in (200,202):
        data = r.json()
        output = {}
        output['name'] = data["name"]
        output['avatar_url'] = data["avatar_url"]
        output['public_repos'] = data["public_repos"]
        output['followers'] = followers
        output['following'] = following
        output['url'] = data["url"]
        output['bio'] = data["bio"]

        return output,200

    else:
        return {'status': r.status_code, 'message':'resource not found'}
    

#-----------------------------------------------------------------------------
#get repos by stars range
def getbystars(x,y):
    try:
        repos = g.search_repositories(query=f'stars:{x}..{y}')
        output = []
        #print(repos[0].created_at)
        for repo in repos:
            dic={}
            dic['name'] = repo.name
            dic['creation_date'] = f'{repo.created_at}'
            dic['stars'] = repo.stargazers_count
            dic['size'] = repo.size
            dic['forks'] = repo.forks
            dic['owner_name'] = repo.owner.login
            output.append(dic)

        #print(output)
        return f'{output}',200

    except:
        return {'status': 404, 'message':'resource not found'}



    '''print(repos[0].name)
    print(repos[0].created_at)
    print(repos[0].stargazers_count)
    print(repos[0].size)
    print(repos[0].forks)
    print(repos[0].owner.login)'''

    #print(repo[0].stargazers_count)
    
#-----------------------------------------------------------------------------

def getissue(author,repo,label):

    try:
        repo = repo.replace('%2F','/')
        #print(repo)
        loc = repo.index('/')
        uname = repo[:loc]
        repo = repo[loc+1:]
        issues = g.search_issues(query=f'repo:{uname}/{repo} label:{label} author:{author} type:issue')
        output = []

        for issue in issues:
            dic={}
            dic['id'] = issue.id
            dic['title'] = issue.title
            dic['state'] = issue.state
            dic['comments_count'] = issue.comments
            dic['assignee'] = issue.assignee.login
            output.append(dic)

        return f'{output}',200


    except:
        return {'status': 404, 'message':'resource not found'}



#--------------------------------------------------------------------------------------------------


def getbycommits(dates,repo):

    try:
        loc = dates.index(',')
        x = dates[:loc]
        y = dates[loc+1:]
        repo = repo.replace('%2F','/')
        
        loc = repo.index('/')
        uname = repo[:loc]
        repo = repo[loc+1:]
        
        commits = g.search_commits(query=f'repo:{uname}/{repo} committer-date:{x}..{y}')
        dic={}
        output=[]
        maxl = 35   #maximum length of array
        
        for commit in commits:
            dic={}

            dic['node_id'] = commit._rawData['node_id']
            dic['message'] = commit._rawData['commit']['message']
            dic['committer_name'] = commit._rawData['author']['login']
            dt =  commit._rawData['commit']['committer']['date']
            dic['date'] = f'{dt}'   #adding date
            dic['comment_count'] = commit._rawData['commit']['comment_count']
            
            output.append(dic)
            maxl-=1
            if maxl == 0:
                break

        return f'{output}',200

        '''print(commits[0]._rawData['node_id'])
        print(commits[0]._rawData['commit']['message'])
        print(commits[0]._rawData['author']['login'])
        print(commits[0]._rawData['commit']['committer']['date'])'''


            
    except:
        return {'status': 404, 'message':'resource not found'}



#getissue("deepak1556","microsoft%2Fvscode", "install-update")
#getbystars(30000,40000)
#getbycommits('2021-07-01,2021-08-30','microsoft%2Fvscode')