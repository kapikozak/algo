class Trie:

    def __init__(self):
        self.data = [None] * 26
        self.ends_here = False
        self.sz = 0


    def insert(self, word: str) -> None:
        node = self

        for c in word:
            ind = ord(c) - ord('a')

            if node.data[ind] is None:
                node.data[ind] = Trie()
                node.sz += 1

            node = node.data[ind]

        node.ends_here = True


    def _search(self, word: str, prefix: bool = False) -> bool:
        node = self

        for c in word:
            ind = ord(c) - ord('a')

            if node.data[ind] is None:
                return False

            node = node.data[ind]

        return True if prefix else node.ends_here


    def search(self, word: str) -> bool:
        return self._search(word)


    def starts_with(self, word: str) -> bool:
        return self._search(word, prefix=True)


    def delete(self, word: str) -> bool:
        node = self
        stack = []

        for c in word:
            ind = ord(c) - ord('a')
            if node.data[ind] is None:
                return False

            stack.append(node)
            node = node.data[ind]

        if not node.ends_here:
            return False

        node.ends_here = False
        prev = node

        for c in reversed(word):

            if prev.sz > 0 or prev.ends_here:
                break

            node = stack.pop()
            node.data[ord(c) - ord('a')] = None
            node.sz -= 1
            prev = node

        return True