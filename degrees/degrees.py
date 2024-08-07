import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f: 
        reader = csv.DictReader(f) #Lo leemos con DictReader y lo guardamos en "reader"
        for row in reader: #Por cada entrada en "reader" 
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            } #Guardamos en people en la fila id la estructura de datos name, birth, y en movies dejamos creado un set
            if row["name"].lower() not in names: #Si el nombre no esta en el mapa names lo metemos 
                names[row["name"].lower()] = {row["id"]}
            else: #En caso de que si añadimos el id del nombre que sea igual, teniendo dos personas que se llaman igual con diferente id
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f: 
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader: # Para cada linea intentamos guardar 
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    s = input("Name: ")
    source = person_id_for_name(s)
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        if degrees == 0:
            print(f"{s} is him")
        else: 
            path = [(None, source)] + path
            for i in range(degrees):
                person1 = people[path[i][1]]["name"]
                person2 = people[path[i + 1][1]]["name"]
                movie = movies[path[i + 1][0]]["title"]
                print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    solution = []

    s = Node(state=source, parent=None, action=None)
    if source == target:
        return solution
    else:
        frontier = QueueFrontier() # Creamos la frontera
        frontier.add(s)
        
        explored = set()

        while True:
            
            if frontier.empty():
                return None
            
            nodo = frontier.remove()
            
            explored.add(nodo.state)

            for movie_id, person_id in neighbors_for_person(nodo.state):
                if not frontier.contains_state(person_id) and person_id not in explored:
                    child = Node(state=person_id, parent=nodo, action=movie_id)
                    if child.state == target: # Si hemos llegado al objetivo haremos backtrack para hallar la solucion
                        solution.append((movie_id, person_id))
                        while nodo.parent is not None:
                            solution.append((nodo.action, nodo.state))
                            nodo = nodo.parent
                        solution.reverse()
                        return solution
                    frontier.add(child)   
    #raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
