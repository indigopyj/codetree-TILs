import heapq
# from collections import defaultdict
MAX_T = 1000001
MAX_N = 50001
Q = int(input())
cmd_list = []
judge_cmd_list = []
hq = []
url_list = ['' for _ in range(MAX_T)]
domain_dict = dict()
job_judger = ['' for _ in range(MAX_N)]


def is_available(curr_t, curr_domain, N):
    if curr_domain in job_judger[1:N+1]:
        return False
    start_t, gap = domain_dict[curr_domain]
    if curr_t < start_t + 3 * gap:
        return False
    # print("true")
    return True


def judger_exist(N):
    for i, jj in enumerate(job_judger[:N+1]):
        if i > 0 and jj == '':
            return i
    return -1



for q in range(Q):
    inputline = list(input().split())
    cmd = int(inputline[0])
    t, J_id, p, u = -1, -1, -1, ''
    if cmd == 100:
        # ready for scoring
        N = int(inputline[1])
        u0 = inputline[2]
        judgers = [0] * N
        domain, u_id = u0.split('/')
        heapq.heappush(hq, (1, 0, domain, int(u_id)))
        domain_dict[domain] = [0, 0]
        url_list[0] = u0

    elif cmd == 200:
        # request scoring, 200 t p u
        t, p = map(int, inputline[1:-1])
        u = inputline[-1]
        domain, u_id = u.split('/')
        heapq.heappush(hq, (p, t, domain, int(u_id)))
        domain_dict[domain] = [0, 0]
        url_list[t] = u
    elif cmd == 300:
        # try scoring
        t = int(inputline[1])
        judge_cmd_list.append((cmd, t, J_id))
        pass
    elif cmd == 400:
        # end scoring
        t, J_id = map(int, inputline[1:])
        judge_cmd_list.append((cmd, t, J_id))
        pass
    else:
        # print num of tasks in queue
        t = int(inputline[1])
        pass
    cmd_list.append((cmd, t, J_id, p, u))
    

for jc in judge_cmd_list:
    # print(jc)
    cmd, curr_t, J_id = jc
    if cmd == 300:
        curr_p, start_t, curr_domain, curr_uid = hq[0]
        curr_url = (curr_domain + '/' + str(curr_uid))
        # print(curr_url, url_list[start_t+1:curr_t])
        if curr_url in url_list[start_t+1:curr_t]:
            cmd_list.append((222, start_t, -1, -1, -1)) # pass adding to queue
            # print(222, start_t)
            heapq.heappop(hq)
            continue
        
        if is_available(curr_t, curr_domain, N):
            heapq.heappop(hq)
            J_id = judger_exist(N)
            if J_id != -1:
                job_judger[J_id] = curr_domain
                domain_dict[curr_domain][0] = curr_t
                # print(333, curr_t, J_id, curr_domain, job_judger[:N+1])
                cmd_list.append((333, curr_t, J_id, -1, -1))
                url_list[start_t] = ''
    else:
        domain = job_judger[J_id]
        if domain == '':
            continue
        domain_dict[domain][1] = curr_t - domain_dict[domain][0]
        # print(400, J_id, domain, domain_dict[domain])
        job_judger[J_id] = ''

cmd_list = sorted(cmd_list, key=lambda x:x[1])
# print(cmd_list)
total_tasks = 0
for c in cmd_list:
    if c[0] == 100 or c[0] == 200:
        total_tasks += 1
    elif c[0] == 222:
        total_tasks -= 1
    elif c[0] == 333:
        total_tasks -= 1
    elif c[0] == 500:
        print(total_tasks)