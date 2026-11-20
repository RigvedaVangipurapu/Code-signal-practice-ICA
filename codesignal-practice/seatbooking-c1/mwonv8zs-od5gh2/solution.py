from collections import defaultdict
class Seat:
    def __init__(self):
        self.seatdetails = defaultdict(list)
        self.seatlist = []
        self.updatetime = 0
        self.schedulemap = defaultdict(list)

    def booking(self, query):
        operation, *args = query



        #  create operation  ---------------------------------------------
        if operation == 'CREATE':
            sno = args[0]
            amount = int(args[1]) if len(args) > 1 else -1
            
            if sno not in self.seatlist:
                self.seatdetails[sno] = [self.updatetime, amount]
                self.seatlist.append(sno)
                self.updatetime += 1
                return "true"
            
            else:
                return "false"

        #  get operation  ---------------------------------------------       
        if operation == 'GET':
            sno = args[0]

            if sno not in self.seatlist:
                return ""
            
            return str(self.seatlist.index(sno)) if self.seatdetails[sno][1] < 0 else str(self.seatdetails[sno][1])

        
        #  delete operation  ---------------------------------------------
        if operation == 'DELETE':
            sno = args[0]

            if sno not in self.seatlist:
                return "false"

            self.seatlist.remove(sno)
            self.seatdetails.pop(sno, None)
            return "true"


        #  recent operation  ---------------------------------------------
        if operation == 'RECENT':
            k = int(args[0])
            temp = defaultdict(int)
            for sno, attr in self.seatdetails.items():
                timestamp = attr[0]
                temp[sno] = timestamp
            
            temp = sorted(temp, key=lambda k: (-temp[k], k))

            ans = ', '.join(temp[:k])
            return ans


        #  transfer operation  ---------------------------------------------
        if operation == 'TRANSFER':
                fromseat = args[0]
                toseat = args[1]
                amount = int(args[2])

                if fromseat not in self.seatlist:
                    return "false"

                if toseat not in self.seatlist:
                    return "false"

                if fromseat == toseat:
                    return "false"

                frommoney = self.seatdetails[fromseat][1]
                tomoney = self.seatdetails[toseat][1]

                if frommoney < amount:
                    return "false"

                self.seatdetails[fromseat][1] = frommoney - amount
                self.seatdetails[toseat][1] = tomoney + amount
                return "true"

        #  schedule operation  ---------------------------------------------
        if operation == 'SCHEDULE':
            schedule_time = int(args[0])
            exec_time = int(args[1])
            sno = args[2]
            amount = int(args[3])

            if schedule_time > exec_time:
                return "false"

            if sno not in self.seatlist:
                self.seatdetails[sno] = [exec_time, amount]
                self.seatlist.append(sno)
                self.updatetime += exec_time + 1
                schedulevar =  "sch"+str(schedule_time)
                self.schedulemap[schedulevar] = [sno,schedule_time]
                return schedulevar
            
            else:
                return "false"

        #  get at operation  ---------------------------------------------
        if operation == 'GET_AT':
            exec_time = int(args[0])
            sno = args[1]

            if sno not in self.seatlist or self.seatdetails[sno][0] > exec_time:
                return ""
            
            return str(self.seatlist.index(sno)) if self.seatdetails[sno][1] < 0 else str(self.seatdetails[sno][1])        
        
        
        
        #  cancel operation  ---------------------------------------------
        if operation == 'CANCEL':
            exec_time = int(args[0])
            schedule_var = args[1]

            if schedule_var not in self.schedulemap:
                return "false"

            sno = self.schedulemap[schedule_var][0]

            if sno not in self.seatlist:
                return false

            create_exec_time = self.seatdetails[sno][0]
            create_schedule_time = self.schedulemap[schedule_var][1]

            if exec_time > create_schedule_time and exec_time < create_exec_time:
                if sno not in self.seatlist:
                    return "false"

                self.seatlist.remove(sno)
                self.seatdetails.pop(sno, None)
                self.schedulemap.pop(schedule_var, None)
                return "true"
            
            else:
                return "false"



        

            


        



def solution(queries):
    results = []
    seat = Seat()
    for query in queries:
        results.append(seat.booking(query))
    return results
