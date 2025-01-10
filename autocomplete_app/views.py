from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

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

# Preprocess the dataset to create a suffix array with lowercase titles
suffix_array = sorted((book[i:].lower(), book) for book in DATASET for i in range(len(book)))


def binary_search(query):
    """Binary search for the query in the suffix array."""
    low, high = 0, len(suffix_array)
    while low < high:
        mid = (low + high) // 2
        if suffix_array[mid][0] < query:
            low = mid + 1
        else:
            high = mid
    return low


@api_view(["GET"])
def autocomplete(request):
    query = request.GET.get("query", "").lower()
    if not query:
        return Response([])

    # Debug: Print the query
    print(f"Query: {query}")

    # Find the starting index of matches
    start = binary_search(query)
    suggestions = []

    # Collect all matches starting from the found index
    for i in range(start, len(suffix_array)):
        suffix, book = suffix_array[i]
        if suffix.startswith(query):
            suggestions.append(book)
        else:
            break

    # Debug: Print the suggestions
    print(f"Suggestions: {suggestions}")

    return Response(suggestions)


def home(request):
    return render(request, 'index.html')