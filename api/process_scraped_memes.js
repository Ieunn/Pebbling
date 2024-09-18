import { connectToDatabase } from './db.js';
import { StorageWrapper } from './storageWrapper.js';
import LRU from 'lru-cache';

const rateLimit = (options) => {
    const tokenCache = new LRU({
      max: options.uniqueTokenPerInterval || 500,
      ttl: options.interval || 60000,
    });
  
    return {
      check: (limit, token) =>
        new Promise((resolve, reject) => {
          const tokenCount = tokenCache.get(token) || [0];
          if (tokenCount[0] === 0) {
            tokenCache.set(token, tokenCount);
          }
          tokenCount[0] += 1;
  
          const currentUsage = tokenCount[0];
          const isRateLimited = currentUsage >= limit;
          resolve({
            isRateLimited,
            limit: limit,
            current: currentUsage,
          });
        }),
    };
  };
  
const limiter = rateLimit({
    interval: 60 * 1000, // 1 minute
    uniqueTokenPerInterval: 500, // Max 500 users per second
});

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
        const token = req.headers['x-forwarded-for'] || 'anonymous';
        const { isRateLimited } = await limiter.check(10, token); // Max 10 requests in 1 minute
        if (isRateLimited) {
            return res.status(429).json({ error: 'Rate limit exceeded' });
        }
        const { db } = await connectToDatabase();
        const memesCollection = db.collection('memes');
        const storage = new StorageWrapper();

        const processedMemes = [];
        const memes = req.body.memes;

        for (const meme of memes) {
            const imageResponse = await fetch(meme.imageUrl);
            const imageBuffer = await imageResponse.arrayBuffer();
            const imageHash = await storage.hashImage(Buffer.from(imageBuffer));

            const existingMeme = await memesCollection.findOne({ image_hash: imageHash });

            if (!existingMeme) {
            const storedImageUrl = await storage.uploadFileobj(Buffer.from(imageBuffer), `xhs_${Date.now()}.jpg`);
            
            const memeData = {
                title: meme.title,
                imageUrl: storedImageUrl,
                source: 'Xiaohongshu',
                originalUrl: meme.originalUrl,
                createdAt: new Date.now(),
                image_hash: imageHash,
                likes: 0,
                dislikes: 0,
                favorites: 0,
                priority: 0
            };

            await memesCollection.insertOne(memeData);
            processedMemes.push(memeData);
            } else {
            processedMemes.push(existingMeme);
            }
        }

        res.status(200).json(processedMemes);
    } catch (error) {
      console.error('Server error:', error);
      res.status(500).json({ error: 'Error processing memes', details: error.message });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}