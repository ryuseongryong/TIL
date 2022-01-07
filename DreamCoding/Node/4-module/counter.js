let count = 0;

function increase() {
  count++;
}

function getCount() {
  return count;
}

module.exports.getCount = getCount;
// module.exports.increase = increase;
console.log(module.exports === exports);
exports = {};
exports.increase = increase;
console.log(module.exports === exports);
// strictly different : basically exports ref module.exports but assign something to exports variable, everything change
console.log(module);
