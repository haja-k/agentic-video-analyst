import React from 'react';
import { FileText, Presentation, Clock, Film } from 'lucide-react';
import { VideoMetadata } from '../services/api';

interface VideoInfoProps {
  metadata: VideoMetadata | null;
  onGenerateReport: (format: 'pdf' | 'pptx') => void;
  generating: boolean;
}

export const VideoInfo: React.FC<VideoInfoProps> = ({
  metadata,
  onGenerateReport,
  generating,
}) => {
  if (!metadata) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Video Information</h2>
        <p className="text-gray-500 text-center">No video uploaded yet</p>
      </div>
    );
  }

  const formatDuration = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Film className="w-5 h-5" />
        Video Information
      </h2>

      <div className="space-y-3 mb-6">
        <div className="flex items-start gap-3">
          <FileText className="w-4 h-4 mt-1 text-gray-400" />
          <div className="flex-1 min-w-0">
            <p className="text-sm text-gray-600">Filename</p>
            <p className="font-medium text-gray-900 truncate">
              {metadata.filename}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Clock className="w-4 h-4 text-gray-400" />
          <div>
            <p className="text-sm text-gray-600">Duration</p>
            <p className="font-medium text-gray-900">
              {formatDuration(metadata.duration)}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-600">Resolution</p>
            <p className="font-medium text-gray-900">{metadata.resolution}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">FPS</p>
            <p className="font-medium text-gray-900">{metadata.fps}</p>
          </div>
        </div>

        <div>
          <p className="text-sm text-gray-600">File Size</p>
          <p className="font-medium text-gray-900">
            {formatFileSize(metadata.fileSize)}
          </p>
        </div>

        <div>
          <p className="text-sm text-gray-600">Video ID</p>
          <p className="font-mono text-xs text-gray-900 break-all">
            {metadata.videoId}
          </p>
        </div>
      </div>

      <div className="border-t border-gray-200 pt-4">
        <h3 className="text-sm font-semibold mb-3">Generate Report</h3>
        <div className="space-y-2">
          <button
            onClick={() => onGenerateReport('pdf')}
            disabled={generating}
            className="w-full flex items-center justify-center gap-2 bg-red-600 text-white py-2 px-4 rounded-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <FileText className="w-4 h-4" />
            Generate PDF Report
          </button>
          <button
            onClick={() => onGenerateReport('pptx')}
            disabled={generating}
            className="w-full flex items-center justify-center gap-2 bg-orange-600 text-white py-2 px-4 rounded-lg hover:bg-orange-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            <Presentation className="w-4 h-4" />
            Generate PowerPoint
          </button>
        </div>
      </div>
    </div>
  );
};
