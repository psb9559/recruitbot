from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
#import urllib.parse
#import urllib.request
from seungbot.models import *
import requests
#import cron

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
		ep = recruit_info.objects.raw('SELECT * FROM seungbot_recruit_info WHERE field = %s ORDER BY a_cnt DESC', [text])
		for i in range(1, 4):
			if user_bot:
				res = {
					"version": "2.0",
						"template": {
							"outputs": [
								{
									"simpleText": {
										"text": "회사명 :" + ep[i].comp_name  + "\n" + "경력/신입 :" + ep[i].j_level  + "\n" +"지원자수 :" + ep[i].a_cnt  + "\n" + "남은 마감일: " + ep[i].submit_date
								}
							}
						]
					}
				}
	elif text == "웹직군 기업보여줘":
		text = 'web'
		ep = recruit_info.objects.raw('SELECT * FROM seungbot_recruit_info WHERE field = %s ORDER BY a_cnt DESC', [text])
		for i in range(1, 4):
			if user_bot:
				res = {
					"version": "2.0",
						"template": {
							"outputs": [
								{
									"simpleText": {
										"text": "회사명 :" + ep[i].comp_name  + "\n" + "경력/신입 :" + ep[i].j_level  + "\n" +"지원자수 :" + ep[i].a_cnt  + "\n" + "남은 마감일: " + ep[i].submit_date
								}
							}
						]
					}
				}
	elif text == "시스템직군 기업보여줘":
		text = 'system'
		ep = recruit_info.objects.raw('SELECT * FROM seungbot_recruit_info WHERE field = %s ORDER BY a_cnt DESC', [text])
		for i in range(1, 4):
			if user_bot:
				res = {
					"version": "2.0",
						"template": {
							"outputs": [
								{
									"simpleText": {
										"text": "회사명 :" + ep[i].comp_name  + "\n" + "경력/신입 :" + ep[i].j_level  + "\n" +"지원자수 :" + ep[i].a_cnt  + "\n" + "남은 마감일: " + ep[i].submit_date
								}
							}
						]
					}
				}


	return JsonResponse(res)