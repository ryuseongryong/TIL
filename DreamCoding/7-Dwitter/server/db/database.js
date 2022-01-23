import Mongoose from 'mongoose';
import { config } from '../config.js';

export async function connectDB() {
  return Mongoose.connect(config.db.host, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    // Mongoose 6.X~ default option
    // useFindAndModify: false,
  });
}

export function useVirtualId(schema) {
  // _id -> id
  schema.virtual('id').get(function () {
    return this._id.toString();
  });
  schema.set('toJSON', { virtuals: true });
  schema.set('toObject', { virtuals: true });
}
let db;

export function getTweets() {
  return db.collection('tweets');
}
