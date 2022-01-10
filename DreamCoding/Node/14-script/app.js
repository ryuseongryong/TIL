// video - mp4, mov
// captured - png, aae
// duplicated - E가 포함된 파일의 원본 파일(E가 포함된 수정파일은 기존 폴더에 유지)

const fs = require('fs');
const path = require('path');

// node script로 argv를 전달받아서 사용하기

// process.argv.forEach(function (val, index, array) {
//   console.log(index + ': ' + val);
// });

const subFolder = process.argv.slice(2)[0];
const pictureFolder =
  '/Users/seongryongryu/Desktop/TIL/DreamCoding/Node/14-script/';

// 1. 폴더 생성
fs.promises.mkdir(pictureFolder + subFolder + '/video').catch(console.error);
fs.promises.mkdir(pictureFolder + subFolder + '/captured').catch(console.error);
fs.promises
  .mkdir(pictureFolder + subFolder + '/duplicated')
  .catch(console.error);

// 2. 특정 확장자 별로 파일 분류
// 2-1 폴더 안의 파일을 하나씩 확인하여 확장자 확인
// 2-2 확장자 별로 파일을 분류하여 지정된 폴더로 이동시키기

fs.promises
  .readdir(pictureFolder + subFolder) //
  .then((fileList) => {
    console.log('processing in ' + pictureFolder + subFolder + '...');
    console.log(fileList);
    fileList.forEach((file) => {
      const extension = path.extname(file);
      const originPath = pictureFolder + subFolder + '/';
      if (extension === '.mp4' || extension === '.mov') {
        fs.rename(originPath + file, originPath + 'video/' + file, (err) => {
          console.log(err);
          console.trace();
        });
        console.log('moved ' + file + ' to video folder');
        console.trace();
      } else if (extension === '.png' || extension === '.aae') {
        fs.rename(originPath + file, originPath + 'captured/' + file, (err) => {
          console.log(err);
          console.trace();
        });
        console.log('moved ' + file + ' to captured folder');
        console.trace();
      }
      // 확장자가 jpg이고 파일명에 E가 포함되어 있으면 원래 파일을 duplicated로 옮기기
      else if (extension === '.jpg' && path.basename(file).includes('E')) {
        const originFile = path.basename(file).split('E').join('');
        fs.rename(
          originPath + originFile,
          originPath + 'duplicated/' + originFile,
          (err) => {
            console.log(err);
            console.trace();
          }
        );
        console.log('moved ' + originFile + ' to duplicated folder');
        console.trace();
      }
    });
  })
  .catch(console.error);
console.trace();
