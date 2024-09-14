import { connectToDatabase } from '../utils/db';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const { db } = await connectToDatabase();
      const memesCollection = db.collection('memes');

      const count = await memesCollection.countDocuments();
      console.log(`Total memes in database: ${count}`);

      if (count === 0) {
        return res.status(404).json({ error: 'No memes found in the database' });
      }

      const randomIndex = Math.floor(Math.random() * count);
      const meme = await memesCollection.findOne({}, { skip: randomIndex });

      if (!meme) {
        console.log('Failed to fetch a meme');
        return res.status(404).json({ error: 'Failed to fetch a meme' });
      }

      res.status(200).json(meme);
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: 'Error fetching meme', details: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}