# encoding=UTF8
# Odps result to csv
# Written by homeway 2021.10.10

import pyperclip
import sys
import time
import json
from workflow import Workflow, ICON_CLOCK, ICON_ERROR, ICON_GROUP, ICON_INFO

reload(sys)
sys.setdefaultencoding('utf-8')

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
        if text.startswith("\""):
            text = text[1:-1]
        text = text.encode(encoding='UTF-8', errors='strict').replace('\\', '')
        outer_list = json.loads(text)
        result = ''
        for item in outer_list:
            result += '\t'.join(map(lambda x: str(x), item)) + '\n'

        wf.add_item(title=trim_title(result, 10),
                    subtitle=result,
                    arg=result,
                    valid=True,
                    icon=ICON_INFO)

    wf.send_feedback()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(proc_workflow))
