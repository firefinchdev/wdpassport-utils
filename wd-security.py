#!/usr/bin/env python

# Created: Tue Jan 7 13:13:15 2013
#      by: funkypopcorn
#      (https://github.com/funkypopcorn)
#
# Modified: Sujay Phadke, 2015
# email: electronicsguy123@gmail.com
# github: https://github.com/electronicsguy/
# 
# changes:
# 1. code cleanup
# 2. added code to detect connected drives, lock status
# 3. Check sudo and required packages at startup

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot
import subprocess
import cookpw
import os

# Store the partition name in this variable
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

class MessageBoxDemo(QtGui.QWidget):
    def __init__(self, title, msg):
        """Constructor"""
        # super(DialogDemo, self).__init__()
        QtGui.QWidget.__init__(self)
        #self.setWindowTitle("MessageBox Demo")
        
	QtGui.QMessageBox.information(self, title, msg)

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

	#self.footerLabel = QtGui.QLabel(Frame)
        #self.footerLabel.setGeometry(QtCore.QRect(50, 420, 541, 41))
        #self.footerLabel.setObjectName(_fromUtf8("footerLabel"))

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
	self.decryptBtn.clicked.connect(self.decryptWD)

        self.mountBtn = QtGui.QPushButton(Frame)
        self.mountBtn.setEnabled(False)
        self.mountBtn.setGeometry(QtCore.QRect(210, 190, 151, 51))
        self.mountBtn.setObjectName(_fromUtf8("mountBtn"))
	self.mountBtn.clicked.connect(self.mountWD)

        self.exitBtn = QtGui.QPushButton(Frame)
        self.exitBtn.setGeometry(QtCore.QRect(390, 190, 151, 51))
        self.exitBtn.setObjectName(_fromUtf8("exitBtn"))
	self.exitBtn.clicked.connect(Frame.close)

        self.messageLabel = QtGui.QLabel(Frame)
        self.messageLabel.setGeometry(QtCore.QRect(40, 270, 121, 21))
        self.messageLabel.setObjectName(_fromUtf8("messageLabel"))

        self.messageBox = QtGui.QTextEdit(Frame)
        self.messageBox.setGeometry(QtCore.QRect(40, 300, 521, 111))
        self.messageBox.setObjectName(_fromUtf8("messageBox"))

	self.disclaimerBtn = QtGui.QPushButton('Disclaimer', Frame)
	#self.disclaimerBtn.move(40, 430)
        self.disclaimerBtn.setGeometry(40, 430, 90, 30)
	self.disclaimerBtn.clicked.connect(self.showDisclaimer)

        self.retranslateUi(Frame)
	self.checkWDdrive()

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
        #self.footerLabel.setText(_translate("Frame", "<html><head/><body><p><span style=\" font-size:10pt; font-style:italic;\">(This utility has only been tested with one WD locked drive attached. <br/>Please do not connect more than 1 locked USB drives!)</span></p></body></html>", None))
	self.disclaimerBtn.setText(_translate("Frame", "Disclaimer", None))

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
		self.messageBox.append("No Western Digital drive attached.")
		self.messageBox.append("Please attach a compatible drive and restart.")
		self.pwBox.setEnabled(False)
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
			self.pwBox.setEnabled(False)
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
	# to-do: the logic here needs to be changed as in:
	# if infact multiple locked drives are connected, it'll output
	# multiple lines (sdb, sdc, etc). That doesn't necessarily mean they are unlocked
	# A per-drive check needs to be made for any partitions identified (like sdb1, sdb2, etc)
	if numLines == 0:
		self.messageBox.append("Error locating WD drive! Please re-connect and try again.")
	elif numLines == 1:
		self.messageBox.append("Drive appears to be locked")
	else:
		self.messageBox.append("Drive is already unlocked!")
		self.pwBox.setEnabled(False)
		PARTNAME = str(lines[0][-4:-1])	    # ignore trailing newline char
		self.messageBox.append("Drive device name: " + PARTNAME)
		self.checkMountStatus()

    def checkMountStatus(self):
	# to-do: add code to check if partitions are already mounted
	self.mountBtn.setEnabled(True)

    def decryptWD(self):
        self.callCookingPW()

    def callCookingPW(self):
        self.messageBox.append("Calling external cookpw-script...")

	# finish processing all pending events
        app.processEvents()

        try:
            pw = str(self.pwBox.text())
	    self.pwBox.clear()
	    fpathc = os.path.dirname(os.path.abspath(__file__))+"/cookpw.py"
            subprocess.check_call("python "+fpathc+" "+pw+" >"+fpathp, shell=True)
    
        except subprocess.CalledProcessError:       
            self.messageBox.append("Cannot execute 'cookpw.py' script.")
	    self.messageBox.append("Please check if the path is correct and retry.")
            return
        try:
            with open(fpathp):
                self.messageBox.append("Sending SCSI commands to unlock the drive...")
                self.unlockDrive()
        except IOError:
            self.messageBox.append("Cannot create 'password.bin' file. Check paths, permissions and retry.")
            return
        

    def unlockDrive(self):
        try:
	    # to-do: make this check a separate subroutine
	    # multiple drives could be supported by showing a list of 'sg<nn>' ids
	    # and selecting the required one
	    # also, I think this check is erroneous. the multiple sg<nn> entries are still reported
	    # by dmesg, even after the other drives are removed
            from subprocess import check_output as qx
            out = qx("/bin/dmesg | grep sg | grep \"type 13\" | awk \'{print $8}\'",shell=True)
            # check # drives attached
	    # each drive gets a dmesg id of the form 'sg<nn>'
            cmp = out.split( )[0]
            multipleDevices = False
            for word in out.split( ):
                if not cmp==word:
                   #multipleDevices = True
                   break
            if not multipleDevices:
                #finally lets send the SCSI command to encrypt
                self.messageBox.append("Secure Harddrive identified at /dev/" + cmp)
                try:
                    subprocess.check_call("sudo sg_raw -s 40 -i " + fpathp + " /dev/" + cmp + " c1 e1 00 00 00 00 00 00 28 00", shell=True)
                    self.messageBox.append("The WD Drive is now unlocked and can be mounted!")
		    self.mountWD()
                except subprocess.CalledProcessError:
                    self.messageBox.append("Failure while sending SCSI decrypt command. Check password and connections.")
                    return
            else:
                self.messageBox.append("Multiple SCSI 'type 13' devices recognized. Please unplug everything except the desired drive and retry.")
                return
        except subprocess.CalledProcessError:
            self.messageBox.append("Failure couldn't find 'sg' type within dmesg!")
            return


    def mountWD(self):
	global PARTNAME
            
        subprocess.call("sudo partprobe 2>/dev/null", shell=True)
        self.messageBox.append("Available devices have been updated!")

	devname = '/dev/' + PARTNAME + '1'
	self.messageBox.append('Mounting device: ' + devname)
        subprocess.check_call("udisksctl mount -b " + devname + " &>/dev/null", shell=True)
        self.messageBox.append("WD Harddrive decrypted and mounted successfully!")

	self.pwBox.setEnabled(False)
	self.decryptBtn.setEnabled(False)
	self.mountBtn.setEnabled(False)        

	return    

    def showDisclaimer(self):
	form = MessageBoxDemo("Disclaimer", "This utility enables temporary unlock for modern WD drives which support hardware level link encryption.\nIt does not support permanent unlocks(removing security) or the process of locking the drive in the first place.\n\nThis utility is not officially licenced by Western Digital. Western Digital Security is a registered trademark of Western Digital. All other trademarks belong to their respective owners.\n\nThis utility has only been tested with one WD locked drive attached.\nPlease do not connect more than 1 locked USB drives!")
    	#form.show()
    

def prompt_sudo():
    if os.geteuid() != 0:
        print >> sys.stderr, "This program requires root permissions. Please try again by prefixing 'sudo'."
        sys.exit(1)

def CheckRequiredUtils():
        try:
            subprocess.check_call("command -v sg_raw >/dev/null 2>&1", shell=True)
        except subprocess.CalledProcessError:
            print "This program requires the 'sg3-utils' (sg3_utils) package to be installed."
	    sys.exit(1)

	try:
            subprocess.check_call("command -v partprobe >/dev/null 2>&1", shell=True)
        except subprocess.CalledProcessError:
            print "This program requires the 'partprobe' package to be installed."
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
    CheckRequiredUtils()
    hFrame.show()
    status = app.exec_()   # run app, show window, wait for input
    sys.exit(status)       # terminate program with a status code returned from app

