#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file ServiceOROCHI.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

from Tkinter import *
import math
import csv
import utils 

#reload(utils)

import ManipulatorCommonInterface_Common_idl
import ManipulatorCommonInterface_MiddleLevel_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import _GlobalIDL, _GlobalIDL__POA


# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
serviceorochi_spec = ["implementation_id", "ServiceOROCHI", 
                 "type_name",         "ServiceOROCHI", 
                 "description",       "ModuleDescription", 
                 "version",           "0.0.1", 
                 "vendor",            "Arthur-AIST/TsukubaUniv", 
                 "category",          "Category", 
                 "activity_type",     "STATIC", 
                 "max_instance",      "1", 
                 "language",          "Python", 
                 "lang_type",         "SCRIPT",
                 ""]
# </rtc-template>

root = Tk()

##
# @class ServiceOROCHI
# @brief ModuleDescription
# 
# 
class ServiceOROCHI(OpenRTM_aist.DataFlowComponentBase):
        
        ##
        # @brief constructor
        # @param manager Maneger Object
        # 
        def __init__(self, manager):

                self.force_stop = "No"
                
                OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

                self._d_pos = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
                """
                """
                self._posIn = OpenRTM_aist.InPort("pos", self._d_pos)

                """
                OROCHIのサービスポートを叩くポート
                """
                self._OROCHI_InterfaceCommonPort = OpenRTM_aist.CorbaPort("OROCHI_InterfaceCommon")
                """
                """
                self._OROCHI_InterfaceMiddlePort = OpenRTM_aist.CorbaPort("OROCHI_InterfaceMiddle")

                """
                """
                self._interfaceCommon = OpenRTM_aist.CorbaConsumer(interfaceType=_GlobalIDL.ManipulatorCommonInterface_Common)
                """
                """
                self._interfaceMiddle = OpenRTM_aist.CorbaConsumer(interfaceType=_GlobalIDL.ManipulatorCommonInterface_Middle)


                # initialize of configuration-data.
                # <rtc-template block="init_conf_param">
                
                # </rtc-template>

        def onPreset1(self):
                val_ =[0, 0, 0, 0, 0, 0]
                self._interfaceMiddle._ptr().movePTPJointAbs(val_)

        def onPreset2(self):
                val_=[0, 10, 80, 0, 90, 0]
                self._interfaceMiddle._ptr().movePTPJointAbs(val_)

        def onPreset3(self):
                val_=[90, 10, 80, 0, 90, 0]
                self._interfaceMiddle._ptr().movePTPJointAbs(val_)

        def move_by_coordinate(self,x,y,z):
                [result, pos] = self._interfaceMiddle._ptr().getFeedbackPosCartesian()
                pos.carPos[0][3] = x
                pos.carPos[1][3] = y
                pos.carPos[2][3] = z
                self._interfaceMiddle._ptr().moveLinearCartesianAbs(pos)

        def get_hand_position(self):
                [result, pos] = self._interfaceMiddle._ptr().getFeedbackPosCartesian()
                hand_x = pos.carPos[0][3]
                hand_y = pos.carPos[1][3]
                hand_z = pos.carPos[2][3]

                return hand_x,hand_y,hand_z

        def getServicePortMiddle(self):
                return self._interfaceMiddle

        def grab_obj(self):
                self.onDown(110)
                self.setGripper(20)
                time.sleep(4)
                self.onUp(110)

        def release_obj(self):
                self.onDown(105)
                self.setGripper(60)
                time.sleep(4)
                self.onUp(105)
        
        def onUp(self,amount):
                [result, pos] = self._interfaceMiddle._ptr().getFeedbackPosCartesian()
                pos.carPos[2][3] = pos.carPos[2][3] + amount
                self._interfaceMiddle._ptr().moveLinearCartesianAbs(pos)
        
        def onDown(self,amount):
                [result, pos] = self._interfaceMiddle._ptr().getFeedbackPosCartesian()
                pos.carPos[2][3] = pos.carPos[2][3] - amount
                self._interfaceMiddle._ptr().moveLinearCartesianAbs(pos)
        
        def onClose(self):
                self._interfaceMiddle._ptr().closeGripper()

        def onOpen(self):
                self._interfaceMiddle._ptr().openGripper()

        def setGripper(self,amount):
                self._interfaceMiddle._ptr().moveGripper(amount)
                

        def pick_and_place(self,model_list):

                for i in range(len(model_list.obj)):

                        #初期位置から移動していない場合は無視する処理を入れる

                        self.onPreset3()
                        self.move_by_coordinate((275-model_list.initial_pos[i][1])*2,(275-model_list.initial_pos[i][0])*2,300)
                        self.grab_obj()
                        self.onPreset3()
                        coords_xy = model_list.obj[i].get_center()

                        print coords_xy

                        if ((275-coords_xy[1])*2 < 0) and ((275-coords_xy[0])*2 < 0):
                                val_=[0, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                val_=[-90, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                val_=[-90, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                self.move_by_coordinate((275-coords_xy[1])*2,(275-coords_xy[0])*2,300)
                                self.onRoll(model_list.obj[i].get_angle())
                                self.release_obj()                          
                                val_=[-90, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                val_=[0, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                self.onPreset3()
 
                        elif ((275-coords_xy[1])*2 < 0) and ((275-coords_xy[0])*2 > 0):
                                val_=[0, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                val_=[0, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                self.move_by_coordinate((275-coords_xy[1])*2,(275-coords_xy[0])*2,300)
                                self.onRoll(90-model_list.obj[i].get_angle())
                                self.release_obj()                          
                                val_=[0, 10, 80, 0, 90, 0]
                                self._interfaceMiddle._ptr().movePTPJointAbs(val_)
                                self.onPreset3() 

                        else:                                                        
                                self.move_by_coordinate((275-coords_xy[1])*2,(275-coords_xy[0])*2,300)
                                self.onRoll(model_list.obj[i].get_angle())
                                self.release_obj()                          
                                self.onPreset3()

##                        if self.force_stop == "Yes": return


        def force_stop(self):
                self.force_stop = "Yes"

        def onRoll(self,degree):
                [result, pos] = self._interfaceMiddle._ptr().getFeedbackPosCartesian()
                print pos.carPos
                pos.carPos = self.rollZ(pos.carPos, degree)
                print pos.carPos
                self._interfaceMiddle._ptr().moveLinearCartesianAbs(pos)


        def rollX(self,pos, degree):
                s = math.sin(degree/180.0*3.14159)
                c = math.cos(degree/180.0*3.14159)
                
                rot = [[1, 0, 0, 0],[0, c, s, 0],[0, -s, c, 0]]
                res = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]

                for i in range(0, 3):
                        for j in range(0, 3):
                                for k in range(0, 3):
                                        res[i][j] = res[i][j] + pos[k][j] * rot[i][k];

                        res[i][3] = pos[i][3]
                return res

        def rollY(self,pos, degree):
                s = math.sin(degree/180.0*3.14159)
                c = math.cos(degree/180.0*3.14159)
                
                rot = [[c, 0, s, 0],[0, 1, 0, 0],[-s, 0, c, 0]]
                res = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]

                for i in range(0, 3):
                        for j in range(0, 3):
                                for k in range(0, 3):
                                        res[i][j] = res[i][j] + pos[k][j] * rot[i][k];

                        res[i][3] = pos[i][3]
                return res

        def rollZ(self,pos, degree):
                s = math.sin(degree/180.0*3.14159)
                c = math.cos(degree/180.0*3.14159)
                
                rot = [[c, s, 0, 0],[-s, c, 0, 0],[0, 0, 1, 0]]
                res = [[0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0, 0]]

                for i in range(0, 3):
                        for j in range(0, 3):
                                for k in range(0, 3):
                                        res[i][j] = res[i][j] + pos[k][j] * rot[i][k];

                        res[i][3] = pos[i][3]
                return res        
                
        ##
        #
        # The initialize action (on CREATED->ALIVE transition)
        # formaer rtc_init_entry() 
        # 
        # @return RTC::ReturnCode_t
        # 
        #
        def onInitialize(self):
                # Bind variables and configuration variable

                # Set InPort buffers
                self.addInPort("pos",self._posIn)
                
                # Set OutPort buffers
                
                # Set service provider to Ports
                
                # Set service consumers to Ports
                self._OROCHI_InterfaceCommonPort.registerConsumer("interfaceCommon", "ManipulatorCommonInterface_Common", self._interfaceCommon)
                self._OROCHI_InterfaceMiddlePort.registerConsumer("interfaceMiddle", "ManipulatorCommonInterface_Middle", self._interfaceMiddle)
                
                # Set CORBA Service Ports
                self.addPort(self._OROCHI_InterfaceCommonPort)
                self.addPort(self._OROCHI_InterfaceMiddlePort)

                self._val = [0, 0, 0, 0, 0, 0, 0]
                self._posList = []


                return RTC.RTC_OK
        
        #       ##
        #       # 
        #       # The finalize action (on ALIVE->END transition)
        #       # formaer rtc_exiting_entry()
        #       # 
        #       # @return RTC::ReturnCode_t
        #
        #       # 
        #def onFinalize(self, ec_id):
        #
        #       return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The startup action when ExecutionContext startup
        #       # former rtc_starting_entry()
                #       # 
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        #def onStartup(self, ec_id):
        #
        #       return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The shutdown action when ExecutionContext stop
        #       # former rtc_stopping_entry()
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        #def onShutdown(self, ec_id):
        #
        #       return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The activated action (Active state entry action)
        #       # former rtc_active_entry()
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       # 
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        def onActivated(self, ec_id):
        
                return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The deactivated action (Active state exit action)
        #       # former rtc_active_exit()
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        def onDeactivated(self, ec_id):
        
                return RTC.RTC_OK
        
                ##
                #
                # The execution action that is invoked periodically
                # former rtc_active_do()
                #
                # @param ec_id target ExecutionContext Id
                #
                # @return RTC::ReturnCode_t
                #
                #
        def onExecute(self, ec_id):                     
        
                return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The aborting action when main logic error occurred.
        #       # former rtc_aborting_entry()
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        #def onAborting(self, ec_id):
        #
        #       return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The error action in ERROR state
        #       # former rtc_error_do()
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        #def onError(self, ec_id):
        #
        #       return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The reset action that is invoked resetting
        #       # This is same but different the former rtc_init_entry()
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        def onReset(self, ec_id):
        
                return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The state update action that is invoked after onExecute() action
        #       # no corresponding operation exists in OpenRTm-aist-0.2.0
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #

        #       #
        #def onStateUpdate(self, ec_id):
        #
        #       return RTC.RTC_OK
        
        #       ##
        #       #
        #       # The action that is invoked when execution context's rate is changed
        #       # no corresponding operation exists in OpenRTm-aist-0.2.0
        #       #
        #       # @param ec_id target ExecutionContext Id
        #       #
        #       # @return RTC::ReturnCode_t
        #       #
        #       #
        #def onRateChanged(self, ec_id):
        #
        #       return RTC.RTC_OK


def ServiceOROCHIInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=serviceorochi_spec)
    manager.registerFactory(profile,
                            ServiceOROCHI,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    ServiceOROCHIInit(manager)

    # Create a component
    comp = manager.createComponent("ServiceOROCHI")

balloon = None
hand_x = IntVar()
hand_x.set(0)
hand_y = IntVar()
hand_y.set(0)
hand_z = IntVar()
hand_z.set(0)

def main():
        
        val_x = StringVar()
        val_y = StringVar()
        val_z = StringVar()

        model_list = utils.Model_list()
        data = utils.Data()

        root.title("Orochi Interface")

        canvasgroup = Canvas(root, width = 550, height = 520)
        commandgroup = LabelFrame(root, text = 'commands', width = 200, height = 400, labelanchor = NW)
        buttongroup = LabelFrame(commandgroup, text = 'preset buttons', width = 100, height = 300, labelanchor = NW)
        textgroup = LabelFrame(commandgroup, text = 'coordinates', width = 200, height = 300, labelanchor = NW)


        row1 = PanedWindow(buttongroup, orient='horizontal')
        row2 = PanedWindow(buttongroup)
        row3 = PanedWindow(buttongroup)
        row4 = PanedWindow(buttongroup)
        row5 = PanedWindow(buttongroup)
        row6 = PanedWindow(buttongroup)

        row1.pack(expand = True, fill = BOTH)
        row2.pack(expand = True, fill = BOTH)
        row3.pack(expand = True, fill = BOTH)
        row4.pack(expand = True, fill=BOTH)
        row5.pack(expand = True, fill=BOTH)
        row6.pack(expand = True, fill=BOTH)

        mgr = OpenRTM_aist.Manager.init(sys.argv)
#       mgr.setModuleInitProc(MyModuleInit)
        mgr.activateManager()
        profile = OpenRTM_aist.Properties(defaults_str=serviceorochi_spec)
        mgr.registerFactory(profile,
                            ServiceOROCHI,
                            OpenRTM_aist.Delete)

        comp = mgr.createComponent("ServiceOROCHI")
        
        ###Create Orochi_canvas
        utils.Orochi_Canvas.canvas = canvasgroup
        orochi_canvas = utils.Orochi_Canvas()
        canvasgroup.create_text(470,25,text = "Gripper Coordinates")
##        comp.get_hand_position()
        canvasgroup.create_text(470,40,text = ("x = %d, y = %d, z = %d" % (hand_x.get(), hand_y.get(), hand_z.get())))

        utils.CanvasItem.canvas = canvasgroup

        for i in range(3):
                for j in range(2):                
                        model_list.add_model(utils.CanvasRectangle(30 + j*(190/2), 280 + i*30,180/2,12/2, fill="red", width=0))


        Button(row1, text='initialize', width=10, height=2, command=lambda:comp.onPreset1() ).pack(in_=row1, side=LEFT, expand=True, fill=BOTH)
        Button(row1, text='', width=10, height=2 ).pack(in_=row1, side=LEFT, expand=True, fill=BOTH)
        Button(row2, text='home1', width=10, height=2, command=lambda:comp.onPreset2() ).pack(in_=row2, side=LEFT, expand=True, fill=BOTH)
        Button(row2, text='home2', width=10, height=2,command=lambda:comp.onPreset3() ).pack(in_=row2, side=LEFT, expand=True, fill=BOTH)
        Button(row3, text='read maze', width=10, height=2).pack(in_=row3, side=LEFT, expand=True, fill=BOTH)
        Button(row3, text='write maze', width=10, height=2).pack(in_=row3, side=LEFT, expand=True, fill=BOTH)
        Button(row4, text='PTP Start', width=10, height=2,command=lambda:comp.pick_and_place(model_list)).pack(in_=row4, side=LEFT, expand=True, fill=BOTH)
        Button(row4, text='STOP', width=10, height=2).pack(in_=row4, side=LEFT, expand=True, fill=BOTH)
        Button(row5, text='create object', width=10, height=2).pack(in_=row5, side=LEFT, expand=True, fill=BOTH)
        Button(row5, text='delete object', width=10, height=2).pack(in_=row5, side=LEFT, expand=True, fill=BOTH)

        Button(textgroup, text = 'send', width=10, height=2,command=lambda:comp.move_by_coordinate(
                eval(val_x.get()),eval(val_y.get()),eval(val_z.get()))).pack(in_=textgroup, side=BOTTOM, expand=True, fill=BOTH)
        Entry(textgroup,text = "x",width = 10, textvariable = val_x).pack(in_=textgroup, side=BOTTOM, expand=True)
        Entry(textgroup,text = "y",width = 10, textvariable = val_y).pack(in_=textgroup, side=BOTTOM, expand=True)
        Entry(textgroup,text = "z",width = 10, textvariable = val_z).pack(in_=textgroup, side=BOTTOM, expand=True)

        canvasgroup.pack(expand = True,padx=5, pady=5, side=LEFT)
        commandgroup.pack(expand = True,padx=5, pady=5, side=LEFT)
#       mazegroup.pack(expand = True,padx=5, pady=5, side=RIGHT)
        buttongroup.pack(expand=True, padx=5, pady=5, side=LEFT)
        textgroup.pack(expand=True, padx=5, pady=5, side=BOTTOM)

        mgr.runManager(True)

        root.mainloop()

if __name__ == "__main__":
        main()

