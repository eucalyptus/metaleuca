Metaleuca
=========

Metaleuca is a bare-metal provision management system that utilizes open-source software Cobbler via EC2-like CLI API

i.e.

metaleuca-run-instances

metaleuca-describe-instances

metaleuca-terminate-instances

...

Using Metaleuca, a user can select an image(profile) and a set of bare-metal machines(systems), then launch those machines to boot up with the selected image using the command-line tools that feel very much like the EC2 tools, or euca2ools. In other words, instead of launching virtual instances, the user is able to self-provision bare-metal instances, which are managed like EC2 instances.

## Open Source Licence ##

Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements. 

## What are the components of Metaleuca? ##

### Metaleuca Service Layer (Metaleuca SLayer) ###

Metaleuca Service Layer, a.k.a Metaleuca Slayer, is a lightweight service layer that manages sequencing of operations that handles launching of bare-metal instances, keeping track of status and resources, and terminating instances; all the information is maintained in Metaleuca's own database that is external to Cobbler's database.

### Metaleuca2ools ###

Metaleuca2ools is a set of CLIs that are exposed to users so that they can directly interact with Metaleuca, similar to EC2 tools and euca2ools.

## METALEUCA COMMANDS ##

### INTERNAL COMMANDS ###

metaleuca-describe-distros  	- describe all distros on Cobbler

metaleuca-describe-profiles		- describe all profiles on Cobbler

metaleuca-describe-systems		- describe all systems on Cobbler

metaleuca-set-profile			- set profile of the target system

metaleuca-reboot-system			- reboot the target system

metaleuca-enable-netboot		- enable netboot of the target system

metaleuca-disable-netboot		- disable netboot of the target system

metaleuca-describe-system-groups	- describe system groups; written in a text file for now

metaleuca-reserve-systems		- reserve systems under user; need to talk to DB

metaleuca-release-systems		- release systems by IPs; unclear if it is the right way to do; need to talk to DB

### COMMANDS EXPOSED TO USERS ###

metaleuca-run-instances			- takes # of instances, group name, profile name, and user name; initate entire provisioning sequence

metaleuca-describe-instances		- need to display matching information as ec2

metaleuca-terminate-instances		- terminate by user name and ip list; need to set the status to "terminated"

metaleuca.py				- main class

### DIRECTORY ###

var					- holds various text files for now

### ETC ###

metaleuca.pyc

metaleuca.py_backup0

talktocobbler.py



## TO DO ##

Need to be able to run instances using IPs -- DONE 090312

Need a way to handle reboot and identify reboot has taken place

Need a way to keep status of running instances

Need a DB to track the status rather than relying on "netboot_enabled" flag.

Need a way to run instances by providing more than one group -- DONE 090312

Need a way to determine when "pending" should become "failed"

Need to track time and timeout per instance run

Need to be able to use IPs directly rather than using name for most calls

## GOOD TO HAVE ##

Use a credentials file, similar to "eucarc" to hold username, prefered group, cobbler ip, username and password

Convert perl scripts into python scripts

Create a separate DB that is configurable

Use NoSQL

Provide Guideline on how to set up Cobbler server

