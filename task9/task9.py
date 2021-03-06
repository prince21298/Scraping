import requests,random,time
from bs4 import BeautifulSoup
import json
import os.path
from os import path
from pprint import pprint
def scrap_top_list():
	if os.path.exists("movie.json"):
		with open ("movie.json",'r') as file:
			read=file.read()
			main_data=json.loads(read)
			return(main_data)
	else:
		url=" https://www.imdb.com/india/top-rated-indian-movies/"
		page=requests.get(url)
		soup=BeautifulSoup(page.text,'html.parser')
		main_div=soup.find('div',class_="lister")
		div=main_div.find('tbody',class_="lister-list")
		trs=div.findAll('tr')
		num=0
		main_data=[]
		for tr in trs:
			num=num+1
			dic={}
			title_colum=tr.find('td',class_="titleColumn").a
			dic['name']=title_colum.get_text()
			dic['position']=num
			year=tr.find('span',class_="secondaryInfo")
			new_year=year['year']=year.get_text()
			cut=int(new_year[1:5])
			dic['year']=cut
			movie_rateing=tr.find('td',class_="ratingColumn imdbRating")
			rateing=movie_rateing.get_text()
			cut_rateing=float(rateing[3:5])
			dic['rateing']=cut_rateing
			dic['url']="https://www.imdb.com"+title_colum["href"][:17]
			main_data.append(dic)
		with open("movie.json","w") as file:
			read = json.dumps(main_data)
			file.write(read)
			file.close()
		return(main_data)
top_movies=scrap_top_list()
def scrap_movie_detail(movie_url):
	randomtime=random.randint(1,3)
	movie_data={}
	timesleep=time.sleep(randomtime)
	data=requests.get(movie_url)
	soup=BeautifulSoup(data.text,'html.parser')
	div=soup.find('div',class_="title_wrapper")
	title=div.find('h1').get_text().split()
	title.pop()
	title1=(" ".join(title))
	movie_data["name"]=title1
	div1=soup.find_all('div',class_="credit_summary_item")
	for i in div1:
		h4=i.find("h4")
		if h4:
			if h4.text=="Directors:":
				lan=i.find_all("a")
				d_list=[]
				for j in lan:
					Directors=j.get_text()
					d_list.append(Directors)
				movie_data["Directors"]=d_list
	div2=soup.find("div",{"class":"article","id":"titleDetails"})
	all_div2=div2.find_all('div',class_="txt-block")
	for i in all_div2:
		h4=i.find("h4")
		if h4:
			if h4.text=="Country:":
				con=i.find('a')
				co=con.text
				movie_data["Country"]=co
			if h4.text=="Language:":
				lan=i.find_all('a')
				l=[]
				for j in lan:
					lan1=j.text
					l.append(lan1)
	movie_data["Language"]=l
	div3=soup.find('div',class_="poster")
	poster=div3.find('a').img["src"]
	movie_data["poster_image_url"]=poster
	div4=soup.find('div',class_="summary_text")
	Bio= div4.text
	movie_data["Bio"]=Bio
	div5=soup.find('div',class_="title_wrapper")
	t=div5.find('time').text.strip().split()
	m=0
	for i in t:
		if "h" in i:
			h=int(i.strip("h"))*60
		elif "min" in i:
			m+=int(i.strip("min"))
	minutes=h+m
	movie_data["rumtime"]=minutes
	a=div5.find("div",class_="subtext")
	al=a.find_all('a')
	all_a=[]
	for i in al:
		all_a.append(i)
	all_a.pop()
	jenre=[]
	for i in all_a:
		j=i.text
		jenre.append(j)
	movie_data["genre"]=jenre
	return (movie_data)
def get_scrap_movie_detail(movie_list):
	row=[]
	for i in movie_list:
		u1=i["url"]
		u2=u1[27:36]+".json"
		if os.path.exists(u2):
			with open (u2,'r') as file:
				read=file.read()
				ro=json.loads(read)	
		else:
			ro=scrap_movie_detail(i["url"])
			with open(u2,"w") as file:
				read = json.dumps(ro)
				file.write(read)
				file.close()
		row.append(ro)
	return(row)
pprint(get_scrap_movie_detail(top_movies))
