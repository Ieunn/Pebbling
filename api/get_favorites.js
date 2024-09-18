import { connectToDatabase } from './db.js';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const { db } = await connectToDatabase();
      const memesCollection = db.collection('memes');

      const favorites = await memesCollection.find({ favorites: { $gt: 0 } })
        .sort({ favorites: -1 })
        .toArray();

      res.status(200).json(favorites);
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: 'Error fetching favorites', details: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}