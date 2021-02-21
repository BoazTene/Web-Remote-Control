/* tslint:disable */
/* eslint-disable */
/**
* @returns {any}
*/
export function keys(): any;
/**
* @param {MessageEvent} e
*/
export function test1(e: MessageEvent): void;
/**
* @param {number} x
* @param {number} y
* @returns {any}
*/
export function send_mouse_pos(x: number, y: number): any;
/**
* @param {string} key
* @returns {any}
*/
export function send_key(key: string): any;
/**
* @returns {any}
*/
export function get_image(): any;
/**
* @param {number} value
*/
export function store_value_in_wasm_memory_buffer_index_zero(value: number): void;
/**
* @returns {number}
*/
export function read_wasm_memory_buffer_and_return_index_one(): number;
/**
* @returns {number}
*/
export function get_wasm_memory_buffer_pointer(): number;
/**
* @param {string} username
* @param {string} password
* @returns {any}
*/
export function host(username: string, password: string): any;
/**
* @param {string} username
* @param {string} password
* @returns {any}
*/
export function login(username: string, password: string): any;
/**
* @returns {any}
*/
export function close(): any;
/**
* @param {any} v
*/
export function test(v: any): void;
/**
* Something to test with. It doesn't really matter what it is.
*/
export class Keyboard {
  free(): void;
/**
*/
  constructor();
/**
* @param {string} key
* @returns {any}
*/
  static press_key(key: string): any;
/**
* @param {string} key
* @returns {any}
*/
  static hold_Key(key: string): any;
/**
* @param {string} key
* @returns {any}
*/
  static key_combination(key: string): any;
}
/**
*/
export class web_socket {
  free(): void;
/**
* @param {string} uri
*/
  constructor(uri: string);
/**
* @returns {number}
*/
  state(): number;
/**
* @param {string} uri
* @returns {WebSocket}
*/
  static connect(uri: string): WebSocket;
/**
* @param {string} data
*/
  send(data: string): void;
/**
*/
  on_message(): void;
}

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly keys: () => number;
  readonly test1: (a: number) => void;
  readonly send_mouse_pos: (a: number, b: number) => number;
  readonly send_key: (a: number, b: number) => number;
  readonly get_image: () => number;
  readonly store_value_in_wasm_memory_buffer_index_zero: (a: number) => void;
  readonly read_wasm_memory_buffer_and_return_index_one: () => number;
  readonly get_wasm_memory_buffer_pointer: () => number;
  readonly host: (a: number, b: number, c: number, d: number) => number;
  readonly login: (a: number, b: number, c: number, d: number) => number;
  readonly close: () => number;
  readonly __wbg_keyboard_free: (a: number) => void;
  readonly keyboard_new: () => number;
  readonly keyboard_press_key: (a: number, b: number) => number;
  readonly keyboard_hold_Key: (a: number, b: number) => number;
  readonly keyboard_key_combination: (a: number, b: number) => number;
  readonly __wbg_web_socket_free: (a: number) => void;
  readonly test: (a: number) => void;
  readonly web_socket_new: (a: number, b: number) => number;
  readonly web_socket_state: (a: number) => number;
  readonly web_socket_connect: (a: number, b: number) => number;
  readonly web_socket_send: (a: number, b: number, c: number) => void;
  readonly web_socket_on_message: (a: number) => void;
  readonly __wbindgen_malloc: (a: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number) => number;
  readonly __wbindgen_export_2: WebAssembly.Table;
  readonly _dyn_core__ops__function__FnMut__A____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__ha83dd714f60d3dca: (a: number, b: number, c: number) => void;
  readonly _dyn_core__ops__function__FnMut__A____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__hb702dce18469130a: (a: number, b: number, c: number) => void;
  readonly __wbindgen_exn_store: (a: number) => void;
  readonly wasm_bindgen__convert__closures__invoke2_mut__h1705e5d3354e6877: (a: number, b: number, c: number, d: number) => void;
}

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {InitInput | Promise<InitInput>} module_or_path
*
* @returns {Promise<InitOutput>}
*/
export default function init (module_or_path?: InitInput | Promise<InitInput>): Promise<InitOutput>;
        