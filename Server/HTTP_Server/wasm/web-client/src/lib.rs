use wasm_bindgen::prelude::*;
use dict::{ Dict, DictIface };
use web_sys::{Event, CustomEvent, CustomEventInit, EventListener};
use std::thread;
use wasm_bindgen::JsCast;
mod md5_encryption;
use std::time::Duration;
mod WebSocket;
mod http;
use web_sys::MessageEvent;



const WASM_MEMORY_BUFFER_SIZE: usize = 2;
static mut WASM_MEMORY_BUFFER: [u8; WASM_MEMORY_BUFFER_SIZE] = [0; WASM_MEMORY_BUFFER_SIZE];
static mut KEYS: std::vec::Vec<dict::DictEntry<std::string::String>> = Dict::<String>::new();

macro_rules! console_log {
  ($($t:tt)*) => (log(&format_args!($($t)*).to_string()))
}

#[wasm_bindgen]
extern {
  #[wasm_bindgen(js_namespace = console)]
  fn log(s: &str);

  pub fn alert(s: &str);
}

#[wasm_bindgen]
pub async fn keys(){
  unsafe{
  KEYS.add(" ".to_string(), "spacebar".to_string() );
  // KEYS.add("ArrowDown".to_string(), "down".to_string() );
  // KEYS.add("ArrowLeft".to_string(), "left".to_string() );
  // KEYS.add("ArrowRight".to_string(), "right".to_string() );
  // KEYS.add("ArrowUp".to_string(), "up".to_string() );
  // KEYS.add("AudioVolumeDown".to_string(), "volumedown".to_string() );
  // KEYS.add("AudioVolumeUp".to_string(), "volumeup".to_string() );
  // KEYS.add("AudioVolumeMute".to_string(), "volumemute".to_string() );
  }
}

#[wasm_bindgen]
pub fn test1(e: MessageEvent) {
  alert("1");
}

#[wasm_bindgen]
pub async fn send_mouse_pos(x: i32, y: i32) {
  // This function sends to the http_api server the mouse location.

  let http = http::Http {};
  let _response: String = http::Http::to_string(http.get(&format!("http://localhost:1234/mouse?x={}&y={}", x, y)).await).await;
}

#[wasm_bindgen]
pub async fn send_key(mut key: String) {
  // This function sends the parameter key to the http_api server.
  // let mut key = _key.clone();
  // alert(&key);
  store_value_in_wasm_memory_buffer_index_zero(1);
  unsafe {
    for i in &KEYS {
      if i.key.eq(&key) {
          key = i.val.to_string();
        }
      }
  }
  
  let http = http::Http {};
  http.post(&format!("http://localhost:1234/key?key={}", key)).await;

  store_value_in_wasm_memory_buffer_index_zero(0);
  

}

#[wasm_bindgen]
pub async fn get_image() -> Result<bool, JsValue> {
    // This function gets from the http_api server the last image the host sent.

    let http = http::Http {};
    let image: String = http::Http::to_string(http.get("http://localhost:1234/image").await).await;
    
    let window = web_sys::window().unwrap();

    let mut detail = CustomEventInit::new();
    detail.detail(&JsValue::from_str(&image));  

    let event = CustomEvent::new_with_event_init_dict("newimage", &detail).unwrap();

    
    window.dispatch_event(&event)
}

#[wasm_bindgen]
pub fn store_value_in_wasm_memory_buffer_index_zero(value: u8) {
    // This function stored a value in the buffer.

    unsafe {
    WASM_MEMORY_BUFFER[0] = value;
    
  }
}

#[wasm_bindgen]
pub fn read_wasm_memory_buffer_and_return_index_one() -> u8 {
  // This function reads the buffer and return the value at index 1

  let value: u8;
  
  unsafe {
    value = WASM_MEMORY_BUFFER[1];
  }
  return value;
}

#[wasm_bindgen]
pub fn get_wasm_memory_buffer_pointer() -> *const u8 {
  // This function return the pointer to the buffer.
  
  let pointer: *const u8;
  unsafe {
    pointer = WASM_MEMORY_BUFFER.as_ptr();
  }
  
  return pointer;
}

#[wasm_bindgen]
pub async fn host(username: String, password: String) {
    // This function register the host with the username and password parameters.

    store_value_in_wasm_memory_buffer_index_zero(3);
    let encrypt_username = format!("{:x}", md5_encryption::encrypt(&username)).to_owned();
    let encrypt_password = format!("{:x}", md5_encryption::encrypt(&password)).to_owned();

    let http = http::Http {};

    let response: String = http::Http::to_string(http.get(&format!("http://localhost:2234/register?username={}&password={}", encrypt_username, encrypt_password)).await).await;
    
    if response.eq("True") {
      store_value_in_wasm_memory_buffer_index_zero(1);
  } else {
      store_value_in_wasm_memory_buffer_index_zero(0);
  }

  let event = Event::new("onrequestend").unwrap();
  let window = web_sys::window().unwrap();

  window.dispatch_event(&event);
}

#[wasm_bindgen]
pub async fn login(username: String, password: String) -> Result<bool, JsValue>  {
    // This function login to a host with the username and password parameters.

    store_value_in_wasm_memory_buffer_index_zero(3);
    let encrypt_username = format!("{:x}", md5_encryption::encrypt(&username)).to_owned();
    let encrypt_password = format!("{:x}", md5_encryption::encrypt(&password)).to_owned();
    let http = http::Http {};
    
    let response: String = http::Http::to_string(http.get(&format!("http://localhost:1234/login?username={}&password={}", encrypt_username, encrypt_password)).await).await;

    if response.eq("True") {
        store_value_in_wasm_memory_buffer_index_zero(1);
        let window = web_sys::window().unwrap();
        
        let location = window.location();
        let _result = location.replace(&format!("http://localhost:5000/RemoteControl?username={}&password={}", encrypt_username, encrypt_password));
        return Ok(true);
    } else if response.eq("False") {
        store_value_in_wasm_memory_buffer_index_zero(0);
    }

    let event = Event::new("onrequestend").unwrap();
    let window = web_sys::window().unwrap();

    window.dispatch_event(&event)
}


#[wasm_bindgen]
pub async fn close() {
  let http = http::Http {};

  http.get("http://localhost:1234/close").await;

}


/// Something to test with. It doesn't really matter what it is.
//


#[wasm_bindgen]
struct Keyboard {
}

#[wasm_bindgen]
impl Keyboard {

  #[wasm_bindgen(constructor)]
    pub fn new() -> Keyboard {
      Keyboard {}
    }

  pub async fn press_key(key: String) { 
    let http = http::Http {};
    http.post(&format!("http://localhost:1234/key?key={}&&hold=false&&combination=false", key)).await;

  }

  pub async fn hold_Key(key: String){
    let http = http::Http {};
    http.post(&format!("http://localhost:1234/key?key={}&&hold=true&&combination=false", key)).await;
  }

  pub async fn key_combination(key: String) {
    let http = http::Http {};
    http.post(&format!("http://localhost:1234/key?key={}&&hold=false&&combination=true", key)).await;
  }

}