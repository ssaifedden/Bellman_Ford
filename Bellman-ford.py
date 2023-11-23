from pyfiglet import Figlet
from termcolor import colored
import networkx as nx
import matplotlib.pyplot as plt

def print_banner(text, color='blue', font='standard'):
    f = Figlet(font=font)
    banner = f.renderText(text)
    colored_banner = colored(banner, color)
    print(colored_banner)

def bellman_ford(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    prev = {}

    for i in range(len(graph) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    prev[v] = u

    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                raise ValueError(colored("Negative weight cycle detected", 'red'))

    return distances, prev

def create_graph_from_input():
    graph = {}
    all_nodes = set()

    print(colored("Enter edges manually. Type 'done' to finish.", 'blue'))

    while True:
        try:
            edge_input = input("Enter edge (source target weight) or 'done' to finish: ")

            if edge_input.lower() == 'done':
                break

            source, target, weight = edge_input.split()
            all_nodes.add(source)
            all_nodes.add(target)

            if source not in graph:
                graph[source] = {}

            graph[source][target] = int(weight)

        except ValueError:
            print(colored("Invalid input. Please enter edges in the format: 'source target weight'", 'red'))

    for node in all_nodes:
        if node not in graph:
            graph[node] = {}

    return graph, all_nodes

def create_graph_from_file(file_path):
    graph = {}
    all_nodes = set()

    while True:
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    source, target, weight = line.strip().split()
                    all_nodes.add(source)
                    all_nodes.add(target)

                    if source not in graph:
                        graph[source] = {}

                    graph[source][target] = int(weight)

        except FileNotFoundError:
            print(colored(f"File not found: {file_path}", 'red'))
            file_path = input(colored("Enter a valid file path or 'exit' to quit: ", 'blue'))

            if file_path.lower() == 'exit':
                return None, None

            continue

        for node in all_nodes:
            if node not in graph:
                graph[node] = {}

        return graph, all_nodes

def draw_graph(graph):
    G = nx.DiGraph()
    for source, targets in graph.items():
        for target, weight in targets.items():
            G.add_edge(source, target, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)

    node_labels = {node: f"{node}" for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    edge_labels = {(source, target): weight for source, targets in graph.items() for target, weight in targets.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()

def main():
    print_banner("Bellman Ford")
    

    print(colored("Choose input method:", 'white') + '\n')
    print(colored("1. Enter edges manually", 'blue'))
    print(colored("2. Load edges from a file", 'blue') + '\n')

    choice = input(colored("Enter the number of your choice: ", 'white'))

    if choice == '1':
        graph, all_nodes = create_graph_from_input()
        if graph is None or all_nodes is None:
            print(colored("Invalid input. Please restart and enter the graph correctly.", 'red'))
            return
    elif choice == '2':
        file_path = input(colored("Enter the path to the input file: ", 'white'))
        graph, all_nodes = create_graph_from_file(file_path)
        if graph is None or all_nodes is None:
            print(colored("Invalid input. Please restart and enter the graph correctly.", 'red'))
            return
    else:
        print(colored("Invalid choice. Exiting.", 'red'))
        return

    while True:
        start_node = input(colored("Enter the start node ('exit' to return to the menu): ", 'white'))
        if start_node.lower() == 'exit':
            break
        elif start_node in all_nodes:
            break
        else:
            print(colored(f"Start node '{start_node}' not found in the graph. Please enter a valid start node.", 'red'))

    distances, prev = bellman_ford(graph, start_node)

    while True:
        option = input(colored("Choose an option:\n1. See graph design\n2. See results\n3. Exit\nEnter the number of your choice: ", 'blue'))

        if option == '1':
            draw_graph(graph)
        elif option == '2':
            for node, dist in distances.items():
                path = []
                curr_node = node
                while curr_node != start_node:
                    path.append(curr_node)
                    curr_node = prev[curr_node]
                path.append(start_node)
                path.reverse()
                print(colored(f"Shortest path from {start_node} to {node}: {' -> '.join(path)}, cost: {dist}", 'white'))
        elif option == '3':
            print(colored("Exiting.", 'red'))
            break
        else:
            print(colored("Invalid option. Try again.", 'red'))

if __name__ == "__main__":
    main()
