use std::io;
use std::io::{BufRead, StdinLock};
use std::collections::{HashMap, HashSet};


// Pure BFS too slow
fn _exists_path_bfs(p0: usize, p1: usize, streets: &Vec<Vec<i8>>) -> bool {
    // Search if there is an existing path from p0 to p1 using the streets
    // # Arguments
    // p0, p1

    // Breadth-first search
    let mut itinerary: Vec<usize> = vec![p0];
    let mut visited: HashSet<usize> = HashSet::new();
    visited.insert(p0);

    while itinerary.len() > 0 {
        // println!("Itinerary: {:?}", itinerary);
        let mut extension = Vec::<usize>::new();
        let mut neighbs: Vec<usize>;
        for node in itinerary.iter(){
            visited.insert(*node);
            neighbs = get_neighbours(&streets[*node], &visited);
            extension.extend(neighbs);
            //println!("Extension{:?}", extension);
        }
        itinerary = extension;
        if visited.contains(&p1){
            return true;
        }
    }
    return false;
}


// Pure DFS too slow
fn exists_path_dfs(start: usize, goal: usize, streets: &mut Vec<Vec<i8>>) -> bool {
    // Check for known shortcut (if path is known or known not to exist)
    // println!("Check from {} to {}", start, goal);
    if streets[start][goal] == 1 {
        return true;
    } else if streets[start][goal] == -1 {
        return false;
    }

    // DFS on graph, remember visited nodes in HashSet
    let mut visited = HashSet::new();
    let path_exists = dfs(&mut visited, streets, start, goal);

    // Collect nodes reachable from start, For all reachable nodes mark the goal node as unreachable
    // if dfs found no path
    if !path_exists {
        let all_neighbs: Vec<usize> = get_neighbours(&streets[start], &HashSet::new());
        let mut reachables = HashSet::<usize>::new();
        for reached in all_neighbs {
            reachables.insert(reached);
        }
        reachables.insert(start);
        // println!("Reachable: {:?}", reachables);
        no_paths(&reachables, goal, streets);
    }

    // print_array(streets, "Streets end");

    return path_exists;
}

fn dfs(visited: &mut HashSet<usize>, streets: &mut Vec<Vec<i8>>, this: usize, goal: usize) -> bool {
    // println!("In {}: visited: {:?}", this, visited);
    // add_paths(visited, this, streets);

    // Get neighbors and check if termination (pos or neg) is reached => No continuation
    let neighbors = get_neighbours(&streets[this], visited);

    if streets[this][goal] == -1 || neighbors.len() == 0 || visited.contains(&this){
        // println!("In {}: Can't go further!", this);
        add_paths(visited, this, streets);
        return false;
    } else if neighbors.contains(&goal) {
        // println!("In {}: Goal is a neighbor!", this);
        visited.insert(this);
        add_paths(visited, goal, streets);
        return true;
    }

    // No termination, add this to visited and continue search
    visited.insert(this);
    // println!("Visit neighbs: {:?}", neighbors);
    for n in neighbors.iter() {
        if dfs(visited, streets, *n, goal) {
            return true;
        }
    }
    // println!("No path found, remove this from visited");
    visited.remove(&this);
    return false;
}

pub fn main(){
    let letter_mapping = get_letter_mapping();

    let stdin = io::stdin();
    let mut map_size: Vec<usize>;
    let mut street_map: Vec<Vec<i8>>;

    // Read in n_cases, initialize read-in buffer line_val
    let mut n_cases_str = String::new();
    let _ = stdin.read_line(&mut n_cases_str);
    let n_cases = n_cases_str.trim().parse::<usize>().unwrap();
    let mut line_val = String::new();

    // Create reader so that it can be passed to read_map (reads unknown no. of lines)
    let mut reader = stdin.lock();

    for _ in 0..n_cases {
        // n_junctions and n_roads
        _ = reader.read_line(&mut line_val);

        // Read in new map
        map_size = read_ints(&line_val);
        street_map = read_map(&mut reader, map_size, &letter_mapping);

        let mut friends: Vec<usize>;
        // Go through all road tests until empty line
        'tests: loop {
            line_val.clear(); // Else it appends to old line_val
            let _ = reader.read_line(&mut line_val);

            // Empty line signals end of testcase
            if line_val.trim() == "" {
                break 'tests;
            }

            // Get junction no.s of friend pair from letter numbers
            friends = line_val.trim().split("<=>")
                .map(|l| letter_to_int(l, &letter_mapping))
                .collect::<Vec<usize>>();

            // Check if there exist ways in both directions, note findings on street_map
            for dir in 0..=1 {
                if !exists_path_dfs(friends[dir], friends[1-dir], &mut street_map) {
                    println!("Footwalking");
                    continue 'tests;
                }
            }
            println!("Car is OK")
        }
        line_val.clear();
        // print_array(&street_map, "Final Street Map");
    }

}
// Helper functions here

fn add_paths(froms: &HashSet<usize>, to: usize, streets: &mut Vec<Vec<i8>>) {
    for past_node in froms {
        // println!("Add path {}=>{}", past_node, to);
        streets[*past_node][to] = 1;
    }
}

fn no_paths(froms: &HashSet<usize>, to: usize, streets: &mut Vec<Vec<i8>>) {
    for past_node in froms {
        // println!("No path {}=>{}", past_node, to);
        streets[*past_node][to] = -1;
    }
}

fn read_ints(line_val: &str) -> Vec<usize> {
    let dims: Vec<usize> = line_val.trim()
                .split_whitespace()
                .map(|v| v.parse::<usize>())
                .filter_map(Result::ok)
                .collect();
    // println!("{:?}", dims);
    return dims;
}

fn read_map(reader: &mut StdinLock, dims: Vec<usize>, mapping: &HashMap<char, usize>) -> Vec<Vec<i8>> {
    // dims[0]: n junctions, dims[1]: n roads
    let mut map = vec![vec![0; dims[0]]; dims[0]];
    let mut junctions: Vec<usize>;

    for _ in 0..dims[1]{
        let mut string = String::new();
        let _ = reader.read_line(&mut string);
        junctions = string.trim().split("=>")
            .map(|s| letter_to_int(s, mapping))
            .collect::<Vec<usize>>();
        map[junctions[0]][junctions[1]] = 1;
    }
    return map;
}

fn letter_to_int(l: &str, mapping: &HashMap<char, usize>) -> usize {
    let len = l.chars().count();
    let mut index: usize = 0;

    for (i, c) in l.chars().enumerate() {
        index = index + (pow(26, len - 1 - i) * mapping.get(&c).unwrap()) as usize;
    }

    return index;
}

fn get_neighbours(adjacency_row: &[i8], visited: &HashSet<usize>) -> Vec<usize> {
    let result: Vec<usize> = adjacency_row.iter()
     .enumerate()
     .filter_map(|(index, &value)| if value == 1 && !visited.contains(&index) { Some(index) } else { None })
     .collect();

    // println!("result {:?}", result);
    return result;
}


fn pow(base: usize, exp: usize) -> usize {
    if exp == 0 {
        return 1;
    }
    let res = pow(base, exp/2);
    if exp % 2 == 0 {
        return res * res;
    } else {
        return base * res * res;
    }
}

fn print_array(array: &Vec<Vec<i8>>, prologue: &str) {
    println!("{}", prologue);
    for row in array {
        for el in row {
            print!("{}", el);
        }
        println!();
    }
}

fn get_letter_mapping() -> HashMap<char, usize> {
    let letters = vec![
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ];
    let mut letter_mapping: HashMap<char, usize> = HashMap::new();
    for (val, letter) in letters.iter().enumerate(){
        letter_mapping.insert(*letter, val);
    }

    return letter_mapping;
}

