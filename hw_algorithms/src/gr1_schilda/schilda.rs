use std::io;
use std::io::{BufRead, StdinLock};
use std::collections::{HashMap, HashSet};


// Pure BFS too slow
fn _exists_path_bfs(p0: usize, p1: usize, streets: &Vec<Vec<bool>>) -> bool {
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
            neighbs =  get_neighbours(&streets[*node], &visited);
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
fn exists_path_dfs(p0: usize, p1: usize, streets: &mut Vec<Vec<bool>>) -> bool {
    let mut visited = HashSet::new();
    // visited.insert(p0);

    return dfs(&mut visited, streets, p0, p1);
}

fn dfs(visited: &mut HashSet<usize>, streets: &mut Vec<Vec<bool>>, this: usize, goal: usize) -> bool {
    // println!("In {}: visited: {:?}", this, visited);
    add_paths(visited, this, streets);

    // Get neighbors and check if termination (pos or neg) is reached => No continuation
    let neighbors = get_neighbours(&streets[this], visited);
    // println!("Neighb: {:?}", neighbors);
    if neighbors.contains(&goal) {
        // println!("Goal is a neighbor!");
        add_paths(visited, goal, streets);
        return true;
    } else if neighbors.len() == 0 || visited.contains(&this) {
        // println!("No neighbors or we were already here.");
        return false;
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
    // Create mapping for letter numbers
    let letters = vec![
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ];
    let mut letter_mapping: HashMap<char, usize> = HashMap::new();
    for (val, letter) in letters.iter().enumerate(){
        letter_mapping.insert(*letter, val);
    }

    let stdin = io::stdin();
    let mut map_size: Vec<usize>;
    let mut street_map: Vec<Vec<bool>>;

    // Read in n_cases, initialize read-in buffer
    let mut n_cases_str = String::new();
    let _ = stdin.read_line(&mut n_cases_str);
    let n_cases = n_cases_str.trim().parse::<usize>().unwrap();
    let mut line_val = String::new();

    // Create reader so that it can be passe to read map (reads unknown no. of lines)
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
            if line_val.trim() == "" {
                break 'tests;
            }
            // Get junction no.s of friends from letter numbers
            friends = line_val.trim().split("<=>")
                .map(|l| letter_to_int(l, &letter_mapping))
                .collect::<Vec<usize>>();

            // Check if there exist ways in both directions
            for dir in 0..=1 {
                if !exists_path_dfs(friends[dir], friends[1-dir], &mut street_map) {
                    println!("Footwalking");
                    continue 'tests;
                }
            }
            println!("Car is OK")
        }
        line_val.clear();
    }

}
// Helper functions here

fn add_paths(froms: &HashSet<usize>, to: usize, streets: &mut Vec<Vec<bool>>) {
    for past_node in froms {
        // println!("Add path {}=>{}", past_node, to);
        streets[*past_node][to] = true;
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

fn read_map(reader: &mut StdinLock, dims: Vec<usize>, mapping: &HashMap<char, usize>) -> Vec<Vec<bool>> {
    // dims[0]: n junctions, dims[1]: n roads
    let mut map = vec![vec![false; dims[0]]; dims[0]];
    let mut junctions: Vec<usize>;

    for _ in 0..dims[1]{
        let mut string = String::new();
        let _ = reader.read_line(&mut string);
        junctions = string.trim().split("=>")
            .map(|s| letter_to_int(s, mapping))
            .collect::<Vec<usize>>();
        map[junctions[0]][junctions[1]] = true;
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

fn get_neighbours(adjacency_row: &[bool], visited: &HashSet<usize>) -> Vec<usize> {
    let result: Vec<usize> = adjacency_row.iter()
     .enumerate()
     .filter_map(|(index, &value)| if value && !visited.contains(&index) { Some(index) } else { None })
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

