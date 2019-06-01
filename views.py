from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
import json
import urllib.parse
import urllib.request
from wonbot.models import *
import requests
# from datetime import datetime
# import time
# from bs4 import BeautifulSoup


@csrf_exempt
def message(request):
	json_str = ((request.body).decode('utf-8'))
	received_json_data = json.loads(json_str)

	#text = received_json_data['userRequest']['utterance']

	try:
		text = received_json_data['userRequest']['utterance']
		s_text = received_json_data['action']['detailParams']['sys_text']['value']
		# field = received_json_data['action']['detailParams']['field']['value']
		# salary = received_json_data['action']['detailParams']['salary']['value']
		# currency = received_json_data['action']['detailParams']['sys.unit.currency']['value']
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
	
	user = User_table.get_or_create(user_key)
	
	if text == "웹개발":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "직군 "+ text +" 입력하셨습니다.\n 학력을 입력해주세요"
						}
					}
				]
			} 
		}
		if user:
			user.set_field(text)
	if text == "서버":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "직군 "+ text +" 입력하셨습니다.\n 학력을 입력해주세요"
						}
					}
				]
			}
		}
		if user:
			user.set_field(text)
	if text == "시스템개발":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "직군 "+ text +" 입력하셨습니다.\n 학력을 입력해주세요"
						}
					}
				]
			}
		}
		if user:
			user.set_field(text)
	if text == "대졸":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "학력은 "+ text +" 입력하셨습니다.\n 연봉을 입력해주세요"
						}
					}
				]
			} 
		}
		if user:
			user.set_education(text)
	if text == "고졸":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "학력은 "+ text +" 입력하셨습니다.\n 연봉을 입력해주세요"
						}
					}
				]
			}
		}
		if user:
			user.set_education(text)
	if text == "초대졸":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "학력은 "+ text +" 입력하셨습니다.\n 연봉을 입력해주세요"
						}
					}
				]
			}
		}
		if user:
			user.set_education(text)
	if text == "2000":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "연봉 "+ text +" 입력하셨습니다.\n '보여줘'를 입력하여 입력된 내용 확인"
						}
					}
				]
			} 
		}
		if user:
			user.set_salary(text)
	if s_text == "3000":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "연봉 "+ text +" 입력하셨습니다.\n '보여줘'를 입력하여 입력된 내용 확인"
						}
					}
				]
			}
		}
		if user:
			user.set_salary(text)
	if text == "2600":
		res = {
			"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "연봉 "+ text +" 입력하셨습니다.\n '보여줘'를 입력하여 입력된 내용 확인"
						}
					}
				]
			}
		}
		if user:
			user.set_salary(text)

	if s_text == "보여줘":
		if user:	
			res = {
				"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "직군 :" + user.field  +"\n" + "학력 :" + user.education  +"\n" +"연봉 :" + str(user.salary)  +"\n" +"입력" 
							}
						}
					]
				} 
			}
	if s_text == "서버직군보여줘":
		#r_text = 'server'
		items = []
		ep = new_recruit_info2.objects.filter(field="server").order_by("-score")
		for k in ep:
			c_name = k.comp_name
			items.append(c_name)
		try:
			res = {
				"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "1위: " + items[0] + "\n" + "2위: " + items[1] + "\n" + "3위: " + items[2]
							}
						}
					]
				}
			}
		except:
			res = {
				"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "기업 조회할 수 없음"
							}
						}
					]
				}
			}
	if s_text == "웹직군보여줘":
		# r_text = 'server'
		items = []
		ep = new_recruit_info2.objects.filter(field="web").order_by("-score")
		for k in ep:
			c_name = k.comp_name
			items.append(c_name)
		try:
			res = {
				"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "1위: " + items[0] + "\n" + "2위: " + items[1] + "\n" + "3위: " + items[2]
							}
						}
					]
				}
			}
		except:
			res = {
				"version": "2.0",
				"template": {
					"outputs": [
						{
							"simpleText": {
								"text": "기업 조회할 수 없음"
							}
						}
					]
				}
			}
	if s_text == "시스템직군보여줘":
			# r_text = 'server'
			items = []
			ep = new_recruit_info2.objects.filter(field="system").order_by("-score")
			for k in ep:
				c_name = k.comp_name
				items.append(c_name)
			try:
				res = {
					"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "1위: " + items[0] + "\n" + "2위: " + items[1] + "\n" + "3위: " + items[2]
								}
							}
						]
					}
				}
			except:
				res = {
					"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "기업 조회할 수 없음"
								}
							}
						]
					}
				}
	if s_text == "조회수높은기업보여줘":
			# r_text = 'server'
			items = []
			cnt_items = []
			ep = new_recruit_info2.objects.all().order_by("-r_cnt")
			for k in ep:
				c_name = k.comp_name
				v_cnt = str(k.r_cnt)
				items.append(c_name)
				cnt_items.append(v_cnt)
			try:
				res = {
					"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "1위: " + items[0] + " 조회수: " + cnt_items[0] + "\n" + "2위: " + items[1] + " 조회수: " + cnt_items[1] + "\n" + "3위: " + items[2] + " 조회수: " + cnt_items[2]
								}
							}
						]
					}
				}
			except:
				res = {
					"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "기업 조회할 수 없음"
								}
							}
						]
					}
				}
	if s_text == "지원자수높은기업보여줘":
			# r_text = 'server'
			items = []
			cnt_items = []
			ep = new_recruit_info2.objects.all().order_by("-a_cnt")
			for k in ep:
				c_name = k.comp_name
				v_cnt = str(k.r_cnt)
				items.append(c_name)
				cnt_items.append(v_cnt)
			try:
				res = {
					"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "1위: " + items[0] + " 지원자수: " + cnt_items[0] + "\n" + "2위: " + items[1] + " 지원자수: " + cnt_items[1] + "\n" + "3위: " + items[2] + " 지원자수: " + cnt_items[2]
								}
							}
						]
					}
				}
			except:
				res = {
					"version": "2.0",
					"template": {
						"outputs": [
							{
								"simpleText": {
									"text": "기업 조회할 수 없음"
								}
							}
						]
					}
				}


	return JsonResponse(res)


			# elif text == "㈜날리지큐브" or "매드업":
	# 	# 	ep = recruitbot.objects.get(cmp_name = text)
	# 	# 	if user:
	# 	# 		res = {
	# 	# 			"version": "2.0",
	# 	# 				"template": {
	# 	# 					"outputs": [
	# 	# 						{
	# 	# 							"simpleText": {
	# 	# 								"text": "회사명 :" + ep.cmp_name  +"\n" + "마감날짜 :" + ep.date  +"\n" +"채용메시지 :" + ep.recruit_msg  +"\n" +"크롤링 저장"
	# 	# 						}
	# 	# 					}
	# 	# 				]
	# 	# 			}
	# 	# 		}	return JsonResponse(res)
