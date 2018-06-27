# -*- coding: UTF-8 -*-
import time
import numpy as np
import threading
import logging
from datetime import datetime
import login
import os

# from Tkinter import *

# root = Tk()
# root.withdraw()  # 隐藏窗口
# root.mainloop()  # 消息循环

log_file = os.path.join(os.getcwd(), 'daily.log')

logging.basicConfig(
    # 默认level=logging.WARNING，只输出小于等于WARNING级别的日志
    level=logging.DEBUG,
    # 日志格式 Mon, 09 Oct 2017 10:45:30 log_study.py[line:19] DEBUG debug
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    # 输出位置，默认控制台
    filename=log_file,
    # 默认值为'a' 追加
    filemode='a')

# 打卡清单
accountDict = [
    {'account': 'acc1',
     'password': 'pass1',
     'overtime': [],
     'holiday_overtime': []
     },
    {'account': 'acc2',
     'password': 'pass2',
     'overtime': [],
     'holiday_overtime': []
     },
    {'account': 'acc3',
     'password': 'pass3',
     'overtime': [1, 2, 4, 6],
     'holiday_overtime': ['2018-4-29', '2018-4-30', '2018-5-1']
     }
]

holidays = [
    # 2018年
    {
        "name": "元旦",
        "festival": "2018-1-1",
        "desc": "1月1日放假，与周末连休。",
        "rest": "拼假建议：2018年1月2日（周二）~2018年1月5日（周五）请假4天，可拼9天元旦小长假",
        "list": [{
            "date": "2017-12-30",
            "status": "1"
        }, {
            "date": "2017-12-31",
            "status": "1"
        }, {
            "date": "2018-1-1",
            "status": "1"
        }],
        "list#num#baidu": "3"
    }, {
        "name": "除夕",
        "festival": "2018-2-15",
        "desc": "除夕",
        "list": [{
            "date": "2018-2-15",
            "status": "1"
        }],
        "list#num#baidu": "1"
    }, {
        "name": "春节",
        "festival": "2018-2-16",
        "desc": "2月15日至21日放假调休，共7天。2月11日（星期日）上班，2月24日（星期六）上班",
        "rest": "拼假建议：2018年2月22日（周四）-2018年2月24日（周六）请假3天，可拼11天春节小长假。",
        "list": [{
            "date": "2018-2-15",
            "status": "1"
        }, {
            "date": "2018-2-16",
            "status": "1"
        }, {
            "date": "2018-2-17",
            "status": "1"
        }, {
            "date": "2018-2-18",
            "status": "1"
        }, {
            "date": "2018-2-19",
            "status": "1"
        }, {
            "date": "2018-2-20",
            "status": "1"
        }, {
            "date": "2018-2-21",
            "status": "1"
        }, {
            "date": "2018-2-24",
            "status": "2"
        }, {
            "date": "2018-2-11",
            "status": "2"
        }],
        "list#num#baidu": "9"
    },
    {
        "name": "清明节",
        "festival": "2018-4-5",
        "desc": "4月5日至7日放假调休，共3天。4月8日（星期日）上班。",
        "rest": "拼假建议：2018年4月2日（周一）~2018年4月4日（周三）请假3天，可拼8天清明节小长假",
        "list": [{
            "date": "2018-4-5",
            "status": "1"
        }, {
            "date": "2018-4-6",
            "status": "1"
        }, {
            "date": "2018-4-7",
            "status": "1"
        }, {
            "date": "2018-4-8",
            "status": "2"
        }],
        "list#num#baidu": "4"
    }, {
        "name": "劳动节",
        "festival": "2018-5-1",
        "desc": "4月29日至5月1日放假，4月28日（星期六）上班。",
        "rest": "拼假建议：2018年5月2日（周三）~2018年5月4日（周五）请假3天，可拼8天劳动节小长假",
        "list": [{
            "date": "2018-4-28",
            "status": "2"
        }, {
            "date": "2018-4-29",
            "status": "1"
        }, {
            "date": "2018-4-30",
            "status": "1"
        }, {
            "date": "2018-5-1",
            "status": "1"
        }],
        "list#num#baidu": "4"
    },
    {
        "name": "端午节",
        "festival": "2018-6-18",
        "desc": "6月18日放假，与周末连休。",
        "rest": "拼假建议：2018年6月19日（周二）~2018年6月22日（周五）请假4天，可拼9天端午节小长假",
        "list": [{
            "date": "2018-6-16",
            "status": "1"
        }, {
            "date": "2018-6-17",
            "status": "1"
        }, {
            "date": "2018-6-18",
            "status": "1"
        }],
        "list#num#baidu": "3"
    },
    {
        "name": "中秋节",
        "festival": "2018-9-24",
        "desc": "9月24日放假，与周末连休。",
        "rest": "拼假建议：2018年9月25日（周二）~2018年9月30日（周日）请假6天，与国庆节衔接，拼16天小长假",
        "list": [{
            "date": "2018-9-22",
            "status": "1"
        }, {
            "date": "2018-9-23",
            "status": "1"
        }, {
            "date": "2018-9-24",
            "status": "1"
        }],
        "list#num#baidu": "3"
    },
    {
        "name": "国庆节",
        "festival": "2018-10-1",
        "desc": "10月1日至7日放假调休，共7天。",
        "rest": "拼假建议：2018年9月25日（周二）~2018年9月30日（周日）请假6天，与中秋节衔接，拼16天小长假",
        "list": [{
            "date": "2018-10-1",
            "status": "1"
        }, {
            "date": "2018-10-2",
            "status": "1"
        }, {
            "date": "2018-10-3",
            "status": "1"
        }, {
            "date": "2018-10-4",
            "status": "1"
        }, {
            "date": "2018-10-5",
            "status": "1"
        }, {
            "date": "2018-10-6",
            "status": "1"
        }, {
            "date": "2018-10-7",
            "status": "1"
        }, {
            "date": "2018-9-29",
            "status": "2"
        }, {
            "date": "2018-9-30",
            "status": "2"
        }],
        "list#num#baidu": 9
    }
]


def get_holiday_generator():
    """
    获取去重后的节假日清单
    :return: 返回 generator
    :Note: generator 是 iterator，一个元素在被遍历后就没有了，
    因此在多线程访问的时候，元素1被线程1访问之后，就在 generator 中删除了，
    其他线程只能从元素2开始访问，要解决这个问题，需要将 generator 转换成 list
    """
    s = set()
    for holiday in holidays:
        for date in holiday['list']:
            if date['date'] not in s:
                yield date
                s.add(date['date'])


# 去重后的节假日信息清单
deduplicate_holiday = list(get_holiday_generator())
# 节假日集合
holiday_dates = {date['date'] for holiday in holidays for date in holiday['list']}


def loop(acc):
    try:
        while True:
            logging.info('')
            logging.info(
                '============================== ' + acc['account'] + ' begin ====================================')
            # 当前日期
            date = datetime.now()
            # 当前日期格式化后的字符串
            date_str = '%s-%s-%s' % (date.year, date.month, date.day)
            # 当前是周几
            day = date.isoweekday()
            # 当前是几点
            hour = date.hour
            # 几分
            minute = date.minute
            # 早上打卡时间
            begin = -1
            # 下午打卡时间
            end = -1
            # 是否是节假日
            if date_str in holiday_dates:
                for holiday in deduplicate_holiday:
                    if date_str == holiday['date']:
                        if holiday['status'] == "2":
                            begin = 8
                            end = 18
                            logging.info(acc['account'] + ', holiday_status = 2, begin = 8, end = 18')
                        if holiday['status'] == "1" and date_str in acc['holiday_overtime']:
                            logging.info(
                                acc['account'] + ', holiday_status = 1, holiday_overtime = True, begin = 8, end = 18')
                            begin = 8
                            end = 18
            else:
                # 如果需要加班
                if day in acc['overtime'] and day <= 5:
                    begin = 8
                    end = 21
                    logging.info(acc['account'] + ', ordinary overtime, begin = 8, end = 21')
                # 不加班的工作日 或者 加班的周末
                elif day <= 5 or day in acc['overtime']:
                    begin = 8
                    end = 18
                    logging.info(acc['account'] + ', ordinary, begin = 8, end = 18')
            # 考勤打卡
            if (hour == begin and minute >= 30) or (hour == end and minute >= 30):
                # 周一到周五晚上加班
                login.kq(acc)
                logging.info(acc['account'] + ' sign in. sleep 3600 seconds\n')
                # 保证在应打卡的时间段中只打一次卡
                time.sleep(60 * 60)
            else:
                # 每次唤醒检查的睡眠间隔 [10,28] 分钟
                sleep_time = np.random.randint(10 * 60, 30 * 60 - 2 * 60)
                logging.info(acc['account'] + ' sleep %s seconds\n' % sleep_time)
                time.sleep(sleep_time)
    except Exception as exception:
        logging.error(str(exception))


if __name__ == "__main__":
    try:
        for accountInfo in accountDict:
            t = threading.Thread(target=loop, args=(accountInfo,))
            t.start()
            # t.setDaemon(True) 主线程结束后子线程也结束
            # t.join() 主线程会在这里等待子线程执行完后在执行
    except Exception as e:
        logging.error(str(e))
