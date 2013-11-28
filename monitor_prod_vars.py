import os
Pid = 1273 #PID for the process to be monitored
ChildProcDepth = 2 #No. of levels till which to monitor child procs too. Careful use a low num.

MonitorValsCount = {'get_cpu_percent':50,
                    'getcwd':'/etc/blah',
                    'exe':  '/usr/bin/bla',
                    'get_cpu_affinity': [1,2,3,4],
                    'get_nice':5,
        } #Dict of all vars to monitor as keys and monitor counts as values.
                    #{'user':5,'system':4},'':}

MailSubject='%s May be down: Proc id %d exceeded limits.'
TempFile = 'TempResults.txt'
MailFile = 'Mail.eml'
OpsList = {1:['anand.jeyahar@gmail.com'],2:['anand.jeyahar@gmail.com',]}
SenderMail = ""

NumReqFailureLimit = 3 #no of failed status codes that trigger email
TimeCheck = 1 #in minutes
