#!/usr/bin/python

#    Licensed to the Apache Software Foundation (ASF) under one
#    or more contributor license agreements.  See the NOTICE file
#    distributed with this work for additional information
#    regarding copyright ownership.  The ASF licenses this file
#    to you under the Apache License, Version 2.0 (the
#    "License"); you may not use this file except in compliance
#    with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing,
#    software distributed under the License is distributed on an
#    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#    KIND, either express or implied.  See the License for the
#    specific language governing permissions and limitations
#    under the License.
#
#    Contributor: Kyo Lee kyo.lee@eucalyptus.com

import re
import sys
import xmlrpclib
import commands
import paramiko
import ConfigParser

class Metaleuca:

	### STATIC VARIABLE
	GROUP_FILE = "./var/machine_map_for_new_datacenter.lst"
	CONFIG_FILE = "./var/metaleuca.ini"

	### CLASS VARIABLE
	cobbler_server = ""
	cobbler_user = ""
	cobbler_password = ""

	target_owner = "qa"
	metaleuca_dir = "/home/qa-group/metaleuca"

	def __init__(self):
		Config = ConfigParser.ConfigParser()
		Config.read(self.CONFIG_FILE)

		self.cobbler_server = Config.get("CobblerInfo", "COBBLER_SERVER")
		self.cobbler_user = Config.get("CobblerInfo", "USER")
		self.cobbler_password = Config.get("CobblerInfo", "PASSWORD")

		self.target_owner = Config.get("CobblerInfo", "OWNER")
		if( self.target_owner == ""):
			self.target_owner = "qa"
		self.metaleuca_dir = Config.get("MetaleucaInfo", "METALEUCA_DIR")
                if( self.metaleuca_dir == ""):
                        self.metaleuca_dir = "/home/qa-group/metaleuca"
		return
		
	def connect(self):
		remote = xmlrpclib.Server("http://" + self.cobbler_server + "/cobbler_api")
		token = remote.login(self.cobbler_user, self.cobbler_password)
		return remote, token


	def connect_to_cobbler(self, server, username, password):
	    	"""
	    	Make the connection to the cobbler server that will be used for the
	    	all operations on the system. This will keep from having to make a 
	    	connection everytime we perform an operation on the server and should
	    	keep a (possible) huge connection load on the cobbler server

	    	server -- The IP or FQDN of the cobbler server
	    	username -- Username with admin rights on the cobbler server
	    	password -- Password of the corresponding username above
	    	"""
	    	remote = xmlrpclib.Server("http://" + server + "/cobbler_api")
	    	token = remote.login(username, password)

	    	return remote, token


	def display_distros(self, server):
		for x in server.get_distros():
			name = x['name']
			os_version = x['os_version']
			kernel = x['kernel']
			initrd = x['initrd']
			print "NAME: " + name + " OS_VERSION: " + os_version + " KERNEL: " + kernel + " INITRD: " + initrd


	def display_profiles(self, server):
		for x in server.get_profiles():
			name = x['name']
			kickstart = x['kickstart']
			distro = x['distro']
			print "NAME: " + name + " DISTRO: " + distro + " KICKSTART: " + kickstart


	def display_systems(self, server):
		for x in server.get_systems():
			name = x['name']
			hostname = x['hostname']
			profile = x['profile']
			status = x['status']
			netboot_enabled = x['netboot_enabled']
			owner = ""
			if len(x['owners']) > 0:
				owner = x['owners'][0]			
			for device in x['interfaces']:
				if device == "eth0" or device == "em1":
					ip = x['interfaces'][device]['ip_address']
					mac = x['interfaces'][device]['mac_address']
		#	if re.match(r"^qa$", owner): 
			if owner == self.target_owner:
				print "Name: " + name + " OWNER: " + owner + " IP: " + ip + " MAC: " + mac + " HOSTNAME: " + hostname + " PROFILE: " + profile + " NETBOOT_ENABLED: " + str(netboot_enabled)


	def display_system_found_by_name(self, server, targetname):
		for x in server.get_systems():
			name = x['name']
			if name == targetname: 
				hostname = x['hostname']
				profile = x['profile']
				status = x['status']
				netboot_enabled = x['netboot_enabled']
				for device in x['interfaces']:
					if device == "eth0" or device == "em1":
						ip = x['interfaces'][device]['ip_address']
						mac = x['interfaces'][device]['mac_address']
				print "Name: " + name + " IP: " + ip + " MAC: " + mac + " HOSTNAME: " + hostname + " PROFILE: " + profile + " STATUS: " + status + " NETBOOT_ENABLED: " + str(netboot_enabled)

	def display_group_by_name(self, server, token, group):
		cmd = "cat " + self.GROUP_FILE				###	QUICK HACK, Prefers DB
		if group is "_ALL":
			print commands.getoutput(cmd)
		else:
			cmd = cmd + " | grep " + group
			print commands.getoutput(cmd)


	def get_system_ip_found_by_name(self, server, targetname):
		for x in server.get_systems():
			name = x['name']
			if name == targetname: 
				hostname = x['hostname']
				for device in x['interfaces']:
					if device == "eth0" or device == "em1":
						ip = x['interfaces'][device]['ip_address']
						return ip
		return "None"

	def get_system_name_found_by_ip(self, server, targetip):
		for x in server.get_systems():
			name = x['name']
			for device in x['interfaces']:
				if device == "eth0" or device == "em1":
					ip = x['interfaces'][device]['ip_address']
					if ip == targetip: 
						return name
		return "None"


	def validate_system_by_name(self, server, targetname):
		output = server.find_system({"name":targetname})
		if len(output) > 0:
			return True
		else:
			return False

	def validate_system_by_ip(self, server, targetip):
		output = server.find_system({"ip":targetip})
		if len(output) > 0:
			return True
		else:
			return False

	def validate_profile_by_name(self, server, targetname):
		output = server.find_profile({"name":targetname})
		if len(output) > 0:
			return True
		else:
			return False

	
	def change_system_found_by_name_modify_its_profile(self, server, token, name, profile):
		print "MODIFY SYSTEM'S PROFILE"
		print "name: " + name + " profile: " + profile 
		handle = server.get_system_handle(name,token)
		server.modify_system(handle, "profile", profile, token)
		server.sync(token)
		self.display_system_found_by_name(server, name)

	def change_system_found_by_name_set_its_netboot_enabled(self, server, token, name, flag):
		print "MODIFY SYSTEM'S NETBOOT_ENABLED"
		print "name: " + name + " netboot_enabled: " + flag 
		handle = server.get_system_handle(name,token)
		server.modify_system(handle, "netboot_enabled", flag, token)
		server.sync(token)
		self.display_system_found_by_name(server, name)

	def power_system_reboot_by_name(self, server, token, name):
		print "POWER SYSTEM: REBOOT"
		print "name: " + name + " power: reboot" 
		handle = server.get_system_handle(name,token)
		server.power_system(handle,'reboot',token)			###	Cobbler Power Management API, but not set for this prototype setup
		server.sync(token)
		exit()
		ip = self.get_system_ip_found_by_name(server, name)
		if ip is "None":
			print "Unable to map ip to name: " + name
			exit()
		username="root"
		password="123qwe"
		client = paramiko.SSHClient()
		client.load_system_host_keys()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		try:
			client.connect(ip, username=username, password=password)
			client.exec_command('reboot -f')
		except:
			print "Reboot Failed"
			client.close()
			exit()
		self.display_system_found_by_name(server, name)


def main():

	COBBLER_SERVER = "192.168.62.1"
	USER = "cobbler"
	PASSWORD = "cobbler"

	metaleuca = Metaleuca();

	server, token = metaleuca.connect_to_cobbler(COBBLER_SERVER, USER, PASSWORD)
	print

	if len(sys.argv) > 1 and sys.argv[1] == "--list-all":
		print "DISPLAY DISTROS"
		metaleuca.display_distros(server)
		print

		print "DISPLAY PROFILES"
		metaleuca.display_profiles(server)
		print

	print "DISPLAY SYSTEMS"
	metaleuca.display_systems(server)
	print

	metaleuca.change_system_found_by_name_modify_its_profile(server, token, "r2-25", "es-ubuntu12_04-x86_64")
	print

	metaleuca.change_system_found_by_name_set_its_netboot_enabled(server, token, "r2-25", "True")
	print

	metaleuca.change_system_found_by_name_set_its_netboot_enabled(server, token, "r2-25", "False")
	print


if __name__ == "__main__":
    main()
    exit

