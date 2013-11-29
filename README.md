process_monitor
===============

A psutlis (python's interface to the /proc filesystem) based program to monitor and send email. 
A simple script to monitor a processes' statistics and mail if they exceed specific values.

It uses psutils python package, which in turn relies on the /proc filesystem drivers.
So all variables enabled by that are possible.

TODO:
    1.Add a file lock mechanism so that it doesn't try to run itself twice.
    2.Check the mail trigger works.

To run:
    1.make sure psutils is installed(pip/easy_install psutils)
    2.Run it once to get an idea of how much time it takes on your machine(to schedule it on cron)
    3.Modify the monitor_prod_vars.py to set the variables and limits as you deem needed.
    4.Run/cron schedule as 'python -e <monitor_prod_vars.py file>'
