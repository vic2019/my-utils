const fs = require('fs');
const path = require('path');
const stream = require('stream');

class prettifyJSON extends stream.Transform {
  constructor() {
    super();
    this.level = 0;
    this.quoted = false;
    this.escaped = false;
    this.withNewLine = function(open, close = '') {
      return `${open}\n${'\t'.repeat(this.level)}${close}`;
    }
  }

  _transform(binChunk, _encoding, callback) {
    const chunk = binChunk.toString(); // Default is binary buffer
    const length = chunk.length;
    let output = '';

    let i = -1;
    while (++i < length) {
      const char = chunk[i];

      if (this.escaped) {
        this.escaped = false;
        output += char;
        continue;
      }

      switch(char) {
        case '[':
        case '{':
          if (/[\]}]/.test(chunk[1 + i])) {
            output += char + chunk[1 + i++];
            break;
          }
          this.level += this.quoted ? 0 : 1;
          output += this.quoted ? char : this.withNewLine(char);
          break;
        case ']':
        case '}':
          this.level -= this.quoted ? 0 : 1;
          output += this.quoted ? char : this.withNewLine('', char);
          break;
        case ',':
          output += this.quoted ? char : this.withNewLine(char);
          break;
        case '"':
          this.quoted = !this.quoted;
          output += char;
          break;
        case '\\':
          this.escaped = true;
          output += char;
          break;
        case ':':
          output += this.quoted ? char : char + ' ';
          break;
        case '\n':
          output += this.quoted ? char : '';
          break;
        default:
          output += char;
          break;
      }
    }
    this.push(output);
    callback();
  }

  _flush(callback) {
    callback();
  }
}


const filepath = path.resolve(__dirname, process.argv[2]);
const outputFilepath = filepath.slice(-filepath.length, -5).concat('_pretty.json');
console.log(filepath, '=>', outputFilepath);

const readStream = fs.createReadStream(filepath);
const writeStream = fs.createWriteStream(outputFilepath);
const transformStream = new prettifyJSON;

readStream.pipe(transformStream).pipe(writeStream).on('finish', () => console.log('Done'));