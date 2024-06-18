def read_interference_graph_from_file(filename):
    """
    Reads an interference graph from a file. Each line in the file should define a node and its interfering nodes, separated by commas.
    The function ensures that the nodes are provided in consecutive ascending order without duplicates.
    It returns a graph as a dictionary or an error message if the file format is not followed,
    """
    graph = {}
    expected_node = 1  # Ensures nodes are listed in consecutive order starting from 1.
    try:
        with open(filename, "r") as f:
            lines = f.readlines()  # Read all lines from the file.
        if not lines:
            return "Error: The file is empty."  # Error if the file is empty.

        for line in lines:
            # Validate file content only contains digits, commas, or whitespace.
            if not all(c.isdigit() or c == ',' or c.isspace() for c in line):
                return "Invalid file content; contains characters other than digits, commas, or end-of-line."

            parts = line.strip().split(',')  # Split each line by comma to separate node IDs.
            node = int(parts[0])  # Convert the first part to integer representing the node ID.
            
            # Check for node order and duplication errors.
            if node != expected_node:
                if node < expected_node:
                    # If a node ID reappears, it's a duplication.
                    return f"Error: Duplicate node definition found for node {node}."
                else:
                    # If there's a gap in node IDs, nodes are missing.
                    return f"Error: Missing node definitions or nodes are not in consecutive order. Expected node {expected_node}, found {node}."

            # Range check for node ID.
            if node < 1 or node > 50:
                return "Node number out of range. Each node must be between 1 and 50."
            
            # Parse and validate neighbor IDs.
            neighbors = [int(n) for n in parts[1:] if n.isdigit()]
            if any(n < 1 or n > 50 for n in neighbors):
                return "Neighbor number out of range. Each neighbor must be between 1 and 50."
            
            # Store node with its neighbors in the graph.
            graph[node] = set(neighbors)
            expected_node += 1  # Prepare for the next expected node ID.

    except ValueError:
        return "Invalid file content; unable to convert to integers."
    except Exception as e:
        return f"Unexpected error: {str(e)}"

    return graph


def rank_nodes_by_neighbours(interference_graph):
    """
    Ranks nodes based on the number of their neighbours in descending order.
    In case of a tie, nodes are sorted by their ID in ascending order.
    Returns a list of tuples, each containing a node ID and its set of neighbours.
    """
    # Prepare a list of tuples for sorting: (node ID, neighbours, count of neighbours).
    nodes_info = [(node, neighbours, len(neighbours)) for node, neighbours in interference_graph.items()]
    
    # Sort nodes first by the count of neighbours (descending), then by node ID (ascending).
    ranked_nodes_info = sorted(nodes_info, key=lambda x: (-x[2], x[0]))
    
    # Return sorted nodes, excluding the neighbour count for simplicity.
    ranked_nodes_with_neighbours = [(node, neighbours) for node, neighbours, _ in ranked_nodes_info]
    
    return ranked_nodes_with_neighbours


def assign_colours(graph, ranked_nodes_with_neighbours):
    """
    Assigns colours to each node based on the provided ranking and ensures no adjacent nodes share the same colour.
    Returns a dictionary mapping each node ID to its assigned colour.
    """
    # Define a list of available colours.
    colours = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    colour_assignment = {}  # Tracks the assigned colour for each node.

    # Iterate over ranked nodes to assign colours.
    for node, _ in ranked_nodes_with_neighbours:
        # Determine which colours have been used by this node's neighbours.
        assigned_colours = {colour_assignment.get(neighbour) for neighbour in graph[node]}
        
        # Assign the first unused colour to this node.
        for colour in colours:
            if colour not in assigned_colours:
                colour_assignment[node] = colour
                break

    return colour_assignment


def write_output_file(filename, colour_assignment):
    """
    Writes the colour assignments for each node to the specified output file.
    Each line in the file contains a node ID and its assigned colour.
    """
    with open(filename, 'w') as f:
        # Write each node's ID and colour, sorted by node ID.
        for node, colour in sorted(colour_assignment.items()):
            f.write(f"{node}{colour}\n")


def main(input_filename, output_filename):
    """
    Main function to orchestrate the reading, processing, and writing of the graph colouring task.
    """
    # Read the graph; handle errors if any.
    graph_or_error = read_interference_graph_from_file(input_filename)
    if isinstance(graph_or_error, str):
        # If an error message was returned, print it and exit.
        print(graph_or_error)
        return

    # Proceed with the correct graph data.
    graph = graph_or_error
    # Rank nodes, assign colours based on ranks, and write the results to the output file.
    ranked_nodes = rank_nodes_by_neighbours(graph)
    colored_graph = assign_colours(graph, ranked_nodes)
    write_output_file(output_filename, colored_graph)


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 program.py input.txt output.txt")
    else:
        main(sys.argv[1], sys.argv[2])
