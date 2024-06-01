use std::io;
use crate::helpers;


pub fn main() {
    let stdin = io::stdin();

    let mut n_cases_str = String::new();
    let _ = stdin.read_line(&mut n_cases_str);
    let n_cases = n_cases_str.trim().parse::<usize>().unwrap();

    let mut line_val = String::new();
    let mut params: Vec<u64>;

    //Initialize important values
    let mut fib = vec![vec![0;2];2]; // saves exp. fib matrix
    let fib_start = vec![1;2]; // starting values F_0 and F_1
    let fib_matrix = vec![vec![1, 1], vec![1, 0]]; // Fibonacci iteration matrix

    for _ in 0..n_cases {
        // params: j m
        //         0 1
        line_val = String::new();
        stdin.read_line(&mut line_val);
        params = helpers::read_ints(&line_val);

        fib = vec![vec![0;2];2];
        let n_iter = params[0];
        let modulo_op = params[1];

        if n_iter > 1 {
            // n > 1: Do algorithm
            helpers::fast_exp(&mut fib, &fib_matrix, n_iter, modulo_op);
        } else if n_iter <= 1 {
            println!("{}", 1);
            continue
        }

        let final_res = helpers::mat_vec_mult(&fib, &fib_start, modulo_op);
        println!("{}", final_res[1]);
    }
}

