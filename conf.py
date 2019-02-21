# -*- coding: utf-8 -*-
# @File 	: conf.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-01 13:08:45
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-21 18:17:19

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
# 苏州 | 合肥
USER_LOCATION = '苏州'


# 填上你想选的课的名字
WANTED_COURSE_LIST = [
	'高级图像处理与分析'
]

# 线程休眠时间
# 如果选课人数满，每隔多长时间再提交一次选课请求
# (最短时间, 最长时间)
# 只能设置小数，设置整数会报错
SLEEP_TIME = (1.1, 3.2)

# 是否输出日志到文件
# 日志文件路径：./runtime.logs
OUT_PUT_LOG_TO_FILE_ENABLED = True

