# -- encoding: UTF-8
"""
This is a GUI library for OROCHI RTC
"""

import sys, types
from Tkinter import *

root = Tk()


rtc = []
ManipulatorCommonInterface_Middle = []

def setRTC(comp):
    global rtc
    rtc = comp

"""
ManipulatorCommonInterface_Common
"""
Common_List = ['clearAlarms()','getActiveAlarm(out RTC::AlarmSeq alarms)','getFeedbackPosJoint(out RTC::JointPos pos)',
               'getManipInfo(out RTC::ManipInfo manipInfo)','getSoftLimitJoint(out RTC::LimitSeq softLimit)','getState(out RTC::ULONG state)',
               'servoOFF()','servoON()','setSoftLimitJoint(in RTC::LimitSeq softLimit)']

"""
ManipulatorCommonInterface_Middle
"""
Middle_List = ['closeGripper()','getBaseOffset(out RTC::HgMatrix offset)','getFeedbackPosCartesian(out RTC::CarPosWithElbow pos)',
               'getMaxSpeedCartesian(out RTC::CartesianSpeed speed)','getMaxSpeedJoint(out RTC::DoubleSeq speed)','getMinAccelTimeCartesian(out double aclTime)',
               'getMinAccelTimeJoint(out double aclTime)','getSoftLimitCartesian(out RTC::LimitValue xLimit,out RTC::LimitValue yLimit,out RTC::LimitValue zLimit )',
               'moveGripper(in RTC::ULONG angleRatio)','moveLinearCartesianAbs(in RTC::CarPosWithElbow carPoint)','moveLinearCartesianRel(in RTC::CarPosWithElbow carPoint)',
               'movePTPCartesianAbs(in RTC::CarPosWithElbow carPoint)','movePTPCartesianRel(in RTC::CarPosWithElbow carPoint)','movePTPJointAbs(in RTC::JointPos jointPoints)',
               'movePTPJointRel(in RTC::JointPos jointPoints)','openGripper()','pause()','resume()','stop()','setAccelTimeCartesian(in double aclTime)','setAccelTimeJoint(in double aclTime)',
               'setBaseOffset(in RTC::HgMatrix offset)','setControlPointOffset(in RTC::HgMatrix offset)','setMaxSpeedCartesian(in RTC::CartesianSpeed speed)',
               'setMaxSpeedJoint(in RTC::DoubleSeq speed)','setMinAccelTimeCartesian(in double aclTime)','setMinAccelTimeJoint(in double aclTime)',
               'setSoftLimitCartesian(in RTC::LimitValue xLimit,in RTC::LimitValue yLimit,in RTC::LimitValue zLimit)','setSpeedCartesian(in RTC::ULONG spdRatio)',
               'setSpeedJoint(in RTC::ULONG spdRatio)']



# Type Call Back Function Definition Division

def on_HgMatrix():
    return None

def on_double():
    return 0.0

def on_CartesianSpeed():
    return None
# TCBFDD End



## Function Declaration String Parser
def parse_func(func_desc):
    func_name = ""
    in_types = []
    out_types = []
    func_name = func_desc.split('(')[0]
    argument_descs = func_desc.split('(')[1].strip()[:-1].split(',')
    for arg_desc in argument_descs:
        tokens= arg_desc.split()
        if tokens[0] == 'in':
            in_types.append(tokens[1])
        elif tokens[1] == 'out':
            out_types.append(tokens[1])
    return (func_name, in_types, out_types)
# FDSP End


def parse_and_call(service_port, declaration):
    func_name, in_types, out_types = parse_func(declaration)
    args = []
    for typ in in_types:
        on_func = getattr(sys.modules[__name__], 'on_'+typ)
        """ returns function which is defined 'on_'+typ"""
        if type(on_func) == types.FunctionType:
            sys.stderr.write(' - Failed To Parse %s\n' % 'on_' + typ)
            return 
        args.append(on_func())
        """add return value to args[]"""

    target_func = getattr(service_port._ptr(), func_name)
    """ returns service port function"""
    target_func(*args)
    """ acceps number of parameters to service port function """


ManipulatorCommonInterface_Common= LabelFrame(root, text = 'ManipulatorCommonInterface_Common',
                   width = 200, height = 300, labelanchor = NW)
ManipulatorCommonInterface_Common.pack(side='left')

ManipulatorCommonInterface_Middle_main = LabelFrame(root, text = 'ManipulatorCommonInterface_Middle',
                   width = 200, height = 300, labelanchor = NW)
ManipulatorCommonInterface_Middle_main.pack(side='left')

Basic_Command = LabelFrame(root, text = 'Basic_Command',
                   width = 200, height = 300, labelanchor = NW)




i = len(Middle_List)/10

if len(Middle_list)/10 > 0
    i + 1;

for x  in i:

    ManipulatorCommonInterface_Middle[x] = LabelFrame(root, text = 'ManipulatorCommonInterface_Middle',
                       width = 200, height = 300, labelanchor = NW)
    ManipulatorCommonInterface_Middle[x].pack(side='left')
      

for x in Common_List:
    Button(ManipulatorCommonInterface_Common, text = x,width=40,command=lambda x=x :parse_and_call(rtc.getServicePortMiddle(), x)).pack(anchor='w')
    
for x in Middle_List:
    Button(ManipulatorCommonInterface_Middle, text = x,width=55,command=lambda x=x :comp.find(x)).pack(anchor='w')

pwUpDown = PanedWindow(Basic_Command, orient='horizontal')
pwLeftRight = PanedWindow(Basic_Command)
pwFrontBack = PanedWindow(Basic_Command)
pwRoll = PanedWindow(Basic_Command)
pwPitch = PanedWindow(Basic_Command)
pwYaw  = PanedWindow(Basic_Command)

pwUpDown.pack(expand = True, fill = BOTH)
pwLeftRight.pack(expand = True, fill = BOTH)
pwFrontBack.pack(expand = True, fill = BOTH)
pwRoll.pack(expand=True, fill=BOTH)
pwPitch.pack(expand=True, fill=BOTH)
pwYaw.pack(expand=True, fill=BOTH)

Button(pwUpDown, text='Up', width=10, height=2, command=lambda:comp.onUp() ).pack(in_=pwUpDown, side=LEFT, expand=True, fill=BOTH)
Button(pwUpDown, text='Down', width=10, height=2, command=lambda:comp.onDown() ).pack(in_=pwUpDown, side=LEFT, expand=True, fill=BOTH)
Button(pwLeftRight, text='Left', width=10, height=2, command=lambda:comp.onLeft()).pack(in_=pwLeftRight, side=LEFT, expand=True, fill=BOTH)
Button(pwLeftRight, text='Right', width=10, height=2, command=lambda:comp.onRight()).pack(in_=pwLeftRight, side=LEFT, expand=True, fill=BOTH)
Button(pwFrontBack, text='Forward', width=10, height=2, command=lambda:comp.onFront() ).pack(in_=pwFrontBack, side=LEFT, expand=True, fill=BOTH)
Button(pwFrontBack, text='Backward', width=10, height=2, command=lambda:comp.onBack() ).pack(in_=pwFrontBack, side=LEFT, expand=True, fill=BOTH)
Button(pwRoll, text='Roll-', width=10, height=2, command=lambda:comp.onRollN() ).pack(in_=pwRoll, side=LEFT, expand=True, fill=BOTH)
Button(pwRoll, text='Roll+', width=10, height=2, command=lambda:comp.onRollP() ).pack(in_=pwRoll, side=LEFT, expand=True, fill=BOTH)
Button(pwPitch, text='Pitch-', width=10, height=2, command=lambda:comp.onPitchN()).pack(in_=pwPitch, side=LEFT, expand=True, fill=BOTH)
Button(pwPitch, text='Pitch+', width=10, height=2, command=lambda:comp.onPitchP()).pack(in_=pwPitch, side=LEFT, expand=True, fill=BOTH)
Button(pwYaw, text='Yaw-', width=10, height=2, command=lambda:comp.onYawN() ).pack(in_=pwYaw, side=LEFT, expand=True, fill=BOTH)
Button(pwYaw, text='Yaw+', width=10, height=2, command=lambda:comp.onYawP() ).pack(in_=pwYaw, side=LEFT, expand=True, fill=BOTH)

Basic_Command.pack(padx = 5, pady = 5, side = LEFT)


root.mainloop()
