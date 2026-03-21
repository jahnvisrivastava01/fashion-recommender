import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ----- Define Fashion Graphs -----

# Female items
items_female = {
    "Dress": ["Red Dress", "Blue Dress", "Black Dress", "White Gown", "Party Dress"],
    "Accessories": ["Earrings", "Necklace", "Handbag", "Scarf", "Belt"],
    "Shoes": ["Heels", "Flats", "Boots", "Sandals"]
}

# Female edges (compatibility)
edges_female = [
    ("Red Dress", "Heels"), ("Red Dress", "Handbag"),
    ("Blue Dress", "Flats"), ("Black Dress", "Boots"),
    ("White Gown", "Necklace"), ("Party Dress", "Heels"),
    ("Scarf", "Handbag"), ("Earrings", "Necklace")
]

# Female occasions
occasions_female = {
    "Red Dress": ["Party", "Evening"],
    "Blue Dress": ["Casual", "Day"],
    "Black Dress": ["Formal", "Evening"],
    "White Gown": ["Party", "Formal"],
    "Party Dress": ["Party"],
    "Heels": ["Formal", "Party"],
    "Flats": ["Casual"],
    "Boots": ["Casual", "Evening"],
    "Sandals": ["Day", "Casual"],
    "Earrings": ["Party", "Formal"],
    "Necklace": ["Formal"],
    "Handbag": ["Day", "Party"],
    "Scarf": ["Casual", "Day"],
    "Belt": ["Formal"]
}

# Male items
items_male = {
    "Dress": ["Shirt", "T-Shirt", "Blazer", "Jeans", "Suit"],
    "Accessories": ["Watch", "Tie", "Sunglasses", "Belt"],
    "Shoes": ["Formal Shoes", "Sneakers", "Loafers"]
}

edges_male = [
    ("Shirt", "Jeans"), ("Blazer", "Tie"), ("Watch", "Blazer"),
    ("Formal Shoes", "Jeans"), ("Tie", "Shirt"), ("Sunglasses", "Blazer")
]

occasions_male = {
    "Shirt": ["Formal", "Casual"],
    "T-Shirt": ["Casual", "Day"],
    "Blazer": ["Formal", "Party"],
    "Jeans": ["Casual", "Day"],
    "Suit": ["Formal", "Party"],
    "Watch": ["Formal", "Casual"],
    "Tie": ["Formal"],
    "Sunglasses": ["Casual", "Day"],
    "Belt": ["Formal"],
    "Formal Shoes": ["Formal"],
    "Sneakers": ["Casual"],
    "Loafers": ["Formal", "Casual"]
}

# ----- Build graph -----
def build_graph(items, edges):
    G = nx.Graph()
    nodes = [i for cat in items.values() for i in cat]
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

# ----- GNN Layer -----
def gnn_layer(adj_matrix, features, weights):
    agg = adj_matrix @ features
    out = np.tanh(agg @ weights)
    return out

# ----- Get Recommendations -----
def get_recommendations(gender, selections, top_k=5):
    if gender == "female":
        G = build_graph(items_female, edges_female)
        occ = occasions_female
    else:
        G = build_graph(items_male, edges_male)
        occ = occasions_male

    nodes = list(G.nodes)
    A = nx.to_numpy_array(G)
    features = np.eye(len(nodes))
    weights = np.random.rand(len(nodes), len(nodes))

    h1 = gnn_layer(A, features, weights)
    embeddings = gnn_layer(A, h1, weights)
    node_idx = {node: i for i, node in enumerate(nodes)}

    selected_nodes = [v for v in selections.values() if v in node_idx]
    if not selected_nodes:
        recommended_nodes = nodes[:top_k]
    else:
        agg_embedding = embeddings[[node_idx[n] for n in selected_nodes]].mean(axis=0)
        sims = cosine_similarity([agg_embedding], embeddings)[0]
        sorted_idx = sims.argsort()[::-1]
        recommended_nodes = [nodes[i] for i in sorted_idx if nodes[i] not in selected_nodes][:top_k]

    # Include occasions
    recommendations = [{"item": n, "occasions": occ.get(n, [])} for n in recommended_nodes]
    return {"recommended_items": recommendations}
