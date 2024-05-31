use std::io;
use std::io::{Lines, StdinLock};
use crate::helpers;

fn pow(base: u64, exp: u64) -> u64 {
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


fn build_identity_mat(mat: &mut Vec<Vec<u64>>, size: usize) {
    // mat = vec![vec![0 as u64; size]; size];
    for i in 0..size {
        for j in 0.. size {
            mat[i][j] = (i == j) as u64;
        }
    }
}

fn mat_vec_mult(a_mat: &Vec<Vec<u64>>, v: &Vec<u64>, mod_op: u64) -> Vec<u64> {
    let mut result: Vec<u64> = vec![0;a_mat.len()];

    let mut run_sum;
    for i in 0..a_mat.len() {
        run_sum = 0;
        for j in 0..a_mat[0].len() {
            run_sum += (a_mat[i][j] * v[j]) % mod_op;
            run_sum = run_sum % mod_op;
        }
        result[i] = run_sum;
    }

    return result;
}


fn read_ints(line_val: &str) -> Vec<u64> {
    let dims: Vec<u64> = line_val.trim()
                .split_whitespace()
                .map(|v| v.parse::<u64>())
                .filter_map(Result::ok)
                .collect();
    // println!("{:?}", dims);
    return dims;
}


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
        params = read_ints(&line_val);

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

        let final_res = mat_vec_mult(&fib, &fib_start, modulo_op);
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
    // println!("{:?} at ({})", new_fib, n);


    if n % 2 == 0 {
        *new_fib = matrix_multiply(new_fib, new_fib, thresh);
    } else {
        *new_fib = matrix_multiply(fib_mat, &matrix_multiply(new_fib, new_fib, thresh), thresh);
    }
}


fn matrix_multiply(A: &Vec<Vec<u64>>, B: &Vec<Vec<u64>>, mod_op: u64) -> Vec<Vec<u64>>{
    let m = A.len();
    let n1 = A[0].len();
    let n2 = B[0].len();
    let mut result = vec![vec![0;n2]; m];

    for i in 0..m {
        for j in 0..n2 {
            for k in 0..n1 {
                result[i][j] += (A[i][k] * B[k][j]) % mod_op;
                result[i][j] = result[i][j] % mod_op;
            }
        }
    }

    return result;
}


