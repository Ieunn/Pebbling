import { defineStore } from 'pinia'
import axios from 'axios'

export const useMemeStore = defineStore('meme', {
  state: () => ({
    memes: [],
    selectedSource: '',
    sources: [],
    loading: false,
    error: null,
    showAuthModal: false,
    viewedMemes: JSON.parse(localStorage.getItem('viewedMemes') || '[]'),
  }),
  actions: {
    async fetchSources() {
      try {
        const response = await axios.get('/api/get_sources')
        this.sources = response.data
        if (this.sources.length > 0) {
          if (!this.sources.includes('Xiaohongshu')) {
            this.sources.push('Xiaohongshu')
          }
          if (!this.selectedSource) {
            this.selectedSource = localStorage.getItem('lastSelectedSource') || this.sources[0]
          }
        }
      } catch (error) {
        console.error('Error fetching sources:', error)
      }
    },
    async fetchMemes(count = 5) {
        this.loading = true
        this.error = null
        try {
          const response = await axios.get('/api/get_memes', {
            params: { 
              source: this.selectedSource,
              exclude: this.viewedMemes.join(','),
              count: count
            }
          })
          if (response.data && response.data.length > 0) {
            const newMemes = response.data.filter(meme => !this.viewedMemes.includes(meme._id))
            this.memes = [...this.memes, ...newMemes]
          }
          
          if (this.memes.length < count) {
            await this.fetchMemes(count - this.memes.length)
          }
        } catch (err) {
          console.error('Error fetching memes:', err)
          this.error = 'Error fetching memes: ' + (err.response?.data?.error || err.message)
        } finally {
          this.loading = false
        }
      },
    async handleSourceChange() {
        if (this.selectedSource === 'Xiaohongshu') {
            this.memes = this.memes.filter((meme) => meme.source === 'Xiaohongshu')
            if (this.checkXiaohongshuCookies()) {
                if (this.memes.length > 0) {
                    console.log('Using existing memes')
                } else {
                    await this.scrapeMemes()
                }
            } else {
                this.showAuthModal = true
            }
        } else {
            await this.resetAndFetchMemes()
        }
    },
    checkXiaohongshuCookies() {
        const cookies = document.cookie
        return cookies.includes('xhsTrackerId') || cookies.includes('websectokenx')
    },
    async scrapeMemes() {
        if (this.memes.length > 0) {
            console.log('Still have unviewed memes, skipping scraping');
            return;
        }
    
        this.loading = true;
        this.error = null;
        try {
            const scrapedMemes = await scrapeXiaohongshuMemes();
            if (scrapedMemes.length > 0) {
                const response = await axios.post('/api/process_scraped_memes', { memes: scrapedMemes });
                if (response.status === 429) {
                    console.log('Rate limit exceeded, fetching from server');
                    await fetchMemes();
                } else {
                    this.memes = response.data;
                }
            } else {
                console.log('No new memes found, fetching from server');
                await fetchMemes();
            }
        } catch (err) {
            if (err.response && err.response.status === 429) {
                console.log('Rate limit exceeded, fetching from server');
            } else {
                console.error('Error scraping memes:', err);
                this.error = 'Error scraping memes: ' + (err.response?.data?.error || err.message);
            }
            await fetchMemes();
        } finally {
            this.loading = false;
        }
    },
    async scrapeXiaohongshuMemes() {
        const memes = [];
        const pageUrl = 'https://www.xiaohongshu.com/search_result?keyword=meme';
        
        try {
            const response = await fetch(pageUrl, {
                credentials: 'include',
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            
            const noteItems = doc.querySelectorAll('.note-item');
            for (let i = 0; i < Math.min(noteItems.length, 10); i++) {
                const noteItem = noteItems[i];
                const titleElement = noteItem.querySelector('.note-title');
                const linkElement = noteItem.querySelector('a');
                
                if (titleElement && linkElement) {
                    const title = titleElement.textContent.trim();
                    const noteUrl = 'https://www.xiaohongshu.com' + linkElement.getAttribute('href');
                    
                    const noteResponse = await fetch(noteUrl, {
                        credentials: 'include',
                        headers: {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        }
                    });
                    
                    if (noteResponse.ok) {
                        const noteHtml = await noteResponse.text();
                        const noteDoc = parser.parseFromString(noteHtml, 'text/html');
                        
                        const imageElements = noteDoc.querySelectorAll('.note-img');
                        for (const imageElement of imageElements) {
                            const imageUrl = imageElement.src;
                            if (imageUrl) {
                                memes.push({
                                    title: title,
                                    imageUrl: imageUrl,
                                    originalUrl: noteUrl
                                });
                            }
                        }
                    }
                }
                
                if (memes.length >= 20) break;
            }
        } catch (error) {
            console.error('Error scraping Xiaohongshu:', error);
        }
        
        return memes;
    },
    async resetAndFetchMemes() {
        this.memes = []
        await this.fetchMemes()
        localStorage.setItem('lastSelectedSource', this.selectedSource)
    },
    async handleSwipe(memeId, action) {
        if (memeId !== 'empty') {
          if (!this.viewedMemes.includes(memeId)) {
            this.viewedMemes.push(memeId)
            localStorage.setItem('viewedMemes', JSON.stringify(this.viewedMemes))
          }
      
          try {
            const memeToSave = this.memes.find(meme => meme._id === memeId)
      
            if (action === 'favorite') {
              let favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
              if (!favorites.some(fav => fav._id === memeId)) {
                favorites.push(memeToSave)
                localStorage.setItem('favorites', JSON.stringify(favorites))
                console.log('Meme added to favorites')
              }
              await axios.post('/api/update_meme_status', { memeId, action: 'like' })
            }
            
            await axios.post('/api/update_meme_status', { memeId, action })
          } catch (error) {
            console.error(`Error updating meme status:`, error)
          }
        }
      
        this.memes = this.memes.slice(1)
        if (this.memes.length < 3) {
          this.fetchMemes(5 - this.memes.length)
        }
    },
  },
})