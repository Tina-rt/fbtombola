from flask import Flask, request, render_template
from FacebookScrapping import FacebookPostScrapping, User, getProfilPhoto, getFbPost
import random, pprint as pp
import json
app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/tirage', methods=['POST', 'GET'])
def tirage():
    print(request.args)
    
    url_pub = request.args['post_url']
    keyword = request.args['answer']

    fb_scr = FacebookPostScrapping()
    reslt = fb_scr.get_user_comments(url_pub)
    winner = {'name' :'', 'comments' :''}
    final_rslt = []
    for comm in reslt:
        if keyword.lower() in comm['comments'].lower():
            final_rslt.append(comm)
    print('result len', len(final_rslt))

    winner = random.choice(final_rslt)
    
    w = User()
    w = w.fromJson(winner)
    
    print('Winner', w)

    post = getFbPost(url_pub)
    
    w.pdp = getProfilPhoto('http://mbasic.facebook.com'+w.profil_links)
    print(w.pdp)


    return render_template('index.html', winner = w, post=post)
    
@app.route('/tirage/api', methods=['GET'])
def tirage_api():
    print(request.args)
    
    url_pub = request.args['post_url']
    keyword = request.args['answer']

    fb_scr = FacebookPostScrapping()
    reslt = fb_scr.get_user_comments(url_pub)
    winner = {'name' :'', 'comments' :''}
    final_rslt = []
    for comm in reslt:
        if keyword.lower() in comm['comments'].lower():
            final_rslt.append(comm)
    print('result len', len(final_rslt))
    pp.pprint(reslt)
    if len(final_rslt) > 0:
        winner = random.choice(final_rslt)
    
        w = User()
        w = w.fromJson(winner)
        
        print('Winner', w)

        
        
        w.pdp = getProfilPhoto('http://mbasic.facebook.com'+w.profil_links)
        print(w.pdp)

        result = {
            'winner': w.toJson(),
            'result': 1
        }
        pp.pprint(result)
        return json.dumps(result)
    else:
        return json.dumps({
            'result': 0
        })

@app.route('/essai', methods=['GET'])
def essai():
    return 'ok'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
