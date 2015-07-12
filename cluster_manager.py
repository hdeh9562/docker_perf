# Author::    Hamid Dehghani Samani
# Copyright:: Copyright (c) 2015
#
# == Description:
# Cluster manger for runing multiple docker contrainers in one physical machine

#! /usr/bin/python

import subprocess

# Calculate CPU usage based on requested QoS
def convertQoSToCpuUsage():
	# Find the smallest QoS
	min = qos_arr[0]	
	for i in range(0,n):
		if qos_arr[i] < min:
			min = qos_arr[i]

	# Calculate cpu usage of each application factor of smallest QoS
	for i in range(0,n):
		tmp = qos_arr[i]/float(min)
		cpu_arr[i] = int(tmp * 1024)

# Number of applications
n=3

# List of containers to be built
woker_nodes=["node1", "node2", "node3"]

# List of application
app_names=["app1", "app2", "app3"]

# Name & tag of the image
image_name="my_project:v1"
image_tag_param = "-t="+image_name

# Build the image
print "Building docker image. Please wait ..."
subprocess.call(["docker", "build", image_tag_param, "."])
# subprocess.call(["docker", "build", "-t=", image_name, "."])

print "n =",n

qos_arr=[]
cpu_arr=[]
mem_arr=[]
io_arr=[]

for i in range (1,n+1):
	print "Reading configuration file for application ", i	
	l=1
	fname = "config/"+"app"+str(i)+".cfg"
	with open(fname) as f:
		content = f.readlines()

	# Extract requested QoS, CPU, Memory, IO
	resource_params = content[2].split(";")
	qos_arr.append(int(resource_params[0]))
	cpu_arr.append(int(resource_params[1]))
	mem_arr.append(resource_params[2])
	io_arr.append(int(resource_params[3]))

convertQoSToCpuUsage()

print "QoS", qos_arr
print "CPU", cpu_arr
print "Memory", mem_arr
print "IO", io_arr

# Create container for each application
for i in range (0,n):
	print "creating a container for app ", i+1, ".Please wait ..."
	container_name = "node"+str(i+1)
	app_name = "app"+str(i+1)+".py"

	# Create a container for node{i}
	subprocess.call(["docker", "run", "-d", "--name", container_name, "-it", "-c", str(cpu_arr[i]), "-m", mem_arr[i], image_name])
	str1 = "Hello from "+container_name

	# Test new container is running
	subprocess.call(["docker", "exec", container_name, "python3", app_name])