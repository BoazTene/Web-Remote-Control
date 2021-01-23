use wasm_bindgen::JsCast;
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::JsFuture;
use web_sys::{Request, RequestInit, RequestMode, Response};
use serde::{Deserialize, Serialize};
use serde_json;

pub struct Http{} 

impl Http{
    // this function make a get request to the url
    // call the to_string method after to convert the result to string
    // for example:
    // let http = http::Http {url: "url"};
    // let res: String = http::Http::to_string(http.get().await).await;
    pub async fn get(self, url: &str) -> Result<String, js_sys::Promise> {
        let mut opts = RequestInit::new();
        
        // opts.headers(&JsValue::from_str("Name: Gila"));
        opts.method("GET");
        opts.mode(RequestMode::Cors);

        let request = Request::new_with_str_and_init(
            url,
            &opts,
        )?;

        let window = web_sys::window().unwrap();

        let resp_value = JsFuture::from(window.fetch_with_request(&request)).await?;

        let resp: Response = resp_value.dyn_into().unwrap();
        
        let text = JsFuture::from(resp.text()?).await?.as_string().unwrap();

        Ok(text)
    }

    // this function gets the result of the get function and convert it to String
    pub async fn to_string(resp: Result<String, js_sys::Promise>) -> String {
        match resp {
            Ok(t) => return t,
            Err(e) => return format!("Error: {:?}", e),
        };
    }
}