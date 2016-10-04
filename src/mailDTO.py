__author__ = 'jmoriano'


class MailWrapper(object):
    """
    Just a simple class to encapsulate a mail message
    """

    def __init__(self, id, subject, from_address, to_address, text, html, date, attachments: []):
        self.from_address = from_address
        self.to_address = to_address
        self.text = text
        self.html = html
        self.attachments = attachments
        self.id = id
        self.date = date
        self.subject = subject

    @staticmethod
    def from_row(rs):
        return MailWrapper(rs[0], rs[1], rs[2], rs[3], rs[4], rs[5], rs[6], [])

    def set_attachments(self, attachments: []):

        self.attachments = attachments

    def as_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'text': self.text,
            'html': self.html,
            'date': self.date,
            'attachments': self.attachments
        }

