const EventEmitter = require('events');
const emitter = new EventEmitter();
const callback1 = (args) => {
  console.log('first callback - ', args);
};

emitter.on('seongryong', callback1);
emitter.on('seongryong', (args) => {
  console.log('second callback - ', args);
});

emitter.emit('seongryong', { message: 1 });
emitter.emit('seongryong', { message: 2 });
// emitter.removeListener('seongryong', callback1);
emitter.removeAllListeners();
emitter.emit('seongryong', { message: 3 });
