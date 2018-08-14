import os

statvfs = os.statvfs('/')

print statvfs.f_frsize * statvfs.f_bfree
