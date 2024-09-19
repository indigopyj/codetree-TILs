import heapq

class Domain():
    def __init__(self, domain, start=0, gap=0):
        self.domain = domain
        self.start = start
        self.gap = gap
        self.wq = []
        self.now_judging = False

    def push(self, curr_p, curr_t, curr_u):
        #print(self.domain, " before ", curr_u, self.wq)
        for item in self.wq:
            if curr_u == item[-1]:
                return False
        heapq.heappush(self.wq, (curr_p, curr_t, curr_u))
        #print(self.domain, "after ", curr_u, self.wq)

        return True
    
    def pop(self):
        return heapq.heappop(self.wq)
    
    def check_judge(self, curr_t):
        if self.now_judging:
            return False
        if curr_t < self.start + 3 * self.gap:
            return False
        return True


Q = int(input())

ans = 0
domain_dict = dict()
# waiting_url = set()
for _ in range(Q):
    inputline = input().split()

    cmd = int(inputline[0])
    if cmd == 100:
        N, u0 = int(inputline[1]), inputline[2]
        domain = u0.split("/")[0]
        job_judgers = []
        for i in range(1, N+1):
            heapq.heappush(job_judgers, i)
        judging_domain = ['' for _ in range(N+1)]
        domain_dict[domain] = Domain(domain=domain)
        domain_dict[domain].push(1, 0, u0)
        # waiting_url.add(u0)
        ans += 1

    elif cmd == 200:
        t, p, u = inputline[1:]
        t, p = int(t), int(p)
        domain = u.split("/")[0]
        if domain not in domain_dict:
            domain_dict[domain] = Domain(domain=domain)
        check = domain_dict[domain].push(p, t, u)
        if check:
            ans += 1
            #print(domain, domain_dict[domain].wq)

    elif cmd == 300:
        t = int(inputline[1])
        possibles = []
        for domain in domain_dict:
            if domain_dict[domain].check_judge(t):
                if domain_dict[domain].wq:
                    input_p, input_t, input_u = domain_dict[domain].wq[0]
                    heapq.heappush(possibles, (input_p, input_t, domain))
        if possibles and job_judgers:
            input_p, input_t, domain = heapq.heappop(possibles)
            j_id = heapq.heappop(job_judgers)
            # waiting_url.discard(u)
            domain_dict[domain].start = t
            domain_dict[domain].now_judging = True
            judging_domain[j_id] = domain
            domain_dict[domain].pop()
            #print(domain, domain_dict[domain].wq)
            ans -= 1

    elif cmd == 400:
        t, j_id = map(int, inputline[1:])
        ended_domain = judging_domain[j_id]
        if ended_domain == '':
            continue
        domain_dict[ended_domain].gap = t - domain_dict[ended_domain].start
        domain_dict[ended_domain].now_judging = False
        judging_domain[j_id] = ''
        heapq.heappush(job_judgers, j_id)
    else:
        print(ans)
    #print(inputline, ans)