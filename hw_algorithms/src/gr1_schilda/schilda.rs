use std::io;
use std::io::{BufRead, StdinLock};
use num_traits::pow;
use std::collections::HashMap;


fn read_ints(line_val: &str) -> Vec<usize> {
    let dims: Vec<usize> = line_val.trim()
                .split_whitespace()
                .map(|v| v.parse::<usize>())
                .filter_map(Result::ok)
                .collect();
    // println!("{:?}", dims);
    return dims;
}

fn read_map(reader: &mut StdinLock, dims: Vec<usize>, mapping: &HashMap<char, i32>) -> Vec<Vec<bool>> {
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

fn letter_to_int(l: &str, mapping: &HashMap<char, i32>) -> usize {
    let len = l.chars().count();
    let mut index: usize = 0;

    for (i, c) in l.chars().enumerate() {
        index = index + (pow(26, len - 1 - i) * mapping.get(&c).unwrap()) as usize;
    }

    return index;
}

fn exists_path(p0: usize, p1: usize, streets: &Vec<Vec<bool>>) -> bool {
    println!("{}, {}\n{:?}", p0, p1, streets);

    todo!("Implement BFS");

}

pub fn main(){
    // Create mapping for letter numbers
    let letters = vec![
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ];
    let mut letter_mapping: HashMap<char, i32> = HashMap::new();
    for (val, letter) in letters.iter().enumerate(){
        letter_mapping.insert(*letter, val as i32);
    }

    let stdin = io::stdin();
    let mut map_size: Vec<usize>;
    let mut street_map: Vec<Vec<bool>>;

    let mut n_cases_str = String::new();
    let _ = stdin.read_line(&mut n_cases_str);
    let n_cases = n_cases_str.trim().parse::<usize>().unwrap();
    let mut line_val = String::new();

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
                if !exists_path(friends[dir], friends[1-dir], &street_map) {
                    println!("Footwalking");
                    continue 'tests;
                }
            }
            println!("Car is OK")
        }
        line_val.clear();
    }

}
