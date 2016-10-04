__author__ = 'jmoriano'
# See https://muffinresearch.co.uk/fake-smtp-server-with-python/


import smtpd
import asyncore
from mailDAO import MailDAO
from mailDTO import MailWrapper
from email.parser import Parser


class FakeSMTPServer(smtpd.SMTPServer):
    """A Fake smtp server"""

    def __init__(*args, **kwargs):
        print("Running fake smtp server on port")
        smtpd.SMTPServer.__init__(*args, **kwargs)

    def process_message(self, peer, mailfrom, rcpttos, data, *args, **kwargs):
        mail_dao = MailDAO()
        received_message = Parser().parsestr(data)
        print("-----------------------------------------------")
        mail_contents = data
        text = ""
        html = ""
        files = {}  # Key is file name, value is file contents
        if received_message.is_multipart():
            for part in received_message.get_payload():
                if part.get_filename():
                    files[part.get_filename()] = part.get_payload()
                elif 'html' in part['content-type']:
                    html = part.get_payload()
                else:
                    text = part.get_payload()
        print("Incoming message!!!")
        print("\tSubject %s" % str(received_message['subject']))
        print("\tPeer %s" % str(peer))
        print("\tMail from %s" % str(mailfrom))
        print("\tRCPTtos %s" % str(rcpttos))

        if files:
            print("\tMail contained files... File contents not displayed in console...")
            for file in files.keys():
                print("\t\tFile name => %s" % file)

        print("\tTEXT %s" % str(text))
        print("\tHTML %s" % str(html))
        for recipient in rcpttos:
            mail_wrapper = MailWrapper(-1, received_message['subject'], mailfrom, recipient, text, html, None, files.keys())
            mail_id = mail_dao.store(mail_wrapper)
            if files:
                mail_dao.store_attachments(mail_id, files)

if __name__ == "__main__":

    smtp_server = FakeSMTPServer(('localhost'), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        smtp_server.close()