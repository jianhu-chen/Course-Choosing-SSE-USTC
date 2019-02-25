# -*- coding: utf-8 -*-
# @File 	: conf.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-01 13:08:45
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-25 21:57:58


# 账号
USER_ACCOUNT = {
	'userId': 'SA18225034',
	'userPwd': ''
}

# 选课学年
YEAR = '2018'

# 选课学期
TERM = '2'

# 你是苏州的学生还是合肥的？
# 苏州 | 合肥 (写其他选项默认为'苏州')
USER_LOCATION = '苏州'


# 填上你想选的课的名字
# 一个列表，可以同时抢多门课（多线程并行处理）
WANTED_COURSE_LIST = [
	'高级数据库技术',
	'自然语言处理',
]

# 线程休眠时间范围
# 如果选课人数满，每隔多长时间再提交一次选课请求
# (最短时间, 最长时间)
# 只能设置小数，设置整数会报错
SLEEP_TIME = (1.1, 3.2)

# 当选择的课程人数已满是否需要继续抢课
FULL_KEEP_CHOOSE = True

# 网络错误或是搜索不到某一课程时是否继续抢课
# 网络错误的情况：同时访问服务器的人数过多时，服务器有时会响应不过来
# 搜索不到某一门课程的情况：课程名字错误/该课程已经在你的已选课程中
# 如果你确定课程名字没错且该课程不在你的已选课程中时可以开启此选项
ERROR_KEEP_CHOOSE = False

# 是否输出日志到文件
# 日志文件路径：./runtime.logs
OUT_PUT_LOG_TO_FILE_ENABLED = True

