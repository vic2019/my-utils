const fs = require('fs');
const one = fs.readFileSync(process.argv[2], 'utf-8');
const two = fs.readFileSync(process.argv[3], 'utf-8');

console.log('one:', one.length, '-', 'two:', two.length);

const oneO = JSON.parse(one);
const twoO = JSON.parse(two);
console.log('deep equal:', JSON.stringify(oneO) === JSON.stringify(twoO));

const length = two.length;
let i = -1;
while(++i < length) {
  if (one[i] != two[i]) {
    console.log('position:', i, 'of', length);
    console.log('\n-------- one --------');
    console.log(one.substr(i - 200, 400));
    console.log('\n------- two --------');
    console.log(two.substr(i - 200, 400));
    console.log();
    break;
  }
}