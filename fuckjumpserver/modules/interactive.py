# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.


import socket
import sys
from paramiko.py3compat import u
from models import models
import datetime
import queue

# windows does not have termios...
try:
    import termios
    import tty

    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, user_obj, bind_host_obj, cmd_caches, log_recording):
    if has_termios:
        posix_shell(chan, user_obj, bind_host_obj, cmd_caches, log_recording)
    else:
        windows_shell(chan,user_obj, bind_host_obj, cmd_caches, log_recording)


def posix_shell(chan, user_obj, bind_host_obj, cmd_caches, log_recording):
    import select

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        cmd = ''

        tab_key = False
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if tab_key:
                        if x not in ('\x07', '\r\n'):
                            # print('tab:',x)
                            cmd += x
                        tab_key = False
                    if len(x) == 0:
                        sys.stdout.write('\r\n*** EOF\r\n')
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if '\r' != x:
                    cmd += x
                else:

                    print('cmd->:', cmd)
                    log_item = models.AuditLog(user_id=user_obj.id,
                                               bind_host_id=bind_host_obj.id,
                                               action_type='cmd',
                                               cmd=cmd,
                                               date=datetime.datetime.now()
                                               )
                    cmd_caches.append(log_item)
                    cmd = ''

                    if len(cmd_caches) >= 10:
                        log_recording(user_obj, bind_host_obj, cmd_caches)
                        cmd_caches = []
                if '\t' == x:
                    tab_key = True
                if len(x) == 0:
                    break
                chan.send(x)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


# thanks to Mike Looijmans for this code
def windows_shell(chan,user_obj, bind_host_obj, cmd_caches, log_recording):
    import threading
    cmd_queue=queue.Queue()
    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")

    def writeall(sock,user_obj, bind_host_obj,log_recording):
        while True:
            data = sock.recv(256)
            if not data:
                cmd_caches =[]
                while cmd_queue.qsize() >0:
                    cmd_caches.append(cmd_queue.get())
                log_recording(user_obj, bind_host_obj, cmd_caches)
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()

    writer = threading.Thread(target=writeall, args=(chan,user_obj, bind_host_obj,log_recording))
    writer.start()

    try:
        cmd = ''
        tab_key = False
        while True:
            d = sys.stdin.read(1)
            if tab_key:
                if d not in ('\x07', '\n'):
                    # print('tab:',x)
                    cmd += d
                tab_key = False
            if '\n' != d:
                cmd += d
            else:
                log_item = models.AuditLog(user_id=user_obj.id,
                                           bind_host_id=bind_host_obj.id,
                                           action_type='cmd',
                                           cmd=cmd,
                                           date=datetime.datetime.now()
                                           )
                cmd_caches.append(log_item)
                cmd_queue.put(log_item)
                cmd = ''

                if len(cmd_caches) >= 10:
                    log_recording(user_obj, bind_host_obj, cmd_caches)
                    cmd_caches = []
                    cmd_queue.queue.clear()
            if '\t' == d:
                tab_key = True
            if not d:
                break
            chan.send(d)
    except EOFError:
        # user hit ^Z or F6
        pass
