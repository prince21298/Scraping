import requests
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
	m_data=[]
	movie_data={}
	data=requests.get(movie_url)
	soup=BeautifulSoup(data.text,'html.parser')
	div=soup.find('div',class_="title_wrapper")
	title=div.find('h1').get_text().split()
	title.pop()
	title1=("".join(title))
	movie_data["name"]=title1
	div1=soup.find('div',class_="credit_summary_item")
	direct=div1.find_all('a')
	Director=[]
	for i in direct:
		Director.append(i.text)
	movie_data["Director"]=Director
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
	div5=soup.find('div',class_="subtext")
	t1=div5.find('time').get_text()
	t=t1.strip().split()
	m=0
	for i in t:
		if "h" in i:
			h=int(i.strip("h"))*60
		elif "min" in i:
			m=int(i.strip("min"))
	minutes=h+m
	movie_data["rumtime"]=minutes
	al=div5.find_all('a')
	all_a=[]
	for i in al:
		all_a.append(i)
	all_a.pop()
	jenre=[]
	for i in all_a:
		j=i.text
		jenre.append(j)
	movie_data["genre"]=jenre
	div8=soup.find_all('div',class_="see-more")
	for i in div8:
		if "See full cast »"==i.text.strip():
			cast=i.find('a').get("href")
	url1=movie_url+cast
	page1=requests.get(url1)
	bs4=BeautifulSoup(page1.text,'html.parser')
	table=bs4.find('table',class_="cast_list")
	tbody=table.find_all('tr')
	c_data=[]
	for i in tbody:
		td=i.find_all('td',class_="")
		for j in td:
			a=j.find('a')
			Id=a.get('href')[6:15]
			name=a.text.strip()
			dict1={"imdb_id":Id,
			"name":name}
			c_data.append(dict1)
	movie_data["cast"]=c_data
	return (movie_data)
def get_scrap_movie_detail(movie_list):
	if os.path.exists("task13.json"):
		with open ("task13.json",'r') as file:
			read=file.read()
			row=json.loads(read)
	else:
		row=[]
		for i in movie_list:
			m_data=scrap_movie_detail(i["url"])
			row.append(m_data)
		with open("task13.json","w") as file:
			read = json.dumps(row)
			file.write(read)
			file.close()
	return(row)
co_cast=(get_scrap_movie_detail(top_movies))
def analys_actors(actors_detail):
	empty_list=[]
	for i in actors_detail:
		c=i["cast"]
		for j in c:
			actors_id=j["imdb_id"]
			if actors_id not in empty_list:
				empty_list.append(actors_id)
	empty_dict={}
	for d in empty_list:
		num=0
		for i in actors_detail:
			c=i["cast"]
			for j in c:
				actors_id=j["imdb_id"]
				actors_name=j["name"]
				if d==actors_id:
					num+=1
					if num>1:
						empty_dict[actors_id]={"name":actors_name,"num_movies":num}		
	return(empty_dict)
pprint(analys_actors(co_cast))


