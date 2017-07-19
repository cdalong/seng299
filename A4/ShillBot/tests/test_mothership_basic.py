
import unittest

from mothership.base import MothershipServer
from workers.basic_worker import BasicUserParseWorker


class TestMothershipBasic(unittest.TestCase):
    pass

    #mothership starts to listen on the specified port
    #receives data from workers


    def testMothershipconnection(self):

        mothership = MothershipServer()

        mothership.run()

        self.assertRaises(ConnectionRefusedError, mothership.run)

    def workercanconnect(self):

        mothership = MothershipServer()

        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        mothership.run()


        try:
            worker.run()
        except:

            self.fail("worker didn't work")

    def receivesdata(self):

        mothership = MothershipServer()
        worker = BasicUserParseWorker("https://www.reddit.com/user/Chrikelnel")

        mothership.run()
        worker.run()

        worker.send_to_mother(None,mothership)

        self.assertRaises(ValueError, worker.send_to_mother(None,mothership)
