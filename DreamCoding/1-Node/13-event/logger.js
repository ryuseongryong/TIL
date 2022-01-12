const EventEmitter = require('events');

// eventEmitter is all about origin object
class Logger extends EventEmitter {
  log(callback) {
    this.emit('log', 'started...');
    callback();
    this.emit('log', 'ended!');
  }
}

module.exports.Logger = Logger;
