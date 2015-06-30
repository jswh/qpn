import router
import sys
import os
def printUsage() :
    print 'usage \n vpn on/off [vpn_setting_name] \n sample \n vpn on default'
    sys.exit()

if len(sys.argv) < 2 :
    printUsage()
action = sys.argv[1]
if len(sys.argv) > 2 :
    setting = sys.argv[2]
else :
    setting = 'default'
v = router.Vpn(setting)
if action == 'on' :
    v.vpnon()
    os.system("osascript pptp.applescript")
elif action == 'off' :
    os.system("osascript pptp.applescript")
    v.vpnoff()
else :
    printUsage()


