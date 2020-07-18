const fs = require('fs');
const path = require('path');

let level = 0;
let quoted = false;
let escaped = false;

function withNewLine(open, close = '') {
  return `${open}\n${'\t'.repeat(level)}${close}`;
}

function transform(binChunk) {
  const chunk = binChunk.toString(); // Default is binary buffer
  const length = chunk.length;
  let output = '';
  let char = '';

  let i = -1;
  while (i++ < length) {
    char = chunk[i];

    if (escaped) {
      escaped = false;
      output += char;
      continue;
    }

    switch(char) {
      case '[':
      case '{':
        level += 1;
        output += quoted ? char : withNewLine(char);
        break;
      case ']':
      case '}':
        level -= 1;
        output += quoted || chunk[i + 1] === ',' ? char : withNewLine('', char);
        break;
      case ',':
        output += quoted ? char : 
          /[[{]]/.test(chunk[i + 1]) ? char + ' ' : withNewLine(char);
        break;
      case '"':
        quoted = !quoted;
        output += char;
        break;
      case '\\':
        escaped = true;
        output += char;
        break;
      case ':':
        output += quoted? char : char + ' ';
        break;
      default:
        output += char;
        break;
    }
  }

  return output;
}


const filepath = path.resolve(__dirname, process.argv[2]);
const outputFilepath = filepath.slice(-filepath.length, -5).concat('_pretty.json');
console.log(filepath, '=>', outputFilepath);

const dataString = fs.readFileSync(filepath, 'utf-8');
const prettified = transform(dataString);
fs.writeFileSync(outputFilepath, prettified);
console.log('Done');