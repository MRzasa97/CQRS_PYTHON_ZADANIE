import abc
import smtplib
from reportMailer import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class AbstractNotifications(abc.ABC):

    @abc.abstractmethod
    def send(self, destination, message):
        raise NotImplementedError


DEFAULT_HOST = config.get_email_host_and_port()['host']
DEFAULT_PORT = config.get_email_host_and_port()['port']



class EmailNotifications(AbstractNotifications):

    def __init__(self, smtp_host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.server = smtplib.SMTP(smtp_host, port=port)
        self.server.noop()

    def send(self, destination, message):
        html_table = "<html><body><table border='1'>"
        lines = message.strip().split('\n')
        for line in lines:
            html_table += "<tr>"
            cells = line.split(',')
            for cell in cells:
                html_table += f"<td>{cell}</td>"
            html_table += "</tr>"
        html_table += "</table></body></html>"

        msg = MIMEMultipart()
        msg.attach(MIMEText(html_table, 'html'))

        msg['Subject'] = 'example service notification'
        msg['From'] = 'example@example.com'
        msg['To'] = destination

        self.server.sendmail(
            from_addr='example@example.com',
            to_addrs=[destination],
            msg=msg.as_string()
        )

        # msg = f'Subject: example service notification\n<html><body><p>{message}</p></body></html>'
        # self.server.sendmail(
        #     from_addr='example@example.com',
        #     to_addrs=[destination],
        #     msg=msg
        # )
