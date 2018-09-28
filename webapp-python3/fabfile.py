#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, re
from datetime import datetime

from fabric.api import *

env.user = 'ubuntu'
#env.sudo_user = 'root'
#env.password = '#########'
env.hosts = ['132.232.190.33']
env.key_filename = r'C:\Users\ldwzy\.ssh\webappssh\webapp'

db_user = 'root'
db_password = '######'

_TAR_FILE = 'dist-awesome.tar'

def build():#打包 在win7系统开发，使用HaoZip软件打包文件
    #includes = ['static', 'templates', 'transwrap', 'favicon.ico', '*.py']
    includes = ['static', 'templates', 'transwrap', '*.py']
    excludes = ['test', '.*', '*.pyc', '*.pyo']
    #local('rm -f dist/%s' % _TAR_FILE)
    if os.path.isfile(r'dist\%s' % _TAR_FILE):    
        local(r'del dist\%s' % _TAR_FILE)
    with lcd(os.path.join(os.path.abspath('.'), 'www')):
        '''    
        cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))
        '''
        cmd = ['HaoZipC a', '-ttar', '..\dist\%s -r' % _TAR_FILE]
        cmd.extend(includes)
        cmd.extend(['-x!%s' % ex for ex in excludes])
        local(' '.join(cmd))

_REMOTE_TMP_TAR = '/home/ubuntu/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/home/ubuntu/srv/awesome'

def deploy(): #
    newdir = 'www-%s' % datetime.now().strftime('%y-%m-%d_%H_%M_%S')   
    run('rm -f %s' % _REMOTE_TMP_TAR)
    put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('mkdir %s' % newdir)
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        sudo('tar -xvf %s' % _REMOTE_TMP_TAR)
    with cd(_REMOTE_BASE_DIR):
        sudo('rm -f www')
        sudo('ln -s %s www' % newdir)
        sudo('chown www-data:www-data www')
        sudo('chown -R www-data:www-data %s' %newdir)
    with settings(warn_only=True):
        sudo('supervisorctl stop awesome')    
        sudo('supervisorctl start awesome')    
        sudo('/etc/init.d/nginx reload')    
        
def test_run():
    #run('ls -al')   
    #put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)    
    #put(r'dist/dist-awesome.tar', _REMOTE_TMP_TAR)    
    local('del ./dist/%s' % _TAR_FILE)    
    
def main():
    build()

if __name__ == '__main__':
    main()    
    