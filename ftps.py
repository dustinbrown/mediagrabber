''' ftp class '''
from ftplib import FTP_TLS

class Ftps(object):
    def __init__(self, host, username, passwd):
        self.host = host
        self.username = username
        self.passwd = passwd

    def connect(self):
        ftps = FTP_TLS(self.host)
        ftps.login(self.username, self.passwd)

        # switch to secure data connection..
        # IMPORTANT!
        # Otherwise, only the user and password is encrypted and not all the file data.
        ftps.prot_p()
        return ftps
