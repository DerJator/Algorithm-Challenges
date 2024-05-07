use std::io;

pub fn main() {
    let stdin = io::stdin();
    let mut line_iter = stdin.lines();


    let n_cases = line_iter.next().unwrap().unwrap().trim().parse::<i32>().unwrap();
    let mut params: Vec<i32>;
    let mut values: Vec<i32>;

    for _ in 0..n_cases { //stdin.lines().enumerate() {
        params = line_iter
            .next()
            .unwrap()
            .unwrap()
            .trim()
            .split_whitespace()
            .map(|x| x.parse::<i32>())
            .filter_map(Result::ok)
            .collect();
        values = line_iter
            .next()
            .unwrap()
            .unwrap()
            .trim()
            .split_whitespace()
            .map(|x| x.parse::<i32>())
            .filter_map(Result::ok)
            .collect();
        println!("p {:?} - v {:?}", params, values);


        match line_iter.next() {
            Some(_) => {}
            None => break
        }

    }

}