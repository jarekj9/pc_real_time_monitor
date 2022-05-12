#!/usr/bin/python3
from subprocess import PIPE, Popen
import psutil
import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re

 
class PLOT:
    def __init__(self):
        self.cpu = collections.deque(np.zeros(20))
        self.ram = collections.deque(np.zeros(20))
        self.wifi = collections.deque(np.zeros(20))

        fig = plt.figure(figsize=(12,6), facecolor='#FFFFFF')
        fig.canvas.set_window_title('Real Time PC Monitor')
        self.ax = plt.subplot(111)
        self.ax.set_facecolor('#FFFFFF')
        animate = FuncAnimation(fig, self.update, interval=1000)
        plt.show()

    def update(self, i):
        self.cpu.popleft()
        self.cpu.append(psutil.cpu_percent())
        self.ram.popleft()
        self.ram.append(psutil.virtual_memory().percent)
        self.wifi.popleft()
        self.wifi.append(self.get_wifi_strength())
        self.ax.cla()
        self.ax.set_xlabel('time (s)')
        self.ax.set_ylabel('value (%)')
        self.ax.set_title('Real Time PC Monitor')

        self.ax.plot(self.cpu, label='CPU usage')
        self.ax.scatter(len(self.cpu)-1, self.cpu[-1])
        self.ax.text(len(self.cpu)-2, self.cpu[-1]+2, "CPU: {}%".format(self.cpu[-1]))
        self.ax.set_ylim(0,100)

        self.ax.plot(self.ram, label='RAM usage')
        self.ax.scatter(len(self.ram)-1, self.ram[-1])
        self.ax.text(len(self.ram)-2, self.ram[-1]+2, "RAM: {}%".format(self.ram[-1]))
        self.ax.set_ylim(0,100)

        self.ax.plot(self.wifi, label='WIFI signal strength')
        self.ax.scatter(len(self.wifi)-1, self.wifi[-1])
        self.ax.text(len(self.wifi)-2, self.wifi[-1]+2, "WIFI: {}%".format(self.wifi[-1]))
        self.ax.set_ylim(0,100)

        plt.legend(loc='lower left')

    def get_wifi_strength(self):
        command = "powershell.exe (netsh wlan show interfaces) -Match '^\s+Signal' -Replace '^\s+Signal\s+:\s+',''"
        with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
            output = process.communicate()[0].decode("utf-8")
        wifi_strength_number = ''.join(re.findall(r'[0-9]*\.?[0-9]*', output))
        return int(wifi_strength_number)


def main():
    plot = PLOT()


if __name__ == '__main__':
    main()