#TODO: Consider abandoning cron and running this continuously as a daemon and check for any contiguous time series.
#TODO: Bad read_x_lists implementation for big files.Should just fileseek for big files, or use tail or similar
#TODO: OR Just consider use a rotating file handler

#TODO: Sanity check on all variables .(data type,numerical limits etc..)
import json,pprint
m_vars = None

def compose_email_body():
    records_2_mail = read_last_x_lists(m_vars.NumReqFailureLimit)
    for rec in records_2_mail:
    	for key in rec:
	    key.pop('headers')
    with open(m_vars.MailFile,'w') as mail_fd:

        pprint.pprint(records_2_mail,mail_fd,depth=3)
        pprint.pprint("Rest of the file can be found at %s"%m_vars.ResultsFile,mail_fd)

def email_results(req_fails,url_fails):
    import smtplib
    from email.mime.text import MIMEText

    mail_msg = None
    compose_email_body()
    with open(m_vars.MailFile) as mail_fd:
        mail_msg = MIMEText(mail_fd.read())
    mail_msg['Subject'] = m_vars.MailSubject%(req_fails,m_vars.NumReqFailureLimit,url_fails,len(m_vars.URLs))
    mail_msg['From'] = m_vars.SenderMail
    mail_msg['To'] = ','.join(m_vars.OpsList.get(req_fails))
    serv = smtplib.SMTP('localhost')
    serv.sendmail(m_vars.SenderMail,m_vars.OpsList.get(req_fails),mail_msg.as_string())
    serv.quit()

def status_check_url(url):
    import urllib2
    import datetime
    results = {}
    print("Checking url:%s for status"%url)
    try:
        url_fd = urllib2.urlopen(url,timeout=10)
        results.update({'timestamp':str(datetime.datetime.utcnow()),
                        'status':url_fd.getcode(),
                        'url':url
                        })
        #results.update({'headers':url_fd.headers})
        url_fd.close()
        print "Request Success with HTTP status:%s\n"%results.get('status')
    except urllib2.URLError as e:
        results.update({'timestamp':str(datetime.datetime.utcnow()),
                        'error':e,
                        'status':999,
                        'url':url})

    return results

def to_mail_or_not(results):
    """
    @results: list of list of dictionaries

    Checks for url failures or request failures against corresponding limit vars.
    Note even a single url failure is counted as that temporal ticks' req failure.
    """
    req_failures = 0
    for result in results:
    #WARNING:Assumes this is run every minute as a cron job
    	req_url_failures = list()
    	for res in result:
            url_failures = 0
    	    status = int(res.get('status'))
    	    if status > 400 and status <600:
    	        url_failures +=1
                req_failures +=1
    	    elif status == 999:
    	        url_failures = m_vars.NumReqFailureLimit+1  #Abort
            else:
                continue
    	    if url_failures > m_vars.URLFailureLimit:
                break
            req_url_failures.append(url_failures)
        if ((req_failures > m_vars.NumReqFailureLimit) and (max(req_url_failures) >m_vars.URLFailureLimit)):
            return (True,req_failures,max(url_failures))
    return (False,req_failures,url_failures)

def stringify_py_objs(res):
    temp_r = list()
    for r in res:
        temp_d = dict()
        for key,val in r.iteritems():
            temp_d.update({str(key):str(val)})
            temp_r.append(temp_d)

    return temp_r

def append_to_file(res):
    global m_vars 		#apparently python compiler fails in this case
    with open(m_vars.ResultsFile,"a+") as out_fd:
        res = stringify_py_objs(res)
        out_fd.write(json.dumps(res)+'\n')

def read_last_x_lists(n):
    #TODO: Consider using tempfile for the tempfile
    import subprocess
    ret = list()
    with open(m_vars.TempFile,'w') as fd:
        cmd_list = ['tail','-n',str(n),m_vars.ResultsFile]
        p =subprocess.Popen(cmd_list,stdout=fd)
        p.wait()

    with open(m_vars.TempFile,'r') as fd:
        for line in fd:
            ret.append(json.loads(line))
    return ret

def main(environ):
    global m_vars
    if environ == 'prodn':
    	import monitor_prod_vars as m_vars

    elif environ == 'stage':
    	import monitor_stage_vars as m_vars

    import pprint,os,json
    import sys
    sys.path.append(os.path.dirname(__file__))
    url = m_vars.Urls

    res = list()
    if isinstance(url,list):
        res = map(status_check_url,url)
    else:
        res.append(status_check_url(url))
    append_to_file(res)
    records_2_check = read_last_x_lists(m_vars.NumReqFailureLimit)
    (send_mail,req_fails,url_fails) = to_mail_or_not(records_2_check)
    print send_mail,req_fails,url_fails
    if send_mail:
        print "Emailing results"
        email_results(req_fails,url_fails)
    if req_fails > 0:
        print "Emailing results:%d failures"%req_fails
        email_results(req_fails,url_fails)

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-e","--environ",dest="environ",help="stage/prodn/retest/sim")
    (options,args) = parser.parse_args()
    print options, args
    if options.environ:
    	main(options.environ)
    else:
        print "-e or --environ  <args> is mandatory.See help"
