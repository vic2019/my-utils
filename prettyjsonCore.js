const fs = require('fs');
const path = require('path');

const filepath = path.resolve(__dirname, process.argv[2]);
const outputFilepath = filepath.slice(-filepath.length, -5).concat('.out.json');
console.log(filepath, '=>', outputFilepath);

const dataString = fs.readFileSync(filepath, 'utf-8');
const parsed = JSON.parse(dataString);
fs.writeFileSync(outputFilepath, JSON.stringify(parsed, null, '\t'));
console.log('Done');