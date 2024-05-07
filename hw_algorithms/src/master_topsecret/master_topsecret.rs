use std::io;
use std::io::{Lines, StdinLock};


fn build_mult_mat(n: usize, l: i32, r: i32) -> Vec<Vec<i32>> {
    let mut matrix: Vec<Vec<i32>> = vec![vec![0;n];n];
    for i in 0..n {
        matrix[i][(i + n - 1) % n] = l;
        matrix[i][i] = 1;
        matrix[i][(i + 1) % n] = r;
    }

    return matrix;
}

fn matrix_multiply(A: &Vec<Vec<i32>>, B: &Vec<Vec<i32>>) -> Vec<Vec<i32>>{
    return A.clone();
}

fn fast_exp(A: &Vec<Vec<i32>>, n: i32, size: usize, thresh: i32, strip: bool) -> Option<Vec<Vec<i32>>> {
    // Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than 10^thresh
    if n == 0 {
        return None;
    }

    let res = fast_exp(A, n / 2, size, thresh, !strip);
    let mut R: Vec<Vec<i32>>;

    match res {
        Some(a_mat) => {R = matrix_multiply(&a_mat, &a_mat)},
        None => {R = A.clone()},
    }

    if n % 2 == 1 && n != 1 {
        R = matrix_multiply(&R, &A);
    }

    return Some(R);
}

fn next_line(iter: &mut Lines<StdinLock>) -> Vec<i32> {
    iter
        .next()
        .unwrap()
        .unwrap()
        .trim()
        .split_whitespace()
        .map(|x| x.parse::<i32>())
        .filter_map(Result::ok)
        .collect()
}

pub fn main() {
    let stdin = io::stdin();
    let mut line_iter = stdin.lines();

    let n_cases = line_iter.next().unwrap().unwrap().trim().parse::<i32>().unwrap();
    let mut params: Vec<i32>;
    let mut values: Vec<i32>;

    for _ in 0..n_cases {
        params = next_line(&mut line_iter);
        values = next_line(&mut line_iter);

        // params: N, S, L, R, X
        let matrix = build_mult_mat(params[0] as usize, params[2], params[3]);
        let A_n = fast_exp(&matrix, params[1], params[0] as usize, params[4], true);
        let final_res: Vec<Vec<i32>>;
        match A_n {
            Some(last) => {final_res = last},
            None => {final_res = matrix},
        }

        println!("FIN: {:?}", final_res);

        match line_iter.next() {
            Some(_) => {}
            None => break
        }

    }

}