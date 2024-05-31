use std::io;
use std::io::{Lines, StdinLock};
use crate::helpers;


pub fn main() {
    let stdin = io::stdin();

    let mut n_cases_str = String::new();
    let _ = stdin.read_line(&mut n_cases_str);
    let n_cases = n_cases_str.trim().parse::<usize>().unwrap();

    let mut line_val = String::new();
    let mut params: Vec<u64>;

    let mut fib = vec![vec![0;2];2];
    let fib_start = vec![1;2];
    let fib_matrix = vec![vec![1, 1], vec![1, 0]];

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
            // S>1: Do algorithm
            fast_exp(&mut fib, &fib_matrix, n_iter, modulo_op);
        } else if n_iter <= 1 {
            println!("{}", 1);
            continue
        }

        let final_res = helpers::mat_vec_mult(&fib, &fib_start, modulo_op);
        // print!("Result vec: ");
        println!("{}", final_res[1]);

    }
}


fn fast_exp(new_fib: &mut Vec<Vec<u64>>, fib_mat: &Vec<Vec<u64>>, n: u64, thresh: u64) {
    // Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than thresh
    // Runtime: log(s) * n^3

    // println!("n: {}", n);
    if n == 0 {
        *new_fib = vec![vec![0, 1], vec![1, 0]];
        return;
    }

    fast_exp(new_fib, fib_mat, n / 2, thresh);

    if n % 2 == 0 {
        *new_fib = helpers::matrix_multiply(new_fib, new_fib, thresh);
    } else {
        *new_fib = helpers::matrix_multiply(fib_mat, &helpers::matrix_multiply(new_fib, new_fib, thresh), thresh);
    }
}


