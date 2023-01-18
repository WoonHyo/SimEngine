class SingleServer:
    def __init__(self, eos):
        self.Eos = eos

        self.event_scheduler = []
        self.store = []
        self.M_s = []
        self.Q_s = []

        self.M = 0
        self.Q = 0
        self.sumQ = 0
        self.before = 0

        self.now = 0
        self.P = 0

    def UpdateEvent(self):
        self.event_scheduler.sort()
        #print("#", self.now, "event scheduler: ", self.event_scheduler)

        if "arr" in self.event_scheduler[0]:
            self.execute_arrive(self.now)
            del self.event_scheduler[0]
        elif "load" in self.event_scheduler[0]:
            self.execute_load(self.now)
            del self.event_scheduler[0]
        elif "unload" in self.event_scheduler[0]:
            self.execute_unload(self.now)
            del self.event_scheduler[0]
        else:
            print("****************")
        # 출력이 안되는 이유: 이미 20까지 할거라고 지정했기 때문

    #         elif (self.event_scheduler[0][0] > self.Eos):
    #             print("**************")
    #             print(self.event_scheduler)
    #             exit
    # self.now +=1

    def isEoS(self):
        # 데이터 초기화

        if self.now == 0:
            self.execute_initial()
            print("초기화", self.event_scheduler)
            self.now = 1
            return True
        else:
            if self.now == 20:
                return False
            else:
                self.now += 1
                return True

    # 초기화
    def execute_initial(self):
        self.event_scheduler.append([self.now, "arr"])
        self.store.append([self.now, "arr"])

        self.event_scheduler.append([self.Eos, "end"])
        self.store.append([self.Eos, "end"])

        self.M_s.append([self.now, self.M])
        self.Q_s.append([self.now, self.Q])

    # Arrival
    def execute_arrive(self, now):
        self.sumQ = self.sumQ + self.Q * (self.now - self.before)
        self.before = self.now
        self.Q += 1

        import numpy as np

        a = self.now + np.round(np.random.exponential(5) / 10, 2)
        self.event_scheduler.append([a, "arr"])
        self.store.append([a, "arr"])
        if (self.M == 0):
            self.event_scheduler.append([self.now, "load"])
            self.store.append([self.now, "load"])

        # 아이템 저장
        self.M_s.append([self.now, self.M])
        self.Q_s.append([self.now, self.Q])

    # Load
    def execute_load(self, now):
        #         self.sumQ = self.sumQ + self.Q*(self.now-self.before)
        #         self.before = self.now
        #         self.M += 1
        #         if self.Q>0:
        #             self.Q -= 1
        #         else: self.Q = 0
        #         a = self.now + np.round(np.random.uniform(4,6),2)
        #         self.event_scheduler.append([a, "unload"])
        #         self.store.append([a, "unload"])

        #         #아이템 저장
        #         self.M_s.append([self.now, self.M])
        #         self.Q_s.append([self.now, self.Q])

        if self.M == 0:
            self.sumQ = self.sumQ + self.Q * (self.now - self.before)
            self.before = self.now
            self.M += 1
            if self.Q > 0:
                self.Q -= 1
            else:
                self.Q = 0

            import numpy as np

            a = self.now + np.round(np.random.uniform(4, 6), 2)
            self.event_scheduler.append([a, "unload"])
            self.store.append([a, "unload"])

            # 아이템 저장
            self.M_s.append([self.now, self.M])
            self.Q_s.append([self.now, self.Q])
        else:
            pass

    # Unload
    def execute_unload(self, now):
        self.M -= 1
        self.P += 1

        if (self.Q > 0):
            self.event_scheduler.append([self.now, "load"])
            self.store.append([self.now, "load"])

        # 아이템 저장
        self.M_s.append([self.now, self.M])
        self.Q_s.append([self.now, self.Q])

    # 통계
    def execute_stat(self):
        self.sumQ = self.sumQ + self.Q * (self.now - self.before)
        AQL = self.sumQ / self.now
        print("sumQ={}, AQL={}, 생산량 P={}".format(self.sumQ, AQL, self.P))

        # 기계상태 출력
        import pandas as pd
        b = pd.DataFrame(self.M_s)
        import matplotlib.pyplot as plt
        plt.figure(figsize=(7,3))
        plt.subplot(1,2,1)
        plt.plot(b[0], b[1], 'r-')
        plt.axis([-0.5, 20.1, -0.1, 1.1])
        plt.title("Machine State")

        # Q길이
        c = pd.DataFrame(self.Q_s)
        plt.subplot(1,2,2)
        plt.plot(c[0], c[1], 'ro')
        plt.title("Q length")
        plt.show()

        # 저장
        store2 = pd.DataFrame(self.store, columns=["Time", "Type"])
        #print('Event Calender')
        return store2