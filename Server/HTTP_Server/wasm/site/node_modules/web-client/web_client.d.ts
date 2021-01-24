/* tslint:disable */
/* eslint-disable */
/**
* @returns {any}
*/
export function keys(): any;
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
* @param {string} value
*/
export function lahoh(value: string): void;
/**
* @param {number} buffer_size
* @returns {number}
*/
export function create_buffer(buffer_size: number): number;
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
export function test(username: string, password: string): any;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly keys: () => number;
  readonly send_mouse_pos: (a: number, b: number) => number;
  readonly send_key: (a: number, b: number) => number;
  readonly get_image: () => number;
  readonly store_value_in_wasm_memory_buffer_index_zero: (a: number) => void;
  readonly lahoh: (a: number, b: number) => void;
  readonly create_buffer: (a: number) => number;
  readonly read_wasm_memory_buffer_and_return_index_one: () => number;
  readonly get_wasm_memory_buffer_pointer: () => number;
  readonly host: (a: number, b: number, c: number, d: number) => number;
  readonly test: (a: number, b: number, c: number, d: number) => number;
  readonly __wbindgen_malloc: (a: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number) => number;
  readonly __wbindgen_export_2: WebAssembly.Table;
  readonly _dyn_core__ops__function__FnMut__A____Output___R_as_wasm_bindgen__closure__WasmClosure___describe__invoke__h9727cc79361dc805: (a: number, b: number, c: number) => void;
  readonly __wbindgen_exn_store: (a: number) => void;
  readonly wasm_bindgen__convert__closures__invoke2_mut__ha2423ea20de566bf: (a: number, b: number, c: number, d: number) => void;
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
        