import os
import time
import pickle
import shutil
import textwrap
import requests
import fortnite_api
from PIL import *; from PIL import Image, ImageDraw, ImageFont

links = []; title = []; body = []; chars = []
fortnite_client = fortnite_api.FortniteAPI('ba158fdba76459a1c37ff234fd2a34018e511ee99356c621def80559aba52386'); news_raw = fortnite_client.news.fetch().br.raw_data ##inititate API

def resize(basewidth, imagein, imageName): ##to resize the image
	img = Image.open(imagein)
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.LANCZOS)
	img.save(imageName)

def watermark_text(input_image_path, output_image_path, text, pos, textSize=26, color=(80, 168, 214)): ##function to overlay the text onto the image
	photo = Image.open(input_image_path)

	# make the image editable
	drawing = ImageDraw.Draw(photo)

	font = ImageFont.truetype("files/font.ttf", textSize) ##font used in game
	drawing.text(pos, text, fill=color, font=font, fontsize=5)
	photo.save(output_image_path)

def watermark_photo(input_image_path, ##to overlay images onto the main image
					output_image_path,
					watermark_image_path,
					position):
	base_image = Image.open(input_image_path)
	watermark = Image.open(watermark_image_path)

	# add watermark to your image
	base_image.paste(watermark, position)
	base_image.save(output_image_path)

def text_wrap_overlay(bodyNum, posX, yOff=608, outname='Temp/output/brNews.png'):
	for line in textwrap.wrap(body[bodyNum], width=50):
		watermark_text('Temp/output/brNews.png', outname, line, pos=(posX, yOff))
		yOff = yOff + 29

try:
	open('files/font.ttf', 'r').close()
except FileNotFoundError:
	print('\nrequired files do not exist.\n Downloading.')
	os.mkdir('files/')
	response = requests.get('http://fnbr.ddns.net/downloads/fnNews/font.ttf')
	if response.status_code == 200:
		with open("files/font.ttf", 'wb') as f:
			f.write(response.content)
	response = requests.get('http://fnbr.ddns.net/downloads/fnNews/template.png')
	if response.status_code == 200:
		with open("files/template.png", 'wb') as f:
			f.write(response.content)
	print('done.\n')


if os.name == 'nt': ##Check for windows or linux
	print('[WARN] Windows Detected. Switching to windows code')
	try:
		os.mkdir('Temp/')
		os.mkdir('Temp/output/')
	except FileExistsError:
		print('[WARN] Temp/ already exists. Skipping')

	while True: ##loop to check for change. Delay: 100s
		links = []; title = []; body = []; chars = [] ##resets lists

		try:
			os.mkdir('Temp/')
			os.mkdir('Temp/output/')
		except FileExistsError:
			pass

		try:
			with open('Temp/news_old' + '.pkl', 'rb') as f: ##pickle load
				news_old = pickle.load(f)
		except:
			print('[WARN] .pkl file doesn\'t exist. Skipping')
			news_old = 'nopickle'

		if news_raw != news_old: ##check for updates
			print('[ALERT] In-game news updated')

			with open('Temp/news_old' + '.pkl', 'wb') as f: ##new pickle dump. to be compared next iteration
			    pickle.dump(news_raw, f, pickle.HIGHEST_PROTOCOL)

			x = 0
			for i in news_raw['messages']:
				title.append(news_raw['messages'][x]['title']) ##adds the data to lists
				links.append(news_raw['messages'][x]['image'])
				body.append(news_raw['messages'][x]['body'])
				x = x + 1

			x = 0; f = ''
			for i in links: ##downloads indervidual images
				url = links[x]
				response = requests.get(url)
				if response.status_code == 200:
					with open("Temp/newsImage"+str(int(x+1))+'.jpg', 'wb') as f:
						f.write(response.content)
						resize(520, 'Temp/newsImage'+str(x+1)+'.jpg', 'Temp/newsImage'+str(x+1)+'.jpg')
						chars.append(str(len(body[int(x)].split()))) ##unrelated line but it works here -- This is for getting the length of the main body of the text.
				x = x + 1

			watermark_photo('files/template.png', 'Temp/output/brNews.png', 'Temp/newsImage1.jpg', position=(115,289))
			watermark_photo('Temp/output/brNews.png', 'Temp/output/brNews.png', 'Temp/newsImage2.jpg', position=(701,289))
			watermark_photo('Temp/output/brNews.png', 'Temp/output/brNews.png', 'Temp/newsImage3.jpg', position=(1286,289)) ##overlays indervidual 3 images over main template

			watermark_text('Temp/output/brNews.png', 'Temp/output/brNews.png', title[0], pos=(124, 561), textSize=38, color=(0, 0, 0))
			watermark_text('Temp/output/brNews.png', 'Temp/output/brNews.png', title[1], pos=(709, 561), textSize=38, color=(0, 0, 0))
			watermark_text('Temp/output/brNews.png', 'Temp/output/brNews.png', title[2], pos=(1295, 561), textSize=38, color=(0, 0, 0)) ##overlays text to template

			text_wrap_overlay(0, 124)
			text_wrap_overlay(1, 709)
			text_wrap_overlay(2, 1295) ##overlays main body text to template

			try:
				os.rename('Temp/output/brNews.png', 'news.png') ##moves to main directory
			except FileExistsError:
				os.remove('news.png')
				os.rename('Temp/output/brNews.png', 'news.png')

			print('[ALERT] Process Finished') ##Nice

			try:
				shutil.rmtree('Temp')
				print('[ALERT] Cleaning Files Complete')
			except:
				print('[WARN] Cleaning Files Failed') ##this doesn't work most of the time idk why
		else:
			time.sleep(100)

else:
	try:
		os.mkdir('/tmp/fnNews/')
	except FileExistsError:
		print('[WARN] /tmp/fnNews already exists. Skipping')
	try:
		os.mkdir('Temp/')
		os.mkdir('Temp/output/')
	except FileExistsError:
		print('[WARN] Temp/ already exists. Skipping')

	while True: ##loop to check for change. Delay: 100s
		links = []; title = []; body = []; chars = [] ##resets lists
		try:
			os.mkdir('Temp/')
			os.mkdir('Temp/output/')
		except:
			pass

		try:
			with open('/tmp/fnNews/news_old' + '.pkl', 'rb') as f: ##pickle load
				news_old = pickle.load(f)
		except:
			print('[WARN] .pkl file doesn\'t exist. Skipping')
			news_old = 'nopickle'

		if news_raw != news_old: ##check for updates
			print('[ALERT] In-game news updated')

			with open('/tmp/fnNews/news_old' + '.pkl', 'wb') as f: ##new pickle dump. to be compared next iteration
			    pickle.dump(news_raw, f, pickle.HIGHEST_PROTOCOL)

			x = 0
			for i in news_raw['messages']:
				title.append(news_raw['messages'][x]['title']) ##adds the data to lists
				links.append(news_raw['messages'][x]['image'])
				body.append(news_raw['messages'][x]['body'])
				x = x + 1

			x = 0; f = ''
			for i in links: ##downloads indervidual images
				url = links[x]
				response = requests.get(url)
				if response.status_code == 200:
					with open("Temp/newsImage"+str(int(x+1))+'.jpg', 'wb') as f:
						f.write(response.content)
						resize(520, 'Temp/newsImage'+str(x+1)+'.jpg', 'Temp/newsImage'+str(x+1)+'.jpg')
						chars.append(str(len(body[int(x)].split()))) ##unrelated line but it works here -- This is for getting the length of the main body of the text.
				x = x + 1

			watermark_photo('files/template.png', 'Temp/output/brNews.png', 'Temp/newsImage1.jpg', position=(115,289))
			watermark_photo('Temp/output/brNews.png', 'Temp/output/brNews.png', 'Temp/newsImage2.jpg', position=(701,289))
			watermark_photo('Temp/output/brNews.png', 'Temp/output/brNews.png', 'Temp/newsImage3.jpg', position=(1286,289)) ##overlays indervidual 3 images over main template

			watermark_text('Temp/output/brNews.png', 'Temp/output/brNews.png', title[0], pos=(124, 561), textSize=38, color=(0, 0, 0))
			watermark_text('Temp/output/brNews.png', 'Temp/output/brNews.png', title[1], pos=(709, 561), textSize=38, color=(0, 0, 0))
			watermark_text('Temp/output/brNews.png', 'Temp/output/brNews.png', title[2], pos=(1295, 561), textSize=38, color=(0, 0, 0)) ##overlays text to template

			text_wrap_overlay(0, 124)
			text_wrap_overlay(1, 709)
			text_wrap_overlay(2, 1295) ##overlays main body text to template

			try:
				os.rename('Temp/output/brNews.png', 'news.png') ##moves to main directory
			except:
				os.remove('news.png')
				os.rename('Temp/output/brNews.png', 'news.png')
			print('[ALERT] Process Finished') ##Nice

			try:
				shutil.rmtree('Temp')
				print('[ALERT] Cleaning Files Complete')
			except:
				print('[WARN] Cleaning Files Failed') ##this doesn't work most of the time idk why
		else:
			time.sleep(100)
