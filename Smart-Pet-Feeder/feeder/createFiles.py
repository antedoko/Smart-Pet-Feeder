#!/var/www/feeder/bin/python
import sys

sys.path.extend(['/var/www/feeder/feeder'])
import os


try:
    appCFGPath = '/var/www/feeder/feeder/app.cfg'

    if os.path.isfile(appCFGPath):
        print('app.cfg already exists. To create again first delete current copy')
    else:
        print('Creating app.cfg. Please wait.')
        f = open(appCFGPath, "w+")

        f.write("""[feederConfig]
Hopper_GPIO_Pin=11
Hopper_Spin_Time=0.6
Motion_Camera_Site_Address=http://yourRemoteAddress.duckdns.org:8081
Seconds_Delay_After_Button_Push=3
Secretkey=SUPER_SECRET_KEY
""")

        f.close()
        # os.chmod(appCFGPath, 0o777)
        print('app.cfg created')



except Exception as e:
    print('Error: ' + str(e))
