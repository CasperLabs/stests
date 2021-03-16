from sh.scripts.svc_utils import common_main
from sh.scripts.svc_utils import SvcCommand

SVC_COMMAND = SvcCommand.STOP

if __name__ == '__main__':
    common_main(SVC_COMMAND)
