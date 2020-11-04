from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import cv2 
import pytesseract
from PIL import Image
import requests
from io import BytesIO
import os
import base64
from selenium.common.exceptions import NoSuchElementException
import cookies
import sys
import json
import config


version = 0.04

response = requests.get('https://api.github.com/repos/meldoner/lztautoparticipation/releases/latest')
latestjson = response.json()
latestver = latestjson['tag_name']
latestver = float(latestver)



try:
	waiting = config.waiting * 60
	auto_start = config.auto_start
except:
	print('Неверные значения в config.py')
	time.sleep(3)
	sys.exit()


def work():

	url = 'https://lolz.guru/forums/contests/'

	if cookies.cookies[0] == {}:
		print('\nНе обнаружено cookie! Вставьте ваши cookie в файл cookies.txt (по инструкции)')
		time.sleep(5)
		sys.exit()


	options = Options()
	options.add_argument('--log-level=3')
	driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')
	os.system("cls")
	if latestver == version:
		print('У вас последняя версия программы - ' + str(version) + '.')
	else:
		print('У вас устаревшая версия программы - ' + str(version) + '. Последняя версия программы - ' + str(latestver) + '.')
	driver.set_window_size(1920,1080)
	driver.set_window_position(0,0)
	driver.get(url)


	cooknum = 0
	for i in range(cookies.cookiecount):
		driver.add_cookie(cookies.cookies[cooknum])
		cooknum = cooknum + 1

	time.sleep(0.3)

	print('\nПриветствую вас в боте!')


	flags = driver.find_element_by_css_selector('a.OverlayTrigger.button.Tooltip').get_attribute("href")

	if flags == 'https://lolz.guru/account/set-viewed-contests-visibility':
		driver.find_element_by_css_selector('a.OverlayTrigger.button.Tooltip').click()
		time.sleep(0.5)
		driver.refresh()

	print('\nНачинаю работу')

	page = 1

	numofpages = driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div/div[2]/div[2]').get_attribute("data-last")
	print('Кол-во страниц розыгрыша = ' + str(numofpages))

	print('\nДостаю ссылки')

	links = []
	
	for get_links in range(int(numofpages)):
		driver.get('https://lolz.guru/forums/contests/page-' + str(page))

		threads = driver.find_elements_by_xpath("//div[not(.//a//h3//i)][contains(@class, 'discussionListItem')]//a[contains(@class, 'PreviewTooltip')]")

		for elem in threads:
			time.sleep(0.01)
			link = elem.get_attribute('href')
			links.append(link)
			print(elem.get_attribute('href'))

		page = page + 1




	sumlist = len(links)
	print('\nВсего розыгрышей: ' + str(sumlist) + '\n')

	if sumlist == 0:
		print('Нет розыгрышей, в которых вы можете участвовать!')
	else:
		print('Список готов! Начинаю участвовать!\n')
	h = 0
	already = 0
	time.sleep(0.3)
	for i in range(sumlist):
		goto = links[h]
		driver.get(goto)
		print("%s" %driver.title)

		time.sleep(0.05)

		def check_exist_accept():
			try:
				driver.find_element_by_class_name('LztContest--Participate')
			except NoSuchElementException:
				return False
			return True

		cheks = check_exist_accept()


		if cheks == True:

			def check_work():
				try:
					driver.find_element_by_class_name('LztContest--alreadyParticipating hidden')
				except NoSuchElementException:
					work_check = 1
				work_check = 0

				if work_check == 1:
					print('Капча введена успешно!\n')
					return True
				else:
					print('Капча не верна! Пробую ещё раз.\n')
					return False

			def captcha_solution():

				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

				time.sleep(0.1)

				gg = driver.find_element_by_xpath("//div[contains(@class, 'ddText')]//img")

				srcimg = gg.get_attribute("src")
				print('Считываю капчу!\n')

				srcimg = srcimg[23:]


				data = base64.b64decode(srcimg)

				with open('captcha.jpg', 'wb') as f:
			   		f.write(data)


				filename = 'captcha.jpg'

				image_to_crop = Image.open('captcha.jpg', 'r')
				image = image_to_crop.crop((-1, 8, 65, 22))
				image.save('cropcaptcha.png')

			


				image = Image.open('cropcaptcha.png', 'r')
				pixels = list(image.getdata())
				new_pixels_list = []
				for rgb in pixels:
				    if rgb[0] < 160:
				        rgb = (0, 0, 0)
				    if rgb[0] > 160:
				        rgb = (255, 255, 255)
				    new_pixels_list.append(rgb)
				image.putdata(new_pixels_list)
				image.save('captchanormal.png')


				image = Image.open('captchanormal.png')
				width = 198
				height = 42
				resized_img = image.resize((width, height), Image.ANTIALIAS)
				resized_img.save('captchanormalx.png')



				imgt = Image.open('captchanormalx.png')

				pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\\tesseract.exe'

				time.sleep(0.1)

				text = pytesseract.image_to_string(imgt, config='--psm 10 --oem 1 -c tessedit_char_whitelist=0123456789+?')

				text = text.split('\n')[0]

				text = text.replace('?','')

				print('Капча = ' + text)

				firstpart = int(text.split('+')[0])

				secondpart = int(text.split('+')[1])

				result =  firstpart + secondpart

				print('\nОтвет = ' + str(result) + '\n')


				time.sleep(0.01)

				driver.find_element_by_name('captcha_question_answer').send_keys(result)

				driver.find_element_by_class_name('LztContest--Participate').click()

					
				
				time.sleep(2)


				try:
					driver.find_element_by_css_selector('div.baseHtml.errorDetails')
				except NoSuchElementException:
					return True
				return False
				

			try_again = captcha_solution()

			if try_again == False:
				print('Капча не верна! Пробую ещё раз.\n')
				driver.find_element_by_class_name('OverlayCloser').click()
				captcha_solution()
			else:
				print('Капча успешно введена!\n')
				pass



			h = h + 1


		else:
			erorr = driver.find_element_by_css_selector('div.error.mn-15-0-0').text
			print(erorr + '\n')

			h = h + 1

	if config.auto_start == 1:
		print('Работа завершена! Запуск скрипта снова через ' + str(config.waiting) + ' минут.')
		print('Сейчас - ' + time.strftime("%H:%M", time.gmtime()))
	else:
		print('Работа окончена! Программа будет закрыта через 2 секунды.')

	driver.quit()

	try:
		os.remove('debug.log')
		os.remove('ghostdriver.log')
	except:
		pass

	time.sleep(2)


try:
	waiting = config.waiting * 60
	auto_start = config.auto_start
except:
	print('Неверные значения в config.py')
	time.sleep(3)
	sys.exit()

if auto_start == 0:
	work()
	os.remove('captchanormalx.png')
	os.remove('captchanormal.png')
	os.remove('captcha.jpg')
	os.remove('cropcaptcha.png')
	sys.exit()


while auto_start == 1:
		work()
		os.remove('captchanormalx.png')
		os.remove('captchanormal.png')
		os.remove('captcha.jpg')
		os.remove('cropcaptcha.png')
		time.sleep(waiting)





