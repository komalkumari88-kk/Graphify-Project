
import json
from pathlib import Path

import streamlit as st

# Find graph.json in the existing Graphify output folder
GRAPH_PATH = (
    Path(__file__).resolve().parent.parent
    / "graphify-out"
    / "graph.json"
)

st.set_page_config(
    page_title="Graphify AI Explorer",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Graphify Code Explorer")
st.caption("Ask questions and explore nodes, source files, and connections.")

STOP_WORDS = {
    "what", "which", "where", "who", "how", "does", "do",
    "is", "are", "the", "a", "an", "in", "on", "of", "to",
    "for", "and", "me", "this", "that", "explain", "show",
    "find", "please", "tell", "about", "connected", "with",
}


@st.cache_data(show_spinner="Loading your Graphify graph...")
def load_graph(path_string):
    with open(path_string, "r", encoding="utf-8") as file:
        graph = json.load(file)

    adjacency = {}
    for link in graph.get("links", []):
        adjacency.setdefault(link.get("source"), []).append(link)
        adjacency.setdefault(link.get("target"), []).append(link)

    return graph, adjacency


def search_nodes(graph, question, limit=10):
    words = [
        word.strip(".,?!:;()[]{}\"'").lower()
        for word in question.split()
    ]
    words = [
        word for word in words
        if word and word not in STOP_WORDS
    ]

    results = []

    for node in graph.get("nodes", []):
        label = str(node.get("label", ""))
        source = str(node.get("source_file", ""))
        node_id = str(node.get("id", ""))

        label_lower = label.lower()
        source_lower = source.lower()
        searchable = f"{label_lower} {source_lower} {node_id.lower()}"

        score = 0
        for word in words:
            if word == label_lower:
                score += 10
            elif word in label_lower:
                score += 5
            elif word in source_lower:
                score += 3
            elif word in searchable:
                score += 1

        if score > 0:
            results.append((score, node))

    results.sort(key=lambda item: item[0], reverse=True)
    return results[:limit]


def answer_question(graph, adjacency, question):
    results = search_nodes(graph, question)

    if not results:
        return {
            "message": (
                "I couldn't find a matching node. Try a specific "
                "function, class, symbol, or filename."
            ),
            "results": [],
        }

    return {
        "message": f"I found {len(results)} matching graph nodes.",
        "results": [
            {
                "score": score,
                "node": node,
                "links": adjacency.get(node.get("id"), [])[:5],
            }
            for score, node in results
        ],
    }


if not GRAPH_PATH.exists():
    st.error(f"Graph file not found: {GRAPH_PATH}")
    st.info("Check that graph.json is inside the graphify-out folder.")
    st.stop()

graph, adjacency = load_graph(str(GRAPH_PATH))

with st.sidebar:
    st.header("Graph summary")
    st.metric("Nodes", len(graph.get("nodes", [])))
    st.metric("Connections", len(graph.get("links", [])))
    st.write("**Graph file:**")
    st.code(str(GRAPH_PATH), language=None)
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(
    "Try asking about a class, function, symbol, or file. "
    "For example: `Where is ToolError defined?`"
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            for item in message.get("results", []):
                node = item["node"]
                with st.expander(
                    f"{node.get('label', 'Unknown')} — "
                    f"{node.get('source_file', 'Unknown file')}"
                ):
                    st.write("**Source file:**", node.get("source_file", "Unknown"))
                    st.write("**Location:**", node.get("source_location", "Unknown"))
                    st.write("**Node ID:**", node.get("id", "Unknown"))
                    st.write("**Match score:**", item["score"])

                    if item["links"]:
                        st.write("**Connections:**")
                        for link in item["links"]:
                            st.write(
                                f"- {link.get('source')} → "
                                f"{link.get('target')} "
                                f"({link.get('relation', 'related')})"
                            )
                    else:
                        st.write("No connections listed for this node.")

question = st.chat_input("Ask a question about your code graph...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    result = answer_question(graph, adjacency, question)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": result["message"],
            "results": result["results"],
        }
    )
    st.rerun()
