// importScripts("../RemoteControl/index.js");
// importScripts('../RemoteControl/index.js');
// let module;
// onmessage = function(e) {
    
//     // send_key(e.data)
//     // console.log('Posting message back to main script');
//     // postMessage(workerResult);
//   }


onmessage = function (event) {
  data = event;
  console.log(data.data)
  postMessage(data.data);
}