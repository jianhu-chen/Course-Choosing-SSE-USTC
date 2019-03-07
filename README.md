# 中科大软件学院研究生选课辅助系统

选课已经结束...

系统采用多线程的方式（每门课一个线程）抢课，所以可以同时抢多门课～




## 环境依赖

我的环境： **python2.7**，除此之外，还需要额外安装两个库：

```bash
pip install requests
pip install prettytable # 美美地打印表格
```



## 适用人员

科大软件学院18级研究生



## 使用方法

- 将项目克隆到本地

  ```bash
  git clone https://github.com/jianhuchen/Course-Choosing-SSE-USTC.git
  ```

- 修改配置文件`conf.py`

- 在项目根目录运行：

  ```shell
  python main.py
  ```

> **退出方法**
>
> 使用`ps -aux`命令，找到此进程的PID（如：10036），再用`kill 10036`杀死进程
>
> **程序在后台跑的方法**
>
> 在命令行运行：
>
> ```shell
> ./main.sh
> ```
>
> 如果因为python版本报错的话，自己把脚本里的代码改一下就行