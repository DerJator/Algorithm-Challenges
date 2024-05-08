use std::io;
use std::io::{Lines, StdinLock};
use num_traits::pow;


fn build_mult_mat(n: usize, l: u64, r: u64) -> Vec<Vec<u64>> {
    let mut matrix: Vec<Vec<u64>> = vec![vec![0;n];n];
    for i in 0..n {
        matrix[i][(i + n - 1) % n] = l;
        matrix[i][i] = 1;
        matrix[i][(i + 1) % n] = r;
    }

    return matrix;
}

fn mat_vec_mult(a_mat: &Vec<Vec<u64>>, v: &Vec<u64>, thresh: u64) -> Vec<u64> {
    let mut result: Vec<u64> = vec![0;a_mat.len()];

    for i in 0..a_mat.len() {
        let mut run_sum = 0;
        for j in 0..a_mat[0].len() {
            run_sum += a_mat[i][j] * v[j];
        }
        result[i] = run_sum % (pow::<u64>(10, thresh as usize));
    }

    return result;
}

fn matrix_multiply(A: &Vec<Vec<u64>>, B: &Vec<Vec<u64>>, thresh: u64) -> Vec<Vec<u64>>{
    let m = A.len();
    let n1 = A[0].len();
    let n2 = B[0].len();
    let mut result = vec![vec![0;n2]; m];

    for i in 0..m {
        for j in 0..n2 {
            for k in 0..n1 {
                result[i][j] += (A[i][k] * B[k][j]) % (pow::<u64>(10, thresh as usize));
            }
        }
    }

    return result;
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
        let matrix = build_mult_mat(params[0] as usize, params[2], params[3]);
        if params[1] <= u64::MAX {
            let A_n;
            if params[1] > 1 {
                // S>1: Do algorithm
                A_n = fast_exp(&matrix, params[1], params[0] as usize, params[4], true);
            } else if params[1] == 1 {
                // S=1: return start matrix
                A_n = None;  // match below handles None as if
            } else {
                // S=0: return Identity
                let mut intermediate: Vec<Vec<u64>> = vec![vec![0 ;params[0] as usize]; params[0] as usize];
                for i in 0..params[0] as usize {
                    intermediate[i][i] = 1;
                }
                A_n = Some(intermediate);
            }

            let algo_res: Vec<Vec<u64>>;
            match A_n {
                Some(last) => { algo_res = last },
                None => { algo_res = matrix },
            }

            let final_res = mat_vec_mult(&algo_res, &values, params[4]);
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

}