제대로 모든 토끼를 반복문으로 불러와서 점수를 더해주면 시간초과가 발생한다

import sys
from heapq import heappush, heappop

input = sys.stdin.readline

# d에 이동거리, point에 점수를 dict[id]로 저장
q = int(input())
d, point = {}, {}
info = []
# cnt에는 추가 점수를 저장하고 마지막에 한번에 더해준다
cnt = 0
for _ in range(q):
    r = list(map(int, input().split()))
    if r[0] == 100:
        n, m, p = r[1], r[2], r[3]
        r = r[4:]
        for i in range(p):
            # 각 토끼의 이동거리를 저장하고 점수는 0으로 초기화
            # 우선순위큐에 정렬할 순서에 맞춰서 값을 넣어준다
            # 좌표 시작점이 [1, 1]인 점 주의
            d[r[2 * i]] = r[2 * i + 1]
            point[r[2 * i]] = 0
            heappush(info, [0, 2, 1, 1, r[2 * i]])

    elif r[0] == 200:
        k, s = r[1], r[2]
        cand2 = []

        for _ in range(k):
            # 조건에 맞는 이동할 토끼를 우선수위큐에서 꺼낸다
            jump, _, x, y, id = heappop(info)
            tx, ty = x, y
            dist = d[id]
            cand = []

            # 상하좌우 이동을 잘 구현하고 도착좌표들을 cand에 저장
            # up
            nx = x - dist
            if nx <= 0:
                a, b = divmod(abs(dist - x + 1), n - 1)
                if a % 2 == 0:
                    if b == 0:
                        nx = 1
                    else:
                        nx = b + 1
                else:
                    if b == 0:
                        nx = n
                    else:
                        nx = n - b
            cand.append([nx, y])

            # down
            nx = x + dist
            if nx > n:
                a, b = divmod(dist - (n - x), n - 1)
                if a % 2 == 0:
                    if b == 0:
                        nx = n
                    else:
                        nx = n - b
                else:
                    if b == 0:
                        nx = 1
                    else:
                        nx = b + 1
            cand.append([nx, y])

            # left
            ny = y - dist
            if ny <= 0:
                a, b = divmod(abs(dist - y + 1), m - 1)
                if a % 2 == 0:
                    if b == 0:
                        ny = 1
                    else:
                        ny = b + 1
                else:
                    if b == 0:
                        ny = m
                    else:
                        ny = m - b
            cand.append([x, ny])

            # right
            ny = y + dist
            if ny > m:
                a, b = divmod(dist - (m - y), m - 1)
                if a % 2 == 0:
                    if b == 0:
                        ny = m
                    else:
                        ny = m - b
                else:
                    if b == 0:
                        ny = 1
                    else:
                        ny = b + 1
            cand.append([x, ny])

            # cand에 있는 도착좌표 후보들을 오름차순으로 정렬
            cand.sort(key=lambda x: (x[0] + x[1], x[0], x[1]), reverse=True)
            x, y = cand[0]

            # 이동하지 않은 토끼들만 점수를 얻는다 -> 이동한 토끼만 점수를 잃는다로 바꿔서 구현
            # cnt에 얻는 점수를 계속 더해주고 마지막 점수 최대값 결과에 더해준다
            point[id] -= x + y
            cnt += x + y

            # 우선순위큐에 점프횟수, 이동좌표가 변경된 토끼를 넣어준다
            # cand2에 이동한 토끼를 저장
            heappush(info, [jump + 1, x + y, x, y, id])
            cand2.append([x, y, id])

        # 이동한 토끼들을 오름차순으로 정렬해서 조건에 맞는 토끼의 점수를 더해준다
        cand2.sort(key=lambda x: (x[0] + x[1], x[0], x[1], x[2]), reverse=True)
        id = cand2[0][-1]
        point[id] += s

    elif r[0] == 300:
        # 조건대로 이동거리 수정
        id, l = r[1], r[2]
        d[id] *= l

    else:
        # 점수의 최대값을 구해주고 추가점수를 더해준다
        print(max(point.values()) + cnt)