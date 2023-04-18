from flask import Flask, redirect, render_template, request,url_for,flash
import subprocess
import commonTasks
import os
import configparser
import os, sys, time

app = Flask(__name__)

# Find config file
# dir = os.path.dirname(__file__)  # os.getcwd()
# configFilePath = os.path.abspath(os.path.join(dir, "app.cfg"))
configParser = configparser.RawConfigParser()
configParser.read('/var/www/feeder/feeder/app.cfg')

# Read in config variables
SECRETKEY = str(configParser.get('feederConfig', 'Secretkey'))
hopperGPIO = str(configParser.get('feederConfig', 'Hopper_GPIO_Pin'))
hopperTime = str(configParser.get('feederConfig', 'Hopper_Spin_Time'))
motionCameraSiteAddress = str(configParser.get('feederConfig', 'Motion_Camera_Site_Address'))

#####################################################################################
##########################################HOME PAGE##################################
#####################################################################################
@app.route('/', methods=['GET', 'POST'])
def home_page():
    try:
        cameraStatusOutput = DetectCamera()

        # cameraStatusOutput = 'supported=0 detected=1'
        if "detected=1" in str(cameraStatusOutput):
            cameraStatus = '1'
        else:
            cameraStatus = '0'

        # Return page
        return render_template('home.html', cameraSiteAddress=motionCameraSiteAddress, cameraStatus=cameraStatus)

    except Exception as e:
        return render_template('error.html', resultsSET=e)


@app.route('/feedbuttonclick', methods=['GET', 'POST'])
def feedbuttonclick():
    try:
        spin = commonTasks.spin_hopper(hopperGPIO, hopperTime)

        if spin != 'ok':
            flash('Error! No feed activated! Error Message: ' + str(spin), 'error')
            return redirect(url_for('home_page'))

        flash('Hranjenje uspješno! :)')
        return redirect(url_for('home_page'))
    except Exception as e:
        return render_template('error.html', resultsSET=e)
    
@app.route('/video', methods=['GET', 'POST'])

def DetectCamera():
    try:

        process = subprocess.Popen(["vcgencmd", "get_camera"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        return process.stdout.read()
    except Exception as e:
        return 'status=0'



app.secret_key = SECRETKEY

# main
if __name__ == '__main__':
    app.debug = False  # reload on code changes. show traceback
    app.run(host='0.0.0.0', threaded=True)
