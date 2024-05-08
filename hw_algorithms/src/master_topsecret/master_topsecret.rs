use std::io;
use std::io::{Lines, StdinLock};

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

fn build_mult_mat(n: usize, l: u64, r: u64) -> Vec<Vec<u64>> {
    let mut matrix: Vec<Vec<u64>> = vec![vec![0;n];n];
    for i in 0..n {
        matrix[i][(i + n - 1) % n] = l;
        matrix[i][i] = 1;
        matrix[i][(i + 1) % n] = r;
    }

    return matrix;
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

    for i in 0..a_mat.len() {
        let mut run_sum = 0;
        for j in 0..a_mat[0].len() {
            run_sum += a_mat[i][j] * v[j];
        }
        result[i] = run_sum % mod_op;
    }

    return result;
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
            }
        }
    }

    return result;
}

fn fast_exp2(A: &mut Vec<Vec<u64>>, ref_mat: &Vec<Vec<u64>>, n: u64, size: usize, thresh: u64, strip: bool) {
    // Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than 10^thresh
    if n == 0 {
        build_identity_mat(A, size);
        return;
    }

    fast_exp2(A, ref_mat, n / 2, size, thresh, !strip);

    if n % 2 == 0 {
        *A = matrix_multiply(A, A, thresh);
    } else {
        *A = matrix_multiply(ref_mat, &matrix_multiply(A, A, thresh), thresh);
    }
}


fn fast_exp(A: &Vec<Vec<u64>>, n: u64, size: usize, thresh: u64, strip: bool) -> Option<Vec<Vec<u64>>> {
    // Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than 10^thresh
    if n == 0 {
        return None;
    }

    let res = fast_exp(A, n / 2, size, thresh, !strip);
    let mut R: Vec<Vec<u64>>;

    match res {
        Some(a_mat) => {R = matrix_multiply(&a_mat, &a_mat, thresh)},
        None => {R = A.clone()},
    }

    if n % 2 == 1 && n != 1 {
        R = matrix_multiply(&R, &A, thresh);
    }

    return Some(R);
}

fn next_line(iter: &mut Lines<StdinLock>) -> Vec<u64> {
    iter
        .next()
        .unwrap()
        .unwrap()
        .trim()
        .split_whitespace()
        .map(|x| x.parse::<u64>())
        .filter_map(Result::ok)
        .collect()
}

pub fn main() {
    let stdin = io::stdin();
    let mut line_iter = stdin.lines();

    let n_cases = line_iter.next().unwrap().unwrap().trim().parse::<u64>().unwrap();
    let mut params: Vec<u64>;
    let mut values: Vec<u64>;

    for _ in 0..n_cases {
        params = next_line(&mut line_iter);
        values = next_line(&mut line_iter);

        // params: N, S, L, R, X
        //         0, 1, 2, 3, 4
        let mut matrix = build_mult_mat(params[0] as usize, params[2], params[3]);
        let mut A_n= matrix.clone();
        let modulo_op = pow(10, params[4]);

        if params[1] > 1 {
            // S>1: Do algorithm
            fast_exp2(&mut A_n, &matrix, params[1], params[0] as usize, modulo_op, true);
        } else if params[1] == 1 {
            // S=1: return start matrix
            A_n = matrix;
        } else {
            // S=0: return Identity
            build_identity_mat(&mut A_n, params[0] as usize);
        }

        /*
        let algo_res: Vec<Vec<u64>>;
        match A_n {
            Some(last) => { algo_res = last },
            None => { algo_res = matrix },
        }
        */

        let final_res = mat_vec_mult(&A_n, &values, modulo_op);
        for el in final_res.iter() {
            print!("{} ", el);
        }
        println!();

        match line_iter.next() {
            Some(_) => {}
            None => break
        }
    }

}