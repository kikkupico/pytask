import unittest
from AsyncProcessRunner import run_command_async
import asyncio
import sys

class TestAsyncProcessRunner(unittest.TestCase):
    def test_phat_execution_simple(self):
        d = ""
        filler = ""
        tcname = ""
        prop_file = ""
        device_type = ""
        work_dir = ""

        cmd = "java -jar -Xms512m -Xmx1024m ../jmeter/bin/ApacheJMeter.jar -n -t " + d + filler + "../PHSanityTestRunner.jmx -l ../jmeter/test_results/" + tcname + ".jtl -j ../logs/" + tcname + "/" + tcname + ".log -L DEBUG -J JMETER_LOG_FILE_NAME='../logs/" + tcname + ".log' -q " + prop_file + " -q resources/helper.properties -q resources/report.properties -q resources/customers/" + device_type + ".properties -q resources/valdationMessages.properties -q resources/ResoureObjects.properties -q resources/user_save_service.properties -J xmlScriptFileName=" + tcname + " -J xmlScriptLocation=" + d + " -G includecontroller=" + work_dir + "/../jmeter/ -G ctat_basedir=" + work_dir + "/../jmeter/"
        if sys.platform == 'win32':
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(run_command_async(loop, cmd)))


