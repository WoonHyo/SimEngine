import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from server.singleserver import SingleServer

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    what = input("How many run your server?: ")
    need = int(input("Need event scheduler? (Yes:1, No:0) "))
    n_of_server = int(what)

    for i in range(n_of_server):
        globals()["server{}".format(i+1)] = SingleServer(20.0, need)

    for i in range(n_of_server):
        a = eval('server{}'.format(i+1))
        while a.isEoS() is True:
            a.UpdateEvent()
        print("Server{} Information".format(i+1))
        a.execute_stat()
