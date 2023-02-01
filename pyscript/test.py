#coding=utf-8

import subprocess


p = subprocess.Popen(['ls','-al'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()
print(out)