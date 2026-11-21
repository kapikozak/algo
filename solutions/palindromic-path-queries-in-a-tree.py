from typing import List

class SegTree:
    def __init__(self, arr: List[int]) -> None:
        self.n = len(arr)
        self.heap = [0] * (4 * self.n)
        self.lazy = [0] * len(self.heap)

        self._rbuild(arr, 0, 0, self.n - 1)

    def _rbuild(self, arr: List[int], h_ind: int, l: int, r: int) -> None:

        if l == r:
            self.heap[h_ind] = arr[l]
            return

        mid = (l + r) // 2

        self._rbuild(arr, 2 * h_ind + 1, l, mid)
        self._rbuild(arr, 2 * h_ind + 2, mid + 1, r)

        self.heap[h_ind] = self.heap[2 * h_ind + 1] ^ self.heap[2 * h_ind + 2]

    def _push(self, h_ind: int, lch: int, rch: int, l: int, r: int, mid: int) -> None:

        if (mid - l + 1) & 1 == 1:
            self.heap[lch] ^= self.lazy[h_ind]

        if (r - mid) & 1 == 1:
            self.heap[rch] ^= self.lazy[h_ind]

        self.lazy[lch] ^= self.lazy[h_ind]
        self.lazy[rch] ^= self.lazy[h_ind]

        self.lazy[h_ind] = 0

    def _pull(self, h_ind: int, lch: int, rch: int) -> None:
        self.heap[h_ind] = self.heap[lch] ^ self.heap[rch]

    def _rupdate(self, h_ind: int, l: int, r: int, ql: int, qr: int, delta: int) -> None:

        if ql <= l and r <= qr:

            if r - l + 1 & 1 == 1:
                self.heap[h_ind] ^= delta

            self.lazy[h_ind] ^= delta
            return

        lch = 2 * h_ind + 1
        rch = 2 * h_ind + 2

        mid = (l + r) // 2

        if self.lazy[h_ind] > 0:
            self._push(h_ind, lch, rch, l, r, mid)

        if ql <= mid:
            self._rupdate(lch, l, mid, ql, qr, delta)

        if qr > mid:
            self._rupdate(rch, mid + 1, r, ql, qr, delta)

        self._pull(h_ind, lch, rch)

    def update(self, l: int, r: int, delta: int) -> None:
        self._rupdate(0, 0, self.n - 1, l, r, delta)

    def _rquery(self, h_ind: int, l: int, r: int, q: int) -> int:

        if l == r:
            return self.heap[h_ind]

        lch = 2 * h_ind + 1
        rch = 2 * h_ind + 2

        mid = (l + r) // 2

        if self.lazy[h_ind] > 0:
            self._push(h_ind, lch, rch, l, r, mid)

        return self._rquery(lch, l, mid, q) if q <= mid else self._rquery(rch, mid + 1, r, q)

    def query(self, q: int) -> int:
        return self._rquery(0, 0, self.n - 1, q)


def palindromePath(n: int, edges: list[list[int]], s: str, queries: list[str]) -> list[bool]:

    def find_lca(u: int, v: int) -> int:

        if depth[u] < depth[v]:
            u, v = v, u

        diff = depth[u] - depth[v]

        for j in range(log2_n + 1):

            if diff & (1 << j):
                u = up[u][j]

        if u == v:
            return u

        for j in range(log2_n, -1, -1):

            if up[u][j] != up[v][j]:
                u = up[u][j]
                v = up[v][j]

        return up[u][0]

    graph = [[] for _ in range(n)]

    for src, dst in edges:
        graph[src].append(dst)
        graph[dst].append(src)

    letters = list(s)
    log2_n = n.bit_length() - 1

    tim = [-1] * n
    up = [[0] * (log2_n + 1) for _ in range(n)]
    depth = [0] * n
    path_xor = [0] * n
    size = [0] * n

    stack = [0]
    ct = 0
    dpt = 0
    xor = 0

    while stack:
        u = stack.pop()

        if tim[u] != -1:
            xor ^= 1 << (ord(letters[u]) - ord('a'))
            size[u] = ct - tim[u]
            dpt -= 1
            continue

        tim[u] = ct
        ct += 1

        depth[u] = dpt
        dpt += 1

        xor ^= 1 << (ord(letters[u]) - ord('a'))
        path_xor[u] = xor

        stack.append(u)

        for v in graph[u]:

            if tim[v] == -1:
                up[v][0] = u
                stack.append(v)

    for exponent in range(1, log2_n + 1):

        for u in range(n):
            up[u][exponent] = up[up[u][exponent - 1]][exponent - 1]

    arr = [0] * n

    for u in range(n):
        arr[tim[u]] = path_xor[u]

    st = SegTree(arr)
    ans = []

    for q in queries:
        task, *node = q.split()

        if task == 'update':
            raw, ch = node
            u = int(raw)

            if ch == letters[u]:
                continue

            delta = (1 << (ord(ch) - ord('a'))) ^ (1 << (ord(letters[u]) - ord('a')))
            letters[u] = ch
            st.update(tim[u], tim[u] + size[u] - 1, delta)

        elif task == 'query':
            u, v = map(int, node)
            lca = find_lca(u, v)
            xor = st.query(tim[u]) ^ st.query(tim[v]) ^ (1 << (ord(letters[lca]) - ord('a')))
            ans.append(xor.bit_count() <= 1)

    return ans