import ftplib


class FTP:
    def __init__(self):
        session = ftplib.FTP('', '', 'Hdms20?6')
        file = open('test.txt', 'rb')  # file to send
        session.storbinary('STOR test.txt', file)  # send the file
        file.close()  # close file and FTP
        session.quit()
