# Concat text by comma
# Written by homeway 2020.8.25

import pyperclip
import sys
import time
from workflow import Workflow, ICON_CLOCK, ICON_ERROR, ICON_GROUP, ICON_INFO


def trim_title(title, length):
    if len(title) > length:
        return title[:length] + "..."
    else:
        return title


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
        # remove function params
        if text.find('(') > 0:
            text = text[:text.index('(')]
        # separate class name and function name
        loc_sep = text.index('#')
        class_name = text[:loc_sep]
        function_name = text[loc_sep + 1:]
        class_and_function = class_name + ' ' + function_name

        # add commands
        watch_cmd = 'watch -x 3 ' + class_and_function + ' {params,returnObj,throwExp}'
        trace_cmd = 'trace ' + class_and_function
        class_cmd = 'sc -df ' + class_name

        wf.add_item(title=trim_title(watch_cmd, 10),
                    subtitle=watch_cmd,
                    arg=watch_cmd,
                    valid=True,
                    icon=ICON_INFO)
        wf.add_item(title=trim_title(trace_cmd, 10),
                    subtitle=trace_cmd,
                    arg=trace_cmd,
                    valid=True,
                    icon=ICON_INFO)
        wf.add_item(title=trim_title(class_cmd, 10),
                    subtitle=class_cmd,
                    arg=class_cmd,
                    valid=True,
                    icon=ICON_INFO)

    wf.send_feedback()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(proc_workflow))
