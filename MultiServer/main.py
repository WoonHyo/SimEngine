from multiprocessing import Pool
from server.singleserver import SingleServer


def run_simulation(log=0):
    server = SingleServer(20.0, log)
    while server.isEoS() is True:
        server.UpdateEvent()
    server.execute_stat()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    what = input("How many run your server?: ")
    need = int(input("Do you want to write event log? (Yes:1, No:0) "))
    n_of_server = int(what)

    with Pool(n_of_server) as p:
        print(p.map(run_simulation, [need] * n_of_server))
