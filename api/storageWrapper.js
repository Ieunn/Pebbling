const python = require('python-bridge');

class StorageWrapper {
  constructor() {
    this.py = python();
    this.py.ex`
from storage import StorageProvider
storage = StorageProvider()
    `;
  }

  async uploadFileobj(fileData, objectName) {
    return this.py`storage.upload_fileobj(${fileData}, ${objectName})`;
  }

  async deleteFile(fileUrl) {
    return this.py`storage.delete_file(${fileUrl}))`;
  }

  async hashImage(imageData) {
    return this.py`storage.hash_image(${imageData})`;
  }

  close() {
    this.py.end();
  }
}

module.exports = StorageWrapper;