
import json
from pathlib import Path

GRAPH_PATH = (
    Path(__file__).resolve().parent.parent
    / "graphify-out"
    / "graph.json"
)


def load_graph():
    with GRAPH_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def search_nodes(graph, question, limit=10):
    words = question.lower().replace("?", "").split()
    results = []

    for node in graph.get("nodes", []):
        label = str(node.get("label", ""))
        source = str(node.get("source_file", ""))
        node_id = str(node.get("id", ""))

        searchable = f"{label} {source} {node_id}".lower()
        score = sum(word in searchable for word in words)

        if score > 0:
            results.append((score, node))

    results.sort(key=lambda item: item[0], reverse=True)
    return results[:limit]


def main():
    if not GRAPH_PATH.exists():
        print(f"Graph file not found: {GRAPH_PATH}")
        print("Check that graph.json is inside graphify-out.")
        return

    print("Loading Graphify graph...")
    graph = load_graph()

    print(f"Loaded {len(graph.get('nodes', []))} nodes.")
    print("Ask questions about names, symbols, or files.")
    print("Type 'summary' or 'exit'.")

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if question.lower() == "summary":
            print("Nodes:", len(graph.get("nodes", [])))
            print("Connections:", len(graph.get("links", [])))
            continue

        if not question:
            continue

        results = search_nodes(graph, question)

        if not results:
            print("No matching nodes found.")
            continue

        print("\nMatching graph nodes:")
        for score, node in results:
            print(f"\nName: {node.get('label', 'Unknown')}")
            print(f"File: {node.get('source_file', 'Unknown')}")
            print(f"Location: {node.get('source_location', 'Unknown')}")
            print(f"Match score: {score}")

            node_id = node.get("id")
            links = graph.get("links", [])
            related = [
                link for link in links
                if link.get("source") == node_id
                or link.get("target") == node_id
            ]

            for link in related[:5]:
                print(
                    "  Connection:",
                    link.get("source"),
                    "->",
                    link.get("target"),
                    f"({link.get('relation', 'related')})",
                )


if __name__ == "__main__":
    main()
