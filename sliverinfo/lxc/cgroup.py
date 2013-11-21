import os

class CGroupNotFound(Exception):
	pass

class CGroupNoSuchValue(Exception):
	pass

class cgroup:
	"""Get Cgroups"""
	def __init__(self,metric, name,basepath="/sys/fs/cgroup"):
		self.cgroup=basepath+'/'+ metric + '/lxc/' +name
		if not os.path.isdir(self.cgroup):
			raise CGroupNotFound


	def getValue(self,name):
		try:
			return open(self.cgroup+'/'+name).read().rstrip('\n')
		except:
			raise CGroupNoSuchValue
			
