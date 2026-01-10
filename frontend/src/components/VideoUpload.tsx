import React, { useState, useRef } from 'react';
import { Upload, Video as VideoIcon, X } from 'lucide-react';
import { useVideoUpload } from '../hooks/useVideoUpload';
import { VideoMetadata } from '../services/api';

interface VideoUploadProps {
  onVideoUploaded: (metadata: VideoMetadata) => void;
}

export const VideoUpload: React.FC<VideoUploadProps> = ({ onVideoUploaded }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { uploadVideo, uploading, progress, error } = useVideoUpload();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type.startsWith('video/')) {
      setSelectedFile(file);
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const metadata = await uploadVideo(selectedFile);
    if (metadata) {
      onVideoUploaded(metadata);
    }
  };

  const handleRemove = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
      setPreviewUrl(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <VideoIcon className="w-5 h-5" />
        Video Upload
      </h2>

      {!selectedFile ? (
        <div
          className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-primary-500 transition-colors"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="w-12 h-12 mx-auto mb-3 text-gray-400" />
          <p className="text-gray-600 mb-2">Click to select a video file</p>
          <p className="text-sm text-gray-400">MP4, MOV, AVI (max 100MB)</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>
      ) : (
        <div className="space-y-4">
          <div className="relative bg-black rounded-lg overflow-hidden">
            {previewUrl && (
              <video
                src={previewUrl}
                controls
                className="w-full max-h-64 object-contain"
              />
            )}
          </div>

          <div className="flex items-center justify-between bg-gray-50 p-3 rounded">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {selectedFile.name}
              </p>
              <p className="text-xs text-gray-500">
                {formatFileSize(selectedFile.size)}
              </p>
            </div>
            <button
              onClick={handleRemove}
              className="ml-3 text-gray-400 hover:text-gray-600"
              disabled={uploading}
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {uploading && (
            <div className="space-y-2">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-sm text-center text-gray-600">
                Uploading... {progress}%
              </p>
            </div>
          )}

          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-3">
              <p className="text-sm text-red-800">{error}</p>
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={uploading}
            className="w-full bg-primary-600 text-white py-2 px-4 rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {uploading ? 'Uploading...' : 'Upload Video'}
          </button>
        </div>
      )}
    </div>
  );
};
