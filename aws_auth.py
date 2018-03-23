const aws = require('aws-sdk');

const AWS_ACCESS_KEY = process.env.ACCESS_KEY;
const AWS_SECRET_KEY = process.env.SECRET_KEY;
const SRC_BUCKET = process.env.SRC_BUCKET;
const DST_BUCKET = process.env.DST_BUCKET;
const REGION = process.env.REGION;

let date = "";

aws.config.update({
  accessKeyId: AWS_ACCESS_KEY,
  secretAccessKey: AWS_SECRET_KEY,
  region: REGION,
});

exports.handler = (event, context, callback) => {
  console.log("event-----start");
  console.log(event);
  console.log("event-----end");
  date = (+new Date());
  upload(event.requestbody).then((puturl) => {
    download(event.requestbody).then((geturl) => {
      callback(null, { 'puturl': puturl, 'geturl': geturl});
    }).catch(function (error) {
      callback(null, error);
    }).catch(function (error) {
      callback(null, error);
    });
  });
};


function upload(file) {
  const bucketPath = SRC_BUCKET + "/" + date; // ミリ秒取得
  const s3 = new aws.S3({
    signatureVersion: 'v4'
  });

  const params = {
    Bucket: bucketPath,
    Key: file.filename,
    Expires: 60,
    ContentType: file.filetype
  };

  return new Promise((resolve, reject) => {
    s3.getSignedUrl('putObject', params, (err, url) => {
      if (err) {
        reject(err);
      }
      resolve(url);
    });
  });
}


function download(file) {
  const bucketPath = DST_BUCKET + "/" + date; // ミリ秒取得
  const filename = file.filename.replace(/\.zip$/, '.pdf'); // ファイル名のみ取得
  console.log(filename);
  const s3 = new aws.S3({
    signatureVersion: 'v4'
  });

  const params = {
    Bucket: bucketPath,
    Key: filename,
    Expires: 60 * 60 * 24 * 7, // 1week
  };

  return new Promise((resolve, reject) => {
    s3.getSignedUrl('getObject', params, (err, url) => {
      if (err) {
        reject(err);
      }
      resolve(url);
    });
  });
}
