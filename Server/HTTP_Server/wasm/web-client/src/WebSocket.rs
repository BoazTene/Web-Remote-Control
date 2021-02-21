use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::JsFuture;
use wasm_bindgen::JsCast;
use web_sys::{ErrorEvent, MessageEvent, WebSocket};
use std::time::{Duration, SystemTime};
use std::thread::sleep;
use js_sys::{Date, Function};
use std::ptr;
use std::io::{Read, Write};

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
pub struct web_socket {
    ws: WebSocket,
}

#[wasm_bindgen]
pub fn test(v: JsValue) {
    console_log!("Open _ test");
}

#[wasm_bindgen]
impl web_socket {
    #[wasm_bindgen(constructor)]
    pub fn new(uri: String) -> web_socket {
        let ws = web_socket::connect(uri).unwrap();
        
        web_socket {ws: ws}
    }
    pub fn state(&self) -> u16 {
        self.ws.ready_state()
    }

    pub fn connect(uri: String) -> Result<WebSocket, JsValue> {
        Ok(WebSocket::new(&uri)?)
    }

    // pub fn wait_for_connect(&self) -> bool {
    //     let time = Date::now();

    //     while (Date::now() - time) < 3000.0  {
            
    //     }

    //     let state = self.ws.ready_state();
    //     alert(&state.to_string());
    //     return state == 1;
    // }

    pub fn send(&self, data: String) {
        match self.ws.send_with_str(&data) {
            Ok(_) => console_log!("binary message successfully sent"),
            Err(err) => console_log!("error sending message: {:?}", err),
        }
    }

    pub fn on_message(&self) {
        let onmessage_callback = Closure::wrap(Box::new(move |e: MessageEvent| {
            // Handle difference Text/Binary,...
            if let Ok(txt) = e.data().dyn_into::<js_sys::JsString>() {
                console_log!("message event, received Text: {:?}", txt);
            } else {
                console_log!("message event, received Unknown: {:?}", e.data());
            }
        }) as Box<dyn FnMut(MessageEvent)>);
        
        self.ws.set_onmessage(Some(onmessage_callback.as_ref().unchecked_ref()));
        onmessage_callback.forget();
    }
}