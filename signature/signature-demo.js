'use strict';

const crypto = require('crypto');

const ALGORITHM_MAP = {
  'HMAC-MD5': 'md5',
  'HMAC-SHA1': 'sha1',
  'HMAC-SHA256': 'sha256',
};

const APP_SECRET = 'pealse input your app secret here';

/**
 * 计算生成UUID（Universally Unique Identifier）
 */
function _uuid() {
  let d = Date.now();
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });
}

/**
 * 计算Content-MD5
 * @param {string} data 请求body，JSON格式字符串，不添加\n、\t、\和空格字符
 * @return {string} Content-MD5 
 */
function calculateMd5(data) {
  const md5 = crypto.createHash('md5');
  return md5.update(data).digest('base64');
}

/**
 * 计算签名，采用HMAC-SHA1签名算法
 * @param {string} algorithm 签名算法
 * @param {string} key 密钥
 * @param {string} data 按规则拼接的加签字符串
 * @return {string} 签名
 */
function calculateSignature(algorithm, key, data) {
  const sha1 = crypto.createHmac(algorithm, key);
  return sha1.update(data).digest('base64');
}

const body = {
	name: "张大爷",
	gender: "male",
	id_card: "510123193810081230",
	mobile: "18612345678",
	birthday: "1930-10-08"
};
const contentMd5 = calculateMd5(JSON.stringify(body));
console.log(`Conetent-MD5 = ${contentMd5}`);

const verb = 'POST';
const contentType = 'application/json;charset=utf-8';
const date = (new Date()).toUTCString();
const host = '***.***.***';
const signatureMethod = 'HMAC-SHA1';
const signatureNonce = _uuid();
const signatureVersion = '1.0';
// GET请求示例：uri = '/v1/olds?mobile=18612345678&order=asc&order_by=old_id&page=1&page_size=50'
const uri = '/v1/olds';

let stringToSign = verb + '\n'
  + (verb === 'POST' || verb === 'PUT' ? contentMd5 + '\n' + contentType + '\n' : '')
  + date + '\n'
  + host + '\n'
  + signatureMethod + '\n'
  + signatureNonce + '\n'
  + signatureVersion + '\n'
  + uri;
console.log(`stringToSign:\n${stringToSign}`);

const signature = calculateSignature(ALGORITHM_MAP[signatureMethod], APP_SECRET, stringToSign);
console.log(`Signature = ${signature}`);
