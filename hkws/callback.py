from ctypes import *
from hkws.model.model import *
import cv2
import ffmpy3
filePath = 'D:/project/bblock/db/'
import numpy as np
import io

l_lst = [1]
hikFunc = CFUNCTYPE(
    None,
    c_long,  # lRealHandle 当前的预览句柄，NET_DVR_RealPlay_V40的返回值
    c_ulong,  # dwDataType  数据类型 1-系统头数据， 2-流数据（包括符合流或者音视频分开的流数据），3-音频数据，112-私有数据，包括智能信息
    POINTER(c_byte),  # *pBuffer 存放数据的缓冲区指针
    c_ulong,  # dwBufSize 缓冲区大小
    c_ulong,  # *pUser 用户数据
)


@CFUNCTYPE(None, c_long, c_ulong, POINTER(c_byte), c_ulong, c_ulong)
def g_real_data_call_back(lRealPlayHandle: c_long,
                          dwDataType: c_ulong,
                          pBuffer: POINTER(c_byte),
                          dwBufSize: c_ulong,
                          dwUser: c_ulong):
    print(' aaaaaaaaaaa callback pBufSize is ', lRealPlayHandle, pBuffer, dwBufSize)
    print(dwDataType)


@CFUNCTYPE(None, c_long, c_ulong, POINTER(c_byte), c_ulong, c_ulong)
def g_standard_data_call_back(lRealPlayHandle: c_long,
                          dwDataType: 4,
                          pBuffer: POINTER(c_byte),
                          dwBufSize: c_ulong,
                          dwUser: c_ulong):
    print(' bbbbbbbbbbb callback pBufSize is ', lRealPlayHandle, pBuffer, dwBufSize)
    print(dwDataType)
    l_lst[0] = pBuffer




alarm_stracture = CFUNCTYPE(
    c_bool,
    c_long,
    NET_DVR_ALARMER,
    NET_VCA_FACESNAP_RESULT,
    c_ulong,
    c_void_p,
)


@CFUNCTYPE(c_bool, c_long, POINTER(NET_DVR_ALARMER), POINTER(NET_VCA_FACESNAP_RESULT), c_ulong, c_void_p)
def face_alarm_call_back(lCommand: c_long,
                         pAlarmer: POINTER(NET_DVR_ALARMER),
                         pAlarmInfo: POINTER(NET_VCA_FACESNAP_RESULT),
                         dwBufLen: c_ulong,
                         pUser: c_void_p):
    print("lCommand ", lCommand)
    alarm_info = NET_VCA_FACESNAP_RESULT()
    memmove(pointer(alarm_info), pAlarmInfo, dwBufLen)
    print("是否有体温数据", alarm_info.byAddInfo)
    if alarm_info.byAddInfo:
        face_addinfo_buff = NET_VCA_FACESNAP_ADDINFO()
        print(sizeof(NET_VCA_FACESNAP_ADDINFO))
    memmove(pointer(face_addinfo_buff), alarm_info.pAddInfoBuffer, sizeof(NET_VCA_FACESNAP_ADDINFO))
    print("体温为", face_addinfo_buff.fFaceTemperature)
    len_pic = alarm_info.dwFacePicLen + 1
    print("人脸截图长度", len_pic)
    print("图片指针为：", alarm_info.pBuffer1)
    a = string_at(alarm_info.pBuffer1, alarm_info.dwFacePicLen)
    with open("test.jpg", "wb") as p_file:
        p_file.write(a)
        p_file.close()
    print(type(a))
    print("检测到人脸")
    return True
