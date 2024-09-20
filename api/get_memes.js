import { connectToDatabase } from './db.js';
import { ObjectId } from 'mongodb';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const { db } = await connectToDatabase();
      const memesCollection = db.collection('memes');

      const { source, exclude, count = 5 } = req.query;
      const excludeIds = exclude ? exclude.split(',').map(id => new ObjectId(id)) : [];

      const query = {
        ...(source && { source }),
        ...(excludeIds.length > 0 && { _id: { $nin: excludeIds } })
      };

      const memes = await memesCollection.aggregate([
        { $match: query },
        { $sample: { size: parseInt(count) } }
      ]).toArray();

      console.log('Query:', query);
      console.log('Retrieved memes:', memes);

      if (memes.length === 0) {
        console.log('No memes found. Database state:', await memesCollection.stats());
        return res.status(404).json({ error: 'No memes found matching the criteria' });
      }

      res.status(200).json(memes);
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: 'Error fetching memes', details: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}