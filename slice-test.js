/**
 * String.slice(-1) is an O(1) operation!
 * The difference in run time comes from memory usage.
 */

const REPETITION = 160000000;
const a = 'acegik';
const b = 'bdfhj'.repeat(REPETITION);
const c = 'moqsuw'.repeat(REPETITION);
const d = 'lnprtv'.repeat(REPETITION);

const start1 = new Date().getTime();
console.log('Op 1:', a.slice(-1));
const end1 = new Date().getTime();

const start2 = new Date().getTime();
console.log('Op 2:', b.slice(-1));
const end2 = new Date().getTime();

const start3 = new Date().getTime();
console.log('Op 3:', c[0]);
const end3 = new Date().getTime();

const start4 = new Date().getTime();
console.log('Op 4:', c[c.length - 1]);
const end4 = new Date().getTime();

const start5 = new Date().getTime();
console.log('Op 5:', d[d.length - 1]);
const end5 = new Date().getTime();

console.log('');
console.log(`Op 1 took ${end1 - start1} milliseconds`);
console.log(`Op 2 took ${end2 - start2} milliseconds`);
console.log(`Op 3 took ${end3 - start3} milliseconds`);
console.log(`Op 4 took ${end4 - start4} milliseconds`);
console.log(`Op 5 took ${end5 - start5} milliseconds`);