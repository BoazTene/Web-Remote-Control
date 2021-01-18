extern crate png;

use scrap;
use std::time::{Duration, Instant}; 
use scrap::{Capturer, Display};
use std::io::ErrorKind::WouldBlock;
use std::thread;
// use std::time::Duration;
// use png;
// use png::HasParameters;
use std::net::TcpStream;
use std::io::BufWriter;

fn main() {
    let start = Instant::now();
    let one_second = Duration::new(1, 0);
    let one_frame = one_second / 60;

    let display = Display::primary().expect("Couldn't find primary display.");
    let mut capturer = Capturer::new(display).expect("Couldn't begin capture.");
    let (w, h) = (capturer.width(), capturer.height());

    loop {
        // Wait until there's a frame.

        let buffer = match capturer.frame() {
            Ok(buffer) => buffer,
            Err(error) => {
                if error.kind() == WouldBlock {
                    // Keep spinning.
                    thread::sleep(one_frame);
                    continue;
                } else {
                    panic!("Error: {}", error);
                }
            }
        };

        println!("Captured! Saving...");

        // Flip the ARGB image into a BGRA image.

        let mut bitflipped = Vec::with_capacity(w * h * 4);
        let stride = buffer.len() / h;

        for y in 0..h {
            for x in 0..w {
                let i = stride * y + 4 * x;
                bitflipped.extend_from_slice(&[
                    buffer[i + 2],
                    buffer[i + 1],
                    buffer[i],
                    255,
                ]);
            }
        }
        print!("{}, {}", h, w);

        // Save the image.
        let duration = start.elapsed();
        println!("Time elapsed in expensive_function() is: {:?}", duration);

        let ref mut stream = BufWriter::new(TcpStream::connect("127.0.0.1:12345").unwrap());
        let mut encoder = png::Encoder::new(stream, w as u32, h as u32); // Width is 2 pixels and height is 1.
        encoder.set_color(png::ColorType::RGBA);
        encoder.set_depth(png::BitDepth::Eight);
        let mut writer = encoder.write_header().unwrap();
        writer.write_image_data(&buffer).unwrap();

        break;
    }
    
}