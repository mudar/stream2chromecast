#!/usr/bin/env python

from multiprocessing import Process
import threading
import stream2chromecast
import cc_device_finder


def start_device(ip_address):
  """ Start playing remote-url to device device using its IP address """ 
  import sys
  args = sys.argv[1:]
  stream2chromecast.playurl(args[0], device_name=ip_address)
  print "Done, %s" % ip_address


def start_multi_process(device_ips):
  """ Mutliple callbacks start_device() using multiprocessing """
  processes = []
  for device_ip in device_ips:
    print "Stream to chromecast %s (%s)" % (cc_device_finder.get_device_name(device_ip), device_ip)
    processes.append(Process(target=start_device, args=(device_ip,)))

  print 
  print "Start multiprocessing..."

  for p in processes:
    p.start()

  for p in processes:
    p.join()


def search_and_start_all():
  """ Find devices on network and stream to all using multiprocessing """
  print "Searching for devices, please wait..."
  start_multi_process(cc_device_finder.search_network(device_limit=4, time_limit=10))


def start_by_ip():
  """ Manually add devices (IPs) and stream to all using multiprocessing """
  print "Start pre-defined devices"
  devices = []

  devices.append("192.168.0.21")
  devices.append("192.168.0.22")
  devices.append("192.168.0.23")
  
  start_multi_process(devices)


try:
#  search_and_start_all()
  start_by_ip()

except KeyboardInterrupt:
  pass

