# encoding=UTF8
# Concat text by comma
# Written by homeway 2020.8.25

import pyperclip
import sys
import time
from ualfred import Workflow, ICON_CLOCK, ICON_ERROR, ICON_GROUP, ICON_INFO

def trim_title(title, length):
    if len(title) > length:
        return title[:length] + "..."
    else:
        return title

def proc_elem_list(elem_list, line_sep, transform_function):
    return line_sep.join(map(transform_function, elem_list))

def proc_workflow(wf):
    if len(sys.argv) > 1:
        text = sys.argv[1]
    else:
        text = ""
        for line in sys.stdin.readlines():
            text += line
    # else:
    #     # Cost 500ms
    #     start_time = time.time()
    #     text = pyperclip.paste()
    #     end_time = time.time()
    #     duration = end_time - start_time
    #     print("Time:" + str(duration * 1000.0))

    if len(text) == 0:
        wf.add_item(title="Clipboard is empty",
                    valid=False,
                    icon=ICON_INFO)
    else:
        line_separator = ','
        elem_list = text.replace("\r", "").split("\n")

        concat_by_comma = proc_elem_list(elem_list, line_separator, lambda e: e)
        concat_by_single_quote = proc_elem_list(elem_list, line_separator, lambda e: "'" + e + "'")
        concat_by_double_quote = proc_elem_list(elem_list, line_separator, lambda e: "\"" + e + "\"")

        wf.add_item(title=trim_title(concat_by_comma, 10),
                    subtitle=concat_by_comma,
                    arg=concat_by_comma,
                    valid=True,
                    icon=ICON_INFO)
        wf.add_item(title=trim_title(concat_by_single_quote, 10),
                    subtitle=concat_by_single_quote,
                    arg=concat_by_single_quote,
                    valid=True,
                    icon=ICON_INFO)
        wf.add_item(title=trim_title(concat_by_double_quote, 10),
                    subtitle=concat_by_double_quote,
                    arg=concat_by_double_quote,
                    valid=True,
                    icon=ICON_INFO)

    wf.send_feedback()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(proc_workflow))
