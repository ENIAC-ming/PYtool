import requests
import configparser
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

# 创建配置文件对象
# config = configparser.ConfigParser()

# # 读取文件
# config.read('config.ini', encoding='utf-8')

# # 获取所有 section
# sections = config.sections()

# # 获取特定 section 的所有键值对
# items = dict(config.items('example_section'))

# for key, value in items.items():
#     print(key, value)

# # 获取特定 section 的特定键的值
# value = config.get('example_section', 'example_key')

def Log(logg,target):
    # 在同目录下，需要提前创建一个D.txt文件

    log_value = logg
    now = datetime.now()
    D_file = open('log'+now.strftime("%Y-%m-%d")+'.txt', mode='a')  # 打开日志文档
    # 将当前时间（字符串）赋值
    now_time = now.strftime("%Y-%m-%d  %H:%M:%S")
    # 将当前时间和出入来的logg的数据合并成一条并赋值
    time_values = now_time + '\t' + log_value + '\n'
    # 将合并后的数据填写到txt
    D_file.write(time_values)


def job(url,target):
    print(url,target) # test
    now = datetime.now()
    # 发送请求
    x = requests.get(url)
    # 返回 http 的状态码 响应状态的描述 返回编码
    print(now.strftime("%Y-%m-%d %H:%M:%S"), target, x.status_code, x.reason, x.text)

    texts = now.strftime("%Y-%m-%d  %H:%M:%S") + '\t' + x.text + '\n'
    with open('log_'+target+now.strftime("_%Y-%m-%d")+'.txt', 'a') as f: # 打开日志文档
        f.write(texts)


# 初始化
config = configparser.ConfigParser()
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



    # print(url,mode) # test



    # if mode == 'corn':
    #     mode = config.get(target, 'mode')
    #     year = month = day = week = day_of_week = hour = minute = second = start_date = end_date = timezone = None
    #     if config.has_option(target, 'hour'):
    #         hour = config.get(target, 'hour')
    #     if config.has_option(target, 'mouth'):
    #         mouth = config.get(target, 'mouth')
    #     if config.has_option(target, 'day'):
    #         day = config.get(target, 'day')
    #     if config.has_option(target, 'week'):
    #         week = config.get(target, 'week')
    #     if config.has_option(target, 'day_of_week'):
    #         day_of_week = config.get(target, 'day_of_week')
    #     if config.has_option(target, 'minute'):
    #         minute = config.get(target, 'minute')
    #     if config.has_option(target, 'second'):
    #         second = config.get(target, 'second')
    #     if config.has_option(target, 'start_date'):
    #         start_date = config.get(target, 'start_date')
    #     if config.has_option(target, 'end_date'):
    #         end_date = config.get(target, 'end_date')
    #     if config.has_option(target, 'timezone'):
    #         timezone = config.get(target, 'timezone')
    #     scheduler.add_job(job, 'cron', args=(url,target), year=(year), month=(month), day=(day), week=(week), day_of_week=(day_of_week), hour=(hour), minute=(minute), second=(second), start_date=start_date, end_date=end_date, timezone=timezone)
    # elif mode == 'date':
    #     run_date = None
    #     if config.has_option(target, 'run_date'):
    #         run_date = config.get(target, 'run_date')
    #     scheduler.add_job(job, 'date', args=(url,target), run_date=run_date)
    # elif mode == 'interval':
    #     weeks = days = hours = minutes = seconds = start_date = end_date = timezone = None
    #     if config.has_option(target, 'weeks'):
    #         weeks = config.getint(target, 'weeks')
    #     if config.has_option(target, 'days'):
    #         days = config.getint(target, 'days')
    #     if config.has_option(target, 'hours'):
    #         hours = config.getint(target, 'hours')
    #     if config.has_option(target, 'minutes'):
    #         minutes = config.getint(target, 'minutes')
    #     if config.has_option(target, 'seconds'):
    #         seconds = config.getint(target, 'seconds')
    #     if config.has_option(target, 'start_date'):
    #         start_date = config.get(target, 'start_date')
    #     if config.has_option(target, 'end_date'):
    #         end_date = config.get(target, 'end_date')
    #     if config.has_option(target, 'timezone'):
    #         timezone = config.get(target, 'timezone')
    #     scheduler.add_job(job, 'interval', args=(url,target), weeks=(weeks), days=(days), hours=(hours), minutes=(minutes), seconds=(seconds), start_date=start_date, end_date=end_date, timezone=timezone)

print('任务开启！')
scheduler.start()