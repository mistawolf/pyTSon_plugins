from ts3plugin import ts3plugin, PluginHost
from pytsonui import setupUi
from PythonQt.QtGui import QDialog, QListWidgetItem, QWidget, QComboBox, QPalette, QTableWidgetItem, QMenu, QAction, QCursor, QApplication, QInputDialog
from PythonQt.QtCore import Qt, QTimer
from datetime import datetime
import ts3lib, ts3defines, os, json, configparser, webbrowser, traceback, urllib.parse


class exporter(ts3plugin):
    shortname = "EX"
    name = "Teamspeak Export/Import"

    apiVersion = 22
    requestAutoload = False
    version = "1.0"
    author = "Bluscream"
    description = "Like YatQA, just as plugin.\n\nCheck out https://r4p3.net/forums/plugins.68/ for more plugins."
    offersConfigure = False
    commandKeyword = ""
    infoTitle = ""
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Export Data", "scripts/exporter/gfx/export.png"),
                (ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 1, "Import Data", "scripts/exporter/gfx/import.png")]
    hotkeys = []
    debug = False
    action = "export"

    def timestamp(self): return '[{:%Y-%m-%d %H:%M:%S}] '.format(datetime.now())

    def __init__(self):
        if self.config['GENERAL']['debug'] == "True": ts3lib.printMessageToCurrentTab("{0}[color=orange]{1}[/color] Plugin for pyTSon by [url=https://github.com/{2}]{2}[/url] loaded.".format(self.timestamp(),self.name,self.author))


    def log(self, message, channel=ts3defines.LogLevel.LogLevel_INFO, server=0):
        try:
            ts3lib.logMessage(message, channel, self.name, server)
            if self.config['GENERAL']['debug'] == "True":
                ts3lib.printMessageToCurrentTab('[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.now())+" "+self.shortname+"> "+message)
                print('[{:%Y-%m-%d %H:%M:%S}]'.format(datetime.now())+" "+self.shortname+"> ("+str(channel)+")"+message)
        except:
            _a = None

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if atype == ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL:
            if menuItemID == 0:
                self.dlg = ServersDialog(self)
                self.dlg.show()
                #ts3lib.printMessageToCurrentTab(str(self.filters))
            elif menuItemID == 1:
                _schid = ts3lib.getCurrentServerConnectionHandlerID()
                (error, _clid) = ts3lib.getClientID(_schid)
                (error, _ip) = ts3lib.getConnectionVariableAsString(_schid,_clid,ts3defines.ConnectionProperties.CONNECTION_SERVER_IP)
                (error, _port) = ts3lib.getConnectionVariableAsString(_schid,_clid,ts3defines.ConnectionProperties.CONNECTION_SERVER_PORT)
                url = ""
                if _port != "":
                    _url = self.config['GENERAL']['api']+"serverlist/result/server/ip/"+_ip+":"+_port+"/"
                else:
                    _url = self.config['GENERAL']['api']+"serverlist/result/server/ip/"+_ip+"/"
                ts3lib.printMessageToCurrentTab(str("Navigating to \""+_url+"\""))
                webbrowser.open(_url)

    def configure(self, qParentWidget):
        try:
            self.dlg = ExportDialog(self)
            self.dlg.show()
        except:
            from traceback import format_exc
            try: ts3lib.logMessage(format_exc(), ts3defines.LogLevel.LogLevel_ERROR, "PyTSon::"+self.name, 0)
            except: print("Error in "+self.name+".configure: "+format_exc())

class ExportDialog(QDialog):
    def buhl(self, s):
        if s.lower() == 'true' or s == 1:
            return True
        elif s.lower() == 'false' or s == 0:
            return False
        else: raise ValueError("Cannot convert {} to a bool".format(s))

    def __init__(self,Class,parent=None):
        self.exporter=Class
        super(QDialog, self).__init__(parent)
        setupUi(self, os.path.join(ts3lib.getPluginPath(), "pyTSon", "scripts", "exporter", "ui", "export.ui"))
        self.setWindowTitle("Which items do you want to "+exporter.action+"?")
