from requests import get
from configparser import ConfigParser
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from sys import exit
import os
def job(url,target):
    now = datetime.now()
    # 发送请求
    x = requests.get(url)
    # 返回 http 的状态码 响应状态的描述 返回编码
    print(now.strftime("%Y-%m-%d %H:%M:%S"), target, x.status_code, x.reason, x.text)
    texts = now.strftime("%Y-%m-%d  %H:%M:%S") + '\t' + x.text + '\n'
    with open('log_'+target+now.strftime("_%Y-%m-%d")+'.txt', 'a') as f: # 打开日志文档
        f.write(texts)

# 帮助
if not os.path.exists('config.ini'):
    print('''【错误】你尚未创建【config.ini】！
 
在配置文件中，使用方括号[]创建一个节
在每个节中，只有trigger和url是必填的

- 若 trigger = date ，则在给定日期时间触发一次。如果不填写run_date，则使用当前时间。

    参数：
    run_date （字符串） – 运行作业的日期/时间

    timezone （字符串） – 如果运行日期没有时区，则为其指定时区

    详情参考【https://apscheduler.readthedocs.io/en/stable/modules/triggers/date.html】

- 若 trigger = interval ，则在指定的时间间隔内触发，如果指定了 start_date ，则从 start_date 开始，否则从 datetime.now() + 间隔时间 开始。

    参数：
    weeks （整数） – 等待的周数

    days （整数） – 等待的天数

    hours （整数） – 等待的小时数

    minutes （整数） – 等待的分钟数

    seconds （整数） – 等待的秒数

    start_date （字符串） – 间隔计算的起点

    end_date （字符串） – 最晚可能触发的日期/时间

    time_zone （字符串） – 用于日期/时间计算的时区

    jitter （整数） – 最多将作业执行延迟jitter秒
    
    详情参考【https://apscheduler.readthedocs.io/en/stable/modules/triggers/interval.html】
          
- 若 trigger = cron 则在当前时间与所有指定的时间约束条件匹配时触发，类似于UNIX cron调度程序的工作方式。

    参数：
    year （整数|字符串）- 4位数年份

    month （整数|字符串）- 月份（1-12）

    day （整数|字符串）- 月份中的日期（1-31）

    week （整数|字符串）- ISO周（1-53）

    day_of_week （整数|字符串）- 星期几的数字或名称（0-6或mon,tue,wed,thu,fri,sat,sun）

    hour （整数|字符串）- 小时（0-23）

    minute （整数|字符串）- 分钟（0-59）

    second （整数|字符串）- 秒（0-59）

    start_date （datetime | str）- 触发的最早可能日期/时间（含）

    end_date （datetime | str）- 触发的最晚可能日期/时间（含）

    timezone （datetime.tzinfo | str）- 用于日期/时间计算的时区（默认为调度程序时区）

    jitter （整数）- 最多将作业执行延迟抖动秒
    
    注意：
    第一个工作日总是星期一。
    
    格式中含有字符串的字段可以用表达式表达。
    
    | 表达式 | 字段 | 描述                                               |
    | :----- | :--- | :------------------------------------------------- |
    | *      | 任何 | 每个值都触发                                       |
    | */a    | 任何 | 每隔a个值触发 actuallly be the same as the minimum |
    | a-b    | 任何 | 在a-b范围内的任何值都触发（a必须小于b）            |
    | a-b/c  | 任何 | 在a-b范围内每隔c个值触发                           |
    | xth y  | 日   | 在一个月内，第x个星期y触发                         |
    | last x | 日   | 在一个月内，最后一个星期x触发                      |
    | last   | 日   | 在一个月内，最后一天触发                           |
    | x,y,z  | 任何 | 触发任意数量的上述表达式的组合                     |

    详情参考【https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html】

下面是一个示例

[EN1]
trigger = interval
url = https://baidu.com
seconds = 10
timezone = Asia/Shanghai

''')
    os.system("pause")
    exit()


# 初始化
config = ConfigParser()
config.read('config.ini', encoding='utf-8')
scheduler = BlockingScheduler()

def toint(a):
    if a == None: return None
    return int(a)

#读取配置文件并设置任务
sections = config.sections()
for target in sections:
    items = dict(config.items(target))
    url = items.pop('url')
    if items['trigger'] == 'interval':
        for k, v in items.items():
            if k == 'weeks' or k == 'days' or k == 'hours' or k == 'minutes' or k == 'seconds':
                items[k] = int(items[k])
    print(items)
    scheduler.add_job(job, args=(url,target), **items)
print('任务开启！')
scheduler.start()
while(True):
    if input() == 'q' :
        os.system("pause")
        exit()