Metaleuca
=========

Metaleuca is a bare-metal provision management system that interacts with open-source software Cobbler via EC2-like CLIs. Using Metaleuca, a user can trigger Cobbler to initiate a group of bare-metal machines to boot up with new, fresh OS images. In other words, Metaleuca allows users to self-provision bare-metal machines and manage them like EC2, or Eucalyptus, virtual instances via the command-lines that feel much like ec2-tools or euca2ools.

## Open Source Licence ##

Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements. 

## Installation Guide ##

https://github.com/eucalyptus/metaleuca/wiki/Metaleuca-Installation-Guide

## What are the components of Metaleuca? ##

### Metaleuca Service Layer (Metaleuca SLayer) ###

Metaleuca Service Layer, a.k.a Metaleuca Slayer, is a lightweight service layer that manages sequencing of the bare-metal provision operations and maintaining the statuses -- all the information is maintained in Metaleuca's own database, which is external to Cobbler's database.

### Metaleuca2ools ###

Metaleuca2ools is a set of CLIs that are exposed to users so that they can directly interact with Metaleuca, similar to EC2-tools and euca2ools.

## METALEUCA COMMANDS ##

metaleuca-describe-distros  	- Describe all distros in Cobbler

metaleuca-describe-profiles		- Describe all profiles in Cobbler

metaleuca-describe-systems		- Describe all systems in Cobbler

metaleuca-set-profile			- Set the profile of the selected system

metaleuca-reboot-system			- Reboot the selected system

metaleuca-enable-netboot		- Enable the netboot of the selected system

metaleuca-disable-netboot		- Disable the netboot of the selected system

metaleuca-describe-system-groups	- Describe the system groups

metaleuca-reserve-systems		- Reserve the selected systems

metaleuca-release-systems		- Release the selected systems

metaleuca-run-instances			- Initate the provision sequence

metaleuca-describe-instances		- Describe the statuses of the provisioned systems

metaleuca-terminate-instances		- Terminated the provisioned systems, returning them back to the resource pool

### DIRECTORY ###

var - Stores the configuration files

## TO DO ##

Need to be able to run instances using IPs -- DONE 090312

Need a way to handle reboot and identify reboot has taken place

Need a way to keep status of running instances

Need a DB to track the status rather than relying on "netboot_enabled" flag.

Need a way to run instances by providing more than one group -- DONE 090312

Need a way to determine when "pending" should become "failed"

Need to track time and timeout per instance run

Need to be able to use IPs directly rather than using name for most calls -- DONE 011313

Use a credentials file, similar to "eucarc" to hold username, prefered group, cobbler ip, username and password

