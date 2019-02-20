# -*- coding: utf-8 -*-
# @File 	: courseChoosingSSE.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-02 11:00:01
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-20 16:34:47

# 导入配置信息
from conf import *
from Student import *

if __name__ == '__main__':
	# 加载配置信息
	userAccount = USER_ACCOUNT
	userLocation = USER_LOCATION
	userYear = YEAR
	userTerm = TERM
	wantedCourseList = WANTED_COURSE_LIST

	# 构造对象
	stu = Student(userAccount, userLocation, userYear, userTerm)
	stu.chooseCourseMultiThread(wantedCourseList)
