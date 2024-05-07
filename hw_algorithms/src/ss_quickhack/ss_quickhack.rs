use std::io;

pub fn ansic_rand(a_0: i32, n_iter: usize, simple: bool) -> Vec<i32> {
    let mut rand_nums: Vec<i32> = Vec::with_capacity(n_iter);
    let mut tmp: i64;
    tmp = a_0 as i64 * 1103515245 + 12345;
    rand_nums.push((tmp % 2147483648) as i32);

    for i in 1..n_iter{
        tmp = *rand_nums.get(i-1).unwrap() as i64 * 1103515245 + 12345;
        rand_nums.push((tmp % 2147483648) as i32);  // Eq. to (i32::MAX + 1) as i64
    }

    if simple {
        rand_nums = rand_nums.iter().map(|x| x % 10).collect();
    }

    return rand_nums
}

pub fn partition(arr: &mut [i32]) -> usize {
    // Pick a random pivot for better average runtime and put it in the last place
    let pivot_ix = ansic_rand(arr[0], 1, false)[0] as usize % arr.len();
    arr.swap(pivot_ix, arr.len() - 1);
    let pivot_ix = arr.len() - 1;

    let pivot = arr[pivot_ix];
    // println!("piv:{} at {}", pivot, pivot_ix);
    let mut i = 0;

    for j in 0..arr.len()-1 {
        if arr[j] <= pivot {
            // println!("{} <= {}: swap", arr[j], pivot);
            arr.swap(i, j); // put smaller elements in front of the list
            i += 1;
        }
        // println!("{}: {:?}", j, arr);
    }
    arr.swap(i, pivot_ix);

    return i;
}

pub fn quickselect(list: &mut [i32], k: usize) -> i32 {
    //println!("qs({:?}), k={}", list, k);
    let pivot_ix = partition(list);
    //println!("Partition: {:?}, Pivot: {} at {}", list, list[pivot_ix], pivot_ix);

    let hi0 = pivot_ix + 1;
    let median: i32;

    if pivot_ix > k {
        median = quickselect(&mut list[0..pivot_ix], k);
    } else if pivot_ix == k {
        // println!("median = {}", list[k]);
        median = list[k];
    } else {
        median = quickselect(&mut list[hi0..], k - pivot_ix - 1);
    }
    return median;
}

pub fn main(){
    let stdin = io::stdin();

    for (i, line) in stdin.lines().enumerate() {
        let line_val = line.unwrap();

        // First line is single digit
        if i == 0 {
            let _n_cases = line_val.trim().parse::<i32>().unwrap();
            continue
        }

        // Other lines contain two ints
        let int_vals: Vec<i32> = line_val
            .split_whitespace()
            .map(|s| s.parse::<i32>())
            .filter_map(Result::ok)
            .collect();

        let mut number_list: Vec<i32> = ansic_rand(int_vals[0], int_vals[1] as usize, false);
        let result = quickselect(&mut number_list[..], int_vals[1] as usize / 2);
        println!("{}", result);
    }
}