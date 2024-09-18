import { getSources } from './db.js';

export default async function handler(req, res) {
  if (req.method === 'GET') {
    try {
      const sources = await getSources();
      res.status(200).json(sources);
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: 'Error fetching sources', details: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}