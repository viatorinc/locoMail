__author__ = 'jmoriano'
import threading
import asyncore
from mailServer import FakeSMTPServer

class ThreadedSMTP(object):
    def start(self, port):
        """Start the listening service"""
        # here I create an instance of the SMTP server, derived from  asyncore.dispatcher
        self.smtp = FakeSMTPServer(('0.0.0.0', port), None)
        # and here I also start the asyncore loop, listening for SMTP connection, within a thread
        # timeout parameter is important, otherwise code will block 30 seconds after the smtp channel has been closed
        self.thread = threading.Thread(target=asyncore.loop, kwargs={'timeout': 1})
        self.thread.start()

    def stop(self):
        """Stop listening now to port 25"""
        # close the SMTPserver to ensure no channels connect to asyncore
        self.smtp.close()
        # now it is save to wait for the thread to finish, i.e. for asyncore.loop() to exit
        self.thread.join()

    # now it finally it is possible to use an instance of this class to check for emails or whatever in a non-blocking way
    def count(self):
        """Return the number of emails received"""
        return len(self.smtp.emails)

    def get(self):
        """Return all emails received so far"""
        return self.smtp.emails