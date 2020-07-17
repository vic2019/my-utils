const fs = require('fs');
const path = require('path');
const stream = require('stream');

class prettifyJSON extends stream.Transform {
  constructor() {
    super();
    this.level = 0;
    this.quoted = false;
    // this.escaped = false;
  }

  _transform(chunk, _encoding, callback) {
    const strChunk = chunk.toString(); // Default is binary buffer
    function peek(index, string) {
      return string[index + 1];
    }
    
    let output = '';
    for (const i in strChunk) {
      switch(strChunk[i]) {
        case '[':
          this.level += 1;
          output += this.quoted ? '[' : `[\n${'\t'.repeat(this.level)}`;
          break;
        case '{':
          this.level += 1;
          output += this.quoted ? '{' : `{\n${'\t'.repeat(this.level)}`;
          break;
        case ']':
          this.level -= 1;
          output += this.quoted ? ']' : `\n${'\t'.repeat(this.level)}]`;
          break;
        case '}':
          this.level -= 1;
          output += this.quoted ? '}' : `\n${'\t'.repeat(this.level)}}`;
          break;
        case ',':
          output += this.quoted ? ',' : 
            /[\]}]/.test(output.slice(-1)) ? ', ' : `,\n${'\t'.repeat(this.level)}`;
          break;
        case '"':
          this.quoted = !this.quoted;
          output += /,/.test(output.slice(-2)) ? `\n${'\t'.repeat(this.level)}"` : '"';
          break;
        case '\\':
          output += this.quoted ? '\\' : '';
          break;
        case ':':
          output += ': ';
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
console.log(filepath, ' => ', outputFilepath);

const readStream = fs.createReadStream(filepath);
const writeStream = fs.createWriteStream(outputFilepath);
const transformStream = new prettifyJSON;

readStream.pipe(transformStream).pipe(writeStream).on('finish', () => console.log('Done'));