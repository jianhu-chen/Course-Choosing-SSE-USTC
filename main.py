# -*- coding: utf-8 -*-
# @File 	: main.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-02 11:00:01
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-26 12:20:09

# 导入配置信息
from conf import *
from Student import *

if __name__ == '__main__':
	userAccount = USER_ACCOUNT
	userLocation = USER_LOCATION
	userYear = YEAR
	userTerm = TERM
	wantedCourseList = WANTED_COURSE_LIST
	sleepTime = SLEEP_TIME
	errorKeepChoose = ERROR_KEEP_CHOOSE
	fullKeepChoose = FULL_KEEP_CHOOSE
	
	stu = Student(userAccount, userLocation, userYear, userTerm, sleepTime)
	stu.chooseCourseMultiThread(wantedCourseList)

