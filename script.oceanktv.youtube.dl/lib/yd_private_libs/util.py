# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon
import os, sys, traceback, binascii

ADDON = xbmcaddon.Addon(id='script.oceanktv.youtube.dl')
T = ADDON.getLocalizedString

TMP_PATH = os.path.join(xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8'),'tmp')
if not os.path.exists(TMP_PATH): os.makedirs(TMP_PATH)
QUEUE_FILE = os.path.join(xbmc.translatePath(ADDON.getAddonInfo('profile')).decode('utf-8'),'download.queue')
MODULE_PATH = os.path.join(xbmc.translatePath(ADDON.getAddonInfo('path')).decode('utf-8'),'lib')


DEBUG = ADDON.getSetting('debug') == 'true'

def LOG(msg,debug=False):
    if debug and not DEBUG: return
    xbmc.log('script.oceanktv.youtube.dl: {0}'.format(msg))

def ERROR(msg=None,hide_tb=False):
    if msg: LOG('ERROR: {0}'.format(msg))
    if hide_tb and not DEBUG:
        errtext = sys.exc_info()[1]
        LOG('%s::%s (%d) - %s' % (msg or '?', sys.exc_info()[2].tb_frame.f_code.co_name, sys.exc_info()[2].tb_lineno, errtext))
        return
    xbmc.log(traceback.format_exc())

def getSetting(key,default=None):
    setting = ADDON.getSetting(key)
    return _processSetting(setting,default)

def _processSetting(setting,default):
    if not setting: return default
    if isinstance(default,bool):
        return setting.lower() == 'true'
    elif isinstance(default,float):
        return float(setting)
    elif isinstance(default,int):
        return int(float(setting or 0))
    elif isinstance(default,list):
        if setting: return binascii.unhexlify(setting).split('\0')
        else: return default

    return setting

def setSetting(key,value):
    value = _processSettingForWrite(value)
    ADDON.setSetting(key,value)

def _processSettingForWrite(value):
    if isinstance(value,list):
        value = binascii.hexlify('\0'.join(value))
    elif isinstance(value,bool):
        value = value and 'true' or 'false'
    return str(value)

def busyDialog(func):
    def inner(*args,**kwargs):
        try:
            xbmc.executebuiltin("ActivateWindow(10138)")
            return func(*args,**kwargs)
        finally:
            xbmc.executebuiltin("Dialog.Close(10138)")
    return inner

class xbmcDialogSelect:
    def __init__(self,heading='Options'):
        self.heading = heading
        self.items = []

    def addItem(self,ID,display):
        self.items.append((ID,display))

    def getResult(self):
        IDs = [i[0] for i in self.items]
        displays = [i[1] for i in self.items]
        idx = xbmcgui.Dialog().select(self.heading,displays)
        if idx < 0: return None
        return IDs[idx]