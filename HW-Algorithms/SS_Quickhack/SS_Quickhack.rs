use std::io;

fn ansic_rand(a_0: i32, n_iter: usize) -> Vec<i32> {
    let mut rand_nums: Vec<i32> = Vec::with_capacity(n_iter);
    let mut tmp: i64;
    tmp = a_0 as i64 * 1103515245 + 12345;
    rand_nums.push((tmp % 2147483648) as i32);

    for i in 1..n_iter{
        tmp = *rand_nums.get(i-1).unwrap() as i64 * 1103515245 + 12345;
        rand_nums.push((tmp % 2147483648) as i32);  // Eq. to (i32::MAX + 1) as i64
    }

    return rand_nums
}

fn quickselect(list: &Vec<i32>, k: usize, l: usize, r: usize) -> i32 {
    let low0 = l;
    let low1 = k - l;
    let hi0 = k + 1;
    let hi1 = r;

    let len_low = low1 - low0;
    let median: i32;

    if len_low > k {
        quickselect(&list[low0..low1], k);
    } else if len_low + 1 > k {
        println!("median = {}", k);
    } else {
        quickselect(&list[hi0..hi1], k - len_low - 1);
    }
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

        let number_list: Vec<i32> = ansic_rand(int_vals[0], int_vals[1] as usize);
        if int_vals[1] < 10 {
            println!("{:?}", number_list);
        }
        let result = quickselect(&number_list, number_list.len() / 2, 0, number_list.len());
        println!("{:?}", result);
    }
}