import urllib.parse
import urllib.request
from seungbot.models import *
import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import math
import xmltodict
import json

def get_subjects(api_list): # 채용 정보 크롤링 함수
	entlist = []

	for i in range(len(api_list)):
		req = requests.get(api_list[i])
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
			get_value = company.get("value")
			entlist.append(get_value)
		for ent_url in entlist:
			api_url = 'http://api.saramin.co.kr/job-search?id=' + ent_url + '&fields=count'
			url_id = int(ent_url)
			try:
				url_list.objects.get(comp_url=api_url)
			except:
				url_list.objects.create(
				comp_url=api_url
				)
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

			a = math.sqrt(view_cnt) / 1007
			aa = math.sqrt(a)


			b = round((view_apply / 10))
			if b > 10:
				result = 0.1
			else:
				result = switch(b)
			result_d = 1 / days

			info_num = aa + result + result_d
			result_num = str(info_num)

			if i == 0:
				try:
					recruit_info.objects.get(comp_name=view_name)
					#get_update(view_name, view_cnt, view_apply, days, view_active)
				except:
					recruit_info.objects.create(
					comp_name=view_name,
					com_id=ent_url,
					field='web',
					j_type=job_type,
					j_level=job_level,
					r_level=require_level,
					r_cnt=view_cnt,
					a_cnt=view_apply,
					k_word=keyword,
					comp_salary=salary,
					submit_date=days,
					view_act=view_active,
					score=result_num)

			if i == 1:
				try:
					recruit_info.objects.get(comp_name=view_name)
					#get_update(view_name, view_cnt, view_apply, days, view_active)
				except:
					recruit_info.objects.create(
					comp_name=view_name,
					com_id=ent_url,
					field='system',
					j_type=job_type,
					j_level=job_level,
					r_level=require_level,
					r_cnt=view_cnt,
					a_cnt=view_apply,
					k_word=keyword,
					comp_salary=salary,
					submit_date=days,
					view_act=view_active,
					score=result_num)

			if i == 2:
				try:
					recruit_info.objects.get(comp_name=view_name)
					#get_update(view_name, view_cnt, view_apply, days, view_active)
				except:
					recruit_info.objects.create(
					comp_name=view_name,
					com_id=ent_url,
					field='server',
					j_type=job_type,
					j_level=job_level,
					r_level=require_level,
					r_cnt=view_cnt,
					a_cnt=view_apply,
					k_word=keyword,
					comp_salary=salary,
					submit_date=days,
					view_act=view_active,
					score=result_num)

	return entlist



api_list= ['http://www.saramin.co.kr/zf_user/search?cat_cd=404&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y',
		 'http://www.saramin.co.kr/zf_user/search?cat_cd=408&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y',
		 'http://www.saramin.co.kr/zf_user/search?cat_cd=402&company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9&panel_type=&search_optional_item=y&search_done=y&panel_count=y']
list = get_subjects(api_list)


def switch(x):
	return {
		1: 1,
		2: 0.9,
		3: 0.8,
		4: 0.7,
		5: 0.6,
		6: 0.5,
		7: 0.4,
		8: 0.3,
		9: 0.2,
		10: 0.1,
	}.get(x)


def get_update():
	for p in url_list.objects.all():
		test_url = p.comp_url
		request = urllib.request.Request(test_url)
		response = urllib.request.urlopen(request)
		jsonString = xmltodict.parse(response)
		a = json.dumps(jsonString)
		s = json.loads(a)

		view_name = s["job-search"]["jobs"]["job"]["company"]["name"]["#text"]
		j_cnt = s["job-search"]["jobs"]["@count"]
		act_cnt = int(j_cnt)

		read_cnt = s["job-search"]["jobs"]["job"]["read-cnt"]
		view_cnt = int(read_cnt)

		apply_cnt = s["job-search"]["jobs"]["job"]["apply-cnt"]
		view_apply = int(apply_cnt)

		view_date = s["job-search"]["jobs"]["job"]["expiration-timestamp"]
		since_timestamp = time.mktime(datetime.today().timetuple())
		until_timestamp = int(view_date)
		days = (datetime.fromtimestamp(until_timestamp) - datetime.fromtimestamp(since_timestamp)).days

		a = math.sqrt(view_cnt) / 1007
		aa = math.sqrt(a)

		b = round((view_apply / 10))
		if b > 10:
			result = 0.1
		else:
			result = switch(b)
		result_d = 1 / days
		result_num = aa + result + result_d

		if act_cnt != 1:
			delete_content = recruit_info.objects.get(comp_name=view_name)
			delete_content.delete()

		update_content = recruit_info.objects.get(comp_name=view_name)
		if view_cnt != update_content.r_cnt:
			update_content.r_cnt = view_cnt
			update_content.save()
		elif view_apply != update_content.a_cnt:
			update_content.a_cnt = view_apply
			update_content.save()
		elif days != update_content.submit_date:
			update_content.submit_date = days
			update_content.save()
		elif view_cnt != update_content.r_cnt and view_apply != update_content.a_cnt:
			update_content.r_cnt = view_cnt
			update_content.a_cnt = view_apply
			update_content.save()
		elif view_cnt != update_content.r_cnt and days != update_content.submit_date:
			update_content.r_cnt = view_cnt
			update_content.submit_date = days
			update_content.save()
		elif view_apply != update_content.a_cnt and days != update_content.submit_date:
			update_content.a_cnt = view_apply
			update_content.submit_date = days
			update_content.save()
		elif view_cnt != update_content.r_cnt and view_apply != update_content.a_cnt and days != update_content.submit_date:
			update_content.r_cnt = view_cnt
			update_content.a_cnt = view_apply
			update_content.submit_date = days
			update_content.save()
		else:
			continue
		if result_num != update_content.score:
			update_content.score = result_num
			update_content.save()

	return True

code = get_update()






