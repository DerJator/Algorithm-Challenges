use std::io;

fn ansic_rand(a_0: i32, n_iter: usize) -> Vec<i32> {
    let mut rand_nums: Vec<i32> = Vec::with_capacity(n_iter);
    let mut tmp: i64;
    tmp = (a_0 * 1103515245 + 12345) as i64;
    rand_nums.push((tmp % 2147483648) as i32);

    for i in 1..n_iter{
        tmp = (rand_nums.get(i-1).unwrap() * 1103515245 + 12345) as i64;
        rand_nums.push((tmp % 2147483648) as i32);  // Eq. to (i32::MAX + 1) as i64
    }

    return rand_nums
}

pub fn main(){
    let stdin = io::stdin();

    for (i, line) in stdin.lines().enumerate(){
        let line_val = line.unwrap();

        // First line is single digit
        if i == 0 {
            let n_cases = line_val.trim().parse::<i32>().unwrap();
            println!("n_cases: {}", n_cases);
            continue
        }

        // Other lines contain two ints
        let int_vals: Vec<i32> = line_val
            .split_whitespace()
            .map(|s| s.parse::<i32>())
            .filter_map(Result::ok)
            .collect();
        println!("{:?}", int_vals);
        if int_vals[1] < 10 {
            println!("{:?}", ansic_rand(int_vals[0], int_vals[1] as usize))
        }
    }
}