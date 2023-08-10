#!/usr/bin/python
# encoding: utf-8

import sys
from ualfred import Workflow, ICON_CLOCK, ICON_ERROR, ICON_GROUP, ICON_INFO
from datetime import date, datetime, time as dtime
import time

SID = 'date_utils'

def toTimestamp(ptime):
    return str(int(time.mktime(ptime.timetuple()))) + '000'


def main(wf):
    args = sys.argv

    text = ''
    if len(args) > 1:
        text = args[1].strip()

    # EventId里的时间戳解析
    if '_' in text and len(text.split("_")) == 5 and text.split("_")[3].isdigit():
        ts = int(text.split("_")[3]) / 1000
        dis_text = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        wf.add_item(title=dis_text, subtitle=text, arg=dis_text, valid=True, icon=ICON_CLOCK)

    # TraceId里的时间戳解析
    if len(text) == 30 and text[8:21].isdigit():
        ts = int(text[8:21]) / 1000
        dis_text = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        wf.add_item(title=dis_text, subtitle=text, arg=dis_text, valid=True, icon=ICON_CLOCK)

    # 时间戳解析
    if text.isdigit():
        ts = int(text)
        if ts > 9999999999:
            dis_text = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
        else:
            dis_text = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        wf.add_item(title=dis_text, subtitle=text, arg=dis_text, valid=True, icon=ICON_CLOCK)

    # 时间转时间戳
    if '-' in text or ':' in text:
        try:
            length_of_text = len(text)
            if length_of_text == 5:
                ptime = datetime.strptime(datetime.now().strftime('%Y-%m-%d ') + text, "%Y-%m-%d %H:%M")
            elif length_of_text == 8:
                ptime = datetime.strptime(datetime.now().strftime('%Y-%m-%d ') + text, "%Y-%m-%d %H:%M:%S")
            elif length_of_text == 10:
                ptime = datetime.strptime(text, "%Y-%m-%d")
            elif length_of_text == 13:
                ptime = datetime.strptime(text, "%Y-%m-%d %H")
            elif length_of_text == 16:
                ptime = datetime.strptime(text, "%Y-%m-%d %H:%M")
            else:
                ptime = datetime.strptime(text, "%Y-%m-%d %H:%M:%S")

            dis_text = toTimestamp(ptime)
            wf.add_item(title=dis_text,
                        subtitle=text,
                        arg=dis_text,
                        valid=True,
                        icon=ICON_CLOCK)

            start_of_day = datetime.combine(ptime.date(), dtime.min)
            end_of_day = datetime.combine(ptime.date(), dtime.max)
            dis_text = ptime.date().strftime("%Y-%m-%d") + "的开始时间与结束时间"
            dis_sub_text = toTimestamp(start_of_day) + "," + toTimestamp(end_of_day)
            wf.add_item(title=dis_text,
                        subtitle=dis_sub_text,
                        arg=dis_sub_text,
                        valid=True,
                        icon=ICON_CLOCK)

        except Exception as e:

            wf.add_item(title="无法解析" + text,
                        subtitle=e.message,
                        icon=ICON_ERROR)

    # 当前时间
    dis_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dis_value = str(int(time.mktime(datetime.now().timetuple()))) + '000'

    wf.add_item(title=u"当前时间",
                subtitle=dis_text + ',' + dis_value,
                arg=dis_value,
                valid=True,
                icon=ICON_CLOCK)

    # 今天到当前时间戳
    start_of_day = str(int(time.mktime(datetime.now().date().timetuple()))) + '000'
    current_time = str(int(time.mktime(datetime.now().timetuple()))) + '000'
    dis_text = start_of_day + "," + current_time
    wf.add_item(title=u"今天到当前时间戳",
                subtitle=dis_text,
                arg=dis_text,
                valid=True,
                icon=ICON_CLOCK)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
