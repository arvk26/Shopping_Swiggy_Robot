####ROBOT-FRAMEWORK INSTALLATION:
- **1. install ActivePython-2.7.2.5-win64-x64.msi
- **2. pip install robotframework
- **3. pip install robotframework-selenium2library
- **4. Install robotframework-ride.exe
- **5. put chromedriver.exe in folder c:\Python27 folder - This folder is in path variable so no need to mention this while browser initialization

####How to execute:
##Approach-1:
 - ** Open RIDE(step#4), Load swiggy project and select suite namely Swiggy and click on start button on this tool.

##Approach-2:
 - ** open cmd.exe and type below command:
 - ** pybot.bat --outputdir c:\project\Logs --debugfile execution --listener C:\Python27\lib\site-packages\robotide\contrib\testrunner\TestRunnerAgent.py:49172:False C:\Project\Swiggy.robot
 - ** Execution log will be present under folder : c:\project\Logs