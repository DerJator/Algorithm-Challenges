use std::io;
use std::str;


pub fn main(){
    let stdin = io::stdin();

    for (i, line) in stdin.lines().enumerate(){
        let line_val = line.unwrap();

        // First line is single digit
        if i == 0 {
            let res = line_val.trim().parse::<i32>().unwrap();
            println!("n_cases: {}", res);
            continue
        }

        // Other lines contain two ints
        let int_vals: Vec<i32> = line_val
            .split_whitespace()
            .map(|s| s.parse::<i32>())
            .filter_map(Result::ok)
            .collect();
        println!("{:?}", int_vals);
    }
}