import psutil
import optparse
import mailutils

global Process,m_vars

def check_monitor_proc():
    pass

def send_mail():
    mailutils.compose_email_body()
    mailutils.email_results()
    pass


def start_monitor_proc(pid):
    global Process
    Process = psutil.Process(pid)
    #Process.wait()

def check_monitor_proc(m_vars):

    global Process
    if():
        return True
    return False

def main(environ):
    #global m_vars
    if environ == 'prodn':
    	import monitor_prod_vars as m_vars

    elif environ == 'stage':
    	import monitor_stage_vars as m_vars
    start_monitor_proc(m_vars.Pid)


    if check_monitor_proc():
        send_mail()

if __name__ == '__main__':
    OP = optparse.OptionParser()
    OP.add_option("-e","--environ",dest="environ",help="stage/prodn/retest/sim")
    (options,args) = OP.parse_args()
    print options, args

    if options.environ:
    	main(options.environ)
    else:
        print "-e or --environ  <args> is mandatory.See help"
        exit()
