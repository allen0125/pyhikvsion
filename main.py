import config
import hkws.soadapter as sdk
import os
import getopt
import sys
import time
import hkws.callback as cb
from ctypes import byref


# 启动函数  python3 main.py -c xxx/xxx


cnfPath = ''
opts, args = getopt.getopt(sys.argv[1:], '-c:')
for opt_name, opt_val in opts:
    if opt_name in ('-c'):
        cnfPath = opt_val

if cnfPath == '':
    print('Please enter the config path.')

# loadconfig
cnf = config.Config()
path = os.path.join(cnfPath, 'local_config.ini')
cnf.InitConfig(path)
# new adpter
adapter = sdk.HKAdapter()
adapter.add_lib(cnf.SDKPath, cnf.suffix)
print(adapter.so_list)
# init hkws linux sdk
adapter.set_sdk_config(2, cnfPath)
initRes = adapter.init_sdk()
if not initRes:
    os._exit(0)


# user login
userId = adapter.login(cnf.IP, cnf.Port, cnf.User, cnf.Password)
if userId < 0:
    adapter.sdk_clean()

print("Login successful,the userId is ", userId)

get_config = adapter.get_dvr_config(userId)
print("获取配置文件  ", get_config)
set_dvr_config = adapter.set_dvr_config(userId)
print("设置设备信息结果为 ", set_dvr_config)

data = adapter.setup_alarm_chan_v31(cb.face_alarm_call_back, None)
print("设置回调函数结果", data)
# 布防
alarm_result = adapter.setup_alarm_chan_v41(userId)
print("设置人脸v41布防结果", alarm_result)



# lRealPlayHandle = adapter.start_preview(None, userId)
# if lRealPlayHandle < 0:
#     os._exit(2)
# print("Start preview successful,the lRealPlayHandle is ", lRealPlayHandle)

# callback = adapter.callback_real_data(lRealPlayHandle, cb.g_standard_data_call_back, userId)
# print('callback_real_data result is ', callback)

# # callback_standard = adapter.callback_standard_data(
# #     lRealPlayHandle, cb.g_standard_data_call_back, userId)
# # print('callback_standard_data result is', callback_standard)

time.sleep(200)

# adapter.stop_preview(lRealPlayHandle)

adapter.close_alarm(alarm_result)

adapter.logout(userId)
adapter.sdk_clean()
