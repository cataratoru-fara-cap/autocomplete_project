from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

DATASET = [
    "To Kill a Mockingbird",
    "1984",
    "The Great Gatsby",
    "The Catcher in the Rye",
    "Moby-Dick",
    "Pride and Prejudice",
    "War and Peace",
    "The Lord of the Rings",
    "The Hobbit",
    "Harry Potter and the Sorcerer's Stone",
    "Crime and Punishment",
    "The Brothers Karamazov",
    "Brave New World",
    "The Kite Runner",
    "The Alchemist",
    "One Hundred Years of Solitude",
    "The Picture of Dorian Gray",
    "The Count of Monte Cristo",
    "Les Misérables",
    "A Tale of Two Cities",
]


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class SuffixTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        for i in range(len(word)):
            current = self.root
            for char in word[i:]:
                if char not in current.children:
                    current.children[char] = TrieNode()
                current = current.children[char]
            current.is_end_of_word = True

    def _search_node(self, prefix):
        current = self.root
        for char in prefix:
            if char not in current.children:
                return None
            current = current.children[char]
        return current

    def _collect_all_words(self, node, prefix, words):
        if node.is_end_of_word:
            words.append(prefix)
        for char, child_node in node.children.items():
            self._collect_all_words(child_node, prefix + char, words)

    def autocomplete(self, prefix):
        node = self._search_node(prefix)
        if not node:
            return []
        words = []
        self._collect_all_words(node, prefix, words)
        return words


# Initialize the trie with some data
trie = SuffixTrie()
for word in DATASET:
    trie.insert(word.lower())

# Preprocess the dataset to create a suffix array with lowercase titles

@api_view(["GET"])
def autocomplete(request):
    query = request.GET.get("query", "").lower()
    if not query:
        return Response([])

    suggestions = trie.autocomplete(query)
    return Response(suggestions)


def home(request):
    return render(request, 'index.html')
