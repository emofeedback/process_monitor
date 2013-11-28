import psutil
import optparse
import mailutils

global Process,m_vars


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

    ret = dict()
    for key in m_vars.MonitorValsCount.keys():

        proc_obj_elem = 'Process.'+key   #Process object member funcs/vars
        if callable(proc_obj_elem):
            val = apply(proc_obj_elem)
            #Damn it sometimes this module returns a custom obj. would have been easier if it's always number
            #Now i have to handle individual cases, more code.. duh.. probs of OOPS design.

            #if isinstance(val,psutil._common.cputimes):
            #    for each in m_vars.get(key):
            #        if val.user > each.get(user):
            #            ret.append( True)
            #    if val > m_vars.get(key).get(
            if isinstance(val,(int,float)):

                if val > m_vars.MonitorValsCount.get(key):
                    ret.update({key: True})
                else:
                    ret.update({key,False})
            if isinstance(val,str,list):
                if val != m_vars.MonitorValsCount.get(key):
                    ret.update({key:True})
                else:
                    ret.update({key:False})
            #Duh.. still so many conditions, there ought to be a better way.

        elif proc_obj_elem > m_vars.MonitorValsCount.get(key):
            ret.update({key:True})
        else:
            ret.update({key:False})
    return ret


def main(environ):
    #global m_vars
    if environ == 'prodn':
    	import monitor_prod_vars as m_vars

    elif environ == 'stage':
    	import monitor_stage_vars as m_vars
    start_monitor_proc(m_vars.Pid)


    ret_dict = check_monitor_proc(m_vars)
    if False in ret_dict.values():
        send_mail(ret_dict)

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
