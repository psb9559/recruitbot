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
	
	if s_text == "웹개발":
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
		if user:
			user.set_field(s_text)
	if s_text == "서버":
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
		if user:
			user.set_field(s_text)
	if s_text == "시스템개발":
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
		if user:
			user.set_field(s_text)
	if s_text == "대졸":
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
		if user:
			user.set_education(s_text)
	if s_text == "고졸":
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
		if user:
			user.set_education(s_text)
	if s_text == "초대졸":
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
		if user:
			user.set_education(s_text)
	if s_text == "2000":
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
		if user:
			user.set_salary(s_text)
	if s_text == "3000":
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
		if user:
			user.set_salary(s_text)
	if text == "4000":
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
		j_items = []
		r_items = []
		s_items = []
		ep = new_recruit_info2.objects.filter(field="server").order_by("-score")
		for k in ep:
			c_name = k.comp_name
			c_type = k.j_level
			c_edu = k.r_level
			c_sal = k.comp_salary
			items.append(c_name)
			j_items.append(c_type)
			r_items.append(c_edu)
			s_items.append(c_sal)
		try:
			res = {
				"version": "2.0",
				"template": {
						"outputs": [
							{
								"listCard": {
									"header": {
										"title": "서버 추천 기업 순위",
										"imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
									},
									"items": [
										{
											"title": "1위: " + items[0],
											"description": j_items[0] + "," + r_items[0] + "," + s_items[0],
											"imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "2위: " + items[1],
											"description":  j_items[1] + "," + r_items[1] + "," + s_items[1],
											"imageUrl": "http://k.kakaocdn.net/dn/N4Epz/btqqHCfF5II/a3kMRckYml1NLPEo7nqTmK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%AC%B4%EC%A7%80(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "3위: " + items[2],
											"description": j_items[2] + "," + r_items[2] + "," + s_items[2],
											"imageUrl": "http://k.kakaocdn.net/dn/bE8AKO/btqqFHI6vDQ/mWZGNbLIOlTv3oVF1gzXKK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
											}
										}
									],
									"buttons": [
										{
											"label": "서버 직군 채용정보 더 보기",
											"action": "webLink",
											"webLinkUrl": "http://www.saramin.co.kr/zf_user/search?cat_cd=402&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
										}
									]
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
		j_items = []
		r_items = []
		s_items = []
		ep = new_recruit_info2.objects.filter(field="web").order_by("-score")
		for k in ep:
			c_name = k.comp_name
			c_type = k.j_level
			c_edu = k.r_level
			c_sal = k.comp_salary
			items.append(c_name)
			j_items.append(c_type)
			r_items.append(c_edu)
			s_items.append(c_sal)
		try:
			res = {
				"version": "2.0",
				"template": {
						"outputs": [
							{
								"listCard": {
									"header": {
										"title": "웹 추천 기업 순위",
										"imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
									},
									"items": [
										{
											"title": "1위: " + items[0],
											"description": j_items[0] + "," + r_items[0] + "," + s_items[0],
											"imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "2위: " + items[1],
											"description":  j_items[1] + "," + r_items[1] + "," + s_items[1],
											"imageUrl": "http://k.kakaocdn.net/dn/N4Epz/btqqHCfF5II/a3kMRckYml1NLPEo7nqTmK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%AC%B4%EC%A7%80(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "3위: " + items[2],
											"description": j_items[2] + "," + r_items[2] + "," + s_items[2],
											"imageUrl": "http://k.kakaocdn.net/dn/bE8AKO/btqqFHI6vDQ/mWZGNbLIOlTv3oVF1gzXKK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
											}
										}
									],
									"buttons": [
										{
											"label": "웹 직군 채용정보 더 보기",
											"action": "webLink",
											"webLinkUrl": "http://www.saramin.co.kr/zf_user/search?cat_cd=404&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
										}
									]
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
			items = []
			j_items = []
			r_items = []
			s_items = []
			ep = new_recruit_info2.objects.filter(field="system").order_by("-score")
			for k in ep:
				c_name = k.comp_name
				c_type = k.j_level
				c_edu = k.r_level
				c_sal = k.comp_salary
				items.append(c_name)
				j_items.append(c_type)
				r_items.append(c_edu)
				s_items.append(c_sal)
			try:
				res = {
					"version": "2.0",
					"template": {
							"outputs": [
								{
									"listCard": {
										"header": {
											"title": "시스템 추천 기업 순위",
											"imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
										},
										"items": [
											{
												"title": "1위: " + items[0],
												"description": j_items[0] + "," + r_items[0] + "," + s_items[0],
												"imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
												"link": {
													"web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
												}
											},
											{
												"title": "2위: " + items[1],
												"description": j_items[1] + "," + r_items[1] + "," + s_items[1],
												"imageUrl": "http://k.kakaocdn.net/dn/N4Epz/btqqHCfF5II/a3kMRckYml1NLPEo7nqTmK/1x1.jpg",
												"link": {
													"web": "https://namu.wiki/w/%EB%AC%B4%EC%A7%80(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
												}
											},
											{
												"title": "3위: " + items[2],
												"description": j_items[2] + " 학력: " + r_items[2] + " 연봉: " + s_items[2],
												"imageUrl": "http://k.kakaocdn.net/dn/bE8AKO/btqqFHI6vDQ/mWZGNbLIOlTv3oVF1gzXKK/1x1.jpg",
												"link": {
													"web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
												}
											}
										],
										"buttons": [
											{
												"label": "시스템 직군 채용정보 더 보기",
												"action": "webLink",
												"webLinkUrl": "http://www.saramin.co.kr/zf_user/search?cat_cd=408&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
											}
										]
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
								"listCard": {
									"header": {
										"title": "조회수 높은 기업 순위",
										"imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
									},
									"items": [
										{
											"title": "1위: " + items[0],
											"description": "조회수: " + cnt_items[0],
											"imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "2위: " + items[1],
											"description":  "조회수: " + cnt_items[1],
											"imageUrl": "http://k.kakaocdn.net/dn/N4Epz/btqqHCfF5II/a3kMRckYml1NLPEo7nqTmK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%AC%B4%EC%A7%80(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "3위: " + items[2],
											"description": "조회수: " + cnt_items[2],
											"imageUrl": "http://k.kakaocdn.net/dn/bE8AKO/btqqFHI6vDQ/mWZGNbLIOlTv3oVF1gzXKK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
											}
										}
									],
									"buttons": [
										{
											"label": "채용정보 더 보기",
											"action": "webLink",
											"webLinkUrl": "http://www.saramin.co.kr/zf_user/search?company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&cat_cd=404%2C408%2C402&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
										}
									]
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
								"listCard": {
									"header": {
										"title": "지원자수 높은 기업 순위",
										"imageUrl": "http://k.kakaocdn.net/dn/xsBdT/btqqIzbK4Hc/F39JI8XNVDMP9jPvoVdxl1/2x1.jpg"
									},
									"items": [
										{
											"title": "1위: " + items[0],
											"description": "지원자수: " + cnt_items[0],
											"imageUrl": "http://k.kakaocdn.net/dn/APR96/btqqH7zLanY/kD5mIPX7TdD2NAxgP29cC0/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%9D%BC%EC%9D%B4%EC%96%B8(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "2위: " + items[1],
											"description":  "지원자수: " + cnt_items[1],
											"imageUrl": "http://k.kakaocdn.net/dn/N4Epz/btqqHCfF5II/a3kMRckYml1NLPEo7nqTmK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EB%AC%B4%EC%A7%80(%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%94%84%EB%A0%8C%EC%A6%88)"
											}
										},
										{
											"title": "3위: " + items[2],
											"description": "지원자수: " + cnt_items[2],
											"imageUrl": "http://k.kakaocdn.net/dn/bE8AKO/btqqFHI6vDQ/mWZGNbLIOlTv3oVF1gzXKK/1x1.jpg",
											"link": {
												"web": "https://namu.wiki/w/%EC%96%B4%ED%94%BC%EC%B9%98"
											}
										}
									],
									"buttons": [
										{
											"label": "채용정보 더 보기",
											"action": "webLink",
											"webLinkUrl": "http://www.saramin.co.kr/zf_user/search?company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&cat_cd=404%2C408%2C402&panel_type=&search_optional_item=y&search_done=y&panel_count=y"
										}
									]
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



