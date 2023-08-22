#!/usr/bin/python
# encoding: utf-8

import sys
from ualfred import Workflow, ICON_CLOCK, ICON_ERROR, ICON_GROUP, ICON_INFO
from datetime import date, datetime, time as dtime
import time

SID = 'date_utils'
fmt = '%Y-%m-%d %H:%M:%S'


def to_timestamp(ptime):
    return str(int(time.mktime(ptime.timetuple()))) + '000'


def format_time(ts, format=fmt):
    if ts > 9999999999:
        ts = ts / 1000
    return datetime.fromtimestamp(ts).strftime(format)


def event_id_parser(text):
    """EventId里的时间戳解析"""
    if '_' in text and len(text.split("_")) == 5 and text.split("_")[3].isdigit():
        return int(text.split("_")[3])


def trace_id_parser(text):
    # TraceId里的时间戳解析
    if len(text) == 30 and text[8:21].isdigit():
        return int(text[8:21])


def timestamp_parser(text):
    if text.isdigit():
        return int(text)


def str_time_parser(text):
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

            dis_text = to_timestamp(ptime)
            return int(dis_text)
        except Exception as e:
            pass


def str_time_formatter(text):
    ts = str_time_parser(text)
    if ts:
        return format_time(ts) + '对应的时间戳', str(ts)


def timestamp_formatter(text):
    ts = str_time_parser(text)
    if ts:
        ptime = datetime.strptime(format_time(ts), fmt)
        start_of_day = datetime.combine(ptime.date(), dtime.min)
        end_of_day = datetime.combine(ptime.date(), dtime.max)
        dis_text = ptime.date().strftime("%Y-%m-%d") + "的开始时间与结束时间"
        dis_sub_text = to_timestamp(start_of_day) + "," + to_timestamp(end_of_day)
        return dis_text, dis_sub_text


def current_time_formatter(text):
    # 当前时间
    dis_text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dis_value = str(int(time.mktime(datetime.now().timetuple()))) + '000'
    return "当前时间", dis_text + "," + dis_value


def today_to_current_time_formatter(text):
    # 今天到当前时间戳
    start_of_day = str(int(time.mktime(datetime.now().date().timetuple()))) + '000'
    current_time = str(int(time.mktime(datetime.now().timetuple()))) + '000'
    dis_text = start_of_day + "," + current_time
    return "今天到当前时间戳", dis_text


def main(wf):
    args = sys.argv

    text = ''
    if len(args) > 1:
        text = args[1].strip()

    # 从时间戳解析出时间
    parser_list = [event_id_parser, trace_id_parser, timestamp_parser]
    for parser in parser_list:
        ts = parser(text)
        if ts:
            dis_text = format_time(ts)
            wf.add_item(title=dis_text, subtitle=text, arg=dis_text, valid=True, icon=ICON_CLOCK)

    # 从文本时间解析出时间戳
    formatter_list = [str_time_formatter, timestamp_formatter, current_time_formatter, today_to_current_time_formatter]
    for format in formatter_list:
        item = format(text)
        if item:
            wf.add_item(title=item[0],
                        subtitle=item[1],
                        arg=item[1],
                        valid=True,
                        icon=ICON_CLOCK)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
