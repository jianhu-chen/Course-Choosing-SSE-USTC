# -*- coding: utf-8 -*-
# @File 	: conf.py
# @Author 	: jianhuChen
# @Date 	: 2019-02-01 13:08:45
# @License 	: Copyright(C), USTC
# @Last Modified by  : jianhuChen
# @Last Modified time: 2019-02-21 00:37:31

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
	'自然语言处理',
	'高级图像处理与分析',
]

# 是否输出日志到文件
# 日志文件路径：./runtime.logs
OUT_PUT_LOG_TO_FILE_ENABLED = True




# X.enable('winLogin_sfLogin_ContentPanel1_btnLogin');
# var x0=X('winLogin_sfLogin_txtUserLoginID'),
# x1=X('winLogin_sfLogin_txtPassword'),
# x2=X('winLogin_sfLogin_txtValidate');
# X.state(x0,{"Text":"SA18225034"});
# X.state(x1,{"Text":""});X.state(x2,{"Text":"25"});window.location.href='/HomePage/default.aspx';

# X.enable('winLogin_sfLogin_ContentPanel1_btnLogin');
# var x0=X('winLogin_sfLogin_ctl00_lbMsg'),
# x1=X('winLogin_sfLogin_txtUserLoginID'),
# x2=X('winLogin_sfLogin_txtPassword'),
# x3=X('winLogin_sfLogin_txtValidate');
# X.state(x0,{"Text":"密码错误,请重试或联系管理员!"});
# x0.setValue("<span>密码错误,请重试或联系管理员!</span>");
# X.state(x1,{"Text":"SA18225034"});
# X.state(x2,{"Text":""});x2.x_setValue();X.state(x3,{"Text":"17"});X('winLogin_sfLogin_txtPassword').focus();
