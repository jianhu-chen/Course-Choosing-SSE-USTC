# -*- coding: utf-8 -*-
# @File 	: main.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-02 11:00:01
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-21 18:18:37

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

	stu = Student(userAccount, userLocation, userYear, userTerm, sleepTime)
	stu.chooseCourseMultiThread(wantedCourseList)

