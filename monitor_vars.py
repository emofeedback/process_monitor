import os
Args= 3314 #Arguments for the process to be started and monitored
Pid = 3314 #Arguments for the process to be started and monitored
ChildProcDepth = 2 #No. of levels till which to monitor child procs too. Careful use a low num.

MailSubject='%s May be down: Proc id %d exceeded limits.'
TempFile = 'TempResults.txt'
MailFile = 'Mail.eml'
OpsList = {1:['anand.jeyahar@gmail.com'],2:['anand.jeyahar@gmail.com',]}
SenderMail = ""

NumReqFailureLimit = 3 #no of failed status codes that trigger email
TimeCheck = 1 #in minutes
