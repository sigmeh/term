#!/usr/bin/env python
import cgi
import subprocess as sp
#import session_server
import json
import os
import sys
print

def test(data):
	with open('TEST','w') as f:
		f.write(data)

class commands(object):	
	def __init__(self):
		pass
	
	def up(self,current_dir,new_cmd):
		'''Move up file hierarchy one unit (unless at root dir); `ls` new dir contents'''	
		if current_dir != '/':
			current_dir = '/'.join(current_dir.split('/')[:-1])
			if not current_dir:
				current_dir = '/'
		self.ls(current_dir,new_cmd)
		return current_dir
	
			
	def ls(self,current_dir,new_cmd):
		'''Perform `ls` operation on current_dir'''
		result = sp.Popen('ls '+' '.join(new_cmd.split(' ')[1:])+' '+current_dir,stdout=sp.PIPE,shell=True).communicate()[0]
		print json.dumps({'data':result,'current_dir':current_dir})	
		return current_dir
	
	
	def cd(self,current_dir,new_cmd):
		'''Change directory'''
		if new_cmd.split()[1] == '..':
			current_dir = '/'.join(current_dir.split('/')[:-1])
			data = ''
		else:		
			files = sp.Popen(('ls '+current_dir).split(),stdout=sp.PIPE).communicate()[0]
			
			if new_cmd.split()[1] in files.split():
				current_dir = current_dir + '/' + new_cmd.split()[1]
				data = ''
			else:
				data = 'Directory not found'
		print json.dumps({'data':data,'current_dir':current_dir})
		return current_dir
	
	
	def pwd(self,current_dir,new_cmd):
		print json.dumps({'data':current_dir,'current_dir':current_dir})
		return current_dir
	
cmds = commands()		




def main():
	
	new_cmd = json.loads(cgi.FieldStorage()['package'].value)

	if new_cmd == 'new session':
		current_dir = os.path.dirname(os.path.abspath(__file__))
		current_session = {'history':[],'current_dir':current_dir}
		with open('current_session','w') as f:
			f.write(json.dumps(current_session))

		print json.dumps({'data':'session started','current_dir':current_dir})
	
	else:
		
		with open('current_session','r') as f:
			current_session = json.loads(f.read())
		current_dir = current_session['current_dir']
		history = current_session['history']
		cmd0 = new_cmd.split(' ')[0]
	
		if cmd0 in [x for x in dir(cmds) if not x.startswith('__')]:
			current_dir = getattr(cmds,cmd0)(current_dir=current_dir,new_cmd=new_cmd)	
	
		else:
			result = sp.Popen(new_cmd,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
			stdout,stderr=result.communicate()
			if stdout:
				data = stdout
			else:
				data = stderr
			
			print json.dumps({'data':data,'current_dir':current_dir})
		
		history.append(new_cmd)
		current_session = {'history':history,'current_dir':current_dir}
		with open('current_session','w') as f:
			f.write(json.dumps(current_session))
		

if __name__ == '__main__':
	main()