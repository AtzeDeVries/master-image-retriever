#!/bin/sh
/usr/bin/python2.7 ./setter.py  > /dev/null &
/usr/bin/python2.7 ./get_master.py > /dev/null &
/usr/bin/python2.7 ./other.py > /dev/null &
