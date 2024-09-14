import { connectToDatabase } from '../utils/db';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const { db } = await connectToDatabase();
      const memesCollection = db.collection('memes');

      const count = await memesCollection.countDocuments();
      const randomIndex = Math.floor(Math.random() * count);

      const meme = await memesCollection.findOne({}, { skip: randomIndex });

      res.status(200).json(meme);
    } catch (error) {
      res.status(500).json({ error: 'Error fetching meme' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}