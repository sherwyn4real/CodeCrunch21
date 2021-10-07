import requests
from github import Github
import os

g = Github(os.getenv('GITHUB_ACCESS'))



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
    




def getissue(author,repo,label):
    owner = author
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {"state": "open"}

    r = requests.get(url, headers=header,params = params)

    if r.status_code in (200,202):
        data = r.json()

        issues = []

        for i in range(len(data)):
            labels = data[i]['labels']
            for dlabel in labels:
                if dlabel['name'] == label:
                    dic={}
                    dic['id'] = data[i]['id']
                    dic['title'] = data[i]['title']
                    dic['state'] = data[i]['state']
                    dic['comments_count'] = data[i]['comments']
                    dic['assignee'] = data[i]['assignee'] #this is a dictionary. need to access 'login' key from it
                    issues.append(dic)
        
        return f'{issues}',200

    else:
        return {'status': r.status_code, 'message':'resource not found'}


#getissues("deepak1556","microsoft%2Fvscode", "install-update")
