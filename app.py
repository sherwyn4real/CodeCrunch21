from flask import Flask,request
from Twitter import username,hashtag,geoloc
from Nasa import first_image
from Github import gt_methods
from Weather import weather_app
import os
from Crypto import crypto_methods
app = Flask(__name__)


Bad_request = { 'status':400, 'message':'Bad Request'}
Not_found = {'status':404, 'message':'Not found'}


@app.route("/")
def home():
    return "Homepage"

@app.route('/weather/city/<string:cname>')
def searchcity(cname):
    return weather_app.search_city(cname)


@app.route('/weather/search')
def searchcoord():
    lat = request.args.get('latitude', default='#' )
    lon = request.args.get('longitude', default='#' )
    pincode = request.args.get('pincode',default='#')

    if(pincode=='#'):
        return weather_app.search_cord_pin([lat,lon])

    elif lat=="#" or lon=='#':
        return weather_app.search_cord_pin(pincode)

    else:
        return Bad_request,400

#----------------------------------------------------------#

@app.route("/crypto/coins")
def getallcoins():
    return crypto_methods.all_coins()



@app.route("/crypto/tokens")
def getalltokens():
    return crypto_methods.all_tokens()


@app.route("/crypto/quote/<string:name>")
def getprice(name):
    return crypto_methods.ticker_coin(name)


@app.route('/crypto/team/<string:name>')
def getteam(name):
    return crypto_methods.team(name)

#----------------------------------------------------------#


@app.route("/nasa/image-of-month")
def nasa1():
    return first_image.getimage()

@app.route("/nasa/images-of-month/<string:y>/<string:m>")
def nasa2(y,m):
    return first_image.getimages(y,m)


@app.route("/nasa/videos-of-month/<string:y>/<string:m>")
def nasa3(y,m):
    return first_image.getvideos(y,m)

@app.route("/nasa/earth-poly-image/<string:dt>")
def nasa4(dt):
    return first_image.getepic(dt)

#----------------------------------------------------------#

@app.route("/twitter/user/<string:uname>")
def twitter1(uname):
    return username.getbyusername(uname)


@app.route("/twitter/hashtag/<string:htag>")
def twitter2(htag):
    return hashtag.getbyhashtag(htag)


@app.route("/twitter/location")
def twitter3():
    lat = request.args.get("latitude",default=None,type=str)
    lon = request.args.get("longitude",default=None,type=str)
    rad = request.args.get("radius",default=None,type=str)
    
    #if(lat!= "##" and lon!="##" and rad!="##" ):
    if(lat and lon and rad ):
        rad=rad[:len(rad)-2] 
        return geoloc.getbygeo(lat,lon,rad)

    else:
        return Bad_request,400

#----------------------------------------------------------#


@app.route("/github/user/<string:username>")
def getprofile(username):
    return gt_methods.getbyusername(username)


@app.route("/github/repo/<string:nos>")
def getrepo(nos):
    print("nos=",nos)
    if ',' not in nos:
        return Not_found,404

    else:
        loc = nos.index(',')
        x = nos[:loc]
        y = nos[loc+1:]
        return gt_methods.getbystars(x,y)


@app.route("/github/issues/<string:author>/<path:repo>/<string:labels>")
def getissues(author,repo,labels):
    return gt_methods.getissue(author,repo,labels)


@app.route("/github/commits/<string:dates>/<path:repo>")
def getcommits(dates,repo):
    return gt_methods.getbycommits(dates,repo)

#-------------------------------------------------------------------#

@app.errorhandler(404)
def page_not_found(e):
    print("SDfsdf")
    return Not_found,404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port = int(os.environ['PORT']))


#app.run(host='0.0.0.0',port = int(os.environ['PORT']))
