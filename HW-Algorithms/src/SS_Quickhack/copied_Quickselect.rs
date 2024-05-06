use std::cmp::Ordering;
use std::io::{self, BufRead};
use rand::Rng;

fn partition(arr: &mut [i32], l: usize, r: usize) -> usize {
    let pivot = arr[r];
    let mut i = l;
    for j in l..r {
        if arr[j] < pivot {
            arr.swap(i, j);
            i += 1;
        }
    }
    arr.swap(i, r);

    i
}

fn random_partition(arr: &mut [i32], l: usize, r: usize) -> usize {
    let n = r - l + 1;
    let pivot = rand::thread_rng().gen_range(0..n);
    arr.swap(l + pivot, r);

    partition(arr, l, r)
}

fn median_util(arr: &mut [i32], l: usize, r: usize, k: usize, a: &mut i32, b: &mut i32) {
    if l <= r {
        let partition_index = random_partition(arr, l, r);
        if partition_index == k {
            *b = arr[partition_index];
            if *a != -1 {
                return;
            }
        } /*else if partition_index == k - 1 {
            *a = arr[partition_index];
            if *b != -1 {
                return;
            }
        } */
        if partition_index >= k {
            median_util(arr, l, partition_index - 1, k, a, b);
        } else {
            median_util(arr, partition_index + 1, r, k, a, b);
        }
    }
}

fn find_median(arr: &mut [i32], n: usize) -> i32 {
    let mut a = -1;
    let mut b = -1;


    median_util(arr, 0, n - 1, n / 2, &mut a, &mut b);
    b
 /* else {
        median_util(arr, 0, n - 1, n / 2, &mut a, &mut b);
        (a + b) / 2
    } */
}

fn ansic_random(a_0: i32, n_iter: usize) -> Vec<i32> {
    let mut random_vals = Vec::with_capacity(n_iter);
    let mut a = a_0;
    for _ in 0..n_iter {
        a = (a * 1103515245 + 12345) % 2147483648; // ANSI C random number
        random_vals.push(a); // Extract the random number and push it into the vector
    }

    random_vals
}

fn main() {

    /*
    let mut arr = [12, 3, 5, 7, 4, 19, 26];
    let n = arr.len();
    let median = find_median(&mut arr, n);
    println!("Median = {}", median);
    */

    // Create a stdin reader
    let stdin = io::stdin();
    // Lock the stdin reader and obtain a handle
    let handle = stdin.lock();
    // Create a buffered reader to efficiently read input line by line
    let mut reader = io::BufReader::new(handle);

    // Iterate over lines from stdin
    let mut s = String::new();
    reader
        .read_line(&mut s)
        .expect("Failed to read the first line");
    let mut n_cases: usize = s.trim().parse().expect("Invalid input");

    for (line_number, line) in reader.lines().enumerate() {
        match line {
            Ok(line) => {
                // Parse the first element as i32
                let params: Vec<&str> = line.split_whitespace().collect();

                let param0: i32 = match params[0].parse() {
                    Ok(num) => num,
                    Err(_) => {
                        eprintln!("Error: Failed to parse the first parameter as i32");
                        return;
                    }
                };

                // Parse the second element as usize
                let param1: usize = match params[1].parse() {
                    Ok(num) => num,
                    Err(_) => {
                        eprintln!("Error: Failed to parse the second parameter as usize");
                        return;
                    }
                };
                let rand_nums = ansic_random(param0, param1);
                for val in rand_nums {
                    println!("{}", val)
                }
            }
            Err(err) => {
                eprintln!("Error reading line: {}", err);
                continue;
            }
        }
    }
}