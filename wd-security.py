#!/usr/bin/env python

# Feel free to use edit and modify
#
# Created: Tue Jan 7 13:13:15 2013
#      by: funkypopcorn
#      (https://github.com/funkypopcorn)
#
# Modified: Sujay Phadke, 2015
# email: electronicsguy123@gmail.com

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
import subprocess
import cookpw
import os

PARTNAME=''

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

fpathc = os.path.dirname(os.path.abspath(__file__))+"/cookpw.py"
fpathp = os.path.dirname(os.path.abspath(__file__))+"/password.bin"

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName(_fromUtf8("Frame"))
        Frame.resize(603, 478)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Raised)
        
	myTitleFont = QtGui.QFont()
        myTitleFont.setFamily(_fromUtf8("Waree"))
        myTitleFont.setPointSize(18)
        myTitleFont.setBold(True)
        myTitleFont.setWeight(75)

	myHeaderFont = QtGui.QFont()
        myHeaderFont.setFamily(_fromUtf8("Times"))
        myHeaderFont.setPointSize(12)
        myHeaderFont.setBold(True)
        myHeaderFont.setWeight(75)
	myHeaderFont.setItalic(True)

	self.titleLabel = QtGui.QLabel(Frame)
        self.titleLabel.setGeometry(QtCore.QRect(50, 30, 511, 30))
        self.titleLabel.setFont(myTitleFont)
        self.titleLabel.setLineWidth(1)
        self.titleLabel.setObjectName(_fromUtf8("titleLabel"))

	self.header1Label = QtGui.QLabel(Frame)
        self.header1Label.setGeometry(QtCore.QRect(50, 60, 511, 30))
        self.header1Label.setFont(myHeaderFont)
        self.header1Label.setLineWidth(1)
        self.header1Label.setObjectName(_fromUtf8("header1Label"))

        self.pwLabel = QtGui.QLabel(Frame)
        self.pwLabel.setGeometry(QtCore.QRect(65, 125, 65, 21))
        self.pwLabel.setObjectName(_fromUtf8("pwLabel"))

        self.pwBox = QtGui.QLineEdit(Frame)
        self.pwBox.setGeometry(QtCore.QRect(140, 120, 381, 31))
        self.pwBox.setObjectName(_fromUtf8("pwBox"))
	self.pwBox.setEchoMode(QtGui.QLineEdit.Password)
	self.pwBox.setPlaceholderText('Enter password to unlock WD drive')

	self.decryptBtn = QtGui.QPushButton(Frame)
        self.decryptBtn.setGeometry(QtCore.QRect(40, 190, 141, 51))
        self.decryptBtn.setObjectName(_fromUtf8("decryptBtn"))

        self.mountBtn = QtGui.QPushButton(Frame)
        self.mountBtn.setEnabled(False)
        self.mountBtn.setGeometry(QtCore.QRect(210, 190, 151, 51))
        self.mountBtn.setObjectName(_fromUtf8("mountBtn"))

        self.exitBtn = QtGui.QPushButton(Frame)
        self.exitBtn.setGeometry(QtCore.QRect(390, 190, 151, 51))
        self.exitBtn.setObjectName(_fromUtf8("exitBtn"))

        self.messageLabel = QtGui.QLabel(Frame)
        self.messageLabel.setGeometry(QtCore.QRect(40, 270, 121, 21))
        self.messageLabel.setObjectName(_fromUtf8("messageLabel"))

        self.messageBox = QtGui.QTextEdit(Frame)
        self.messageBox.setGeometry(QtCore.QRect(40, 300, 521, 111))
        self.messageBox.setObjectName(_fromUtf8("messageBox"))

        self.footerLabel = QtGui.QLabel(Frame)
        self.footerLabel.setGeometry(QtCore.QRect(50, 420, 541, 41))
        self.footerLabel.setObjectName(_fromUtf8("footerLabel"))

        self.retranslateUi(Frame)
	self.checkWDdrive()
        QtCore.QObject.connect(self.exitBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), Frame.close)
        QtCore.QObject.connect(self.decryptBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.decryptWD)
        QtCore.QObject.connect(self.mountBtn, QtCore.SIGNAL(_fromUtf8("clicked()")), self.autoMount)
	QtCore.QObject.connect(self.pwBox, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), self.pwBox_text_changed)
	QtCore.QObject.connect(self.pwBox, QtCore.SIGNAL(_fromUtf8("returnPressed()")), self.pwBox_check_text)
	self.pwBox.setFocus()
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(_translate("Frame", "WD-Security", None))
        self.decryptBtn.setText(_translate("Frame", "Unlock Drive", None))
	self.decryptBtn.setEnabled(False)
        self.pwLabel.setText(_translate("Frame", "Password:", None))
        self.messageLabel.setText(_translate("Frame", "Status/Error-Log:", None))
        self.titleLabel.setText(_translate("Frame", "WD Security for Linux", None))
	self.header1Label.setText(_translate("Frame", "An unofficial solution", None))
        self.exitBtn.setText(_translate("Frame", "Exit", None))
        self.mountBtn.setText(_translate("Frame", "Mount Drive", None))
        self.footerLabel.setText(_translate("Frame", "<html><head/><body><p><span style=\" font-size:10pt; font-style:italic;\">(This utility has only been tested with one WD locked drive attached. <br/>Please do not connect more than 1 locked USB drives!)</span></p></body></html>", None))


    # Grey-out button if no password entered
    @pyqtSlot(str)
    def pwBox_text_changed(self, text):
        if text:  # Check to see if text is filled in
	    self.decryptBtn.setEnabled(True)
        else:
            self.decryptBtn.setEnabled(False)

    # Check that password is not empty when ENTER is pressed
    @pyqtSlot(str)
    def pwBox_check_text(self):
	if self.pwBox.text().length() > 0:
	    self.decryptWD()
	else:
	    self.pwBox.setFocus()

    def checkWDdrive(self):
	cmd = 'lsusb |grep -i "Western Digital" | sed -e \'s/:.*//\''
	p = subprocess.Popen(cmd, universal_newlines=True, shell=True, 
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	pout = p.stdout.read()
	retcode = p.wait()
	if pout == "":	
		self.messageBox.append("No Western Digital drive attached")
	else:
		self.messageBox.append("Western Digital Drive found at: " + pout)
	
		cmd2 = 'lsblk | grep -i "WD Unlocker" | wc -l'
		p2 = subprocess.Popen(cmd2, universal_newlines=True, shell=True, 
			stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		pout2 = p2.stdout.read()
		retcode2 = p2.wait()
		if int(pout2) == 0:
			self.messageBox.append("Either the drive is not locked or doesn't support WD security")
			self.messageBox.append("If you believe this is false, please re-connect the disk and try again.")
		else:
			self.messageBox.append("Checking drive lock status...")
			self.checkUnlockStatus()

    def checkUnlockStatus(self):
	global PARTNAME
	cmd = 'ls  -l /dev/disk/by-id | grep "/sd" | grep -i "usb-WD" | perl -pe \'s/(.*?)usb-WD_(.*)-\d:\d -> \.\.\/\.\.\/(.*?)/$2 $3/\''
	p = subprocess.Popen(cmd, universal_newlines=True, shell=True, 
		stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	lines = p.stdout.readlines()
	numLines = len(lines)
	retcode = p.wait()
	if numLines == 0:
		self.messageBox.append("Error locating WD drive! Please re-connect and try again.")
	elif numLines == 1:
		self.messageBox.append("Drive appears to be locked")
	else:
		self.messageBox.append("Drive is already unlocked!")
		self.pwBox.setEnabled(False)
		self.mountBtn.setEnabled(True)
		PARTNAME = str(lines[0][-4:-1])		# ignore trailing newline char
		self.messageBox.append("Drive device name: " + PARTNAME)

    def decryptWD(self):
        try:
            subprocess.check_call("command -v sg_raw >/dev/null 2>&1", shell=True)
            self.callCookingPW()
        except subprocess.CalledProcessError:
            self.messageBox.setText("sg3-utils not installed, so we are going to install it...")
            try:
                subprocess.check_call("gksudo apt-get install sg3-utils", shell=True)
            except subprocess.CalledProcessError:
                self.messageBox.append("Installation went wrong! You have to install/compile it manually sorry!")
                return
            self.messageBox.append("sg3-utils installed successfully!")
            self.callCookingPW()


    def callCookingPW(self):
        self.messageBox.append("Calling external cookpw-script...")
        app.processEvents()
        try:
            pw = str(self.pwBox.text())
	    self.pwBox.clear()
            if not pw == "":
                fpathc = os.path.dirname(os.path.abspath(__file__))+"/cookpw.py"
                subprocess.check_call("python "+fpathc+" "+pw+" >"+fpathp, shell=True)
            else:
                self.messageBox.append("Password left empty pls type in PW and click Mount again!")
                return
        except subprocess.CalledProcessError:       
            self.messageBox.append("Script calling went wrong, pls check if the path to cookpw.py is correct!")
            return
        try:
            with open(fpathp):
                self.messageBox.append("Sending SCSI commands to encrypt/unlock the drive...")
                self.unlockDrive()
        except IOError:
            self.messageBox.append("Something went wrong while executing cookpw.py -> password.bin not created!")
            return
        

    def unlockDrive(self):
        try:
            from subprocess import check_output as qx
            out = qx("/bin/dmesg | grep sg | grep \"type 13\" | awk \'{print $8}\'",shell=True)
            #check if there is only one unique sg device otherwise stop
            try:
                cmp = out.split( )[0]
            except IndexError:
                self.messageBox.append("Couldn't find WD Drive in dmesg, pls unplug and replug the drive again!")
                return
            multipleDevices = False;
            for word in out.split( ):
                if not cmp==word:
                   multipleDevices = True
                   break
            if not multipleDevices:
                #finally lets send the SCSI command to encrypt
                self.messageBox.append("Secure Harddrive identified at /dev/"+cmp)
                try:
                    #subprocess.check_call("gksudo whoami", shell=True)
                    subprocess.check_call("sudo sg_raw -s 40 -i "+fpathp+" /dev/"+cmp+" c1 e1 00 00 00 00 00 00 28 00", shell=True)
                    self.messageBox.append("Drive is now unlocked and can be mounted!")
		    self.mountWD()
                    #self.mountBtn.setEnabled(True)
                except subprocess.CalledProcessError:
                    self.messageBox.append("Failure while sending SCSI decrypt command. Check password and connections.")
                    return
            else:
                self.messageBox.append("Failure multiple SCSI type 13 devices recognized pls unplug everything except the WD drive and wait a bit before you retry.")
                return
        except subprocess.CalledProcessError:
            self.messageBox.append("Failure couldn't find sg type within dmesg!")
            return


    def mountWD(self):
        self.decryptBtn.setEnabled(False)
        try:
            subprocess.check_call("command -v partprobe >/dev/null 2>&1", shell=True)
            self.autoMount()
        except subprocess.CalledProcessError:
            self.messageBox.setText("parted not installed, so we are going to install it...")
            try:
                subprocess.check_call("gksudo apt-get install parted", shell=True)
            except subprocess.CalledProcessError:
                self.messageBox.append("Installation went wrong! You have to install/compile parted manually sorry!")
                return
            self.messageBox.append("Parted installed successfully!")
            self.autoMount()


    def autoMount(self):
	global PARTNAME
        #try:
            #subprocess.check_call("gksudo whoami", shell=True)
        subprocess.call("sudo partprobe 2>/dev/null", shell=True)
        self.messageBox.append("Available devices have been updated!")
        #    try:
	devname = '/dev/' + PARTNAME + '1'
	self.messageBox.append('Mounting device: ' + devname)
        subprocess.check_call("udisksctl mount -b " + devname + " &>/dev/null", shell=True)
        self.messageBox.append("WD Harddrive decrypted and mounted successfully!")
	self.mountBtn.setEnabled(False)        
	return
        #    except subprocess.CalledProcessError:
        #        self.messageBox.setText("Failure: udisk automoint didn't work! Maybe the uuid/Volume Serial Number you entered is wrong!")
        #        return
        #except subprocess.CalledProcessError:
        #    self.messageBox.setText("Failure: partprobe not successfull -> check path to partprobe (which partprobe)")
        #    return


def prompt_sudo():
    if os.geteuid() != 0:
        print >> sys.stderr, "This program requires root permissions. Please try again by prefixing 'sudo'."
        sys.exit(1)

if __name__ == "__main__":
# ref: http://pyqt.sourceforge.net/Docs/PyQt4/qapplication.html
    import sys
    global app
    app = QtGui.QApplication(sys.argv)
    hFrame = QtGui.QFrame()    
    hWin = Ui_Frame()
    hWin.setupUi(hFrame)
    
    prompt_sudo()
    hFrame.show()
    status = app.exec_()   # run app, show window, wait for input
    sys.exit(status)       # terminate program with a status code returned from app

