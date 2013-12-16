echo off
setlocal
for %%I in (python.exe) do if exist %%~$path:I set f=%%~$path:I
if exist %f% do (
  %f:python.exe=%omniidl.exe -bpython -I"%RTM_ROOT%rtm\idl" -I"C:\Users\Arthur\Desktop\OpenRTM\workspace\idl" -I"C:\Users\Arthur\Desktop\産総研\OROCHI\liborochi\rtm\OrochiRTC\idl" idl/ManipulatorCommonInterface_Common.idl idl/ManipulatorCommonInterface_MiddleLevel.idl 
) else do (
  echo "python.exe" can not be found.
  echo Please modify PATH environmental variable for python command.
)
endlocal
