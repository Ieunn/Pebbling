import { connectToDatabase } from './db.js';
import { ObjectId } from 'mongodb';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { db } = await connectToDatabase();
      const memesCollection = db.collection('memes');

      const { memeId, action } = req.body;

      const updateObj = {};
      if (action === 'like' || action === 'favorite') {
        updateObj.likes = 1;
      }
      if (action === 'dislike') {
        updateObj.dislikes = 1;
      }
      if (action === 'favorite') {
        updateObj.favorites = 1;
      }

      await memesCollection.updateOne(
        { _id: new ObjectId(memeId) },
        { $inc: updateObj }
      );

      res.status(200).json({ message: `Meme ${action} successfully` });
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: `Error updating meme status`, details: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}