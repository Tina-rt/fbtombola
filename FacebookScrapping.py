import requests, re
from bs4 import BeautifulSoup

from pprint import pprint as pp

class User:
    profil_links = ''
    nom = ''
    commentaire = ''
    pdp = ''

    def __init__(self, nom='', profil_links='', commentaire='', pdp=''):
        self.nom = nom
        self.profil_links = str(profil_links)
        self.commentaire = commentaire 
        self.pdp = pdp 

    def __repr__(self):
        return f'{self.profil_links}\n{self.nom}'
    
    def toJson(self):
        return {
            'name' : self.nom,
            'link': self.profil_links,
            'pdp': self.pdp,
            'comments': self.commentaire
        }
    def fromJson(self, json):
        return User(
            nom=json['name'],
            profil_links=json['link'],
            pdp=json['pdp'],
            commentaire=json['comments']
        )
    def __repr__(self):
        return self.nom
        

login_url = 'https://mbasic.facebook.com/login'

with open('personalInfo', 'r') as file:
    data = file.read().split('\n')

payload = {
    'email': data[0],
    'pass': data[1]
}

def change_url(link):
    link = link.replace('web', 'mbasic')
    link = link.replace('www', 'mbasic')
    return link



def getFbPost(link):
    link = change_url(link)
    
    with requests.Session() as session:
        post = session.post(login_url, data=payload)

        if 'photos' not in link:
            page = session.get(link)
            soup = BeautifulSoup(page.content, "html.parser")

            img_ = soup.find_all('a',)
            for a in img_:
                try:
                    if 'photos' in a['href']:
                        link = 'https://mbasic.facebook.com'+a['href']
                except: pass
        print('Getting post detail at', link)
        
        # print(post)
        page = session.get(link)
        
        soup = BeautifulSoup(page.content, "html.parser")
        list_div = soup.find('div', class_='msg')
        actor = soup.find('a', class_='actor-link')
        
        post_content = list(list_div.children)[2].text
        
        # print(post_content)
        return {
            'actor': actor.text,
            
            'content': post_content
        }      

def getProfilPhoto(link):
    link = change_url(link)
    
    print('Getting profile pic at', link)
    with requests.Session() as session:
        post = session.post(login_url, data=payload)
        print(post)
        page = session.get(link)
        
        soup = BeautifulSoup(page.content, "html.parser")
        img_list = soup.find_all('img')
        for img_el in img_list:
            try:
                if 'profile picture' in img_el['alt']:
                    print('pdp link', img_el['src'] )
                    return img_el['src'] 
            except:pass
            
        # print(img_list)



class FacebookPostScrapping:
    def get_user_comments(self,  fb_url):
        
        fb_url = change_url(fb_url)

            
        print('Fecthing comments in', fb_url)
    
        with requests.Session() as session:
            post = session.post(login_url, data=payload)
            # print(post)
            
            result = {}
            list_com = []
            page_num = 0
            

            if 'photos' not in fb_url:
                print('no photos in fb url')
                page = session.get(fb_url)
                soup = BeautifulSoup(page.content, "html.parser")

                img_ = soup.find_all('a',)
                for a in img_:
                    try:
                        if 'photos' in a['href']:
                            fb_url = 'https://mbasic.facebook.com'+a['href']
                    except: pass
            if 'photos' not in fb_url and 'post' not in fb_url:
                return []
                        

            nbre_com = 100
            # comments = []
            while True:
                fb_url +='&p={}'.format(page_num)

                page = session.get(fb_url)
                soup = BeautifulSoup(page.content, "html.parser")
                
                
                comments_container = soup.find_all('div', id =re.compile('^\d+') )
                
                print(len(comments_container))
                
                
                for comm in comments_container:
                
                    temp = list(comm.children)[0]
                    # print(list(comm)[0])
                    try:
                        ch1 = list(comm.children)[0]
                        ch2 = list(ch1.children)[0]
                        aut_link = list(ch2.children)[0]['href']
                    except:
                        pass

                    
                    # aut_link = 'Author'
                    aut = list(list(temp.children)[0].children)[0].text
                    commentaire = list(temp)[1].text

                    list_com.append(User(nom=aut, profil_links=aut_link, commentaire=commentaire).toJson())

                    # print(commentaire)
                
                page_num += 10
                
                if comments_container == []:
                    break
            print("Nombre com : ", len(list_com))
               
            session.close()
        return list_com

# link = getProfilPhoto("https://mbasic.facebook.com/titi.randria.39?comment_id=Y29tbWVudDozMjUzMDc5NzQxNDgwMzc3XzMyNTMwODQ3MzgxNDY1NDQ%3D")
# print(link)
# fb = FacebookPostScrapping()

# for r in fb.get_user_comments('https://www.facebook.com/211001825688199/posts/3256149221173429'):
#     print(r)
