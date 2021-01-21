



// #[wasm_bindgen]
// pub struct Buffer{
//     buffer_size: u8,
//     buffer: [u8; buffer_size:usize],
// }

// pub fn new_buffer(buffer_size) -> {

// }

// impl Buffer{
//     pub fn new(&mut self){
//         self.buffer = [0; self.buffer_size];
//     }

//     pub fn store_value_in_wasm_memory_buffer_index_zero(&mut self, value: u8) {
//         unsafe {
//             self.buffer[0] = value;
//         }
//     }

//     pub fn read_wasm_memory_buffer_and_return_index_one(&self) -> u8 {
//         let value: u8;
//         unsafe {
//             value = self.buffer[1];
//         }
//         return value;
//     }

//     pub fn get_wasm_memory_buffer_pointer(&self) -> *const u8 {
//         let pointer: *const u8;
//         unsafe {
//             pointer = self.buffer.as_ptr();
//         }

//         return pointer;
//     }

// }