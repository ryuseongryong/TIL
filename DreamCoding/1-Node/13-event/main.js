const logger = require('./logger.js');
const emitter = new logger.Logger();

emitter.on('log', (event) => {
  console.log(event);
});

emitter.log(() => {
  console.log('...... doing something!');
});
