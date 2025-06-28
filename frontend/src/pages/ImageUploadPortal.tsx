import axios from 'axios';
import React, { useState, useEffect, useRef } from 'react';

interface UploadedImage {
  url: string;
}

interface UploadResponse {
  url: string;
}

const ImageUploadPortal: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [imageLinks, setImageLinks] = useState<UploadedImage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Clean up object URLs when preview changes or component unmounts
  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    
    if (!selectedFile) return;

    // Validate file type
    if (!selectedFile.type.startsWith('image/')) {
      setError('Please select a valid image file (JPEG, PNG, GIF, etc.)');
      setFile(null);
      setPreview(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    // Validate file size (example: 5MB limit)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('File size too large (max 5MB)');
      setFile(null);
      setPreview(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setError('');
  };

  const handleUpload = async () => {
    if (!file) return;
    
    setLoading(true);
    setError('');

    try {
      const formData = new FormData();
      formData.append('image', file);

      const response = await axios.post<UploadResponse>(
        'http://localhost:5000/api/upload/image', 
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setImageLinks(prev => [...prev, { url: response.data.url }]);
    } catch (err) {
      let errorMessage = 'Upload failed';
      
      if (axios.isAxiosError(err)) {
        errorMessage = err.response?.data?.message || err.message;
      } else if (err instanceof Error) {
        errorMessage = err.message;
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
      setFile(null);
      setPreview(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const handleRemoveUpload = () => {
    setFile(null);
    setPreview(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 to-pink-400 px-4 py-12 flex flex-col items-center justify-start space-y-10">
      {/* Upload Box */}
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-2xl space-y-6">
        <h2 className="text-3xl font-bold text-center text-gray-800">Upload Image</h2>

        {error && <div className="text-red-600 text-sm text-center p-2 bg-red-50 rounded-lg">{error}</div>}

        <div className="space-y-4">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-600 file:text-white hover:file:bg-indigo-700"
          />

          {preview && (
            <div className="flex flex-col items-center space-y-4">
              <img
                src={preview}
                alt="Preview"
                className="max-h-60 rounded-lg object-contain border border-gray-300"
              />
              <button
                onClick={handleRemoveUpload}
                className="px-4 py-1 text-sm rounded bg-red-500 text-white hover:bg-red-600 transition"
              >
                Remove Preview
              </button>
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full py-2 px-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition disabled:opacity-50 font-medium"
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Uploading...
              </span>
            ) : 'Upload'}
          </button>
        </div>
      </div>

      {/* Uploaded Images Table */}
      {imageLinks.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-4xl space-y-6">
          <h3 className="text-2xl font-semibold text-gray-800 text-center">Uploaded Images</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white border border-gray-200 text-sm text-left text-gray-700 rounded-md overflow-hidden">
              <thead className="bg-gray-100 text-gray-800">
                <tr>
                  <th className="py-2 px-4 border-b">Link</th>
                </tr>
              </thead>
              <tbody>
                {imageLinks.map((img, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="py-2 px-4 border-b">
                      <a 
                        href={img.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline break-all"
                      >
                        {img.url}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default ImageUploadPortal;