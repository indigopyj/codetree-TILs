import heapq
from collections import defaultdict


class Domain():
    def __init__(self, domain='', start=0, gap=0):
        self.domain = domain
        self.start = start
        self.gap = gap
        self.waiting_queue = []
        self.now_judging = False
    
    def hq_push(self, p, t, u):
        for item in self.waiting_queue:
            if u == item[-1]:
                # print(u, self.waiting_queue)
                return False
        heapq.heappush(self.waiting_queue, (p, t, u))
        return True
    
    def check_judge(self, curr_t):
        if self.now_judging:
            return False
        if curr_t < self.start + 3 * self.gap:
            return False
        return True
    
    def hq_pop(self):
        return heapq.heappop(self.waiting_queue)
    

    def print_(self):
        print(self.start, self.gap, self.now_judging, self.waiting_queue)


    
MAX_T = 1000001
MAX_N = 50001
Q = int(input())
cmd_list = []
judge_cmd_list = []
hq = []
waiting_domain = set()
domain_dict = defaultdict(Domain)
job_judger = []

def is_available(curr_t, curr_domain, N):
    if curr_domain in job_judger[1:N+1]:
        return False
    start_t, gap = domain_dict[curr_domain]
    if curr_t < start_t + 3 * gap:
        return False
    # print("true")
    return True


# def judger_exist(N):
#     job_judger
#     for i, jj in enumerate(job_judger[:N+1]):
#         if i > 0 and jj == '':
#             return i
#     return -1


ans = 0

for q in range(Q):
    inputline = list(input().split())
    cmd = int(inputline[0])
    t, J_id, p, u = -1, -1, -1, ''
    if cmd == 100:
        # ready for scoring
        N = int(inputline[1])
        u0 = inputline[2]
        judgers = [0] * N
        domain = u0.split('/')[0]
        domain_dict[domain] = Domain(domain=domain, start=0, gap=0)
        check = domain_dict[domain].hq_push(1, 0, u0)
        if check:
            ans += 1
        waiting_domain.add(domain)
        # init. job judger
        for i in range(1, N+1):
            heapq.heappush(job_judger, i) # number
        judging_domain = ['' for _ in range(N+1)]

    elif cmd == 200:
        # request scoring, 200 t p u
        t, p = map(int, inputline[1:-1])
        u = inputline[-1]
        domain = u.split('/')[0]
        check = domain_dict[domain].hq_push(p, t, u)
        if check:
            ans += 1
        waiting_domain.add(domain)

    elif cmd == 300:
        # try scoring
        t = int(inputline[1])
        tmp_hq = []
        for d_i, domain_info in domain_dict.items():
            if domain_info.check_judge(t):
                priority, input_time, url = domain_info.waiting_queue[0]
                heapq.heappush(tmp_hq, (priority, input_time, d_i))
        if tmp_hq and job_judger:
            j_id = heapq.heappop(job_judger)
            _, _, d_i = tmp_hq[0]
            # print("job start: ", j_id, domain_dict[d_i])
            waiting_domain.remove(d_i)
            domain_dict[d_i].hq_pop()
            judging_domain[j_id] = d_i
            domain_dict[d_i].start = t
            domain_dict[d_i].now_judging = True
            ans -= 1
            # domain_dict[d_i].print_()
            
    elif cmd == 400:
        # end scoring
        t, j_id = map(int, inputline[1:])
        d_i = judging_domain[j_id]
        domain_dict[d_i].gap = t - domain_dict[d_i].start 
        domain_dict[d_i].now_judging = False
        # domain_dict[d_i].print_()

    else:
        # print num of tasks in queue
        t = int(inputline[1])
        print(ans)
    
    


# for jc in judge_cmd_list:
#     # print(jc)
#     cmd, curr_t, J_id = jc
#     if cmd == 300:
#         curr_p, start_t, curr_domain, curr_uid = hq[0]
#         curr_url = (curr_domain + '/' + str(curr_uid))
#         if curr_url in url_list[start_t+1:curr_t]:
#             cmd_list.append((222, start_t, -1, -1, -1)) # pass adding to queue
#             # print(222, start_t)
#             heapq.heappop(hq)
#             continue
#         tmp_hq = []
#         while hq:
#             curr_p, start_t, curr_domain, curr_uid = heapq.heappop(hq)
#             if not is_available(curr_t, curr_domain, N):
#                 tmp_hq.append((curr_p, start_t, curr_domain, curr_uid))
#                 continue
#             if job_judger:
#                 J_id = heapq.heappop(job_judger)
#                 judging_domain[J_id] = curr_domain
#                 domain_dict[curr_domain][0] = curr_t
#                 # print(333, curr_t, J_id, curr_domain, job_judger[:N+1])
#                 cmd_list.append((333, curr_t, J_id, -1, -1))
#                 url_list[start_t] = ''
#             break
#         for tmp in tmp_hq:
#             heapq.heappush(hq, tmp)
#     else:
#         domain = judging_domain[J_id]
#         if domain == '':
#             continue
#         domain_dict[domain][1] = curr_t - domain_dict[domain][0]
#         # print(400, J_id, domain, domain_dict[domain])
#         heapq.heappush(job_judger, J_id)

# cmd_list = sorted(cmd_list, key=lambda x:x[1])
# # print(cmd_list)
# total_tasks = 0
# for c in cmd_list:
#     if c[0] == 100 or c[0] == 200:
#         total_tasks += 1
#     elif c[0] == 222:
#         total_tasks -= 1
#     elif c[0] == 333:
#         total_tasks -= 1
#     elif c[0] == 500:
#         print(total_tasks)