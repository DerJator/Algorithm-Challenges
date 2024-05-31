
/// Returns base^exp, implemented efficiently
pub fn pow(base: u64, exp: u64) -> u64 {
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


/* MATRIX STUFF */

/// Builds u64 Identity matrix of dim size x size
fn build_identity_mat(mat: &mut Vec<Vec<u64>>, size: usize) {
    // mat = vec![vec![0 as u64; size]; size];
    for i in 0..size {
        for j in 0.. size {
            mat[i][j] = (i == j) as u64;
        }
    }
}

/// u64 matrix-vector multiplication O(m*n)
pub fn mat_vec_mult(a_mat: &Vec<Vec<u64>>, v: &Vec<u64>, mod_op: u64) -> Vec<u64> {
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

/// Standard u64 matrix multiplication O(m^3)
pub fn matrix_multiply(A: &Vec<Vec<u64>>, B: &Vec<Vec<u64>>, mod_op: u64) -> Vec<Vec<u64>>{
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



/// Recursively multiply squared matrix A until exponent n is reached. Keep numbers lower than thresh
/// Runtime: log(n) * m^3
/// NOT YET TESTED IN UNIVERSAL FORM
fn fast_exp(new_val: &mut Vec<Vec<u64>>, base_mat: &Vec<Vec<u64>>, n: u64, modulo_op: u64) {

    // println!("n: {}", n);
    if n == 0 {
        build_identity_mat(new_val, new_val.len());
        return;
    }

    fast_exp(new_val, base_mat, n / 2, modulo_op);

    if n % 2 == 0 {
        *new_val = matrix_multiply(new_val, new_val, modulo_op);
    } else {
        *new_val = matrix_multiply(base_mat, &matrix_multiply(new_val, new_val, modulo_op), modulo_op);
    }
}


/* PARSING */
/// Function takes in line string (from stdin.read_line()) and gives u64 vector of ints
pub fn read_ints(line_val: &str) -> Vec<u64> {
    let dims: Vec<u64> = line_val.trim()
                .split_whitespace()
                .map(|v| v.parse::<u64>())
                .filter_map(Result::ok)
                .collect();
    // println!("{:?}", dims);
    return dims;
}
