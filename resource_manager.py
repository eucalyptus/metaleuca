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
import commands
import MySQLdb as mdb
import ConfigParser

class ResourceManager:

	### STATIC VARIABLE
	GROUP_FILE = "./var/machine_map_for_new_datacenter.lst"
	CONFIG_FILE = "./var/metaleuca.ini"

	### CLASS VARIABLE
	db_host = ""
	db_user = ""
	db_password = ""
	db_name = ""

	def __init__(self):
		Config = ConfigParser.ConfigParser()
		Config.read(self.CONFIG_FILE)

		self.db_host = Config.get("DBInfo", "HOST")
		self.db_user = Config.get("DBInfo", "USER")
		self.db_password = Config.get("DBInfo", "PASSWORD")
		self.db_name = Config.get("DBInfo", "NAME")

		return

	def display_group_by_name(self, group):
		cmd = "cat " + self.GROUP_FILE				###	QUICK HACK, Prefers DB
		if group is "_ALL":
			return commands.getoutput(cmd)
		else:
			cmd = cmd + " | grep " + group
			return commands.getoutput(cmd)


	def display_only_freed_group_by_name(self, group):
		grouplist = self.display_group_by_name(group)
		freed = self.display_user_by_name("FREED")
		freed_systems = freed.split('\n')
		freedhash = {}
		for freed_system in freed_systems:
			words = freed_system.split()
			ip = words[0]
			freedhash[ip] = 1
		glist = grouplist.split('\n')
		message = ""
		for g in glist:
			gwords = g.split()
			if len(gwords) > 0:
				this_ip = gwords[0]
				this_group = gwords[1]
				if this_ip in freedhash.keys():
					message += this_ip + "\t" + this_group + "\tFREED\n"
		return message.rstrip()


	def display_user_by_name(self, user):
		con = mdb.connect(self.db_host, self.db_user, self.db_password, self.db_name);
		with con: 
    			cur = con.cursor(mdb.cursors.DictCursor)
			if user is "_ALL":
    				cur.execute("SELECT ip, owner FROM reserve_machine_pool_records")
			else:
				cur.execute("SELECT ip, owner FROM reserve_machine_pool_records WHERE owner='" + user + "'")
			rows = cur.fetchall()
			message = ""
			if len(rows) == 0:
				message = "No system under user: " + user
			else:
				for row in rows:
					message += "%s\t%s\n" % (row["ip"], row["owner"])
			return message.rstrip()
		
