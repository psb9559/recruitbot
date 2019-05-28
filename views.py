from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import urllib.parse
import urllib.request
from seungbot.models import *
import requests
#import cron
#from datetime import datetime
#import time
#from bs4 import BeautifulSoup
#import math

# def get_subjects(url_list): # 채용 정보 크롤링 함수
# 	entlist = []
#
# 	for i in range(len(url_list)):
# 		req = requests.get(url_list[i])
# 		html = req.text
# 		soup = BeautifulSoup(html, 'html.parser')
# 		divs1 = soup.find_all("div", {"class": "item_recruit"})
# 		for company in divs1:
# 			content = company.find("div", {"class": "area_job"}).find("h2", {"class": "job_tit"}).find("a")
# 			company_content = content.get('title')
# 			grade1 = company.find("div", {"class": "area_job"}).find("div", {"class": "job_date"})
# 			grade2 = grade1.find("span", {"class": "date"})
# 			company_grade = grade2.text
# 			name = company.find("div", {"class": "area_corp"}).find("strong", {"class": "corp_name"}).find("a")
# 			company_title = name.get('title')
# 			try:
# 				recruitinfo.objects.get(cmp_name=company_title)
# 			except:
# 				recruitinfo.objects.create(
# 				cmp_name=company_title,
# 				date=company_grade,
# 				recruit_content=company_content
# 				)
#
# 			get_value = company.get("value")
# 			entlist.append(get_value)
# 			for ent_url in entlist:
# 				api_url = 'http://api.saramin.co.kr/job-search?id=' + ent_url + '&fields=count'
# 				html_result = requests.get(api_url)
# 				result_txt = html_result.text
# 				result_soup = BeautifulSoup(result_txt, 'html.parser')
# 				view_name = result_soup.find("company").find("name").text
# 				job_type = result_soup.find("job-type").text
# 				job_level = result_soup.find("experience-level").text
# 				require_level = result_soup.find("required-education-level").text
#
#
# 				read_cnt = result_soup.find("read-cnt").text
# 				view_cnt = int(read_cnt)
#
# 				apply_cnt = result_soup.find("apply-cnt").text
# 				view_apply = int(apply_cnt)
#
# 				keyword = result_soup.find('keyword').text
# 				salary = result_soup.find("salary").text
#
#
# 				view_date = result_soup.find("expiration-timestamp").text
# 				since_timestamp = time.mktime(datetime.today().timetuple())
# 				until_timestamp = int(view_date)
#
# 				days = (datetime.fromtimestamp(until_timestamp) - datetime.fromtimestamp(since_timestamp)).days
#
# 				act_num = result_soup.find("active").text
# 				view_active = int(act_num)
#
# 				if i == 0:
# 					try:
# 						test.objects.get(comp_name=view_name)
# 					except:
# 						test.objects.create(
# 						comp_name=view_name,
# 						j_type=job_type,
# 						j_level=job_level,
# 						r_level=require_level,
# 						r_cnt=view_cnt,
# 						a_cnt=view_apply,
# 						k_word=keyword,
# 						comp_salary=salary,
# 						submit_date=days,
# 						view_act=view_active,
# 						field = 'web')
#
# 				if i == 1:
# 					try:
# 						test.objects.get(comp_name=view_name)
# 					except:
# 						test.objects.create(
# 						comp_name=view_name,
# 						j_type=job_type,
# 						j_level=job_level,
# 						r_level=require_level,
# 						r_cnt=view_cnt,
# 						a_cnt=view_apply,
# 						k_word=keyword,
# 						comp_salary=salary,
# 						submit_date=days,
# 						view_act=view_active,
# 						field = 'system')
#
# 				if i == 2:
# 					try:
# 						test.objects.get(comp_name=view_name)
# 					except:
# 						test.objects.create(
# 						comp_name=view_name,
# 						j_type=job_type,
# 						j_level=job_level,
# 						r_level=require_level,
# 						r_cnt=view_cnt,
# 						a_cnt=view_apply,
# 						k_word=keyword,
# 						comp_salary=salary,
# 						submit_date=days,
# 						view_act=view_active,
# 						field = 'server')
#
# 	return entlist
#
#
#
# url_list= ['http://www.saramin.co.kr/zf_user/search?cat_cd=404&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y',
# 		 'http://www.saramin.co.kr/zf_user/search?cat_cd=408&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y',
# 		 'http://www.saramin.co.kr/zf_user/search?cat_cd=402&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y']
# list = get_subjects(url_list)
#
# def get_rank(type):
# 	if type == 'server':
# 		for key in test.objects.filter(field=type):
# 			app_cnt = key.a_cnt
# 			view_cnt = key.r_cnt
# 			date_cnt = key.submit_date
# 			a = pow(view_cnt, 2) / 1007
# 			aa = math.sqrt(a)
# 			aaa = aa / 7
#
# 			b = round((app_cnt / 10))
# 			if b > 10:
# 				result = 0.1
# 			else:
# 				result = switch(b)
# 			result_d = 1 / date_cnt
# 			result_num = aaa + result + result_d
#
#
#
#
#
#
#
#
# def switch(x):
# 	return {
# 		1: 1,
# 		2: 0.9,
# 		3: 0.8,
# 		4: 0.7,
# 		5: 0.6,
# 		6: 0.5,
# 		7: 0.4,
# 		8: 0.3,
# 		9: 0.2,
# 		10: 0.1,
# 	}.get(x)
#
#
#
#
#

@csrf_exempt
def message(request):
	json_str = ((request.body).decode('utf-8'))
	received_json_data = json.loads(json_str)
	try:
		text = received_json_data['userRequest']['utterance']
		s_text = received_json_data['action']['detailParams']['sys_text']['value']
		user_key = received_json_data['userRequest']['user']['properties']['plusfriendUserKey']
	except KeyError:
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
	
	if s_text == "웹개발" or "시스템개발" or "서버":
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
			user_bot.set_salary(s_text)
	elif s_text == "보여줘":
		if user_bot:
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "직군 :" + user_bot.u_field  +"\n" + "학력 :" + user_bot.u_education  +"\n" +"연봉 :" + str(user_bot.salary)  +"\n" +"입력"
							}
						}
					]
				} 
			}			

	elif text == "서버직군 기업보여줘":
		text = 'server'
		#get_rank(text)
		ep = test.objects.get(field=text)
		if user_bot:
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "회사명 :" + ep.comp_name  + "\n" + "경력/신입 :" + ep.j_level  + "\n" +"지원자수 :" + ep.a_cnt  + "\n" + "남은 마감일: " + ep.submit_date
							}
						}
					]
				}
			}
	elif text == "웹직군 기업보여줘":
		text = 'web'
		#get_rank(text)
		ep = test.objects.get(field=text)
		if user_bot:
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "회사명 :" + ep.comp_name  + "\n" + "경력/신입 :" + ep.j_level  + "\n" +"지원자수 :" + ep.a_cnt  + "\n" + "남은 마감일: " + ep.submit_date
							}
						}
					]
				}
			}
	elif text == "시스템직군 기업보여줘":
		text = 'system'
		#get_rank(text)
		ep = test.objects.get(field=text)
		if user_bot:
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "회사명 :" + ep.comp_name  + "\n" + "경력/신입 :" + ep.j_level  + "\n" +"지원자수 :" + ep.a_cnt  + "\n" + "남은 마감일: " + ep.submit_date
							}
						}
					]
				}
			}


	return JsonResponse(res)