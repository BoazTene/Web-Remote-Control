use wasm_bindgen::prelude::*;
use wasm_bindgen::JsCast;
use wasm_bindgen_futures::JsFuture;
use dict::{ Dict, DictIface };
use web_sys::{HtmlImageElement, Event, CustomEvent, CustomEventInit, Request, RequestInit, RequestMode, Response};
use serde::{Deserialize, Serialize};
use std::fmt::Debug;
mod md5_encryption;
mod http;

const WASM_MEMORY_BUFFER_SIZE: usize = 2;
static mut WASM_MEMORY_BUFFER: [u8; WASM_MEMORY_BUFFER_SIZE] = [0; WASM_MEMORY_BUFFER_SIZE];
static mut KEYS: std::vec::Vec<dict::DictEntry<std::string::String>> = Dict::<String>::new();

#[wasm_bindgen]
extern {
    pub fn alert(s: &str);
}

#[wasm_bindgen]
pub async fn keys(){
  unsafe{
  KEYS.add(" ".to_string(), "space".to_string() );
  KEYS.add("ArrowDown".to_string(), "down".to_string() );
  KEYS.add("ArrowLeft".to_string(), "left".to_string() );
  KEYS.add("ArrowRight".to_string(), "right".to_string() );
  KEYS.add("ArrowUp".to_string(), "up".to_string() );
  KEYS.add("AudioVolumeDown".to_string(), "volumedown".to_string() );
  KEYS.add("AudioVolumeUp".to_string(), "volumeup".to_string() );
  KEYS.add("AudioVolumeMute".to_string(), "volumemute".to_string() );
  }
}

#[wasm_bindgen]
pub async fn send_mouse_pos(x: i32, y: i32) {
  let http = http::Http {};
  let response: String = http::Http::to_string(http.get(&format!("http://localhost:1234/mouse?x={}&y={}", x, y)).await).await;
}

#[wasm_bindgen]
pub async fn send_key(mut key: String) {
  unsafe{
  for i in &KEYS {
    if i.key.eq(&key) {
      key = i.val.to_string();
    }
  }
}

  // key = KEYS.get(&key).to_owned();

  let http = http::Http {};
  let response: String = http::Http::to_string(http.get(&format!("http://localhost:1234/key?key={}", key)).await).await;

}

#[wasm_bindgen]
pub async fn get_image() {
    let http = http::Http {};
    let image: String = http::Http::to_string(http.get("http://localhost:1234/image").await).await;
    // alert(&format!("{}", image));
    
    let window = web_sys::window().unwrap();

    let mut detail = CustomEventInit::new();
    detail.detail(&JsValue::from_str(&image));  

    let event = CustomEvent::new_with_event_init_dict("newimage", &detail).unwrap();

    
    window.dispatch_event(&event);
}

#[wasm_bindgen]
pub fn store_value_in_wasm_memory_buffer_index_zero(value: u8) {
    unsafe {
    WASM_MEMORY_BUFFER[0] = value;
    
  }
}

// // #[wasm_bindgen]
// // pub fn store_string_in_wasm_memory_buffer(value: String) {
// //     unsafe {
        
// //     WASM_MEMORY_BUFFER[0] = value;
    
// //   }
// // }
#[wasm_bindgen]
pub fn lahoh(value: &str) {
  alert(&value);
}

#[wasm_bindgen]
pub fn create_buffer(buffer_size: u8) -> *const u8{
    const buffer_size: usize = 2;
    static mut buffer: [u8; buffer_size] = [0; buffer_size];
    let pointer: *const u8;
    unsafe {
      pointer = buffer.as_ptr();
    }

    return pointer;
}

#[wasm_bindgen]
pub fn read_wasm_memory_buffer_and_return_index_one() -> u8 {
  let value: u8;
  unsafe {
    value = WASM_MEMORY_BUFFER[1];
  }
  return value;
}

#[wasm_bindgen]
pub fn get_wasm_memory_buffer_pointer() -> *const u8 {
  let pointer: *const u8;
  unsafe {
    pointer = WASM_MEMORY_BUFFER.as_ptr();
  }

  return pointer;
}

#[wasm_bindgen]
pub async fn host(mut username: String, mut password: String) {
    store_value_in_wasm_memory_buffer_index_zero(3);
    let encrypt_username = format!("{:x}", md5_encryption::encrypt(&username)).to_owned();
    let encrypt_password = format!("{:x}", md5_encryption::encrypt(&password)).to_owned();
    // let encrypt_username = username;
    // let encrypt_password = password;
    let http = http::Http {};
    alert(&encrypt_username);
    alert(&encrypt_password);

    // alert(&format!("{}, {}, {}, {}", encrypt_username, username, encrypt_password, password));
    let response: String = http::Http::to_string(http.get(&format!("http://localhost:2234/register?username={}&password={}", encrypt_username, encrypt_password)).await).await;

}

#[wasm_bindgen]
pub async fn test(mut username: String, mut password: String) {
    store_value_in_wasm_memory_buffer_index_zero(3);
    let encrypt_username = format!("{:x}", md5_encryption::encrypt(&username)).to_owned();
    let encrypt_password = format!("{:x}", md5_encryption::encrypt(&password)).to_owned();
    let http = http::Http {};
    
    alert(&encrypt_username);
    alert(&encrypt_password);
    // alert(&format!("{}, {}, {}, {}", encrypt_username, username, encrypt_password, password));
    let response: String = http::Http::to_string(http.get(&format!("http://localhost:1234/login?username={}&password={}", encrypt_username, encrypt_password)).await).await;

    if response.eq("True") {
        store_value_in_wasm_memory_buffer_index_zero(1);
        let window = web_sys::window().unwrap();
        
        let location = window.location();
        location.replace(&format!("http://192.168.1.28:5000?username={}&password={}", encrypt_username, encrypt_password));
    } else {
        store_value_in_wasm_memory_buffer_index_zero(0);
    }

    let event = Event::new("onrequestend").unwrap();
    let window = web_sys::window().unwrap();
    window.dispatch_event(&event);
}
