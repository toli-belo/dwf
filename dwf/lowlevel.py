#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
===========================================
Digilent's DWF library wrapper for python.
===========================================

Copyright notice
================

Copyright (c) 2016 MURAMATSU Atsushi <amura@tomato.sakura.ne.jp>

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php


Supported platforms
===================

* Python 2.6, 2.7 or Python 3.3 or above
* Windows, OSX, or Linux with Digilent's Waveforms 2015 or lator

This code is tested with Waveforms SDK, October 12, 2015 version.
'''

import sys
import os
from ctypes import *

if sys.platform.startswith("win"):
    dwfdll = cdll.dwf
elif sys.platform.startswith("darwin"):
    try:
        dwfdll = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
    except OSError:
        dwfdll = cdll.LoadLibrary(
            "/Applications/WaveForms.app/Contents/Frameworks/dwf.framework/dwf")
else:
    dwfdll = cdll.LoadLibrary("libdwf.so")

BOOL = c_int

#################################################################
# Function-based APIs
##################

# hardware device handle
HDWF = c_int
hdwfNone = 0

# device enumeration filters
ENUMFILTER = c_int
enumfilterAll = 0
enumfilterEExplorer = 1
enumfilterDiscovery = 2

# device ID
DEVID = c_int
devidEExplorer = 1
devidDiscovery = 2

# device version
DEVVER = c_int
devverEExplorerC = 2
devverEExplorerE = 4
devverEExplorerF = 5
devverDiscoveryA = 1
devverDiscoveryB = 2
devverDiscoveryC = 3

# trigger source
TRIGSRC = c_ubyte
trigsrcNone = 0
trigsrcPC = 1
trigsrcDetectorAnalogIn = 2
trigsrcDetectorDigitalIn = 3
trigsrcAnalogIn = 4
trigsrcDigitalIn = 5
trigsrcDigitalOut = 6
trigsrcAnalogOut1 = 7
trigsrcAnalogOut2 = 8
trigsrcAnalogOut3 = 9
trigsrcAnalogOut4 = 10
trigsrcExternal1 = 11
trigsrcExternal2 = 12
trigsrcExternal3 = 13
trigsrcExternal4 = 14

# instrument states:
DwfState = c_ubyte
DwfStateReady = 0
DwfStateConfig = 4
DwfStatePrefill = 5
DwfStateArmed = 1
DwfStateWait = 7
DwfStateTriggered = 3
DwfStateRunning = 3
DwfStateDone = 2

#
DwfEnumConfigInfo = c_int
DECIAnalogInChannelCount = 1
DECIAnalogOutChannelCount = 2
DECIAnalogIOChannelCount = 3
DECIDigitalInChannelCount = 4
DECIDigitalOutChannelCount = 5
DECIDigitalIOChannelCount = 6
DECIAnalogInBufferSize = 7
DECIAnalogOutBufferSize = 8
DECIDigitalInBufferSize = 9
DECIDigitalOutBufferSize = 10

# acquisition modes:
ACQMODE = c_int
acqmodeSingle = 0
acqmodeScanShift = 1
acqmodeScanScreen = 2
acqmodeRecord = 3

# analog acquisition filter:
FILTER = c_int
filterDecimate = 0
filterAverage = 1
filterMinMax = 2

# analog in trigger mode:
TRIGTYPE = c_int
trigtypeEdge = 0
trigtypePulse = 1
trigtypeTransition = 2

# analog in trigger condition
TRIGCOND = c_int
trigcondRisingPositive = 0
trigcondFallingNegative = 1

# analog in trigger length condition
TRIGLEN = c_int
triglenLess = 0
triglenTimeout = 1
triglenMore = 2

# error codes for DWF Public API:
DWFERC = c_int
dwfercNoErc = 0                 # No error occurred
dwfercUnknownError = 1          # API waiting on pending API timed out
dwfercApiLockTimeout = 2        # API waiting on pending API timed out
dwfercAlreadyOpened = 3         # Device already opened
dwfercNotSupported = 4          # Device not supported
dwfercInvalidParameter0 = 0x10  # Invalid parameter sent in API call
dwfercInvalidParameter1 = 0x11  # Invalid parameter sent in API call
dwfercInvalidParameter2 = 0x12  # Invalid parameter sent in API call
dwfercInvalidParameter3 = 0x13  # Invalid parameter sent in API call
dwfercInvalidParameter4 = 0x14  # Invalid parameter sent in API call

# analog out signal types
FUNC = c_ubyte
funcDC = 0
funcSine = 1
funcSquare = 2
funcTriangle = 3
funcRampUp = 4
funcRampDown = 5
funcNoise = 6
funcCustom = 30
funcPlay = 31

# analog io channel node types
ANALOGIO = c_ubyte
analogioEnable = 1
analogioVoltage = 2
analogioCurrent = 3
analogioPower = 4
analogioTemperature = 5

AnalogOutNode = c_int
AnalogOutNodeCarrier = 0
AnalogOutNodeFM = 1
AnalogOutNodeAM = 2

DwfAnalogOutMode = c_int
DwfAnalogOutModeVoltage = 0
DwfAnalogOutModeCurrent = 1

DwfAnalogOutIdle = c_int
DwfAnalogOutIdleDisable = 0
DwfAnalogOutIdleOffset = 1
DwfAnalogOutIdleInitial = 2

DwfDigitalInClockSource = c_int
DwfDigitalInClockSourceInternal = 0
DwfDigitalInClockSourceExternal = 1

DwfDigitalInSampleMode = c_int
DwfDigitalInSampleModeSimple = 0
# alternate samples: noise|sample|noise|sample|... 
# where noise is more than 1 transition between 2 samples
DwfDigitalInSampleModeNoise = 1

DwfDigitalOutOutput = c_int
DwfDigitalOutOutputPushPull = 0
DwfDigitalOutOutputOpenDrain = 1
DwfDigitalOutOutputOpenSource = 2
DwfDigitalOutOutputThreeState = 3 # for custom and random

DwfDigitalOutType = c_int
DwfDigitalOutTypePulse = 0
DwfDigitalOutTypeCustom = 1
DwfDigitalOutTypeRandom = 2

DwfDigitalOutIdle = c_int
DwfDigitalOutIdleInit = 0
DwfDigitalOutIdleLow = 1
DwfDigitalOutIdleHigh = 2
DwfDigitalOutIdleZet = 3

# Macro used to verify if bit is 1 or 0 in given bit field
#define IsBitSet(fs, bit) ((fs & (1<<bit)) != 0)
def IsBitSet(fs, bit):
    return ((fs & (1<<bit)) != 0)

class DWFError(RuntimeError):
    def __init__(self, error, errormsg, others=None):
        self.error = error
        self.errormsg = errormsg
        self.others = others
    def __str__(self):
        return "ERROR(%d): %s" % (
            self.error, self.errormsg)
def _mkstring(buf):
    if sys.version_info[0] >= 3:
        return bytes(buf.value).decode('latin-1')
    return str(buf.value)

_ARGIN = 1
_ARGOUT = 2
_ARGIN_WITH_ZERO = 4
def _errcheck(result, func, args):
    if not result:
        err = DWFERC()
        errmsg = create_string_buffer(512)
        dwfdll.FDwfGetLastError(byref(err))
        dwfdll.FDwfGetLastErrorMsg(errmsg)
        raise DWFError(err.value, _mkstring(errmsg), (func, args))
    return args

def _define(funcname, protos, params, prefix=""):
    prototype = CFUNCTYPE(BOOL, *protos)
    func = prototype((funcname, dwfdll), params)
    func.errcheck = _errcheck
    globals()[prefix + funcname] = func

def _xdefine(funcname, protos, params):
    _define(funcname, protos, params, prefix="_")

# Error and version APIs:
#  FDwfGetLastError(DWFERC *pdwferc);
_define("FDwfGetLastError",
        (POINTER(DWFERC),), ((_ARGOUT, "pdwferc"),))
#  FDwfGetLastErrorMsg(char szError[512]);
_xdefine("FDwfGetLastErrorMsg",
        (c_char_p,), ((_ARGIN, "szError"),))
def FDwfGetLastErrorMsg(szError=None):
    if szError is not None: return _FDwfGetLastErrorMsg(szError)
    szError = create_string_buffer(512)
    _FDwfGetLastErrorMsg(szError)
    return _mkstring(szError)
#  FDwfGetVersion(char szVersion[32]);
# Returns DLL version, for instance: "2.4.3"
_xdefine("FDwfGetVersion",
         (c_char_p,), ((_ARGIN, "szVersion"),))
def FDwfGetVersion(szVersion=None):
    if szVersion is not None: return _FDwfGetVersion(szVersion)
    szVersion = create_string_buffer(32)
    _FDwfGetVersion(szVersion)
    return _mkstring(szVersion)

# DEVICE MANAGMENT FUNCTIONS
# Enumeration:
#  FDwfEnum(ENUMFILTER enumfilter, int *pcDevice);
_define("FDwfEnum",
        (ENUMFILTER, POINTER(c_int),),
        ((_ARGIN, "enumfilter", enumfilterAll), (_ARGOUT, "pcDevice"),))
#  FDwfEnumDeviceType(int idxDevice, DEVID *pDeviceId, DEVVER *pDeviceRevision);
_define("FDwfEnumDeviceType",
        (c_int, POINTER(DEVID), POINTER(DEVVER),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "pDeviceId"),
         (_ARGOUT, "pDeviceRevision"),))
#  FDwfEnumDeviceIsOpened(int idxDevice, BOOL *pfIsUsed);
_define("FDwfEnumDeviceIsOpened",
        (c_int, POINTER(BOOL),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "pfIsUsed"),))
#  FDwfEnumUserName(int idxDevice, char szUserName[32]);
_xdefine("FDwfEnumUserName",
         (c_int, c_char_p,), ((_ARGIN, "idxDevice"), (_ARGIN, "szUserName"),))
def FDwfEnumUserName(idxDevice, szUserName=None):
    if szUserName is not None: return _FDwfEnumUserName(idxDevice, szUserName)
    szUserName = create_string_buffer(32)
    _FDwfEnumUserName(idxDevice, szUserName)
    return _mkstring(szUserName)
#  FDwfEnumDeviceName(int idxDevice, char szDeviceName[32]);
_xdefine("FDwfEnumDeviceName",
        (c_int, c_char_p,), ((_ARGIN, "idxDevice"), (_ARGIN, "szDeviceName"),))
def FDwfEnumDeviceName(idxDevice, szDeviceName=None):
    if szDeviceName is not None:
        return _FDwfEnumDeviceName(idxDevice, szDeviceName)
    szDeviceName = create_string_buffer(32)
    _FDwfEnumDeviceName(idxDevice, szDeviceName)
    return _mkstring(szDeviceName)
#  FDwfEnumSN(int idxDevice, char szSN[32]);
_xdefine("FDwfEnumSN",
         (c_int, c_char_p,), ((_ARGIN, "idxDevice"), (_ARGIN, "szSN"),))
def FDwfEnumSN(idxDevice, szSN=None):
    if szSN is not None: return _FDwfEnumSN(idxDevice, szSN)
    szSN = create_string_buffer(32)
    _FDwfEnumSN(idxDevice, szSN)
    return _mkstring(szSN)
#  FDwfEnumConfig(int idxDevice, int *pcConfig);
_define("FDwfEnumConfig",
        (c_int, POINTER(c_int),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "pcConfig"),))
#  FDwfEnumConfigInfo(int idxConfig, DwfEnumConfigInfo info, int *pv);
_define("FDwfEnumConfigInfo",
        (c_int, DwfEnumConfigInfo, POINTER(c_int),),
        ((_ARGIN, "idxConfig"), (_ARGIN, "info"), (_ARGOUT, "pv"),))

# Open/Close:
#  FDwfDeviceOpen(int idxDevice, HDWF *phdwf);
_define("FDwfDeviceOpen",
        (c_int, POINTER(HDWF),),
        ((_ARGIN, "idxDevice", -1), (_ARGOUT, "phdwf"),))
#  FDwfDeviceConfigOpen(int idxDev, int idxCfg, HDWF *phdwf);
_define("FDwfDeviceConfigOpen",
        (c_int, c_int, POINTER(HDWF),),
        ((_ARGIN, "idxDev"), (_ARGIN, "idxCfg"), (_ARGOUT, "phdwf"),))
#  FDwfDeviceClose(HDWF hdwf);
_define("FDwfDeviceClose",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfDeviceCloseAll();
_define("FDwfDeviceCloseAll", (), ())
#  FDwfDeviceAutoConfigureSet(HDWF hdwf, BOOL fAutoConfigure);
_define("FDwfDeviceAutoConfigureSet",
        (HDWF, BOOL,), ((_ARGIN, "hdwf"), (_ARGIN, "fAutoConfigure"),))
#  FDwfDeviceAutoConfigureGet(HDWF hdwf, BOOL *pfAutoConfigure);
_define("FDwfDeviceAutoConfigureGet",
        (HDWF, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfAutoConfigure"),))
#  FDwfDeviceReset(HDWF hdwf);
_define("FDwfDeviceReset",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfDeviceEnableSet(HDWF hdwf, BOOL fEnable);
_define("FDwfDeviceEnableSet",
        (HDWF, BOOL,), ((_ARGIN, "hdwf"), (_ARGIN, "fEnable"),))
#  FDwfDeviceTriggerInfo(HDWF hdwf, int *pfstrigsrc);
# use IsBitSet
_define("FDwfDeviceTriggerInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfstrigsrc"),))
#  FDwfDeviceTriggerSet(HDWF hdwf, int idxPin, TRIGSRC trigsrc);
_define("FDwfDeviceTriggerSet",
        (HDWF, c_int, TRIGSRC,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxPin"), (_ARGIN, "trigsrc"),))
#  FDwfDeviceTriggerGet(HDWF hdwf, int idxPin, TRIGSRC *ptrigsrc);
_define("FDwfDeviceTriggerGet",
        (HDWF, c_int, POINTER(TRIGSRC),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxPin"), (_ARGOUT, "ptrigsrc"),))
#  FDwfDeviceTriggerPC(HDWF hdwf);
_define("FDwfDeviceTriggerPC",
        (HDWF,), ((_ARGIN, "hdwf"),))


# ANALOG IN INSTRUMENT FUNCTIONS
# Control and status: 
#  FDwfAnalogInReset(HDWF hdwf);
_define("FDwfAnalogInReset",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfAnalogInConfigure(HDWF hdwf, BOOL fReconfigure, BOOL fStart);
_define("FDwfAnalogInConfigure",
        (HDWF, BOOL, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "fReconfigure"), (_ARGIN, "fStart"),))
#  FDwfAnalogInStatus(HDWF hdwf, BOOL fReadData, DwfState *psts);
_define("FDwfAnalogInStatus",
        (HDWF, BOOL, POINTER(DwfState),),
        ((_ARGIN, "hdwf"), (_ARGIN, "fReadData"), (_ARGOUT, "psts"),))
#  FDwfAnalogInStatusSamplesLeft(HDWF hdwf, int *pcSamplesLeft);
_define("FDwfAnalogInStatusSamplesLeft",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcSamplesLeft"),))
#  FDwfAnalogInStatusSamplesValid(HDWF hdwf, int *pcSamplesValid);
_define("FDwfAnalogInStatusSamplesValid",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcSamplesValid"),))
#  FDwfAnalogInStatusIndexWrite(HDWF hdwf, int *pidxWrite);
_define("FDwfAnalogInStatusIndexWrite",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pidxWrite"),))
#  FDwfAnalogInStatusAutoTriggered(HDWF hdwf, BOOL *pfAuto);
_define("FDwfAnalogInStatusAutoTriggered",
        (HDWF, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfAuto"), ))
#  FDwfAnalogInStatusData(HDWF hdwf, int idxChannel, double *rgdVoltData, int cdData);
_xdefine("FDwfAnalogInStatusData",
         (HDWF, c_int, POINTER(c_double), c_int,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
          (_ARGIN, "rgdVoltData"), (_ARGIN, "cdData"),))
def FDwfAnalogInStatusData(hdwf, idxChannel,
                           rgdVoltData_or_cdData, cdData=None):
    if cdData is not None:
        return _FDwfAnalogInStatusData(hdwf, idxChannel,
                                       rgdVoltData_or_cdData, cdData)
    cdData = int(rgdVoltData_or_cdData)
    rgdVoltData = (c_double * cdData)()
    _FDwfAnalogInStatusData(hdwf, idxChannel, rgdVoltData, cdData)
    return tuple(rgdVoltData)
#  FDwfAnalogInStatusNoise(HDWF hdwf, int idxChannel, double *rgdMin, double *rgdMax, int cdData);
_xdefine("FDwfAnalogInStatusNoise",
         (HDWF, c_int, POINTER(c_double), POINTER(c_double), c_int,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
          (_ARGIN, "rgdMin"), (_ARGIN, "rgdMax"), (_ARGIN, "cdData"),))
def FDwfAnalogInStatusNoise(hdwf, dxChannel,
                            rgdMin_or_cdData, rgdMax=None, cdData=None):
    if rgdMax is not None and cdData is not None:
        return _FDwfAnalogInStatusNoise(
            hdwf, dxChannel, rgdMin_or_cdData, rgdMax, cdData)
    cdData = rgdMin_or_cdData
    rgdMin = (c_double * cdData)()
    rgdMax = (c_double * cdData)()
    _FDwfAnalogInStatusNoise(hdwf, dxChannel, rgdMin, rgdMax, cdData)
    return tuple(rgdMin), tuple(rgdMax)

#  FDwfAnalogInStatusSample(HDWF hdwf, int idxChannel, double *pdVoltSample);
_define("FDwfAnalogInStatusSample",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pdVoltSample"),))
#  FDwfAnalogInStatusRecord(HDWF hdwf, int *pcdDataAvailable, int *pcdDataLost, int *pcdDataCorrupt);
_define("FDwfAnalogInStatusRecord",
        (HDWF, POINTER(c_int), POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcdDataAvailable"),
         (_ARGOUT, "pcdDataLost"), (_ARGOUT, "pcdDataCorrupt"),))
#  FDwfAnalogInRecordLengthSet(HDWF hdwf, double sLegth);
_define("FDwfAnalogInRecordLengthSet",
        (HDWF, c_double,), ((_ARGIN, "hdwf"), (_ARGIN, "sLength"),))
#  FDwfAnalogInRecordLengthGet(HDWF hdwf, double *psLegth);
_define("FDwfAnalogInRecordLengthGet",
        (HDWF, POINTER(c_double),), ((_ARGIN, "hdwf"), (_ARGOUT, "psLength"),))

# Acquisition configuration:
#  FDwfAnalogInFrequencyInfo(HDWF hdwf, double *phzMin, double *phzMax);
_define("FDwfAnalogInFrequencyInfo",
        (HDWF, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "phzMin"), (_ARGOUT, "phzMax"),))
#  FDwfAnalogInFrequencySet(HDWF hdwf, double hzFrequency);
_define("FDwfAnalogInFrequencySet",
        (HDWF, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "hzFrequency"),))
#  FDwfAnalogInFrequencyGet(HDWF hdwf, double *phzFrequency);
_define("FDwfAnalogInFrequencyGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "phzFrequency"),))
#  FDwfAnalogInBitsInfo(HDWF hdwf, int *pnBits);
# Returns the number of ADC bits 
_define("FDwfAnalogInBitsInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnBits"),))

#  FDwfAnalogInBufferSizeInfo(HDWF hdwf, int *pnSizeMin, int *pnSizeMax);
_define("FDwfAnalogInBufferSizeInfo",
        (HDWF, POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pnSizeMin"), (_ARGOUT, "pnSizeMax"),))
#  FDwfAnalogInBufferSizeSet(HDWF hdwf, int nSize);
_define("FDwfAnalogInBufferSizeSet",
        (HDWF, c_int,), ((_ARGIN, "hdwf"), (_ARGIN, "nSize"),))
#  FDwfAnalogInBufferSizeGet(HDWF hdwf, int *pnSize);
_define("FDwfAnalogInBufferSizeGet",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnSize"),))

#  FDwfAnalogInNoiseSizeInfo(HDWF hdwf, int *pnSizeMax);
_define("FDwfAnalogInNoiseSizeInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnSizeMax"),))
#  FDwfAnalogInNoiseSizeGet(HDWF hdwf, int *pnSize);
_define("FDwfAnalogInNoiseSizeGet",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnSize"),))

#  FDwfAnalogInAcquisitionModeInfo(HDWF hdwf, int *pfsacqmode);
# use IsBitSet
_define("FDwfAnalogInAcquisitionModeInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsacqmode"),))
#  FDwfAnalogInAcquisitionModeSet(HDWF hdwf, ACQMODE acqmode);
_define("FDwfAnalogInAcquisitionModeSet",
        (HDWF, ACQMODE,), ((_ARGIN, "hdwf"), (_ARGIN, "acqmode"),))
#  FDwfAnalogInAcquisitionModeGet(HDWF hdwf, ACQMODE *pacqmode);
_define("FDwfAnalogInAcquisitionModeGet",
        (HDWF, POINTER(ACQMODE),), ((_ARGIN, "hdwf"), (_ARGOUT, "pacqmode"),))

# Channel configuration:
#  FDwfAnalogInChannelCount(HDWF hdwf, int *pcChannel);
_define("FDwfAnalogInChannelCount",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pcChannel"),))
#  FDwfAnalogInChannelEnableSet(HDWF hdwf, int idxChannel, BOOL fEnable);
_define("FDwfAnalogInChannelEnableSet",
        (HDWF, c_int, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "fEnable"),))
#  FDwfAnalogInChannelEnableGet(HDWF hdwf, int idxChannel, BOOL *pfEnable);
_define("FDwfAnalogInChannelEnableGet",
        (HDWF, c_int, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfEnable"),))
#  FDwfAnalogInChannelFilterInfo(HDWF hdwf, int *pfsfilter);
# use IsBitSet
_define("FDwfAnalogInChannelFilterInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsfilter"),))
#  FDwfAnalogInChannelFilterSet(HDWF hdwf, int idxChannel, FILTER filter);
_define("FDwfAnalogInChannelFilterSet",
        (HDWF, c_int, FILTER,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "filter"),))
#  FDwfAnalogInChannelFilterGet(HDWF hdwf, int idxChannel, FILTER *pfilter);
_define("FDwfAnalogInChannelFilterGet",
        (HDWF, c_int, POINTER(FILTER),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfilter"),))
#  FDwfAnalogInChannelRangeInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
_define("FDwfAnalogInChannelRangeInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pvoltsMin"), (_ARGOUT, "pvoltsMax"),
         (_ARGOUT, "pnSteps"), ))
#  FDwfAnalogInChannelRangeSteps(HDWF hdwf, double rgVoltsStep[32], int *pnSteps);
_xdefine("FDwfAnalogInChannelRangeSteps",
         (HDWF, POINTER(c_double), POINTER(c_int),),
         ((_ARGIN, "hdwf"), (_ARGIN, "rgVoltsStep"), (_ARGOUT, "pnSteps"),))
def FDwfAnalogInChannelRangeSteps(hdwf, rgVoltsStep=None, pnSteps=None):
    if rgVoltsStep is not None and pnSteps is not None:
        return _FDwfAnalogInChannelRangeSteps(hdwf, rgVoltsStep, pnSteps)
    rgVoltsSteps = (c_double * 32)()
    pnSteps = c_int()
    _FDwfAnalogInChannelRangeSteps(hdwf, rgVoltsStep, byref(pnSteps))
    return tuple([ rgVoltSteps[i] for i in range(pnSteps.value) ])
#  FDwfAnalogInChannelRangeSet(HDWF hdwf, int idxChannel, double voltsRange);
_define("FDwfAnalogInChannelRangeSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "voltsRange"),))
#  FDwfAnalogInChannelRangeGet(HDWF hdwf, int idxChannel, double *pvoltsRange);
_define("FDwfAnalogInChannelRangeGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pvoltsRange"),))
#  FDwfAnalogInChannelOffsetInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
_define("FDwfAnalogInChannelOffsetInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pvoltsMin"), (_ARGOUT, "pvoltsMax"),
         (_ARGOUT, "pnSteps"),))
#  FDwfAnalogInChannelOffsetSet(HDWF hdwf, int idxChannel, double voltOffset);
_define("FDwfAnalogInChannelOffsetSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "voltOffset"),))
#  FDwfAnalogInChannelOffsetGet(HDWF hdwf, int idxChannel, double *pvoltOffset);
_define("FDwfAnalogInChannelOffsetGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pvoltOffset"),))
#  FDwfAnalogInChannelAttenuationSet(HDWF hdwf, int idxChannel, double xAttenuation);
_define("FDwfAnalogInChannelAttenuationSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "xAttenuation"),))
#  FDwfAnalogInChannelAttenuationGet(HDWF hdwf, int idxChannel, double *pxAttenuation);
_define("FDwfAnalogInChannelAttenuationGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pxAttenuation"),))


# Trigger configuration:
#  FDwfAnalogInTriggerSourceInfo(HDWF hdwf, int *pfstrigsrc);
# use IsBitSet
_define("FDwfAnalogInTriggerSourceInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfstrigsrc"),))
#  FDwfAnalogInTriggerSourceSet(HDWF hdwf, TRIGSRC trigsrc);
_define("FDwfAnalogInTriggerSourceSet",
        (HDWF, TRIGSRC,), ((_ARGIN, "hdwf"), (_ARGIN, "trigsrc"),))
#  FDwfAnalogInTriggerSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
_define("FDwfAnalogInTriggerSourceGet",
        (HDWF, POINTER(TRIGSRC),), ((_ARGIN, "hdwf"), (_ARGOUT, "ptrigsrc"),))

#  FDwfAnalogInTriggerPositionInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
_define("FDwfAnalogInTriggerPositionInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"),
         (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"), (_ARGOUT, "pnSteps"),))
#  FDwfAnalogInTriggerPositionSet(HDWF hdwf, double secPosition);
_define("FDwfAnalogInTriggerPositionSet",
        (HDWF, c_double,), ((_ARGIN, "hdwf"), (_ARGIN, "secPosition"),))
#  FDwfAnalogInTriggerPositionGet(HDWF hdwf, double *psecPosition);
_define("FDwfAnalogInTriggerPositionGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecPosition"),))
#  FDwfAnalogInTriggerPositionStatus(HDWF hdwf, double *psecPosition);
_define("FDwfAnalogInTriggerPositionStatus",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecPosition"),))

#  FDwfAnalogInTriggerAutoTimeoutInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
_define("FDwfAnalogInTriggerAutoTimeoutInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"),
         (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"), (_ARGOUT, "pnSteps"),))
#  FDwfAnalogInTriggerAutoTimeoutSet(HDWF hdwf, double secTimeout);
_define("FDwfAnalogInTriggerAutoTimeoutSet",
        (HDWF, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "secTimeout"),))
#  FDwfAnalogInTriggerAutoTimeoutGet(HDWF hdwf, double *psecTimeout);
_define("FDwfAnalogInTriggerAutoTimeoutGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecTimeout"),))

#  FDwfAnalogInTriggerHoldOffInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnStep);
_define("FDwfAnalogInTriggerHoldOffInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"),
         (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"), (_ARGOUT, "pnStep"),))
#  FDwfAnalogInTriggerHoldOffSet(HDWF hdwf, double secHoldOff);
_define("FDwfAnalogInTriggerHoldOffSet",
        (HDWF, c_double,), ((_ARGIN, "hdwf"), (_ARGIN, "secHoldOff"),))
#  FDwfAnalogInTriggerHoldOffGet(HDWF hdwf, double *psecHoldOff);
_define("FDwfAnalogInTriggerHoldOffGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecHoldOff"),))

#  FDwfAnalogInTriggerTypeInfo(HDWF hdwf, int *pfstrigtype);
# use IsBitSet
_define("FDwfAnalogInTriggerTypeInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfstrigtype"),))
#  FDwfAnalogInTriggerTypeSet(HDWF hdwf, TRIGTYPE trigtype);
_define("FDwfAnalogInTriggerTypeSet",
        (HDWF, TRIGTYPE,),
        ((_ARGIN, "hdwf"), (_ARGIN, "trigtype"),))
#  FDwfAnalogInTriggerTypeGet(HDWF hdwf, TRIGTYPE *ptrigtype);
_define("FDwfAnalogInTriggerTypeGet",
        (HDWF, POINTER(TRIGTYPE),), ((_ARGIN, "hdwf"), (_ARGOUT, "ptrigtype"),))

#  FDwfAnalogInTriggerChannelInfo(HDWF hdwf, int *pidxMin, int *pidxMax);
_define("FDwfAnalogInTriggerChannelInfo",
        (HDWF, POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pidxMin"), (_ARGOUT, "pidxMax"),))
#  FDwfAnalogInTriggerChannelSet(HDWF hdwf, int idxChannel);
_define("FDwfAnalogInTriggerChannelSet",
        (HDWF, c_int,), ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),))
#  FDwfAnalogInTriggerChannelGet(HDWF hdwf, int *pidxChannel);
_define("FDwfAnalogInTriggerChannelGet",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pidxChannel"),))

#  FDwfAnalogInTriggerFilterInfo(HDWF hdwf, int *pfsfilter);
# use IsBitSet
_define("FDwfAnalogInTriggerFilterInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsfilter"),))
#  FDwfAnalogInTriggerFilterSet(HDWF hdwf, FILTER filter);
_define("FDwfAnalogInTriggerFilterSet",
        (HDWF, FILTER,), ((_ARGIN, "hdwf"), (_ARGIN, "filter"),))
#  FDwfAnalogInTriggerFilterGet(HDWF hdwf, FILTER *pfilter);
_define("FDwfAnalogInTriggerFilterGet",
        (HDWF, POINTER(FILTER),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfilter"),))

#  FDwfAnalogInTriggerLevelInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
_define("FDwfAnalogInTriggerLevelInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"),
         (_ARGOUT, "pvoltsMin"), (_ARGOUT, "pvoltsMax"), (_ARGOUT, "pnSteps"),))
#  FDwfAnalogInTriggerLevelSet(HDWF hdwf, double voltsLevel);
_define("FDwfAnalogInTriggerLevelSet",
        (HDWF, c_double,), ((_ARGIN, "hdwf"), (_ARGIN, "voltsLevel"),))
#  FDwfAnalogInTriggerLevelGet(HDWF hdwf, double *pvoltsLevel);
_define("FDwfAnalogInTriggerLevelGet",
        (HDWF, POINTER(c_double),), ((_ARGIN, "hdwf"), (_ARGOUT, "pvoltsLevel"),))

#  FDwfAnalogInTriggerHysteresisInfo(HDWF hdwf, double *pvoltsMin, double *pvoltsMax, double *pnSteps);
_define("FDwfAnalogInTriggerHysteresisInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pvoltsMin"),
         (_ARGOUT, "pvoltsMax"), (_ARGOUT, "pnSteps"), ))
#  FDwfAnalogInTriggerHysteresisSet(HDWF hdwf, double voltsLevel);
_define("FDwfAnalogInTriggerHysteresisSet",
        (HDWF, c_double,), ((_ARGIN, "hdwf"), (_ARGIN, "voltsLevel"),))
#  FDwfAnalogInTriggerHysteresisGet(HDWF hdwf, double *pvoltsHysteresis);
_define("FDwfAnalogInTriggerHysteresisGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pvoltsHysteresis"),))

#  FDwfAnalogInTriggerConditionInfo(HDWF hdwf, int *pfstrigcond);
# use IsBitSet
_define("FDwfAnalogInTriggerConditionInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfstrigcond"),))
#  FDwfAnalogInTriggerConditionSet(HDWF hdwf, TRIGCOND trigcond);
_define("FDwfAnalogInTriggerConditionSet",
        (HDWF, TRIGCOND,), ((_ARGIN, "hdwf"), (_ARGIN, "trigcond"),))
#  FDwfAnalogInTriggerConditionGet(HDWF hdwf, TRIGCOND *ptrigcond);
_define("FDwfAnalogInTriggerConditionGet",
        (HDWF, POINTER(TRIGCOND),), ((_ARGIN, "hdwf"), (_ARGOUT, "ptrigcond"),))

#  FDwfAnalogInTriggerLengthInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
_define("FDwfAnalogInTriggerLengthInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecMin"),
         (_ARGOUT, "psecMax"), (_ARGOUT, "pnSteps"),))
#  FDwfAnalogInTriggerLengthSet(HDWF hdwf, double secLength);
_define("FDwfAnalogInTriggerLengthSet",
        (HDWF, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "secLength"),))
#  FDwfAnalogInTriggerLengthGet(HDWF hdwf, double *psecLength);
_define("FDwfAnalogInTriggerLengthGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecLength"),))

#  FDwfAnalogInTriggerLengthConditionInfo(HDWF hdwf, int *pfstriglen);
# use IsBitSet
_define("FDwfAnalogInTriggerLengthConditionInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfstriglen"),))
#  FDwfAnalogInTriggerLengthConditionSet(HDWF hdwf, TRIGLEN triglen);
_define("FDwfAnalogInTriggerLengthConditionSet",
        (HDWF, TRIGLEN,), ((_ARGIN, "hdwf"), (_ARGIN, "triglen"),))
#  FDwfAnalogInTriggerLengthConditionGet(HDWF hdwf, TRIGLEN *ptriglen);
_define("FDwfAnalogInTriggerLengthConditionGet",
        (HDWF, POINTER(TRIGLEN),), ((_ARGIN, "hdwf"), (_ARGOUT, "ptriglen"),))


# ANALOG OUT INSTRUMENT FUNCTIONS
# Configuration:
#  FDwfAnalogOutCount(HDWF hdwf, int *pcChannel);
_define("FDwfAnalogOutCount",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pcChannel"),))

#  FDwfAnalogOutMasterSet(HDWF hdwf, int idxChannel, int idxMaster);
_define("FDwfAnalogOutMasterSet",
        (HDWF, c_int, c_int,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxMaster"),))
#  FDwfAnalogOutMasterGet(HDWF hdwf, int idxChannel, int *pidxMaster);
_define("FDwfAnalogOutMasterGet",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pidxMaster"),))

#  FDwfAnalogOutTriggerSourceInfo(HDWF hdwf, int idxChannel, int *pfstrigsrc);
# use IsBitSet
_define("FDwfAnalogOutTriggerSourceInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfstrigsrc"),))
#  FDwfAnalogOutTriggerSourceSet(HDWF hdwf, int idxChannel, TRIGSRC trigsrc);
_define("FDwfAnalogOutTriggerSourceSet",
        (HDWF, c_int, TRIGSRC,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "trigsrc"),))
#  FDwfAnalogOutTriggerSourceGet(HDWF hdwf, int idxChannel, TRIGSRC *ptrigsrc);
_define("FDwfAnalogOutTriggerSourceGet",
        (HDWF, c_int, POINTER(TRIGSRC),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "ptrigsrc"),))

#  FDwfAnalogOutRunInfo(HDWF hdwf, int idxChannel, double *psecMin, double *psecMax);
_define("FDwfAnalogOutRunInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"),))
#  FDwfAnalogOutRunSet(HDWF hdwf, int idxChannel, double secRun);
_define("FDwfAnalogOutRunSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "secRun"),))
#  FDwfAnalogOutRunGet(HDWF hdwf, int idxChannel, double *psecRun);
_define("FDwfAnalogOutRunGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "psecRun"),))
#  FDwfAnalogOutRunStatus(HDWF hdwf, int idxChannel, double *psecRun);
_define("FDwfAnalogOutRunStatus",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "psecRun"),))

#  FDwfAnalogOutWaitInfo(HDWF hdwf, int idxChannel, double *psecMin, double *psecMax);
_define("FDwfAnalogOutWaitInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"), ))
#  FDwfAnalogOutWaitSet(HDWF hdwf, int idxChannel, double secWait);
_define("FDwfAnalogOutWaitSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "secWait"),))
#  FDwfAnalogOutWaitGet(HDWF hdwf, int idxChannel, double *psecWait);
_define("FDwfAnalogOutWaitGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "psecWait"),))

#  FDwfAnalogOutRepeatInfo(HDWF hdwf, int idxChannel, int *pnMin, int *pnMax);
_define("FDwfAnalogOutRepeatInfo",
        (HDWF, c_int, POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pnMin"), (_ARGOUT, "pnMax"),))
#  FDwfAnalogOutRepeatSet(HDWF hdwf, int idxChannel, int cRepeat);
_define("FDwfAnalogOutRepeatSet",
        (HDWF, c_int, c_int,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "cRepeat"),))
#  FDwfAnalogOutRepeatGet(HDWF hdwf, int idxChannel, int *pcRepeat);
_define("FDwfAnalogOutRepeatGet",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pcRepeat"),))
#  FDwfAnalogOutRepeatStatus(HDWF hdwf, int idxChannel, int *pcRepeat);
_define("FDwfAnalogOutRepeatStatus",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pcRepeat"),))

#  FDwfAnalogOutRepeatTriggerSet(HDWF hdwf, int idxChannel, BOOL fRepeatTrigger);
_define("FDwfAnalogOutRepeatTriggerSet",
        (HDWF, c_int, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "fRepeatTrigger"),))
#  FDwfAnalogOutRepeatTriggerGet(HDWF hdwf, int idxChannel, BOOL *pfRepeatTrigger);
_define("FDwfAnalogOutRepeatTriggerGet",
        (HDWF, c_int, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pfRepeatTrigger"),))

# EExplorer channel 3&4 current/voltage limitation
#  FDwfAnalogOutLimitationInfo(HDWF hdwf, int idxChannel, double *pMin, double *pMax);
_define("FDwfAnalogOutLimitationInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pMin"), (_ARGOUT, "pMax"),))
#  FDwfAnalogOutLimitationSet(HDWF hdwf, int idxChannel, double limit);
_define("FDwfAnalogOutLimitationSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "limit"),))
#  FDwfAnalogOutLimitationGet(HDWF hdwf, int idxChannel, double *plimit);
_define("FDwfAnalogOutLimitationGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "plimit"),))

#  FDwfAnalogOutModeSet(HDWF hdwf, int idxChannel, DwfAnalogOutMode mode);
_define("FDwfAnalogOutModeSet",
        (HDWF, c_int, DwfAnalogOutMode,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "mode"),))
#  FDwfAnalogOutModeGet(HDWF hdwf, int idxChannel, DwfAnalogOutMode *pmode);
_define("FDwfAnalogOutModeGet",
        (HDWF, c_int, POINTER(DwfAnalogOutMode),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pmode"),))

#  FDwfAnalogOutIdleInfo(HDWF hdwf, int idxChannel, int *pfsidle);
# use IsBitSet
_define("FDwfAnalogOutIdleInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfsidle"),))
#  FDwfAnalogOutIdleSet(HDWF hdwf, int idxChannel, DwfAnalogOutIdle idle);
_define("FDwfAnalogOutIdleSet",
        (HDWF, c_int, DwfAnalogOutIdle,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idle"),))
#  FDwfAnalogOutIdleGet(HDWF hdwf, int idxChannel, DwfAnalogOutIdle *pidle);
_define("FDwfAnalogOutIdleGet",
        (HDWF, c_int, POINTER(DwfAnalogOutIdle),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pidle"),))

#  FDwfAnalogOutNodeInfo(HDWF hdwf, int idxChannel, int *pfsnode);
# use IsBitSet
_define("FDwfAnalogOutNodeInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfsnode"),))

#  FDwfAnalogOutNodeEnableSet(HDWF hdwf, int idxChannel, AnalogOutNode node, BOOL fEnable);
_define("FDwfAnalogOutNodeEnableSet",
        (HDWF, c_int, AnalogOutNode, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "node"), (_ARGIN, "fEnable"),))
#  FDwfAnalogOutNodeEnableGet(HDWF hdwf, int idxChannel, AnalogOutNode node, BOOL *pfEnable);
_define("FDwfAnalogOutNodeEnableGet",
        (HDWF, c_int, AnalogOutNode, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pfEnable"), ))

#  FDwfAnalogOutNodeFunctionInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, int *pfsfunc);
# use IsBitSet
_define("FDwfAnalogOutNodeFunctionInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pfsfunc"),))
#  FDwfAnalogOutNodeFunctionSet(HDWF hdwf, int idxChannel, AnalogOutNode node, FUNC func);
_define("FDwfAnalogOutNodeFunctionSet",
        (HDWF, c_int, AnalogOutNode, FUNC,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "node"), (_ARGIN, "func"),))
#  FDwfAnalogOutNodeFunctionGet(HDWF hdwf, int idxChannel, AnalogOutNode node, FUNC *pfunc);
_define("FDwfAnalogOutNodeFunctionGet",
        (HDWF, c_int, AnalogOutNode, POINTER(FUNC),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pfunc"), ))

#  FDwfAnalogOutNodeFrequencyInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *phzMin, double *phzMax);
_define("FDwfAnalogOutNodeFrequencyInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "phzMin"), (_ARGOUT, "phzMax"),))
#  FDwfAnalogOutNodeFrequencySet(HDWF hdwf, int idxChannel, AnalogOutNode node, double hzFrequency);
_define("FDwfAnalogOutNodeFrequencySet",
        (HDWF, c_int, AnalogOutNode, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "node"), (_ARGIN, "hzFrequency"),))
#  FDwfAnalogOutNodeFrequencyGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *phzFrequency);
_define("FDwfAnalogOutNodeFrequencyGet",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "phzFrequency"),))
# Carrier Amplitude or Modulation Index 
#  FDwfAnalogOutNodeAmplitudeInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pMin, double *pMax);
_define("FDwfAnalogOutNodeAmplitudeInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pMin"), (_ARGOUT, "pMax"), ))
#  FDwfAnalogOutNodeAmplitudeSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double vAmplitude);
_define("FDwfAnalogOutNodeAmplitudeSet",
        (HDWF, c_int, AnalogOutNode, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "node"), (_ARGIN, "vAmplitude"),))
#  FDwfAnalogOutNodeAmplitudeGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pvAmplitude);
_define("FDwfAnalogOutNodeAmplitudeGet",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pvAmplitude"),))

#  FDwfAnalogOutNodeOffsetInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pMin, double *pMax);
_define("FDwfAnalogOutNodeOffsetInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pMin"), (_ARGOUT, "pMax"),))
#  FDwfAnalogOutNodeOffsetSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double vOffset);
_define("FDwfAnalogOutNodeOffsetSet",
        (HDWF, c_int, AnalogOutNode, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "node"), (_ARGIN, "vOffset"),))
#  FDwfAnalogOutNodeOffsetGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pvOffset);
_define("FDwfAnalogOutNodeOffsetGet",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pvOffset"),))

#  FDwfAnalogOutNodeSymmetryInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *ppercentageMin, double *ppercentageMax);
_define("FDwfAnalogOutNodeSymmetryInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "ppercentageMin"), (_ARGOUT, "ppercentageMax"), ))
#  FDwfAnalogOutNodeSymmetrySet(HDWF hdwf, int idxChannel, AnalogOutNode node, double percentageSymmetry);
_define("FDwfAnalogOutNodeSymmetrySet",
        (HDWF, c_int, AnalogOutNode, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGIN, "percentageSymmetry"),))
#  FDwfAnalogOutNodeSymmetryGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *ppercentageSymmetry);
_define("FDwfAnalogOutNodeSymmetryGet",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "ppercentageSymmetry"),))

#  FDwfAnalogOutNodePhaseInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pdegreeMin, double *pdegreeMax);
_define("FDwfAnalogOutNodePhaseInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pdegreeMin"), (_ARGOUT, "pdegreeMax"), ))
#  FDwfAnalogOutNodePhaseSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double degreePhase);
_define("FDwfAnalogOutNodePhaseSet",
        (HDWF, c_int, AnalogOutNode, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "node"), (_ARGIN, "degreePhase"),))
#  FDwfAnalogOutNodePhaseGet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *pdegreePhase);
_define("FDwfAnalogOutNodePhaseGet",
        (HDWF, c_int, AnalogOutNode, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pdegreePhase"), ))

#  FDwfAnalogOutNodeDataInfo(HDWF hdwf, int idxChannel, AnalogOutNode node, int *pnSamplesMin, int *pnSamplesMax);
_define("FDwfAnalogOutNodeDataInfo",
        (HDWF, c_int, AnalogOutNode, POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "pnSamplesMin"), (_ARGOUT, "pnSamplesMax"), ))
#  FDwfAnalogOutNodeDataSet(HDWF hdwf, int idxChannel, AnalogOutNode node, double *rgdData, int cdData);
_xdefine("FDwfAnalogOutNodeDataSet",
         (HDWF, c_int, AnalogOutNode, POINTER(c_double), c_int,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
          (_ARGIN, "rgdData"), (_ARGIN, "cdData"), ))
def FDwfAnalogOutNodeDataSet(hdwf, idxChannel, node, rgdData, cdData=None):
    if cdData is not None:
        return _FDwfAnalogOutNodeDataSet(
            hdwf, idxChannel, node, rgdData, cdData)
    cdData = len(rgdData)
    rgdData_ = (c_double * cdData)()
    for i, v in enumerate(rgdData): rgdData_[i] = rgdData[i]
    return _FDwfAnalogOutNodeDataSet(hdwf, idxChannel, node, rgdData_, cdData)

# needed for EExplorer, don't care for ADiscovery
#  FDwfAnalogOutCustomAMFMEnableSet(HDWF hdwf, int idxChannel, BOOL fEnable);
_define("FDwfAnalogOutCustomAMFMEnableSet",
        (HDWF, c_int, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "fEnable"),))
#  FDwfAnalogOutCustomAMFMEnableGet(HDWF hdwf, int idxChannel, BOOL *pfEnable);
_define("FDwfAnalogOutCustomAMFMEnableGet",
        (HDWF, c_int, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfEnable"),))

# Control:
#  FDwfAnalogOutReset(HDWF hdwf, int idxChannel);
_define("FDwfAnalogOutReset",
        (HDWF, c_int,), ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),))
#  FDwfAnalogOutConfigure(HDWF hdwf, int idxChannel, BOOL fStart);
_define("FDwfAnalogOutConfigure",
        (HDWF, c_int, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "fStart"),))
#  FDwfAnalogOutStatus(HDWF hdwf, int idxChannel, DwfState *psts);
_define("FDwfAnalogOutStatus",
        (HDWF, c_int, POINTER(DwfState),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "psts"),))
#  FDwfAnalogOutNodePlayStatus(HDWF hdwf, int idxChannel, AnalogOutNode node, int *cdDataFree, int *cdDataLost, int *cdDataCorrupted);
_define("FDwfAnalogOutNodePlayStatus",
        (HDWF, c_int, AnalogOutNode,
         POINTER(c_int), POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
         (_ARGOUT, "cdDataFree"), (_ARGOUT, "cdDataLost"),
         (_ARGOUT, "cdDataCorrupted"),))
#  FDwfAnalogOutNodePlayData(HDWF hdwf, int idxChannel, AnalogOutNode node, double *rgdData, int cdData);
_xdefine("FDwfAnalogOutNodePlayData",
         (HDWF, c_int, AnalogOutNode, POINTER(c_double), c_int,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "node"),
          (_ARGIN, "rgdData"), (_ARGIN, "cdData"),))
def FDwfAnalogOutNodePlayData(hdwf, idxChannel, node, rgdData, cdData=None):
    if cdData is not None:
        return _FDwfAnalogOutNodePlayData(
            hdwf, idxChannel, node, rgdData, cdData)
    cdData = len(rgdData)
    rgdData_ = (c_double * cdData)()
    for i, v in enumerate(rgdData): rgdData_[i] = rgdData[i]
    return _FDwfAnalogOutNodePlayData(hdwf, idxChannel, node, rgdData_, cdData)

# ANALOG IO INSTRUMENT FUNCTIONS
# Control:
#  FDwfAnalogIOReset(HDWF hdwf);
_define("FDwfAnalogIOReset",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfAnalogIOConfigure(HDWF hdwf);
_define("FDwfAnalogIOConfigure",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfAnalogIOStatus(HDWF hdwf);
_define("FDwfAnalogIOStatus",
        (HDWF,), ((_ARGIN, "hdwf"),))

# Configure:
#  FDwfAnalogIOEnableInfo(HDWF hdwf, BOOL *pfSet, BOOL *pfStatus);
_define("FDwfAnalogIOEnableInfo",
        (HDWF, POINTER(BOOL), POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfSet"), (_ARGOUT, "pfStatus"),))
#  FDwfAnalogIOEnableSet(HDWF hdwf, BOOL fMasterEnable);
_define("FDwfAnalogIOEnableSet",
        (HDWF, BOOL,), ((_ARGIN, "hdwf"), (_ARGIN, "fMasterEnable"),))
#  FDwfAnalogIOEnableGet(HDWF hdwf, BOOL *pfMasterEnable);
_define("FDwfAnalogIOEnableGet",
        (HDWF, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfMasterEnable"),))
#  FDwfAnalogIOEnableStatus(HDWF hdwf, BOOL *pfMasterEnable);
_define("FDwfAnalogIOEnableStatus",
        (HDWF, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfMasterEnable"),))
#  FDwfAnalogIOChannelCount(HDWF hdwf, int *pnChannel);
_define("FDwfAnalogIOChannelCount",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pnChannel"),))
#  FDwfAnalogIOChannelName(HDWF hdwf, int idxChannel, char szName[32], char szLabel[16]);
_xdefine("FDwfAnalogIOChannelName",
         (HDWF, c_int, c_char_p, c_char_p,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
          (_ARGIN, "szName"), (_ARGIN, "szLabel"),))
def FDwfAnalogIOChannelName(hdwf, idxChannel, szName=None, szLabel=None):
    if szName is not None and szLabel is not None:
        return _FDwfAnalogIOChannelName(hdwf, idxChannel, szName, szLabel)
    szName = create_string_buffer(32)
    szLabel = create_string_buffer(16)
    _FDwfAnalogIOChannelName(hdwf, idxChannel, szName, szLabel)
    return _mkstring(szName), _mkstring(szLabel)
#  FDwfAnalogIOChannelInfo(HDWF hdwf, int idxChannel, int *pnNodes);
_define("FDwfAnalogIOChannelInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pnNodes"),))
#  FDwfAnalogIOChannelNodeName(HDWF hdwf, int idxChannel, int idxNode, char szNodeName[32], char szNodeUnits[16]);
_xdefine("FDwfAnalogIOChannelNodeName",
         (HDWF, c_int, c_int, c_char_p, c_char_p,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxNode"),
          (_ARGIN, "szNodeName"), (_ARGIN, "szNodeUnits"),))
def FDwfAnalogIOChannelNodeName(
        hdwf, idxChannel, idxNode, szNodeName=None, szNodeUnits=None):
    if szNodeName is not None and szNodeUnits is not None:
        return _FDwfAnalogIOChannelNodeName(
            hdwf, idxChannel, idxNode, szNodeName, szNodeUnits)
    szNodeName = create_string_buffer(32)
    szNodeUnits = create_string_buffer(16)
    _FDwfAnalogIOChannelNodeName(
        hdwf, idxChannel, idxNode, szNodeName, szNodeUnits)
    return _mkstring(szNodeName), _mkstring(szNodeUnits)
#  FDwfAnalogIOChannelNodeInfo(HDWF hdwf, int idxChannel, int idxNode, ANALOGIO *panalogio);
_define("FDwfAnalogIOChannelNodeInfo",
        (HDWF, c_int, c_int, POINTER(ANALOGIO),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxNode"),
         (_ARGOUT, "panalogio"),))
#  FDwfAnalogIOChannelNodeSetInfo(HDWF hdwf, int idxChannel, int idxNode, double *pmin, double *pmax, int *pnSteps);
_define("FDwfAnalogIOChannelNodeSetInfo",
        (HDWF, c_int, c_int,
         POINTER(c_double), POINTER(c_double), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxNode"),
         (_ARGOUT, "pmin"), (_ARGOUT, "pmax"), (_ARGOUT, "pnSteps"),))
#  FDwfAnalogIOChannelNodeSet(HDWF hdwf, int idxChannel, int idxNode, double value);
_define("FDwfAnalogIOChannelNodeSet",
        (HDWF, c_int, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "idxNode"), (_ARGIN, "value"),))
#  FDwfAnalogIOChannelNodeGet(HDWF hdwf, int idxChannel, int idxNode, double *pvalue);
_define("FDwfAnalogIOChannelNodeGet",
        (HDWF, c_int, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxNode"),
         (_ARGOUT, "pvalue"),))
#  FDwfAnalogIOChannelNodeStatusInfo(HDWF hdwf, int idxChannel, int idxNode, double *pmin, double *pmax, int *pnSteps);
_define("FDwfAnalogIOChannelNodeStatusInfo",
        (HDWF, c_int, c_int,
         POINTER(c_double), POINTER(c_double), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxNode"),
         (_ARGOUT, "pmin"), (_ARGOUT, "pmax"), (_ARGOUT, "pnSteps"),))
#  FDwfAnalogIOChannelNodeStatus(HDWF hdwf, int idxChannel, int idxNode, double *pvalue);
_define("FDwfAnalogIOChannelNodeStatus",
        (HDWF, c_int, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "idxNode"),
         (_ARGOUT, "pvalue"),))


# DIGITAL IO INSTRUMENT FUNCTIONS
# Control:
#  FDwfDigitalIOReset(HDWF hdwf);
_define("FDwfDigitalIOReset",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfDigitalIOConfigure(HDWF hdwf);
_define("FDwfDigitalIOConfigure",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfDigitalIOStatus(HDWF hdwf);
_define("FDwfDigitalIOStatus",
        (HDWF,), ((_ARGIN, "hdwf"), ))

# Configure:
#  FDwfDigitalIOOutputEnableInfo(HDWF hdwf, unsigned int *pfsOutputEnableMask);
_define("FDwfDigitalIOOutputEnableInfo",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsOutputEnableMask"), ))
#  FDwfDigitalIOOutputEnableSet(HDWF hdwf, unsigned int fsOutputEnable);
_define("FDwfDigitalIOOutputEnableSet",
        (HDWF, c_uint,), ((_ARGIN, "hdwf"), (_ARGIN, "fsOutputEnable"), ))
#  FDwfDigitalIOOutputEnableGet(HDWF hdwf, unsigned int *pfsOutputEnable);
_define("FDwfDigitalIOOutputEnableGet",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsOutputEnable"),))
#  FDwfDigitalIOOutputInfo(HDWF hdwf, unsigned int *pfsOutputMask);
_define("FDwfDigitalIOOutputInfo",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsOutputMask"),))
#  FDwfDigitalIOOutputSet(HDWF hdwf, unsigned int fsOutput);
_define("FDwfDigitalIOOutputSet",
        (HDWF, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "fsOutput"),))
#  FDwfDigitalIOOutputGet(HDWF hdwf, unsigned int *pfsOutput);
_define("FDwfDigitalIOOutputGet",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsOutput"),))
#  FDwfDigitalIOInputInfo(HDWF hdwf, unsigned int *pfsInputMask);
_define("FDwfDigitalIOInputInfo",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsInputMask"),))
#  FDwfDigitalIOInputStatus(HDWF hdwf, unsigned int *pfsInput);
_define("FDwfDigitalIOInputStatus",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsInput"),))


# DIGITAL IN INSTRUMENT FUNCTIONS
# Control and status: 
#  FDwfDigitalInReset(HDWF hdwf);
_define("FDwfDigitalInReset",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfDigitalInConfigure(HDWF hdwf, BOOL fReconfigure, BOOL fStart);
_define("FDwfDigitalInConfigure",
        (HDWF, BOOL, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "fReconfigure"), (_ARGIN, "fStart"),))
#  FDwfDigitalInStatus(HDWF hdwf, BOOL fReadData, DwfState *psts);
_define("FDwfDigitalInStatus",
        (HDWF, BOOL, POINTER(DwfState),),
        ((_ARGIN, "hdwf"), (_ARGIN, "fReadData"), (_ARGOUT, "psts"),))
#  FDwfDigitalInStatusSamplesLeft(HDWF hdwf, int *pcSamplesLeft);
_define("FDwfDigitalInStatusSamplesLeft",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcSamplesLeft"),))
#  FDwfDigitalInStatusSamplesValid(HDWF hdwf, int *pcSamplesValid);
_define("FDwfDigitalInStatusSamplesValid",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcSamplesValid"),))
#  FDwfDigitalInStatusIndexWrite(HDWF hdwf, int *pidxWrite);
_define("FDwfDigitalInStatusIndexWrite",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pidxWrite"),))
#  FDwfDigitalInStatusAutoTriggered(HDWF hdwf, BOOL *pfAuto);
_define("FDwfDigitalInStatusAutoTriggered",
        (HDWF, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfAuto"),))
#  FDwfDigitalInStatusData(HDWF hdwf, void *rgData, int countOfDataBytes);
_xdefine("FDwfDigitalInStatusData",
         (HDWF, POINTER(c_ubyte), c_int,),
         ((_ARGIN, "hdwf"), (_ARGIN, "rgData"), (_ARGIN, "countOfDataBytes"),))
def FDwfDigitalInStatusData(hdwf, rgData_or_count, countOfDataBytes=None):
    if countOfDataBytes is not None:
        return _FDwfDigitalInStatusData(hdwf, rgData_or_count, countOfDataBytes)
    countOfDataBytes = rgData_or_count
    rgData = (c_ubyte * countOfDataBytes)()
    _FDwfDigitalInStatusData(hdwf, rgData, countOfDataBytes)
    return tuple([ rgData[i] for i in range(countOfDataBytes) ])
#  FDwfDigitalInStatusRecord(HDWF hdwf, int *pcdDataAvailable, int *pcdDataLost, int *pcdDataCorrupt);
_define("FDwfDigitalInStatusRecord",
        (HDWF, POINTER(c_int), POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcdDataAvailable"),
         (_ARGOUT, "pcdDataLost"), (_ARGOUT, "pcdDataCorrupt"),))

# Acquistion configuration:
#  FDwfDigitalInInternalClockInfo(HDWF hdwf, double *phzFreq);
_define("FDwfDigitalInInternalClockInfo",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "phzFreq"),))

#  FDwfDigitalInClockSourceInfo(HDWF hdwf, int *pfsDwfDigitalInClockSource);
# use IsBitSet
_define("FDwfDigitalInClockSourceInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsDwfDigitalInClockSource"),))
#  FDwfDigitalInClockSourceSet(HDWF hdwf, DwfDigitalInClockSource v);
_define("FDwfDigitalInClockSourceSet",
        (HDWF, DwfDigitalInClockSource,),
        ((_ARGIN, "hdwf"), (_ARGIN, "v"),))
#  FDwfDigitalInClockSourceGet(HDWF hdwf, DwfDigitalInClockSource *pv);
_define("FDwfDigitalInClockSourceGet",
        (HDWF, POINTER(DwfDigitalInClockSource),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pv"),))

#  FDwfDigitalInDividerInfo(HDWF hdwf, unsigned int *pdivMax);
_define("FDwfDigitalInDividerInfo",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pdivMax"),))
#  FDwfDigitalInDividerSet(HDWF hdwf, unsigned int div);
_define("FDwfDigitalInDividerSet",
        (HDWF, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "div"),))
#  FDwfDigitalInDividerGet(HDWF hdwf, unsigned int *pdiv);
_define("FDwfDigitalInDividerGet",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pdiv"),))

#  FDwfDigitalInBitsInfo(HDWF hdwf, int *pnBits);
# Returns the number of Digital In bits
_define("FDwfDigitalInBitsInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnBits"),))
#  FDwfDigitalInSampleFormatSet(HDWF hdwf, int nBits);
# valid options 8/16/32
_define("FDwfDigitalInSampleFormatSet",
        (HDWF, c_int,), ((_ARGIN, "hdwf"), (_ARGIN, "nBits"),))
#  FDwfDigitalInSampleFormatGet(HDWF hdwf, int *pnBits);
_define("FDwfDigitalInSampleFormatGet",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pnBits"),))

#  FDwfDigitalInBufferSizeInfo(HDWF hdwf, int *pnSizeMax);
_define("FDwfDigitalInBufferSizeInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnSizeMax"),))
#  FDwfDigitalInBufferSizeSet(HDWF hdwf, int nSize);
_define("FDwfDigitalInBufferSizeSet",
        (HDWF, c_int,), ((_ARGIN, "hdwf"), (_ARGIN, "nSize"),))
#  FDwfDigitalInBufferSizeGet(HDWF hdwf, int *pnSize);
_define("FDwfDigitalInBufferSizeGet",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pnSize"),))

#  FDwfDigitalInSampleModeInfo(HDWF hdwf, int *pfsDwfDigitalInSampleMode);
# use IsBitSet
_define("FDwfDigitalInSampleModeInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsDwfDigitalInSampleMode"),))
#  FDwfDigitalInSampleModeSet(HDWF hdwf, DwfDigitalInSampleMode v);
_define("FDwfDigitalInSampleModeSet",
        (HDWF, DwfDigitalInSampleMode,), ((_ARGIN, "hdwf"), (_ARGIN, "v"),))
#  FDwfDigitalInSampleModeGet(HDWF hdwf, DwfDigitalInSampleMode *pv);
_define("FDwfDigitalInSampleModeGet",
        (HDWF, POINTER(DwfDigitalInSampleMode),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pv"),))

#  FDwfDigitalInAcquisitionModeInfo(HDWF hdwf, int *pfsacqmode);
# use IsBitSet
_define("FDwfDigitalInAcquisitionModeInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfsacqmode"),))
#  FDwfDigitalInAcquisitionModeSet(HDWF hdwf, ACQMODE acqmode);
_define("FDwfDigitalInAcquisitionModeSet",
        (HDWF, ACQMODE,), ((_ARGIN, "hdwf"), (_ARGIN, "acqmode"),))
#  FDwfDigitalInAcquisitionModeGet(HDWF hdwf, ACQMODE *pacqmode);
_define("FDwfDigitalInAcquisitionModeGet",
        (HDWF, POINTER(ACQMODE),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pacqmode"),))

# Trigger configuration:
#  FDwfDigitalInTriggerSourceInfo(HDWF hdwf, int *pfstrigsrc);
# use IsBitSet
_define("FDwfDigitalInTriggerSourceInfo",
        (HDWF, POINTER(c_int),), ((_ARGIN, "hdwf"), (_ARGOUT, "pfstrigsrc"),))
#  FDwfDigitalInTriggerSourceSet(HDWF hdwf, TRIGSRC trigsrc);
_define("FDwfDigitalInTriggerSourceSet",
        (HDWF, TRIGSRC,), ((_ARGIN, "hdwf"), (_ARGIN, "trigsrc"),))
#  FDwfDigitalInTriggerSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
_define("FDwfDigitalInTriggerSourceGet",
        (HDWF, POINTER(TRIGSRC),), ((_ARGIN, "hdwf"), (_ARGOUT, "ptrigsrc"),))

#  FDwfDigitalInTriggerPositionInfo(HDWF hdwf, unsigned int *pnSamplesAfterTriggerMax);
_define("FDwfDigitalInTriggerPositionInfo",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pnSamplesAfterTriggerMax"),))
#  FDwfDigitalInTriggerPositionSet(HDWF hdwf, unsigned int cSamplesAfterTrigger);
_define("FDwfDigitalInTriggerPositionSet",
        (HDWF, c_uint,), ((_ARGIN, "hdwf"), (_ARGIN, "cSamplesAfterTrigger"),))
#  FDwfDigitalInTriggerPositionGet(HDWF hdwf, unsigned int *pcSamplesAfterTrigger);
_define("FDwfDigitalInTriggerPositionGet",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcSamplesAfterTrigger"),))

#  FDwfDigitalInTriggerAutoTimeoutInfo(HDWF hdwf, double *psecMin, double *psecMax, double *pnSteps);
_define("FDwfDigitalInTriggerAutoTimeoutInfo",
        (HDWF, POINTER(c_double), POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"),
         (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"), (_ARGOUT, "pnSteps"),))
#  FDwfDigitalInTriggerAutoTimeoutSet(HDWF hdwf, double secTimeout);
_define("FDwfDigitalInTriggerAutoTimeoutSet",
        (HDWF, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "secTimeout"),))
#  FDwfDigitalInTriggerAutoTimeoutGet(HDWF hdwf, double *psecTimeout);
_define("FDwfDigitalInTriggerAutoTimeoutGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecTimeout"),))

#  FDwfDigitalInTriggerInfo(HDWF hdwf, unsigned int *pfsLevelLow, unsigned int *pfsLevelHigh, unsigned int *pfsEdgeRise, unsigned int *pfsEdgeFall);
_define("FDwfDigitalInTriggerInfo",
        (HDWF, POINTER(c_uint), POINTER(c_uint),
         POINTER(c_uint), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsLevelLow"), (_ARGOUT, "pfsLevelHigh"),
         (_ARGOUT, "pfsEdgeRise"), (_ARGOUT, "pfsEdgeFall"),))
#  FDwfDigitalInTriggerSet(HDWF hdwf, unsigned int fsLevelLow, unsigned int fsLevelHigh, unsigned int fsEdgeRise, unsigned int fsEdgeFall);
_define("FDwfDigitalInTriggerSet",
        (HDWF, c_uint, c_uint, c_uint, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "fsLevelLow"), (_ARGIN, "fsLevelHigh"),
         (_ARGIN, "fsEdgeRise"), (_ARGIN, "fsEdgeFall"),))
#  FDwfDigitalInTriggerGet(HDWF hdwf, unsigned int *pfsLevelLow, unsigned int *pfsLevelHigh, unsigned int *pfsEdgeRise, unsigned int *pfsEdgeFall);
_define("FDwfDigitalInTriggerGet",
        (HDWF, POINTER(c_uint), POINTER(c_uint),
         POINTER(c_uint), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfsLevelLow"), (_ARGOUT, "pfsLevelHigh"),
         (_ARGOUT, "pfsEdgeRise"), (_ARGOUT, "pfsEdgeFall"),))
# the logic for trigger bits: Low and High and (Rise or Fall)
# bits set in Rise and Fall means any edge

# DIGITAL OUT INSTRUMENT FUNCTIONS
# Control:
#  FDwfDigitalOutReset(HDWF hdwf);
_define("FDwfDigitalOutReset",
        (HDWF,), ((_ARGIN, "hdwf"),))
#  FDwfDigitalOutConfigure(HDWF hdwf, BOOL fStart);
_define("FDwfDigitalOutConfigure",
        (HDWF, BOOL,), ((_ARGIN, "hdwf"), (_ARGIN, "fStart"), ))
#  FDwfDigitalOutStatus(HDWF hdwf, DwfState *psts);
_define("FDwfDigitalOutStatus",
        (HDWF, POINTER(DwfState),), ((_ARGIN, "hdwf"), (_ARGOUT, "psts"),))

# Configuration:
#  FDwfDigitalOutInternalClockInfo(HDWF hdwf, double *phzFreq);
_define("FDwfDigitalOutInternalClockInfo",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "phzFreq"),))

#  FDwfDigitalOutTriggerSourceInfo(HDWF hdwf, int *pfstrigsrc);
# use IsBitSet
_define("FDwfDigitalOutTriggerSourceInfo",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfstrigsrc"),))
#  FDwfDigitalOutTriggerSourceSet(HDWF hdwf, TRIGSRC trigsrc);
_define("FDwfDigitalOutTriggerSourceSet",
        (HDWF, TRIGSRC,), ((_ARGIN, "hdwf"), (_ARGIN, "trigsrc"),))
#  FDwfDigitalOutTriggerSourceGet(HDWF hdwf, TRIGSRC *ptrigsrc);
_define("FDwfDigitalOutTriggerSourceGet",
        (HDWF, POINTER(TRIGSRC),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "ptrigsrc"),))

#  FDwfDigitalOutRunInfo(HDWF hdwf, double *psecMin, double *psecMax);
_define("FDwfDigitalOutRunInfo",
        (HDWF, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"),))
#  FDwfDigitalOutRunSet(HDWF hdwf, double secRun);
_define("FDwfDigitalOutRunSet",
        (HDWF, c_double,), ((_ARGIN, "hdwf"), (_ARGIN, "secRun"),))
#  FDwfDigitalOutRunGet(HDWF hdwf, double *psecRun);
_define("FDwfDigitalOutRunGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecRun"),))
#  FDwfDigitalOutRunStatus(HDWF hdwf, double *psecRun);
_define("FDwfDigitalOutRunStatus",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecRun"),))

#  FDwfDigitalOutWaitInfo(HDWF hdwf, double *psecMin, double *psecMax);
_define("FDwfDigitalOutWaitInfo",
        (HDWF, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecMin"), (_ARGOUT, "psecMax"),))
#  FDwfDigitalOutWaitSet(HDWF hdwf, double secWait);
_define("FDwfDigitalOutWaitSet",
        (HDWF, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "secWait"),))
#  FDwfDigitalOutWaitGet(HDWF hdwf, double *psecWait);
_define("FDwfDigitalOutWaitGet",
        (HDWF, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "psecWait"),))

#  FDwfDigitalOutRepeatInfo(HDWF hdwf, unsigned int *pnMin, unsigned int *pnMax);
_define("FDwfDigitalOutRepeatInfo",
        (HDWF, POINTER(c_uint), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pnMin"), (_ARGOUT, "pnMax"),))
#  FDwfDigitalOutRepeatSet(HDWF hdwf, unsigned int cRepeat);
_define("FDwfDigitalOutRepeatSet",
        (HDWF, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "cRepeat"),))
#  FDwfDigitalOutRepeatGet(HDWF hdwf, unsigned int *pcRepeat);
_define("FDwfDigitalOutRepeatGet",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcRepeat"),))
#  FDwfDigitalOutRepeatStatus(HDWF hdwf, unsigned int *pcRepeat);
_define("FDwfDigitalOutRepeatStatus",
        (HDWF, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcRepeat"),))

#  FDwfDigitalOutRepeatTriggerSet(HDWF hdwf, BOOL fRepeatTrigger);
_define("FDwfDigitalOutRepeatTriggerSet",
        (HDWF, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "fRepeatTrigger"),))
#  FDwfDigitalOutRepeatTriggerGet(HDWF hdwf, BOOL *pfRepeatTrigger);
_define("FDwfDigitalOutRepeatTriggerGet",
        (HDWF, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pfRepeatTrigger"),))

#  FDwfDigitalOutCount(HDWF hdwf, int *pcChannel);
_define("FDwfDigitalOutCount",
        (HDWF, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGOUT, "pcChannel"),))
#  FDwfDigitalOutEnableSet(HDWF hdwf, int idxChannel, BOOL fEnable);
_define("FDwfDigitalOutEnableSet",
        (HDWF, c_int, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "fEnable"),))
#  FDwfDigitalOutEnableGet(HDWF hdwf, int idxChannel, BOOL *pfEnable);
_define("FDwfDigitalOutEnableGet",
        (HDWF, c_int, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfEnable"),))

#  FDwfDigitalOutOutputInfo(HDWF hdwf, int idxChannel, int *pfsDwfDigitalOutOutput);
# use IsBitSet
_define("FDwfDigitalOutOutputInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pfsDwfDigitalOutOutput"),))
#  FDwfDigitalOutOutputSet(HDWF hdwf, int idxChannel, DwfDigitalOutOutput v); 
_define("FDwfDigitalOutOutputSet",
        (HDWF, c_int, DwfDigitalOutOutput,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "v"),))
#  FDwfDigitalOutOutputGet(HDWF hdwf, int idxChannel, DwfDigitalOutOutput *pv);
_define("FDwfDigitalOutOutputGet",
        (HDWF, c_int, POINTER(DwfDigitalOutOutput),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pv"),))

#  FDwfDigitalOutTypeInfo(HDWF hdwf, int idxChannel, int *pfsDwfDigitalOutType);
# use IsBitSet
_define("FDwfDigitalOutTypeInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pfsDwfDigitalOutType"),))
#  FDwfDigitalOutTypeSet(HDWF hdwf, int idxChannel, DwfDigitalOutType v);
_define("FDwfDigitalOutTypeSet",
        (HDWF, c_int, DwfDigitalOutType,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "v"),))
#  FDwfDigitalOutTypeGet(HDWF hdwf, int idxChannel, DwfDigitalOutType *pv);
_define("FDwfDigitalOutTypeGet",
        (HDWF, c_int, POINTER(DwfDigitalOutType),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pv"),))

#  FDwfDigitalOutIdleInfo(HDWF hdwf, int idxChannel, int *pfsDwfDigitalOutIdle);
# use IsBitSet
_define("FDwfDigitalOutIdleInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pfsDwfDigitalOutIdle"),))
#  FDwfDigitalOutIdleSet(HDWF hdwf, int idxChannel, DwfDigitalOutIdle v);
_define("FDwfDigitalOutIdleSet",
        (HDWF, c_int, DwfDigitalOutIdle,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "v"),))
#  FDwfDigitalOutIdleGet(HDWF hdwf, int idxChannel, DwfDigitalOutIdle *pv);
_define("FDwfDigitalOutIdleGet",
        (HDWF, c_int, POINTER(DwfDigitalOutIdle),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pv"),))

#  FDwfDigitalOutDividerInfo(HDWF hdwf, int idxChannel, unsigned int *vMin, unsigned int *vMax);
_define("FDwfDigitalOutDividerInfo",
        (HDWF, c_int, POINTER(c_uint), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "vMin"), (_ARGOUT, "vMax"),))
#  FDwfDigitalOutDividerInitSet(HDWF hdwf, int idxChannel, unsigned int v);
_define("FDwfDigitalOutDividerInitSet",
        (HDWF, c_int, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "v"),))
#  FDwfDigitalOutDividerInitGet(HDWF hdwf, int idxChannel, unsigned int *pv);
_define("FDwfDigitalOutDividerInitGet",
        (HDWF, c_int, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pv"),))
#  FDwfDigitalOutDividerSet(HDWF hdwf, int idxChannel, unsigned int v);
_define("FDwfDigitalOutDividerSet",
        (HDWF, c_int, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "v"),))
#  FDwfDigitalOutDividerGet(HDWF hdwf, int idxChannel, unsigned int *pv);
_define("FDwfDigitalOutDividerGet",
        (HDWF, c_int, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pv"),))

#  FDwfDigitalOutCounterInfo(HDWF hdwf, int idxChannel, unsigned int *vMin, unsigned int *vMax);
_define("FDwfDigitalOutCounterInfo",
        (HDWF, c_int, POINTER(c_uint), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "vMin"), (_ARGOUT, "vMax"),))
#  FDwfDigitalOutCounterInitSet(HDWF hdwf, int idxChannel, BOOL fHigh, unsigned int v);
_define("FDwfDigitalOutCounterInitSet",
        (HDWF, c_int, BOOL, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "fHigh"), (_ARGIN, "v"),))
#  FDwfDigitalOutCounterInitGet(HDWF hdwf, int idxChannel, int *pfHigh, unsigned int *pv);
_define("FDwfDigitalOutCounterInitGet",
        (HDWF, c_int, POINTER(c_int), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pfHigh"), (_ARGOUT, "pv"),))
#  FDwfDigitalOutCounterSet(HDWF hdwf, int idxChannel, unsigned int vLow, unsigned int vHigh);
_define("FDwfDigitalOutCounterSet",
        (HDWF, c_int, c_uint, c_uint,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "vLow"), (_ARGIN, "vHigh"),))
#  FDwfDigitalOutCounterGet(HDWF hdwf, int idxChannel, unsigned int *pvLow, unsigned int *pvHigh);
_define("FDwfDigitalOutCounterGet",
        (HDWF, c_int, POINTER(c_uint), POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pvLow"), (_ARGOUT, "pvHigh"),))

#  FDwfDigitalOutDataInfo(HDWF hdwf, int idxChannel, unsigned int *pcountOfBitsMax);
_define("FDwfDigitalOutDataInfo",
        (HDWF, c_int, POINTER(c_uint),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pcountOfBitsMax"),))
#  FDwfDigitalOutDataSet(HDWF hdwf, int idxChannel, void *rgBits, unsigned int countOfBits);
_xdefine("FDwfDigitalOutDataSet",
         (HDWF, c_int, POINTER(c_ubyte), c_uint,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
          (_ARGIN, "rgBits"), (_ARGIN, "countOfBits"),))
def FDwfDigitalOutDataSet(hdwf, idxChannel, rgBits, countOfBits=None):
    if countOfBits is not None:
        return _FDwfDigitalOutDataSet(hdwf, idxChannel, rgBits, countOfBits)
    if type(rgBits[0]) is tuple: #rgBits is sequence of tuple
        countOfBits = len(rgBits)*2
        rgBits_ = (c_ubyte * ((countObBits + 7)// 8))()
        index = 0
        byte = 0x00
        mask = 0x01
        for io, oe in rgBits:
            if io: byte |= mask
            mask <<= 1
            if oe: byte |= mask
            mask <<= 1
            if mask > 0x80:
                rgBits_[index] = byte
                mask = 0x01
                byte = 0x00
                index += 1
        if index != len(rgBits_):
            rgBits_[index] = byte
    else:
        countOfBits = len(rgBits)
        rgBits_ = (c_ubyte * ((countOfBits + 7)// 8))()
        index = 0
        byte = 0x00
        mask = 0x01
        for io in rgBits:
            if io: byte |= mask
            mask <<= 1
            if mask > 0x80:
                rgBits_[index] = byte
                mask = 0x01
                byte = 0x00
                index += 1
        if index != len(rgBits_):
            rgBits_[index] = byte
    return _FDwfDigitalOutDataSet(hdwf, idxChannel, rgBits_, countOfBits)
# bits order is lsb first
#  for TS output the count of bits its the total number of IO|OE bits,
#  it should be an even number
# BYTE:   0                 |1     ...
# bit:    0 |1 |2 |3 |...|7 |0 |1 |...
# sample: IO|OE|IO|OE|...|OE|IO|OE|...
#  or Python's sequence of tuple
# [ (IO, OE), (IO, OE) ... (IO, OE) ]

# FDwfDigitalOutDataSet support functions
def create_bitdata_stream(data, bits, msb_first=False):
    result = []
    for v in data:
        for i in range(bits):
            if msb_first:
                mask = 1 << (bits - i - 1)
            else:
                mask = 1 << i
            result.append((v & mask) != 0)
    return result
def create_bus_bitdata_streams(data, bits):
    result = []
    for i in range(bits):
        d = []
        mask = 1 << i
        for v in data:
            d.append((v & mask) != 0)
        result.append(d)
    return tuple(result)

# OBSOLETE, do not use them:
STS = c_ubyte
stsRdy = 0
stsArm = 1
stsDone = 2
stsTrig = 3
stsCfg = 4
stsPrefill = 5
stsNotDone = 6
stsTrigDly = 7
stsError = 8
stsBusy = 9
stsStop = 10

#  FDwfAnalogOutEnableSet(HDWF hdwf, int idxChannel, BOOL fEnable);
_define("FDwfAnalogOutEnableSet",
        (HDWF, c_int, BOOL,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "fEnable"),))
#  FDwfAnalogOutEnableGet(HDWF hdwf, int idxChannel, BOOL *pfEnable);
_define("FDwfAnalogOutEnableGet",
        (HDWF, c_int, POINTER(BOOL),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfEnable"),))
#  FDwfAnalogOutFunctionInfo(HDWF hdwf, int idxChannel, int *pfsfunc);
# use IsBitSet
_define("FDwfAnalogOutFunctionInfo",
        (HDWF, c_int, POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfsfunc"),))
#  FDwfAnalogOutFunctionSet(HDWF hdwf, int idxChannel, FUNC func);
_define("FDwfAnalogOutFunctionSet",
        (HDWF, c_int, FUNC,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "func"),))
#  FDwfAnalogOutFunctionGet(HDWF hdwf, int idxChannel, FUNC *pfunc);
_define("FDwfAnalogOutFunctionGet",
        (HDWF, c_int, POINTER(FUNC),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pfunc"),))
#  FDwfAnalogOutFrequencyInfo(HDWF hdwf, int idxChannel, double *phzMin, double *phzMax);
_define("FDwfAnalogOutFrequencyInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "phzMin"), (_ARGOUT, "phzMax"),))
#  FDwfAnalogOutFrequencySet(HDWF hdwf, int idxChannel, double hzFrequency);
_define("FDwfAnalogOutFrequencySet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "hzFrequency"),))
#  FDwfAnalogOutFrequencyGet(HDWF hdwf, int idxChannel, double *phzFrequency);
_define("FDwfAnalogOutFrequencyGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "phzFrequency"),))
#  FDwfAnalogOutAmplitudeInfo(HDWF hdwf, int idxChannel, double *pvoltsMin, double *pvoltsMax);
_define("FDwfAnalogOutAmplitudeInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pvoltsMin"), (_ARGOUT, "pvoltsMax"),))
#  FDwfAnalogOutAmplitudeSet(HDWF hdwf, int idxChannel, double voltsAmplitude);
_define("FDwfAnalogOutAmplitudeSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "voltsAmplitude"),))
#  FDwfAnalogOutAmplitudeGet(HDWF hdwf, int idxChannel, double *pvoltsAmplitude);
_define("FDwfAnalogOutAmplitudeGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pvoltsAmplitude"),))
#  FDwfAnalogOutOffsetInfo(HDWF hdwf, int idxChannel, double *pvoltsMin, double *pvoltsMax);
_define("FDwfAnalogOutOffsetInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pvoltsMin"), (_ARGOUT, "pvoltsMax"),))
#  FDwfAnalogOutOffsetSet(HDWF hdwf, int idxChannel, double voltsOffset);
_define("FDwfAnalogOutOffsetSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "voltsOffset"),))
#  FDwfAnalogOutOffsetGet(HDWF hdwf, int idxChannel, double *pvoltsOffset);
_define("FDwfAnalogOutOffsetGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pvoltsOffset"),))
#  FDwfAnalogOutSymmetryInfo(HDWF hdwf, int idxChannel, double *ppercentageMin, double *ppercentageMax);
_define("FDwfAnalogOutSymmetryInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "ppercentageMin"), (_ARGOUT, "ppercentageMax"),))
#  FDwfAnalogOutSymmetrySet(HDWF hdwf, int idxChannel, double percentageSymmetry);
_define("FDwfAnalogOutSymmetrySet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "percentageSymmetry"),))
#  FDwfAnalogOutSymmetryGet(HDWF hdwf, int idxChannel, double *ppercentageSymmetry);
_define("FDwfAnalogOutSymmetryGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "ppercentageSymmetry"),))
#  FDwfAnalogOutPhaseInfo(HDWF hdwf, int idxChannel, double *pdegreeMin, double *pdegreeMax);
_define("FDwfAnalogOutPhaseInfo",
        (HDWF, c_int, POINTER(c_double), POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pdegreeMin"), (_ARGOUT, "pdegreeMax"),))
#  FDwfAnalogOutPhaseSet(HDWF hdwf, int idxChannel, double degreePhase);
_define("FDwfAnalogOutPhaseSet",
        (HDWF, c_int, c_double,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGIN, "degreePhase"),))
#  FDwfAnalogOutPhaseGet(HDWF hdwf, int idxChannel, double *pdegreePhase);
_define("FDwfAnalogOutPhaseGet",
        (HDWF, c_int, POINTER(c_double),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"), (_ARGOUT, "pdegreePhase"),))
#  FDwfAnalogOutDataInfo(HDWF hdwf, int idxChannel, int *pnSamplesMin, int *pnSamplesMax);
_define("FDwfAnalogOutDataInfo",
        (HDWF, c_int, POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "pnSamplesMin"), (_ARGOUT, "pnSamplesMax"),))
#  FDwfAnalogOutDataSet(HDWF hdwf, int idxChannel, double *rgdData, int cdData);
_define("FDwfAnalogOutDataSet",
        (HDWF, c_int, POINTER(c_double), c_int,),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGIN, "rgdData"), (_ARGIN, "cdData"), ))
#  FDwfAnalogOutPlayStatus(HDWF hdwf, int idxChannel, int *cdDataFree, int *cdDataLost, int *cdDataCorrupted);
_define("FDwfAnalogOutPlayStatus",
        (HDWF, c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int),),
        ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
         (_ARGOUT, "cdDataFree"), (_ARGOUT, "cdDataLost"),
         (_ARGOUT, "cdDataCorrupted"),))
#  FDwfAnalogOutPlayData(HDWF hdwf, int idxChannel, double *rgdData, int cdData);
_xdefine("FDwfAnalogOutPlayData",
         (HDWF, c_int, POINTER(c_double), c_int,),
         ((_ARGIN, "hdwf"), (_ARGIN, "idxChannel"),
          (_ARGIN, "rgdData"), (_ARGIN, "cdData"),))
def FDwfAnalogOutPlayData(hdwf, idxChannel, rgdData, cdData=None):
    if cdData is not None:
        return _FDwfAnalogOutPlayData(hdwf, idxChannel, rgdData, cdData)
    cdData = len(rgdData)
    rgdData_ = (c_double * cdData)()
    for i, v in enumerate(cdData): rgdData_[i] = rgdData[i]
    return _FDwfAnalogOutPlayData(hdwf, idxChannel, rgdData, cdData)
#  FDwfEnumAnalogInChannels(int idxDevice, int *pnChannels);
_define("FDwfEnumAnalogInChannels",
        (c_int, POINTER(c_int),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "pnChannels"),))
#  FDwfEnumAnalogInBufferSize(int idxDevice, int *pnBufferSize);
_define("FDwfEnumAnalogInBufferSize",
        (c_int, POINTER(c_int),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "pnBufferSize"),))
#  FDwfEnumAnalogInBits(int idxDevice, int *pnBits);
_define("FDwfEnumAnalogInBits",
        (c_int, POINTER(c_int),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "pnBits"), ))
#  FDwfEnumAnalogInFrequency(int idxDevice, double *phzFrequency);
_define("FDwfEnumAnalogInFrequency",
        (c_int, POINTER(c_double),),
        ((_ARGIN, "idxDevice"), (_ARGOUT, "phzFrequency"), ))
