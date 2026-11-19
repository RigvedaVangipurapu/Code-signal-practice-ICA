from collections import defaultdict

class Ledger:
    def __init__(self):
        self.registry = []
        self.registry_lookup = set()
        self.record = dict()
        self.createamt = dict()

        self.time = defaultdict(list)
        self.maxtime = 0

    def process(self, query):
        operation, *args = query

        if operation == 'CREATE':
            value = args[0]
            amount = args[1] if len(args) > 1 else '-1'

            # deal with timestamps for non AT functions before getting into it
            self.maxtime += 1
            timestamps = self.time[value]

            if len(timestamps) < 3:
                timestamps.append(self.maxtime)

            else:
                numactions = 0
                for time in timestamps[::-1]:
                    if self.maxtime - time < 10:
                        numactions += 1

                if numactions > 3:
                    self.maxtime -= 1
                    return "false"
                self.time.append(self.maxtime)


            if value in self.registry_lookup:
                return "false"
            self.registry.append(value)
            self.registry_lookup = set(self.registry)
            self.record[value] = 0
            if int(amount) > 0:
                self.createamt[value] = int(amount)
            return "true"

        if operation == 'GET':
            value = args[0]

            for i in range(len(self.registry)):
                if self.registry[i] == value:
                    if value in self.createamt:
                        return str(self.createamt[value])
                    return str(i)
            return ""

        if operation == 'DELETE':
            value = args[0]


            # deal with timestamps for non AT functions before getting into it
            self.maxtime += 1
            timestamps = self.time[value]

            if len(timestamps) < 3:
                timestamps.append(self.maxtime)

            else:
                numactions = 0
                for time in timestamps[::-1]:
                    if self.maxtime - time < 10:
                        numactions += 1

                if numactions > 3:
                    self.maxtime -= 1
                    return "false"
                self.time.append(self.maxtime)


            if value in self.registry_lookup:
                self.registry.remove(value)
                self.registry_lookup = set(self.registry)
                self.record.pop(value, None)
                self.createamt.pop(value, None)
                return "true"
            else:
                return "false"

        if operation == 'RECORD':
            value, amount = args

            # deal with timestamps for non AT functions before getting into it
            self.maxtime += 1
            timestamps = self.time[value]

            if len(timestamps) < 3:
                timestamps.append(self.maxtime)

            else:
                numactions = 0
                for time in timestamps[::-1]:
                    if self.maxtime - time < 10:
                        numactions += 1

                if numactions > 3:
                    self.maxtime -= 1
                    return "false"
                self.time.append(self.maxtime)

            if value in self.record:
                self.record[value] += int(amount)
                return str(self.record[value])
            return ""

        if operation == 'TOP':
            value = args[0]

            temp = dict(sorted(self.record.items(), key=lambda kv: (-kv[1], kv)))
            res = ''
            counter = 0
            for k, v in temp.items():
                if v != 0 and counter < int(value):
                    res = res + k + '(' + str(v) + ')'
                    res += ', '
                    counter += 1
            return res[:len(res) - 2] if len(res) > 0 else ""

        if operation == 'TRANSFER':
            from_user, to_user, transferamt = args
            dollars = int(transferamt)

            if from_user == to_user:
                return "false"
            if from_user not in self.registry_lookup:
                return "false"

            if to_user not in self.registry_lookup:
                return "false"

            if from_user in self.createamt and self.createamt[from_user] >= dollars:
                if to_user in self.createamt:
                    self.createamt[to_user] += dollars
                else:
                    self.createamt[to_user] = dollars
                self.createamt[from_user] = int(self.createamt[from_user]) - dollars
                return "true"

            return "false"


        if operation == 'ACTION':

            if len(self.time[value] ) < 3:
                self.time[value].append(time)
                self.maxtime = max(self.maxtime + 1 , time)
                return "true"

            return "false"

        else:
            return "false"


def solution(queries):
    ledger = Ledger()
    results = []
    for query in queries:
        results.append(ledger.process(query))
    return results