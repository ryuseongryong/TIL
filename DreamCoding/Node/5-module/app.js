import * as counter from './counter.js';

counter.increase();
counter.increase();
counter.increase();

console.log(counter.getCount());

import { increase, getCount } from './counter.js';

increase();
console.log(getCount());
