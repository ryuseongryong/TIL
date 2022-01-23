/* 
'bob' : 'https://m.media-amazon.com/images/M/MV5BNzg0MWEyZjItOTZlMi00YmRjLWEyYzctODIwMDU0OThiMzNkXkEyXkFqcGdeQXVyNjUxMjc1OTM@._V1_UY317_CR13,0,214,317_AL_.jpg'
'seongryong' : 'https://avatars.githubusercontent.com/u/58920833?s=400&u=ac2997091b3a84b129630b576fddccaaadabecc4&v=4' 
*/
import Mongoose from 'mongoose';
import { useVirtualId } from '../db/database.js';

const userSchema = new Mongoose.Schema({
  username: { type: String, required: true },
  name: { type: String, required: true },
  email: { type: String, required: true },
  password: { type: String, required: true },
  url: String,
});

useVirtualId(userSchema);
const User = Mongoose.model('User', userSchema);

export async function findByUsername(username) {
  return User.findOne({ username });
}

export async function findById(id) {
  return User.findById(id);
}

export async function createUser(user) {
  return new User(user).save().then((data) => data.id);
}

function mapOptionalUser(user) {
  return user ? { ...user, id: user._id.toString() } : user;
}
