import heapq
from collections import defaultdict


class Domain():
    def __init__(self, domain='', start=0, gap=0):
        self.domain = domain
        self.start = start
        self.gap = gap
        self.waiting_queue = [] # 도메인마다 queue 생성
        self.now_judging = False
    
    def hq_push(self, p, t, u): 
        for item in self.waiting_queue:
            if u == item[-1]:
                return False
        heapq.heappush(self.waiting_queue, (p, t, u))
        return True
    
    def check_judge(self, curr_t): # 채점 가능한지 체크
        if self.now_judging:
            return False
        if curr_t < self.start + 3 * self.gap:
            return False
        return True
    
    def hq_pop(self):
        return heapq.heappop(self.waiting_queue)
    
    def print_(self):
        print(self.start, self.gap, self.now_judging, self.waiting_queue)

Q = int(input())
domain_dict = dict()
job_judger = [] # 놀고있는 judger를 뱉어줄 priority queue
ans = 0

for q in range(Q):
    inputline = list(input().split())
    cmd = int(inputline[0])
    t, J_id, p, u = -1, -1, -1, ''
    if cmd == 100:
        # ready for scoring
        N = int(inputline[1])
        u0 = inputline[2]
        domain = u0.split('/')[0]
        domain_dict[domain] = Domain(domain=domain, start=0, gap=0)
        check = domain_dict[domain].hq_push(1, 0, u0)
        if check:
            ans += 1
        # init. job judger
        for i in range(1, N+1):
            heapq.heappush(job_judger, i) # number
        judging_domain = ['' for _ in range(N+1)] # 각 채점기가 채점중인 domain 기록

    elif cmd == 200:
        # request scoring, 200 t p u
        t, p = map(int, inputline[1:-1])
        u = inputline[-1]
        domain = u.split('/')[0]
        if domain not in domain_dict:
            domain_dict[domain] = Domain(domain=domain, start=0, gap=0)
        check = domain_dict[domain].hq_push(p, t, u) # push가 안될 경우(즉, domain이 겹치는 경우) return false
        if check: # push가 되는 경우 채점 대기 큐에 들어감
            ans += 1

    elif cmd == 300:
        # try scoring
        t = int(inputline[1])
        tmp_hq = [] # 먼저 각 도메인 별로 채점 가능한 애들만 모은 뒤, 거기서 우선순위를 매길 예정
        for d_i, domain_info in domain_dict.items(): # 각 도메인 별로 큐를 확인해서 채점 가능한 애들만 모으자
            if domain_info.check_judge(t): # 대기중인 도메인 중에 채점 가능한 원소가 있다면
                if domain_info.waiting_queue: # waiting queue가 비어있지 않다면
                    priority, input_time, url = domain_info.waiting_queue[0]
                    heapq.heappush(tmp_hq, (priority, input_time, d_i))
        if tmp_hq and job_judger: # 채점 가능한 애들이 존재하고, 지금 작업 가능한 채점기가 있다면
            j_id = heapq.heappop(job_judger)
            _, _, d_i = tmp_hq[0] # 제일 우선순위가 높은 애를 꺼내자
            # 대기중인 큐에서 해당 노드에 대한 정보를 제거함
            domain_dict[d_i].hq_pop()
            # 채점기 j_id 가 채점 시작
            judging_domain[j_id] = d_i
            domain_dict[d_i].start = t
            domain_dict[d_i].now_judging = True
            ans -= 1
            
    elif cmd == 400:
        # end scoring
        t, j_id = map(int, inputline[1:])
        d_i = judging_domain[j_id]
        if d_i == '': # 만약 j_id 채점기가 채점하고 있는 것이 없다면 패스
            continue
        # j_id가 채점하고 있던 노드의 정보 갱신
        domain_dict[d_i].gap = t - domain_dict[d_i].start 
        domain_dict[d_i].now_judging = False
        # 놀고 있는 judger로 다시 추가시키기
        heapq.heappush(job_judger, j_id)
        judging_domain[j_id] = ''

    else:
        # print num of tasks in queue
        t = int(inputline[1])
        print(ans)