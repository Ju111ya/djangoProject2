import socket
from contextlib import closing
from django.http import HttpResponseRedirect
from django.shortcuts import render
from python_on_whales import *
from siteAlb.forms import versSim
from argparse import ArgumentParser
from time import sleep
from pymavlink import mavutil
from pymavlink.dialects.v10.ardupilotmega import MAVLink as mavlink1
from pymavlink.dialects.v10 import ardupilotmega


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]
s.close

names_conts = ""
stack_of_ports = ""
status = ""
n=0

def wait_heartbeat(m:mavutil.mavudp):
    print("Waiting for APM heartbeat")
    m.wait_heartbeat()
    print("Heartbeat from APM (system %u component %u)" % (m.target_system, m.target_system))


def home_view(request):
    form = versSim()
    return render(request, 'home.html', {'form': form, 'title': 'Albatros simulator'})


def ports():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def sim_running(request):
    username = request.user.get_username()
    version = request.POST.get("vers_field")
    count = str(request.POST.get("count_cont"))
    global name_cont
    global n
    n = int(count)
    print(type(count))
    print(type(n))
    global status
    global names_conts
    global stack_of_ports
    status = ""
    names_conts = ""
    stack_of_ports=""
    start_sim(username, version, n)
    print(status)
    return render(request, 'wrkng_sim.html',
                  {'title': 'Start simulator', 'data_time': count, 'status': status, 'port': stack_of_ports, 'IP': IP,
                   'username': names_conts})




def start_sim(username, version, n):
    if version == "4.1":
        doc_v = "ghcr.io/albatros-llc-ap/arduplane_sim:4_1_custom"
    else:
        doc_v = "ghcr.io/albatros-llc-ap/arduplane_sim:3_9_custom"
    global status
    print(status)
    global names_conts
    global stack_of_ports
    for i in range(n):
        port = ports()
        name_cont = username + str(port)
        names_conts += name_cont + " "
        stack_of_ports += str(port) + " "
        try:
            docker.run(
                doc_v,
                name=name_cont,
                remove=True,
                detach=True,
                publish=[(port, 100, "udp")]
            )
            status_cont(name_cont)
        except DockerException as e:
            print(f"Exit code {e.return_code} while running {e.docker_command}")
            status = "not running"

    portss = stack_of_ports.split(" ")
    portss.pop()
    print(portss)
    connection: mavutil.mavudp
    for i in range(n):
        source = f"udpin:localhost:{int(portss[i])}"
        connection = mavutil.mavlink_connection(device=source)
        wait_heartbeat(connection)
        mav: mavlink1
        mav = connection.mav
        mav.param_set_send(connection.target_system, connection.target_component, b'SIM_WIND_SPD', 10, mavutil.ardupilotmega.MAV_PARAM_TYPE_INT64)
    return names_conts, stack_of_ports



def status_cont(name_cont):
    global status
    cont = docker.container.inspect(name_cont)
    if cont.state.running:
        status = "running"
    return status


def stop_sim(request):
    global n
    global names_conts
    names = names_conts.split(" ")
    names.pop()
    print(names)
    for i in range(0, n):
        name_cont = names[i]
        try:
            docker.stop(name_cont)
        except:
            return HttpResponseRedirect('/')
    names.clear()
    return HttpResponseRedirect('/')




