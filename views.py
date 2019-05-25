from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import urllib.parse
import urllib.request
from .models import recruituser, recruitinfo, companyinfo
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup

def get_subjects(): # 채용 정보 크롤링 함수
	subjects = []

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
			cmp_name=company_title,
			date=company_grade,
			recruit_content=company_content
			)

		get_value = company.get("value")
		subjects.append(get_value)

	return subjects

entlist = get_subjects()


def get_rank():
	get_list = []
	for ent_url in entlist:
		api_url = 'http://api.saramin.co.kr/job-search?id=' + ent_url + '&fields=count'
		html_result = requests.get(api_url)
		result_txt = html_result.text
		result_soup = BeautifulSoup(result_txt, 'html.parser')
		view_name = result_soup.find("company").find("name").text
		job_type = result_soup.find("job-type").text
		job_level = result_soup.find("experience-level").text
		require_level = result_soup.find("required-education-level").text


		read_cnt = result_soup.find("read-cnt").text
		view_cnt = int(read_cnt)

		apply_cnt = result_soup.find("apply-cnt").text
		view_apply = int(apply_cnt)

		keyword = result_soup.find('keyword').text
		salary = result_soup.find("salary").text


		view_date = result_soup.find("expiration-timestamp").text
		since_timestamp = time.mktime(datetime.today().timetuple())
		until_timestamp = int(view_date)

		days = (datetime.fromtimestamp(until_timestamp) - datetime.fromtimestamp(since_timestamp)).days

		act_num = result_soup.find("active").text
		view_active = int(act_num)
		companyinfo.objects.create(
		comp_name=view_name,
		j_type=job_type,
		j_level=job_level,
		r_level=require_level,
		r_cnt=view_cnt,
		a_cnt=view_apply,
		k_word=keyword,
		comp_salary=salary,
		submit_date=days,
		view_act=view_active
		)


	return get_list

rank_list = get_rank()
#
# def get_name():
# 	name_list = []
# 	for p in recruitrank.objects.raw('SELECT * FROM seungbot_recruitbank ORDER BY result_num DESC'):
# 		rank_name = p.c_name
# 		ep = recruitinfo.object.get(cmp_name = rank_name)
# 		if ep.cmp_name == rank_name:
# 			name_list.append(rank_name)
# 	return name_list
#
# bot_ans = get_name()
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