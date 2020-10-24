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
import shutil
import json


shutil.rmtree('chromedata', ignore_errors=True)

url = 'https://lolz.guru/forums/contests/'

if cookies.cookies[0] == {}:
	print('\nНе обнаружено cookie! Вставьте ваши cookie в файл cookies.txt (по инструкции)')
	time.sleep(5)
	sys.exit()

time.sleep(0.2)

options = Options()
options.add_argument('--headless')
options.add_argument('--log-level=3')
driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')
os.system("cls")
driver.set_window_size(1920,1080)
driver.set_window_position(0,0)
driver.get(url)




cooknum = 0
for i in range(cookies.cookiecount):
	driver.add_cookie(cookies.cookies[cooknum])
	cooknum = cooknum + 1

time.sleep(0.2)

print('\nПриветствую вас в боте!')

SCROLL_PAUSE_TIME = 1.5

last_height = driver.execute_script("return document.body.scrollHeight")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

time.sleep(1)

driver.refresh()
time.sleep(4)

print('\nНачинаю работу!\n')

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height



time.sleep(1.5)

threads = driver.find_elements_by_xpath("//div[not(.//a//h3//i)][contains(@class, 'discussionListItem')]//a[contains(@class, 'PreviewTooltip')]")

print('Достаю ссылки.\n')

time.sleep(1)

links = []
for elem in threads:
	time.sleep(0.01)
	link = elem.get_attribute('href')
	links.append(link)
	print(elem.get_attribute('href'))


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
	driver.execute_script("window.open('');")
	driver.switch_to.window(driver.window_handles[1])
	driver.get(goto)
	print("Розыгрыш : %s" %driver.title)

	time.sleep(0.1)

	def check_exist_accept():
		try:
			driver.find_element_by_class_name('LztContest--Participate')
		except NoSuchElementException:
			return False
		return True

	cheks = check_exist_accept()


	if cheks == True:

		def check_work():
			work_check = 0
			try:
				driver.find_element_by_class_name('LztContest--alreadyParticipating')
			except NoSuchElementException:
				work_check = 0
			work_check = 1

			if work_check == 1:
				print('Капча введена успешно!\n')
			else:
				print('Капча не верна! Пробую ещё раз.\n')
				captcha_solution()

		def captcha_solution():

			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			gg = driver.find_element_by_xpath("//div[contains(@class, 'ddText')]//img")

			srcimg = gg.get_attribute("src")
			print('Считываю капчу!\n')

			time.sleep(0.3)

			srcimg = srcimg[23:]


			data = base64.b64decode(srcimg)

			with open('captcha.jpg', 'wb') as f:
		   		f.write(data)

			time.sleep(0.1)


			filename = 'captcha.jpg'

			image = Image.open('captcha.jpg')

			width = 300
			height = 90
			resized_img = image.resize((width, height), Image.ANTIALIAS)
			resized_img.save('captchax2.5.jpg')

			time.sleep(0.3)

			imgx3 = Image.open('captchax2.5.jpg')

			pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'


			text = pytesseract.image_to_string(imgx3, config='--psm 6 -c tessedit_char_whitelist=0123456789?+')

			text = text[:-2]

			print('\nКапча = ' + text)

			text = text.replace('?','')

			text = text.replace('+',' ')

			text_chars = sum(len(word) for word in text)


			if text_chars == 5:
				a = int(text[:-2])
				b = int(text[2:])
				result = a + b
				print('Ответ: ' + str(result) + '\n')

			elif text_chars == 4:
				a = int(text[:-2])
				b = int(text[2:])
				result = a + b
				print('Ответ: ' + str(result) + '\n')

			elif text_chars == 3:
				a = int(text[:-1])
				b = int(text[1:])
				result = a + b
				print('Ответ: ' + str(result) + '\n')

			time.sleep(0.01)

			driver.find_element_by_name('captcha_question_answer').send_keys(result)

			driver.find_element_by_class_name('LztContest--Participate').click()

				
			os.remove('captcha.jpg')
			os.remove('captchax2.5.jpg')
			time.sleep(0.3)

			global work_check
			
			check_work()

		captcha_solution()


		driver.close()
		driver.switch_to.window(driver.window_handles[0])


		h = h + 1


	else:
		driver.close()
		driver.switch_to.window(driver.window_handles[0])
		print('Вы не можете участвовать в розыгрыше.\n')

		h = h + 1


print('Работа окончена! Программа будет закрыта через 2 секунды.')
driver.quit()
os.remove('debug.log')
os.remove('ghostdriver.log')
time.sleep(2)
shutil.rmtree('chromedata', ignore_errors=True)
shutil.rmtree('__pycache__', ignore_errors=True)
sys.exit()






