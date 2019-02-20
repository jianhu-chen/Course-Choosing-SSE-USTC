# -*- coding: utf-8 -*-
# @File 	: Student.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-01 13:08:45
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-20 16:27:56

import requests
import re
import os
import time 
import random
import threading # 多线程

from prettytable import PrettyTable  # 打印表格


class Student:
	def __init__(self, userAccount, userLocation, userYear, userTerm):
		'''
			作用：初始化用户信息
		'''
		self.userId = userAccount['userId']
		self.userPwd = userAccount['userPwd']
		self.userName = self.userId
		self.userLocation = userLocation
		self.userYear = userYear
		self.userTerm = userTerm
		self.userYearTerm = userYear + '-' + userTerm
		# 构建一个Session对象，可以保存页面Cookie
		self.sess = requests.Session()
		# 构造请求报头
		self.headers = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'}

	def getCheckcodeFromCookies(self, cookies):
		'''
			作用：获取验证码
			返回：验证码
		'''
		text = cookies['CheckCode']
		textNum = [int(x) for x in text]
		textSum = textNum[0] + textNum[1] + textNum[2] + textNum[3]
		return textSum

	def getStuInfoHtml(self):
		'''
			作用：获取个人信息页面源码，用于测试信息是否爬取成功
			返回：个人信息页面源码
		'''
		stuInfoUrl = 'http://mis.sse.ustc.edu.cn/PersonalSetting/ModifyPersonalInfoStu.aspx'
		response = self.sess.get(stuInfoUrl, headers=self.headers)
		stuInfoHtml = response.text.encode('utf-8')
		return stuInfoHtml

	def printStuInfo(self):
		'''
			作用：打印个人信息
			返回：是否登陆成功
		'''
		self.writeLogs('正在询您的个人信息，请稍候...')
		stuInfoHtml = self.getStuInfoHtml()
		try:
			namePattern = re.compile(r'txtName",allow.*?value:"(.*?)"', re.S)
			name = namePattern.findall(stuInfoHtml)[0].strip()
			stuNoPattern = re.compile(r'txtStuNo",allow.*?value:"(.*?)"', re.S)
			stuNo = stuNoPattern.findall(stuInfoHtml)[0].strip()
			nationPattern = re.compile(r'txtNation",max.*?value:"(.*?)"', re.S)
			nation = nationPattern.findall(stuInfoHtml)[0].strip()
			birthdayPattern = re.compile(r'dpBirthDay",value:"(.*?)"', re.S)
			birthday = birthdayPattern.findall(stuInfoHtml)[0].strip()
			emailPattern = re.compile(r'txtEmail",allow.*?value:"(.*?)"', re.S)
			email = emailPattern.findall(stuInfoHtml)[0].strip()
			phonePattern = re.compile(r'txtPhone",max.*?value:"(.*?)"', re.S)
			phone = phonePattern.findall(stuInfoHtml)[0].strip()
		except:
			self.writeLogs('查询您的个人信息失败...\n请检查您的账号/密码是否输入正确！', error=True)
			return False
		self.writeLogs('查询您的个人信息成功...')
		# 记录名字信息
		self.userName = name
		self.writeLogs('-'*60 + '\n' + \
			'学号：{}\t姓名：{}\t出生日期：{}'.format(stuNo, name, birthday) + '\n' + \
			'联系方式：{}\t电子邮件：{}'.format(phone, email) + '\n' + \
			'-'*60
			, info = False)
		return True
			
	def login(self):
		'''
			作用：登录软件学院信息化平台并获取学生信息页面
			返回：是否登陆成功
		'''
		# 登录接口
		loginUrl = 'http://mis.sse.ustc.edu.cn/default.aspx'
		# 验证码地址
		checkcodeUrl = 'http://mis.sse.ustc.edu.cn/ValidateCode.aspx?ValidateCodeType=1&0.011150883024061309'
		# 发送图片的请求，获取图片数据流
		response = self.sess.get(checkcodeUrl, headers=self.headers)
		# checkcodeData = response.content
		cookies = response.cookies.get_dict()
		# 获取验证码里的数字之和
		textSum = self.getCheckcodeFromCookies(cookies)
		# 构造登录数据
		data = {
			'__EVENTTARGET' : 'winLogin$sfLogin$ContentPanel1$btnLogin',
			'__EVENTARGUMENT' : '',
			'__VIEWSTATE' : '/wEPDwUKLTMzNjg2NDcwNGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgwFCHdpbkxvZ2luBRB3aW5Mb2dpbiRzZkxvZ2luBRZ3aW5Mb2dpbiRzZkxvZ2luJGN0bDAwBR93aW5Mb2dpbiRzZkxvZ2luJHR4dFVzZXJMb2dpbklEBRx3aW5Mb2dpbiRzZkxvZ2luJHR4dFBhc3N3b3JkBRx3aW5Mb2dpbiRzZkxvZ2luJHR4dFZhbGlkYXRlBR53aW5Mb2dpbiRzZkxvZ2luJENvbnRlbnRQYW5lbDMFLHdpbkxvZ2luJHNmTG9naW4kQ29udGVudFBhbmVsMyRjYnhTYXZlTXlJbmZvBS53aW5Mb2dpbiRzZkxvZ2luJENvbnRlbnRQYW5lbDMkYnRuUmVmVmFsaWRDb2RlBR53aW5Mb2dpbiRzZkxvZ2luJENvbnRlbnRQYW5lbDEFJ3dpbkxvZ2luJHNmTG9naW4kQ29udGVudFBhbmVsMSRidG5Mb2dpbgUIV25kTW9kYWy2ePrTvZjBBql35+4HcyIqDYPkPGG8BipKo3FdUE8sdA==',
			'X_CHANGED' : 'true',
			'winLogin$sfLogin$txtUserLoginID' : self.userId,
			'winLogin$sfLogin$txtPassword' : self.userPwd,
			'winLogin$sfLogin$txtValidate' : textSum,
			'winLogin_Hidden' : 'false',
			'WndModal_Hidden' : 'true',
			'X_TARGET' : 'winLogin_sfLogin_ContentPanel1_btnLogin',
			'winLogin_sfLogin_ctl00_Collapsed' : 'false',
			'winLogin_sfLogin_ContentPanel3_Collapsed' : 'false',
			'winLogin_sfLogin_ContentPanel1_Collapsed' : 'false',
			'winLogin_sfLogin_Collapsed' : 'false',
			'winLogin_Collapsed' : 'false',
			'WndModal_Collapsed' : 'false',
			'X_STATE' : 'e30=',
			'X_AJAX' : 'true',
		}			
		# 发送登录需要的POST数据，获取登录后的Cookie(保存在sess里)
		self.writeLogs('正在进入软件学院信息化平台...')
		response = self.sess.post(loginUrl, data=data, headers=self.headers)
		# 测试是否登录成功	
		# try:
		# 	re.compile(r'HomePage', re.S).findall(response.text.encode('utf-8'))[0]
		# except:
		# 	isLogin = False
		# else:
		# 	isLogin = True
		# if isLogin:
		# 打印学生信息，并返回是否查询成功
		loginResult = self.printStuInfo()
		# 返回登录是否成功
		return loginResult

	def getStuChoosedHtml(self):
		'''
			作用：获取已选课程网页源码
			返回：已选课程网页源码
		'''
		self.writeLogs('正在查询您的已选课程，请稍候...')
		# 用已有登录状态的Cookie发送请求，获取目标页面源码
		stuChoosedUrl = 'http://mis.sse.ustc.edu.cn/Teaching/CourseChooseInfo/ListStudentChoosed.aspx'
		data = {
			'__EVENTTARGET' : 'global$QueryForm$ctl00$ddlYearTerm',
			'__EVENTARGUMENT' : '',
			'__VIEWSTATE' : '/wEPDwUKMTY1MDg5NDA0NWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgoFBmdsb2JhbAUQZ2xvYmFsJFF1ZXJ5Rm9ybQUkZ2xvYmFsJFF1ZXJ5Rm9ybSRjdGwwMCRUcmlnZ2VyU2VhcmNoBSJnbG9iYWwkUXVlcnlGb3JtJGN0bDAwJGRkbFllYXJUZXJtBSdnbG9iYWwkUXVlcnlGb3JtJGN0bDAwJHR4dENob29zZWRDcmVkaXQFI2dsb2JhbCRRdWVyeUZvcm0kY3RsMDAkdHh0TWF4Q3JlZGl0BRBnbG9iYWwkTWFpblBhbmVsBRlnbG9iYWwkTWFpblBhbmVsJEdyaWRMaXN0BQhXbmRNb2RhbAUNV25kTW9kYWxTbWFsbFpa0iUSyEAielWliBEkTe5bNJ4XM7afcwd3z9sFCGAp',
			'global$QueryForm$ctl00$TriggerSearch' : '课程名称',
			'global$QueryForm$ctl00$ddlYearTerm' : self.userYearTerm,
			'X_CHANGED' : 'false',
			'WndModal_Hidden' : 'true',
			'WndModalSmall_Hidden' : 'true',
			'global_QueryForm_Collapsed' : 'false',
			'global_MainPanel_GridList_Collapsed' : 'false',
			'global_MainPanel_GridList_SelectedRowIndexArray' : '',
			'global_MainPanel_GridList_HiddenColumnIndexArray' : '',
			'global_MainPanel_GridList_RowStates' : '[]',
			'global_MainPanel_Collapsed' : 'false',
			'global_Collapsed' : 'false',
			'WndModal_Collapsed' : 'false',
			'WndModalSmall_Collapsed' : 'false',
			'X_STATE' : 'eyJnbG9iYWxfUXVlcnlGb3JtX2N0bDAwX2RkbFllYXJUZXJtIjp7IlhfSXRlbXMiOltbIjIwMTgtMiIsIjIwMTgtMiIsMV0sWyIyMDE4LTEiLCIyMDE4LTEiLDFdLFsiMjAxOC0wIiwiMjAxOC0wIiwxXSxbIjIwMTctMiIsIjIwMTctMiIsMV0sWyIyMDE3LTEiLCIyMDE3LTEiLDFdLFsiMjAxNy0wIiwiMjAxNy0wIiwxXSxbIjIwMTYtMiIsIjIwMTYtMiIsMV0sWyIyMDE2LTEiLCIyMDE2LTEiLDFdLFsiMjAxNi0wIiwiMjAxNi0wIiwxXSxbIjIwMTUtMiIsIjIwMTUtMiIsMV0sWyIyMDE1LTEiLCIyMDE1LTEiLDFdLFsiMjAxNS0wIiwiMjAxNS0wIiwxXSxbIjIwMTQtMiIsIjIwMTQtMiIsMV0sWyIyMDE0LTEiLCIyMDE0LTEiLDFdLFsiMjAxNC0wIiwiMjAxNC0wIiwxXSxbIjIwMTMtMiIsIjIwMTMtMiIsMV0sWyIyMDEzLTEiLCIyMDEzLTEiLDFdLFsiMjAxMy0wIiwiMjAxMy0wIiwxXSxbIjIwMTItMiIsIjIwMTItMiIsMV0sWyIyMDEyLTEiLCIyMDEyLTEiLDFdLFsiMjAxMS0yIiwiMjAxMS0yIiwxXSxbIjIwMTEtMSIsIjIwMTEtMSIsMV0sWyIyMDEwLTIiLCIyMDEwLTIiLDFdLFsiMjAxMC0xIiwiMjAxMC0xIiwxXSxbIjIwMDktMiIsIjIwMDktMiIsMV1dLCJTZWxlY3RlZFZhbHVlIjoiMjAxOC0yIn0sImdsb2JhbF9RdWVyeUZvcm1fY3RsMDBfdHh0Q2hvb3NlZENyZWRpdCI6eyJUZXh0IjoiMCJ9LCJnbG9iYWxfUXVlcnlGb3JtX2N0bDAwX3R4dE1heENyZWRpdCI6eyJUZXh0IjoiMjMifSwiZ2xvYmFsX01haW5QYW5lbF9HcmlkTGlzdCI6eyJYX1Jvd3MiOnsiVmFsdWVzIjpbXSwiRGF0YUtleXMiOltdfX19',
			'X_AJAX' : 'false',
		}
		response = self.sess.post(stuChoosedUrl, data = data, headers=self.headers)
		stuChoosedHtml = response.text.encode('utf-8')
		return stuChoosedHtml

	def printStuChoosed(self):
		'''
			作用：打印已选课程
			stuChoosedHtml：包含已选课程信息的html页面
		'''
		stuChoosedHtml = self.getStuChoosedHtml()
		self.writeLogs('{}的已选课程信息如下：'.format(self.userName))
		# 已选学分
		choosedCreditPattern = re.compile(r'txtChoosedCredit",value:"(.*?)"', re.S)
		choosedCredit = choosedCreditPattern.findall(stuChoosedHtml)[0]
		# 限选学分
		maxCreditPattern = re.compile(r'txtMaxCredit",value:"(.*?)"', re.S)
		maxCredit = maxCreditPattern.findall(stuChoosedHtml)[0]
		self.writeLogs('\t'*3+'【学年学期：{}\t已选学分：{}\t限选学分：{}】'.format(self.userYearTerm, choosedCredit, maxCredit), info=False)
		tablebHead = ['序号', '课程编号', '课程名称', '学分', '班号', '授课老师', '授课时间地点', \
						'选课开始时间', '选课结束时间', '退选结束时间', '已选人数', '最大人数']
		choosedCoursePattern = re.compile(r'\["([SGB].*?)","<a.*?>(.*?)</a>","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)",', re.S)
		choosedCourseInfo = choosedCoursePattern.findall(stuChoosedHtml)
		# print choosedCourseInfo
		# 开始打印已选课程 
		# 构造表格
		del tablebHead[6] # 删除上课时间和地点，信息太长，打印不方便
		prettyTableHead = tablebHead
		choosedCourseTable = PrettyTable(prettyTableHead)
		for i in range(len(choosedCourseInfo)): # 几门课
			oneChoosedCourse = list(choosedCourseInfo[i])
			del oneChoosedCourse[5] # 删除上课时间和地点，信息太长，打印不方便
			prettyTableRow = [i]+oneChoosedCourse # 加上序号
			choosedCourseTable.add_row(prettyTableRow)
		self.writeLogs(str(choosedCourseTable), info=False)

	def getCourseStatusHtml(self, courseName):
		'''
			作用：获取【选课列表】某门课的状态的网页源码，从而获取已选课人数和课程容量
			返回：【选课列表】某门课的状态的网页源码
		'''
		# 用已有登录状态的Cookie发送请求，获取目标页面源码
		stuChooseListUrl = 'http://mis.sse.ustc.edu.cn/Teaching/CourseChooseInfo/ListStudentToChoose.aspx'
		
		data = {
			'__EVENTTARGET' : 'global$QueryForm$ctl00$TriggerSearch',
			'__EVENTARGUMENT' : 'Trigger$2',
			'__VIEWSTATE' : '/wEPDwUKMTg4OTI4NDIxOA8WAh4JbWFqb3JUeXBlBRjlpKfmlbDmja7kuI7kurrlt6Xmmbrog71kGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYNBQZnbG9iYWwFEGdsb2JhbCRRdWVyeUZvcm0FJGdsb2JhbCRRdWVyeUZvcm0kY3RsMDAkVHJpZ2dlclNlYXJjaAUhZ2xvYmFsJFF1ZXJ5Rm9ybSRjdGwwMCRkZGxBZGRyZXNzBSNnbG9iYWwkUXVlcnlGb3JtJGN0bDAwJGRkbFN0dWR5WWVhcgUeZ2xvYmFsJFF1ZXJ5Rm9ybSRjdGwwMCRkZGxUZXJtBSdnbG9iYWwkUXVlcnlGb3JtJGN0bDAxJHR4dENob29zZWRDcmVkaXQFI2dsb2JhbCRRdWVyeUZvcm0kY3RsMDEkdHh0TWF4Q3JlZGl0BRBnbG9iYWwkTWFpblBhbmVsBTVnbG9iYWwkTWFpblBhbmVsJGdyaWRBY3RUQmFyJGJ0blZpZXdNdWx0aXBsZUNob2ljZU9uZQUZZ2xvYmFsJE1haW5QYW5lbCRHcmlkTGlzdAUIV25kTW9kYWwFDFduZE1vZGFsX01DT5z07eospMaEA3q5abbcC1AtMyFQ1txhYgDjzNrw/fHC',
			'global$QueryForm$ctl00$TriggerSearch' : courseName,
			'global$QueryForm$ctl00$ddlAddress' : self.userLocation,
			'global$QueryForm$ctl00$ddlStudyYear' : self.userYear,
			'global$QueryForm$ctl00$ddlTerm' : self.userTerm,
			'X_CHANGED' : 'true',
			'WndModal_Hidden' : 'true',
			'WndModal_MCO_Hidden' : 'true',
			'global_QueryForm_Collapsed' : 'false',
			'global_MainPanel_GridList_Collapsed' : 'false',
			'global_MainPanel_GridList_SelectedRowIndexArray' : '',
			'global_MainPanel_GridList_HiddenColumnIndexArray' : '',
			'global_MainPanel_GridList_RowStates' : '[]',
			'global_MainPanel_Collapsed' : 'false',
			'global_Collapsed' : 'false',
			'WndModal_Collapsed' : 'false',
			'WndModal_MCO_Collapsed' : 'false',
			'X_STATE' : 'eyJnbG9iYWxfUXVlcnlGb3JtX2N0bDAwX1RyaWdnZXJTZWFyY2giOnsiVGV4dCI6IuamgueOh+iuuiJ9LCJnbG9iYWxfUXVlcnlGb3JtX2N0bDAwX2RkbEFkZHJlc3MiOnsiWF9JdGVtcyI6W1si6IuP5beeIiwi6IuP5beeIiwxXSxbIuWQiOiCpSIsIuWQiOiCpSIsMV1dLCJTZWxlY3RlZFZhbHVlIjoi6IuP5beeIn0sImdsb2JhbF9RdWVyeUZvcm1fY3RsMDBfZGRsU3R1ZHlZZWFyIjp7IlhfSXRlbXMiOltbIjIwMTgiLCIyMDE4IiwxXSxbIjIwMTkiLCIyMDE5IiwxXV0sIlNlbGVjdGVkVmFsdWUiOiIyMDE4In0sImdsb2JhbF9RdWVyeUZvcm1fY3RsMDBfZGRsVGVybSI6eyJTZWxlY3RlZFZhbHVlIjoiMiIsIlhfSXRlbXMiOltbIjAiLCIwIiwxXSxbIjEiLCIxIiwxXSxbIjIiLCIyIiwxXV19LCJnbG9iYWxfUXVlcnlGb3JtX2N0bDAxX3R4dENob29zZWRDcmVkaXQiOnsiVGV4dCI6IjAifSwiZ2xvYmFsX1F1ZXJ5Rm9ybV9jdGwwMV90eHRNYXhDcmVkaXQiOnsiVGV4dCI6IjIzIn0sImdsb2JhbF9NYWluUGFuZWxfZ3JpZEFjdFRCYXJfYnRuVmlld011bHRpcGxlQ2hvaWNlT25lIjp7Ik9uQ2xpZW50Q2xpY2siOiJYKCdXbmRNb2RhbF9NQ08nKS5ib3hfc2hvdygnL1RlYWNoaW5nL0NvdXJzZUNob29zZUluZm8vQ29tbWVuY2VkTXVsdGlwbGVDaG9pY2VPbmVDb3Vyc2VMaXN0LmFzcHg/SW5wdXRlZEtleT0lZTYlYTYlODIlZTclOGUlODclZTglYWUlYmEmQWRkcmVzcz0lZTglOGIlOGYlZTUlYjclOWUmTWFqb3JUeXBlPSVlNSVhNCVhNyVlNiU5NSViMCVlNiU4ZCVhZSVlNCViOCU4ZSVlNCViYSViYSVlNSViNyVhNSVlNiU5OSViYSVlOCU4MyViZCZZZWFyVGVhbT0yMDE4LTImQ3VycmVudFVzZXJHdWlkPTExNTk5ZWNkLTc4MmEtNDY5NS1hYjlmLTFiYTlkYWYxMzAwYycsJ+afpeeci+WkmumAieS4gOivvueoiycpO3JldHVybiBmYWxzZTsifSwiZ2xvYmFsX01haW5QYW5lbF9HcmlkTGlzdCI6eyJYX1Jvd3MiOnsiVmFsdWVzIjpbXSwiRGF0YUtleXMiOltdfX19',
			'X_AJAX' : 'true',
		}
		response = self.sess.post(stuChooseListUrl, data=data, headers=self.headers)
		stuChooseListHtml = response.text.encode('utf-8')
		with open('a.html', 'w') as f:
			f.write(stuChooseListHtml)
		return stuChooseListHtml
	
	def printCourseStatus(self, courseName):
		'''
			作用：打印某门课的状态
			courseName ：课程名称
			返回：(已选人数，最大人数)
		'''
		self.writeLogs('正在查询课程【{}】状态...'.format(courseName))
		courseStatusHtml = self.getCourseStatusHtml(courseName)
		tablebHead = ['课程编号', '课程名称', '学分', '班号', '授课老师', '授课时间地点', \
						'选课开始时间', '选课结束时间', '已选人数', '最大人数']
		ChooseListPattern = re.compile(r'\["([SGB].*?)","<a.*?>(.*?)</a>","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)","(.*?)",', re.S)
		courseStatus = ChooseListPattern.findall(courseStatusHtml)
		# 开始打印选课列表 
		# 构造表格
		del tablebHead[5] # 删除上课时间和地点，信息太长，打印不方便
		prettyTableHead = tablebHead
		ChooseListTable = PrettyTable(prettyTableHead)
		try:
			courseStatus = list(courseStatus[0])
		except:
			self.writeLogs('查询课程【{}】状态失败，请检查课程名字是否正确！'.format(courseName), error=True)
			return (0, 0)
		del courseStatus[5] # 删除上课时间和地点，信息太长，打印不方便
		prettyTableRow = courseStatus
		ChooseListTable.add_row(prettyTableRow)
		self.writeLogs(str(ChooseListTable), info=False)
		return (courseStatus[-2], courseStatus[-1])

	def chooseCourse(self, index, courseName):
		'''
			作用：抢课
		'''
		chooseCouserUrl = 'http://mis.sse.ustc.edu.cn/Teaching/CourseChooseInfo/ListStudentToChoose.aspx'
		# 构造表单
		data = {
			'__EVENTTARGET' : 'global$MainPanel$GridList',
			'__EVENTARGUMENT' : 'Command$0$10$Choose$',
			'__VIEWSTATE' : '/wEPDwUKMTY1MDg5NDA0NWQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgoFBmdsb2JhbAUQZ2xvYmFsJFF1ZXJ5Rm9ybQUkZ2xvYmFsJFF1ZXJ5Rm9ybSRjdGwwMCRUcmlnZ2VyU2VhcmNoBSJnbG9iYWwkUXVlcnlGb3JtJGN0bDAwJGRkbFllYXJUZXJtBSdnbG9iYWwkUXVlcnlGb3JtJGN0bDAwJHR4dENob29zZWRDcmVkaXQFI2dsb2JhbCRRdWVyeUZvcm0kY3RsMDAkdHh0TWF4Q3JlZGl0BRBnbG9iYWwkTWFpblBhbmVsBRlnbG9iYWwkTWFpblBhbmVsJEdyaWRMaXN0BQhXbmRNb2RhbAUNV25kTW9kYWxTbWFsbFpa0iUSyEAielWliBEkTe5bNJ4XM7afcwd3z9sFCGAp',
			'global$QueryForm$ctl00$TriggerSearch' : courseName,
			'global$QueryForm$ctl00$ddlAddress' : self.userLocation,
			'global$QueryForm$ctl00$ddlStudyYear' : self.userYear,
			'global$QueryForm$ctl00$ddlTerm' : self.userTerm,
			'X_CHANGED' : 'false',
			'WndModal_Hidden' : 'true',
			'WndModalSmall_Hidden' : 'true',
			'global_QueryForm_Collapsed' : 'false',
			'global_MainPanel_GridList_Collapsed' : 'false',
			'global_MainPanel_GridList_SelectedRowIndexArray' : 0,
			'global_MainPanel_GridList_HiddenColumnIndexArray' : '',
			'global_MainPanel_GridList_RowStates' : '[]',
			'global_MainPanel_Collapsed' : 'false',
			'global_Collapsed' : 'false',
			'WndModal_Collapsed' : 'false',
			'WndModalSmall_Collapsed' : 'false',
			'X_STATE' : 'eyJnbG9iYWxfUXVlcnlGb3JtX2N0bDAwX2RkbFllYXJUZXJtIjp7IlhfSXRlbXMiOltbIjIwMTgtMSIsIjIwMTgtMSIsMV0sWyIyMDE4LTAiLCIyMDE4LTAiLDFdLFsiMjAxNy0yIiwiMjAxNy0yIiwxXSxbIjIwMTctMSIsIjIwMTctMSIsMV0sWyIyMDE3LTAiLCIyMDE3LTAiLDFdLFsiMjAxNi0yIiwiMjAxNi0yIiwxXSxbIjIwMTYtMSIsIjIwMTYtMSIsMV0sWyIyMDE2LTAiLCIyMDE2LTAiLDFdLFsiMjAxNS0yIiwiMjAxNS0yIiwxXSxbIjIwMTUtMSIsIjIwMTUtMSIsMV0sWyIyMDE1LTAiLCIyMDE1LTAiLDFdLFsiMjAxNC0yIiwiMjAxNC0yIiwxXSxbIjIwMTQtMSIsIjIwMTQtMSIsMV0sWyIyMDE0LTAiLCIyMDE0LTAiLDFdLFsiMjAxMy0yIiwiMjAxMy0yIiwxXSxbIjIwMTMtMSIsIjIwMTMtMSIsMV0sWyIyMDEzLTAiLCIyMDEzLTAiLDFdLFsiMjAxMi0yIiwiMjAxMi0yIiwxXSxbIjIwMTItMSIsIjIwMTItMSIsMV0sWyIyMDExLTIiLCIyMDExLTIiLDFdLFsiMjAxMS0xIiwiMjAxMS0xIiwxXSxbIjIwMTAtMiIsIjIwMTAtMiIsMV0sWyIyMDEwLTEiLCIyMDEwLTEiLDFdLFsiMjAwOS0yIiwiMjAwOS0yIiwxXV0sIlNlbGVjdGVkVmFsdWUiOiIyMDE4LTEifSwiZ2xvYmFsX1F1ZXJ5Rm9ybV9jdGwwMF90eHRDaG9vc2VkQ3JlZGl0Ijp7IlRleHQiOiIxNiJ9LCJnbG9iYWxfUXVlcnlGb3JtX2N0bDAwX3R4dE1heENyZWRpdCI6eyJUZXh0IjoiMTgifSwiZ2xvYmFsX01haW5QYW5lbF9HcmlkTGlzdCI6eyJYX1Jvd3MiOnsiVmFsdWVzIjpbWyJTRTA1MTAyYiIsIjxhIGhyZWY9XCJqYXZhc2NyaXB0OjtcIiBvbmNsaWNrPVwiamF2YXNjcmlwdDpYKCYjMzk7V25kTW9kYWwmIzM5OykuYm94X3Nob3coJiMzOTsvVGVhY2hpbmcvQ291cnNlSW5mby9WaWV3QnlDb3Vyc2VJRC5hc3B4P0NvdXJzZUlEPVNFMDUxMDJiJiMzOTssJiMzOTvlt6XnqIvnoZXlo6vln7rnoYDoi7Hor60t6K+m57uGJiMzOTspO1wiPuW3peeoi+ehleWjq+WfuuehgOiLseivrTwvYT4iLCIyIiwi6IuP5beeNOePrSIsIuWImOWzsDIyNSgt5pqC5peg5bel5Y+3LSkiLCIyLTQg5ZGoL+WRqOS4gC/kuIrljYgoNO+8jDUpL+aAnei0pOalvDIwMl82LTExIOWRqC/lkajkuIAv5LiK5Y2IKDTvvIw1KS/mgJ3otKTmpbwyMDJfMTItMTMg5ZGoL+WRqOS4gC/mmZrkuIooMTHvvIwxMu+8jDEzKS/mgJ3otKTmpbwyMDJfMi00IOWRqC/lkajkuIkv5LiK5Y2IKDHvvIwy77yMMykv5oCd6LSk5qW8MjAyXzYtMTEg5ZGoL+WRqOS4iS/kuIrljYgoMe+8jDLvvIwzKS/mgJ3otKTmpbwyMDJfMTItMTMg5ZGoL+WRqOS6jC/kuIvljYgoOe+8jDEwKS/mgJ3otKTmpbwyMDIiLCIyMDE4LTktOSIsIjIwMTgtOS0xNyIsIjIwMTgtOS0xNyIsIjM3IiwiNDAiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cIkV4dC5kZWZlcihmdW5jdGlvbigpe3dpbmRvdy5FeHQuTWVzc2FnZUJveC5zaG93KHt0aXRsZTomIzM5O+aPkOekuiYjMzk7LG1zZzomIzM5O+ehruWumuWPlua2iCYjMzk7LGJ1dHRvbnM6RXh0Lk1lc3NhZ2VCb3guT0tDQU5DRUwsaWNvbjpFeHQuTWVzc2FnZUJveC5JTkZPLGZuOmZ1bmN0aW9uKGJ0bil7aWYoYnRuPT0mIzM5O2NhbmNlbCYjMzk7KXtyZXR1cm4gZmFsc2U7fWVsc2V7X19kb1Bvc3RCYWNrKCYjMzk7Z2xvYmFsJE1haW5QYW5lbCRHcmlkTGlzdCYjMzk7LCYjMzk7Q29tbWFuZCQwJDExJENhbmNlbENob29zZSQmIzM5Oyk7fX19KTt9LDApO1gudXRpbC5zdG9wRXZlbnRQcm9wYWdhdGlvbi5hcHBseShudWxsLCBhcmd1bWVudHMpO1wiPuWPlua2iOmAieivvjwvYT4iXSxbIlNFMDUxMTEiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cImphdmFzY3JpcHQ6WCgmIzM5O1duZE1vZGFsJiMzOTspLmJveF9zaG93KCYjMzk7L1RlYWNoaW5nL0NvdXJzZUluZm8vVmlld0J5Q291cnNlSUQuYXNweD9Db3Vyc2VJRD1TRTA1MTExJiMzOTssJiMzOTvnrpfms5Xorr7orqHkuI7liIbmnpAt6K+m57uGJiMzOTspO1wiPueul+azleiuvuiuoeS4juWIhuaekDwvYT4iLCIzIiwi6IuP5bee54+tIiwi5byg5puZKOaaguaXoOW3peWPtykiLCI2LTE3IOWRqC/lkajkupQv5LiL5Y2IKDbvvIw377yMOO+8jDkpL+aYjuW+t+alvEMyMzlfMi00IOWRqC/lkajkupQv5LiL5Y2IKDbvvIw377yMOO+8jDkpL+aYjuW+t+alvEMyMzkiLCIyMDE4LTktOCIsIjIwMTgtOS0yNCIsIjIwMTgtOS0yNCIsIjEzNCIsIjEyMCIsIjxhIGhyZWY9XCJqYXZhc2NyaXB0OjtcIiBvbmNsaWNrPVwiRXh0LmRlZmVyKGZ1bmN0aW9uKCl7d2luZG93LkV4dC5NZXNzYWdlQm94LnNob3coe3RpdGxlOiYjMzk75o+Q56S6JiMzOTssbXNnOiYjMzk756Gu5a6a5Y+W5raIJiMzOTssYnV0dG9uczpFeHQuTWVzc2FnZUJveC5PS0NBTkNFTCxpY29uOkV4dC5NZXNzYWdlQm94LklORk8sZm46ZnVuY3Rpb24oYnRuKXtpZihidG49PSYjMzk7Y2FuY2VsJiMzOTspe3JldHVybiBmYWxzZTt9ZWxzZXtfX2RvUG9zdEJhY2soJiMzOTtnbG9iYWwkTWFpblBhbmVsJEdyaWRMaXN0JiMzOTssJiMzOTtDb21tYW5kJDEkMTEkQ2FuY2VsQ2hvb3NlJCYjMzk7KTt9fX0pO30sMCk7WC51dGlsLnN0b3BFdmVudFByb3BhZ2F0aW9uLmFwcGx5KG51bGwsIGFyZ3VtZW50cyk7XCI+5Y+W5raI6YCJ6K++PC9hPiJdLFsiU0UwNTIzN2EiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cImphdmFzY3JpcHQ6WCgmIzM5O1duZE1vZGFsJiMzOTspLmJveF9zaG93KCYjMzk7L1RlYWNoaW5nL0NvdXJzZUluZm8vVmlld0J5Q291cnNlSUQuYXNweD9Db3Vyc2VJRD1TRTA1MjM3YSYjMzk7LCYjMzk757O757uf5bu65qih5LiO5YiG5p6QLeivpue7hiYjMzk7KTtcIj7ns7vnu5/lu7rmqKHkuI7liIbmnpA8L2E+IiwiMyIsIuiLj+W3nuePrSIsIumZiOWNmigt5pqC5peg5bel5Y+3LSkiLCIxMi0xOSDlkagv5ZGo5LiJL+S4iuWNiCgx77yMMu+8jDPvvIw0KS/mmI7lvrfmpbxDMjM5XzEyLTE5IOWRqC/lkajkuIAv5LiK5Y2IKDTvvIw1KS/mmI7lvrfmpbxDMjM5IiwiMjAxOC05LTgiLCIyMDE4LTExLTI2IiwiMjAxOC0xMS0yNiIsIjEyNSIsIjEyMCIsIjxhIGhyZWY9XCJqYXZhc2NyaXB0OjtcIiBvbmNsaWNrPVwiRXh0LmRlZmVyKGZ1bmN0aW9uKCl7d2luZG93LkV4dC5NZXNzYWdlQm94LnNob3coe3RpdGxlOiYjMzk75o+Q56S6JiMzOTssbXNnOiYjMzk756Gu5a6a5Y+W5raIJiMzOTssYnV0dG9uczpFeHQuTWVzc2FnZUJveC5PS0NBTkNFTCxpY29uOkV4dC5NZXNzYWdlQm94LklORk8sZm46ZnVuY3Rpb24oYnRuKXtpZihidG49PSYjMzk7Y2FuY2VsJiMzOTspe3JldHVybiBmYWxzZTt9ZWxzZXtfX2RvUG9zdEJhY2soJiMzOTtnbG9iYWwkTWFpblBhbmVsJEdyaWRMaXN0JiMzOTssJiMzOTtDb21tYW5kJDIkMTEkQ2FuY2VsQ2hvb3NlJCYjMzk7KTt9fX0pO30sMCk7WC51dGlsLnN0b3BFdmVudFByb3BhZ2F0aW9uLmFwcGx5KG51bGwsIGFyZ3VtZW50cyk7XCI+5Y+W5raI6YCJ6K++PC9hPiJdLFsiU0UwNTQyM2EiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cImphdmFzY3JpcHQ6WCgmIzM5O1duZE1vZGFsJiMzOTspLmJveF9zaG93KCYjMzk7L1RlYWNoaW5nL0NvdXJzZUluZm8vVmlld0J5Q291cnNlSUQuYXNweD9Db3Vyc2VJRD1TRTA1NDIzYSYjMzk7LCYjMzk75py65Zmo5a2m5LmgLeivpue7hiYjMzk7KTtcIj7mnLrlmajlrabkuaA8L2E+IiwiMyIsIuiLj+W3nuePrSIsIuW8oOabmSjmmoLml6Dlt6Xlj7cpIiwiMTItMTkg5ZGoL+WRqOS4iS/kuIvljYgoNu+8jDfvvIw4KS/mmI7lvrfmpbxDMjQwXzEzLTIwIOWRqC/lkajml6Uv5LiL5Y2IKDbvvIw377yMOCkv5piO5b635qW8QzI0MCIsIjIwMTgtOS04IiwiMjAxOC0xMS0yNiIsIjIwMTgtMTEtMjYiLCIxMDMiLCIxMDAiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cIkV4dC5kZWZlcihmdW5jdGlvbigpe3dpbmRvdy5FeHQuTWVzc2FnZUJveC5zaG93KHt0aXRsZTomIzM5O+aPkOekuiYjMzk7LG1zZzomIzM5O+ehruWumuWPlua2iCYjMzk7LGJ1dHRvbnM6RXh0Lk1lc3NhZ2VCb3guT0tDQU5DRUwsaWNvbjpFeHQuTWVzc2FnZUJveC5JTkZPLGZuOmZ1bmN0aW9uKGJ0bil7aWYoYnRuPT0mIzM5O2NhbmNlbCYjMzk7KXtyZXR1cm4gZmFsc2U7fWVsc2V7X19kb1Bvc3RCYWNrKCYjMzk7Z2xvYmFsJE1haW5QYW5lbCRHcmlkTGlzdCYjMzk7LCYjMzk7Q29tbWFuZCQzJDExJENhbmNlbENob29zZSQmIzM5Oyk7fX19KTt9LDApO1gudXRpbC5zdG9wRXZlbnRQcm9wYWdhdGlvbi5hcHBseShudWxsLCBhcmd1bWVudHMpO1wiPuWPlua2iOmAieivvjwvYT4iXSxbIlNFMDU0MjQiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cImphdmFzY3JpcHQ6WCgmIzM5O1duZE1vZGFsJiMzOTspLmJveF9zaG93KCYjMzk7L1RlYWNoaW5nL0NvdXJzZUluZm8vVmlld0J5Q291cnNlSUQuYXNweD9Db3Vyc2VJRD1TRTA1NDI0JiMzOTssJiMzOTvkurrlt6Xmmbrog70t6K+m57uGJiMzOTspO1wiPuS6uuW3peaZuuiDvTwvYT4iLCIzIiwi6IuP5bee54+tIiwi5L2Z6Imz546uKOaaguaXoOW3peWPtykiLCI2LTEwIOWRqC/lkajkuowv5LiK5Y2IKDHvvIwy77yMMykv5piO5b635qW8QzI0MF82LTkg5ZGoL+WRqOWFrS/kuIrljYgoM++8jDTvvIw1KS/mmI7lvrfmpbxDMjQwXzItNCDlkagv5ZGo5LqML+S4iuWNiCgx77yMMu+8jDMpL+aYjuW+t+alvEMyNDBfMTEtMTQg5ZGoL+WRqOWFrS/kuIrljYgoM++8jDTvvIw1KS/mmI7lvrfmpbxDMjQwIiwiMjAxOC05LTgiLCIyMDE4LTktMjQiLCIyMDE4LTktMjQiLCIxMDgiLCIxMDAiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cIkV4dC5kZWZlcihmdW5jdGlvbigpe3dpbmRvdy5FeHQuTWVzc2FnZUJveC5zaG93KHt0aXRsZTomIzM5O+aPkOekuiYjMzk7LG1zZzomIzM5O+ehruWumuWPlua2iCYjMzk7LGJ1dHRvbnM6RXh0Lk1lc3NhZ2VCb3guT0tDQU5DRUwsaWNvbjpFeHQuTWVzc2FnZUJveC5JTkZPLGZuOmZ1bmN0aW9uKGJ0bil7aWYoYnRuPT0mIzM5O2NhbmNlbCYjMzk7KXtyZXR1cm4gZmFsc2U7fWVsc2V7X19kb1Bvc3RCYWNrKCYjMzk7Z2xvYmFsJE1haW5QYW5lbCRHcmlkTGlzdCYjMzk7LCYjMzk7Q29tbWFuZCQ0JDExJENhbmNlbENob29zZSQmIzM5Oyk7fX19KTt9LDApO1gudXRpbC5zdG9wRXZlbnRQcm9wYWdhdGlvbi5hcHBseShudWxsLCBhcmd1bWVudHMpO1wiPuWPlua2iOmAieivvjwvYT4iXSxbIlNFMDU3MTRhIiwiPGEgaHJlZj1cImphdmFzY3JpcHQ6O1wiIG9uY2xpY2s9XCJqYXZhc2NyaXB0OlgoJiMzOTtXbmRNb2RhbCYjMzk7KS5ib3hfc2hvdygmIzM5Oy9UZWFjaGluZy9Db3Vyc2VJbmZvL1ZpZXdCeUNvdXJzZUlELmFzcHg/Q291cnNlSUQ9U0UwNTcxNGEmIzM5OywmIzM5O+W3peeoi+WunumqjOe7vOWQiC3or6bnu4YmIzM5Oyk7XCI+5bel56iL5a6e6aqM57u85ZCIPC9hPiIsIjAuNSIsIuiLj+W3nuePrSIsIuS4geeukCgwNjUwNSkiLCIxLTEg5ZGoL+WRqOS4gC/kuIrljYgoMe+8jDIpL+aYjuW+t+alvEMyMzkiLCIyMDE4LTktOCIsIjIwMTgtMTEtMjYiLCIyMDE4LTExLTI2IiwiNDQyIiwiNDQ1IiwiPGEgaHJlZj1cImphdmFzY3JpcHQ6O1wiIG9uY2xpY2s9XCJFeHQuZGVmZXIoZnVuY3Rpb24oKXt3aW5kb3cuRXh0Lk1lc3NhZ2VCb3guc2hvdyh7dGl0bGU6JiMzOTvmj5DnpLomIzM5Oyxtc2c6JiMzOTvnoa7lrprlj5bmtogmIzM5OyxidXR0b25zOkV4dC5NZXNzYWdlQm94Lk9LQ0FOQ0VMLGljb246RXh0Lk1lc3NhZ2VCb3guSU5GTyxmbjpmdW5jdGlvbihidG4pe2lmKGJ0bj09JiMzOTtjYW5jZWwmIzM5Oyl7cmV0dXJuIGZhbHNlO31lbHNle19fZG9Qb3N0QmFjaygmIzM5O2dsb2JhbCRNYWluUGFuZWwkR3JpZExpc3QmIzM5OywmIzM5O0NvbW1hbmQkNSQxMSRDYW5jZWxDaG9vc2UkJiMzOTspO319fSk7fSwwKTtYLnV0aWwuc3RvcEV2ZW50UHJvcGFnYXRpb24uYXBwbHkobnVsbCwgYXJndW1lbnRzKTtcIj7lj5bmtojpgInor748L2E+Il0sWyJTRTA1NzIwIiwiPGEgaHJlZj1cImphdmFzY3JpcHQ6O1wiIG9uY2xpY2s9XCJqYXZhc2NyaXB0OlgoJiMzOTtXbmRNb2RhbCYjMzk7KS5ib3hfc2hvdygmIzM5Oy9UZWFjaGluZy9Db3Vyc2VJbmZvL1ZpZXdCeUNvdXJzZUlELmFzcHg/Q291cnNlSUQ9U0UwNTcyMCYjMzk7LCYjMzk7UHl0aG9u56iL5bqP6K6+6K6hLeivpue7hiYjMzk7KTtcIj5QeXRob27nqIvluo/orr7orqE8L2E+IiwiMC41Iiwi6IuP5bee54+tIiwi57+f5bu66IqzKOaaguaXoOW3peWPtykiLCI2LTEwIOWRqC/lkajkupQv5LiK5Y2IKDTvvIw1KS/mmI7lvrfmpbxDMTEyXzItNCDlkagv5ZGo5LqUL+S4iuWNiCg077yMNSkv5piO5b635qW8QzExMl8yLTQg5ZGoL+WRqOWbmy/kuIvljYgoNu+8jDfvvIw4KS/mmI7lvrfmpbxDMTEyXzYtMTAg5ZGoL+WRqOWbmy/kuIvljYgoNu+8jDfvvIw4KS/mmI7lvrfmpbxDMTEyIiwiMjAxOC05LTgiLCIyMDE4LTktMTciLCIyMDE4LTktMTciLCIxMjAiLCIxMjAiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cIkV4dC5kZWZlcihmdW5jdGlvbigpe3dpbmRvdy5FeHQuTWVzc2FnZUJveC5zaG93KHt0aXRsZTomIzM5O+aPkOekuiYjMzk7LG1zZzomIzM5O+ehruWumuWPlua2iCYjMzk7LGJ1dHRvbnM6RXh0Lk1lc3NhZ2VCb3guT0tDQU5DRUwsaWNvbjpFeHQuTWVzc2FnZUJveC5JTkZPLGZuOmZ1bmN0aW9uKGJ0bil7aWYoYnRuPT0mIzM5O2NhbmNlbCYjMzk7KXtyZXR1cm4gZmFsc2U7fWVsc2V7X19kb1Bvc3RCYWNrKCYjMzk7Z2xvYmFsJE1haW5QYW5lbCRHcmlkTGlzdCYjMzk7LCYjMzk7Q29tbWFuZCQ2JDExJENhbmNlbENob29zZSQmIzM5Oyk7fX19KTt9LDApO1gudXRpbC5zdG9wRXZlbnRQcm9wYWdhdGlvbi5hcHBseShudWxsLCBhcmd1bWVudHMpO1wiPuWPlua2iOmAieivvjwvYT4iXSxbIlNFMDU3MjEiLCI8YSBocmVmPVwiamF2YXNjcmlwdDo7XCIgb25jbGljaz1cImphdmFzY3JpcHQ6WCgmIzM5O1duZE1vZGFsJiMzOTspLmJveF9zaG93KCYjMzk7L1RlYWNoaW5nL0NvdXJzZUluZm8vVmlld0J5Q291cnNlSUQuYXNweD9Db3Vyc2VJRD1TRTA1NzIxJiMzOTssJiMzOTvmt7HluqblrabkuaDlrp7ot7Ut6K+m57uGJiMzOTspO1wiPua3seW6puWtpuS5oOWunui3tTwvYT4iLCIxIiwi6IuP5bee54+tIiwi5p2o5bOwKDA5NzU5KSIsIjEyLTE5IOWRqC/lkajkupQv5LiK5Y2IKDTvvIw1KS/mlY/lrabmpbwxMDJfMTItMTkg5ZGoL+WRqOWbmy/kuIvljYgoNu+8jDfvvIw4KS/mlY/lrabmpbwxMDIiLCIyMDE4LTktOCIsIjIwMTgtMTEtMjYiLCIyMDE4LTExLTI2IiwiMTc4IiwiMTcwIiwiPGEgaHJlZj1cImphdmFzY3JpcHQ6O1wiIG9uY2xpY2s9XCJFeHQuZGVmZXIoZnVuY3Rpb24oKXt3aW5kb3cuRXh0Lk1lc3NhZ2VCb3guc2hvdyh7dGl0bGU6JiMzOTvmj5DnpLomIzM5Oyxtc2c6JiMzOTvnoa7lrprlj5bmtogmIzM5OyxidXR0b25zOkV4dC5NZXNzYWdlQm94Lk9LQ0FOQ0VMLGljb246RXh0Lk1lc3NhZ2VCb3guSU5GTyxmbjpmdW5jdGlvbihidG4pe2lmKGJ0bj09JiMzOTtjYW5jZWwmIzM5Oyl7cmV0dXJuIGZhbHNlO31lbHNle19fZG9Qb3N0QmFjaygmIzM5O2dsb2JhbCRNYWluUGFuZWwkR3JpZExpc3QmIzM5OywmIzM5O0NvbW1hbmQkNyQxMSRDYW5jZWxDaG9vc2UkJiMzOTspO319fSk7fSwwKTtYLnV0aWwuc3RvcEV2ZW50UHJvcGFnYXRpb24uYXBwbHkobnVsbCwgYXJndW1lbnRzKTtcIj7lj5bmtojpgInor748L2E+Il1dLCJEYXRhS2V5cyI6W1siYTlhZTFiYjAtZmRmMy00ZTVlLWE1M2ItODdhYzZlMDAyOTc1Il0sWyI0MzVjZDBiYy1jMWFhLTQ4ZWUtODc4MS0xOWE5ZWZkNzJkZmUiXSxbIjg5OWZlNzczLWUwNzktNDdiZS04MWU1LWI5OWQ3M2UyMTk3OCJdLFsiYjFiNzJhYzMtZjMxNS00MzU4LWFlNGYtODRkNmEzN2Q4Zjk3Il0sWyJhYjdkMTNlOC02NDRmLTRiNDAtODMzMi01MTUzMjdkMzM1ZjEiXSxbIjkwY2FmMDI2LTI4NzItNGQ3ZC04ZjQ3LTY5ZWU0ZGE2ZjhlNiJdLFsiYjhlMDljMmMtNWZmMy00ZjkxLWJhYTYtNjljN2FhYzk1YWJjIl0sWyJkODNjZGNlMy1hMTIxLTRmMDItYjA0ZC00ZjRkNDgxZmQ1YWMiXV19LCJSZWNvcmRDb3VudCI6OCwiWF9TdGF0ZXMiOltbXSxbXSxbXSxbXSxbXSxbXSxbXSxbXV19fQ==',
			'X_AJAX' : 'true',
		}
		
		# 线程抢课
		while True:
			# 发送抢课需要的POST数据，获取登录后的Cookie(保存在sess里)
			response = self.sess.post(chooseCouserUrl, data=data, headers=self.headers)
			result = response.text.encode('utf-8')
			self.writeLogs('线程{}：正在抢课【{}】\t结果：{}'.format(index, courseName, result))
			sleepTime = random.gauss(2, 1)
			self.writeLogs('线程{}：防止被发现，休息{:.2f}秒...'.format(index, sleepTime))
			time.sleep(sleepTime) # 休息一会儿

	def chooseCourseMultiThread(self, wantedCourseList):
		'''多线程抢课'''
		if self.login():
			courseNum = len(wantedCourseList)
			self.printStuChoosed() # 打印已选课程信息
			self.writeLogs('共检测到{}个任务，正在分配线程处理...'.format(courseNum))
			for i, courseName in enumerate(wantedCourseList):
				thread = threading.Thread(target=self.chooseCourse, args=(i, courseName))
				thread.start()

	def writeLogs(self, log, info=True, error=False):
		if error:
			log = '[ERROR] ' + log
		elif info:
			log = '[INFO] ' + log
		else: 
			pass
		print log
		with open('runtime.logs', 'a') as f:
			f.write('['+time.ctime()+']\n'+log+'\n\n')
