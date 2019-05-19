from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
#import urllib.parse
#import datetime
import time
from .models import recruituser, recruitinfo
import requests
from bs4 import BeautifulSoup

def get_subjects(): # 채용 정보 크롤링 함수
	subjects = []
	while True:
		req = requests.get('http://www.saramin.co.kr/zf_user/search?cat_cd=404&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y')
		html = req.text
		soup = BeautifulSoup(html, 'html.parser')
   
		divs1 = soup.find_all("div", {"class": "item_recruit"})
		for company in divs1:
			content = company.find("div", {"class": "area_job"}).find("h2", {"class": "job_tit"}).find("a")
			company_content = content.get('title')
			grade1 = company.find("div", {"class": "area_job"}).find("div", {"class": "job_date"})
			grade2 = grade1.find("span", {"class": "date"})
			company_grade = grade2.text
			name = company.find("div", {"class": "area_corp"}).find("strong", {"class": "corp_name"}).find("a")
			company_title = name.get('title')
        	try:
            	recruitinfo.objects.get(cmp_name=company_title)
        	except:
            	recruitinfo.objects.create(
            	cmp_name = company_title,
            	date = company_grade,
            	recruit_content = company_content
            	)
        	# url을 받아서 url 안의 내용들을 크롤링 하는 소스
        	url_received = company.find("h2", {"class": "job_tit"}).find("a")
        	get_url = url_received.get('class href')
        	result_url = str(get_url)
        	subjects.append(result_url)
			time.sleep(3600)

    return subjects

result_url = ''
entlist = []
entlist = get_subjects()

view_list = []
day_list = []
url_list = []
rank_list = []
def get_rank():
    for ent_url in entlist:
        url_content = 'http://www.saramin.co.kr' + ent_url
        html_result = requests.get(url_content)
        result_txt = html_result.text
        result_soup = BeautifulSoup(result_txt, 'html.parser')
        view_num = result_soup.find("ul", {"class": "meta"}).find("li").find("strong") # 조회수 크롤링
        result_view = int(view_num) # 조회수

        view_day = result_soup.find("div", {"class": "info_timer"}).find("span", {"class": "day"})
        result_day = int(view_day) # 남은 일수
        url_list.append(url_content)
        view_list.append(result_view)
        day_list.append(result_day) # 크롤링한 url, 조회수, 남은 일수를 각각 리스트에 대입
	for i in range(0, 40):
		num1 = view_list[i]
		num2 = day_list[i]
		rank_num = num1 + num2
		rank_list.append(rank_num)







@csrf_exempt
def message(request):
	json_str = ((request.body).decode('utf-8'))
	received_json_data = json.loads(json_str)
	
	try:
		text = received_json_data['userRequest']['utterance']
		s_text = received_json_data['action']['detailParams']['sys_text']['value']
		user_key = received_json_data['userRequest']['user']['properties']['plusfriendUserKey']	
	except KeyError:
		# 비정상적인 JSON 요청
		return JsonResponse({
		"version": "2.0",
			"template": {
				"outputs": [
					{
						"simpleText": {
							"text": "요청이 비정상적입니다. 관리자에게 문의해주세요."
						}
					}
				]
			}
		})
	
	user_bot = recruituser.get_or_create(user_key)
	
	if s_text == "SI" or "SM" or "SW":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "직군 "+ s_text +" 입력하셨습니다.\n 학력을 입력해주세요"
						}
					}
				]
			} 
		}
		if user_bot:
			user_bot.set_field(s_text)
	elif s_text == "대졸" or "고졸" or "초대졸":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "학력은 "+ s_text +" 입력하셨습니다.\n 연봉을 입력해주세요"
						}
					}
				]
			} 
		}
		if user_bot:
			user_bot.set_education(s_text)
	elif s_text == "2000" or "3000" or "4000":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "연봉 "+ s_text +" 입력하셨습니다.\n '보여줘'를 입력하여 입력된 내용 확인"
						}
					}
				]
			} 
		}
		if user_bot:
			user_bot.set_salary(strtoint(s_text))
	elif s_text == "보여줘":
		if user_bot:
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "직군 :" + user.u_field  +"\n" + "학력 :" + user.u_education  +"\n" +"연봉 :" + str(user.salary)  +"\n" +"입력" 
							}
						}
					]
				} 
			}			
	elif text == "경일게임아카데미" :
		ep = recruitinfo.objects.get(cmp_name = text)
		if user_bot:
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "회사명 :" + ep.cmp_name  +"\n" + "마감날짜 :" + ep.date  +"\n" +"채용메시지 :" + ep.recruit_content  +"\n" +"크롤링 저장" 
							}
						}
					]
				} 
			}
	return JsonResponse(res)