import requests
from flask import Flask, request, jsonify
import json


report_error_crypto = {
    "status": 404,
  "message": "coin/token not found"
}

crypto_not_found = {
    "error":"crypto not found"
    }


           
#========================================================================
#Crypto

def all_coins():
    url=f'https://api.coinpaprika.com/v1/coins'
    response = requests.get(url)
    #result = response.json()
    #return result
    if response.status_code in (200,202):
        res=response.json()
        result=[]
        
        for d in res:
            dict_result={}
            for key,val in d.items():
                if(key=="id" or key=="name" or key=="symbol" or key=="type"):
                    dict_result[key]=val
            result.append(dict_result)        
                    
        #result = response.json()
        #result = {key: result[key] for key in ["id","name","symbol","type"]}
        return jsonify(result)
    else:
        return report_error_crypto,404



def all_tokens():
    url=f'https://api.coinpaprika.com/v1/coins'
    response = requests.get(url)
    if response.status_code in (200,202):
        res=response.json()
        result=[]
        
        for d in res:
            if d["type"]=="token":
                dict_result={}
                for key,val in d.items():
                    if(key=="id" or key=="name" or key=="symbol" or key=="type"):
                        dict_result[key]=val
                result.append(dict_result)        
                    
        #result = response.json()
        #result = {key: result[key] for key in ["id","name","symbol","type"]}
        return jsonify(result)
    else:
        return report_error_crypto,404



def ticker_coin(name):
    url=f'https://api.coinpaprika.com/v1/coins'
    response = requests.get(url)
    if response.status_code in (200,202):
        res=response.json()
      
        exists = False
        for d in res:
            if(d["name"].lower() == name.lower()):
                coin_id=d["id"]
                exists = True
                break   
    if exists == False:
        return report_error_crypto,404

    
    url_coin=f'https://api.coinpaprika.com/v1/tickers/{coin_id}'
    response = requests.get(url_coin)
    if response.status_code in (200,202):
        res=response.json()
        #return res
        #{"id":"btc-bitcoin","name":"Bitcoin","symbol":"BTC","rank":1,"circulating_supply":18837762,"total_supply":18837762,"max_supply":21000000,"USD_price":53891.578939916}
        output = {
            "id":res["id"],
            "name":res["name"],
            "symbol":res["symbol"],
            "rank":res["rank"],
            "circulating_supply":res["circulating_supply"],
            "total_supply":res["total_supply"],
            "max_supply":res["max_supply"],
            "USD_price":res["quotes"]["USD"]["price"]
            }
        return jsonify(output)
    else:
        return report_error_crypto,404

def get_link(lst):
    for d in lst:
        for k,v in d.items():
            return v
    

def founder(res):
    found=[]
    for d in res["team"]:
        dic={}
        if (d["position"]=="Founder" or d["position"]=="Co-Founder"):
            dic["name"]=d["name"]
            f_id=d["id"]
            url_link=f'https://api.coinpaprika.com/v1/people/{f_id}'
            response = requests.get(url_link)
            if response.status_code in (200,202):
                res=response.json()
                dic["links"]=get_link(res["links"]["additional"])  #res["links"]["additional"]["url"]
                dic_copy=dic.copy()
                found.append(dic_copy)      
    return found


def devs(persons):

    for person in persons:
        
        id = person['id']
        print("id=",id)
        url = f'https://api.coinpaprika.com/v1/people/{id}'

        r = requests.get(url)

        if r.status_code in (200,202):
            data = r.json()

            links = data['links']
            if 'github' not in links:
                person['github'] = ""
            else:
                person['github'] = links['github'][0]['url']

            if 'twitter' not in links:
                person['twitter'] = ""
            
            else:
                person['twitter'] = links['twitter'][0]['url']

            if 'linkedin' not in links:
                person['linkedin'] = ""

            else:
                person['linkedin'] = links['linkedin'][0]['url']


        else:
            return report_error_crypto,404


    for person in persons:
        del person['id']

    return persons



def team(name):
    url=f'https://api.coinpaprika.com/v1/coins'
    response = requests.get(url)
    
    if response.status_code in (200,202):
        res=response.json()

        exists = False
      
        for d in res:
            if(d["name"].lower() == name.lower()):
                coin_id=d["id"]
                exists = True
                break

        if exists == False:
            return report_error_crypto,404
          
        url_coin=f'https://api.coinpaprika.com/v1/coins/{coin_id}'
        response = requests.get(url_coin)    
        if response.status_code in (200,202):
            res=response.json()
            output = {
                "name":res["name"],
                "symbol":res["symbol"],
                "rank":res["rank"],
                "type":res["type"],
                "founders":founder(res)  #[{"name":d["name"] for d in res["team"] if (d["position"]=="Founder" or d["position"]=="Co-Founder")}]
                }
            
            dev_ids=[]
            for person in res['team']:
                dic={}
                dic['name'] = person['name']
                dic['position'] = person['position']
                dic['id'] = person['id']

                dev_ids.append(dic)

            developers = devs(dev_ids)
            output['developers'] = developers

            return jsonify(output),200


#team('Bitcoin')

