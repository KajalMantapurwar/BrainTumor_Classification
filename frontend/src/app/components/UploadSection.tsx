import { Upload, Brain, MapPin, Loader2 } from 'lucide-react';
import { ImageWithFallback } from './figma/ImageWithFallback';
import { useState, useRef } from 'react';
import API from '../../api';

export function UploadSection() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [isGeneratingHeatmap, setIsGeneratingHeatmap] = useState(false);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [heatmapUrl, setHeatmapUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      // Create preview URL
      const url = URL.createObjectURL(file);
      setPreviewUrl(url);
      // Reset previous results
      setPredictionResult(null);
      setHeatmapUrl(null);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  const handleDetectTumor = async () => {
    if (!selectedFile) {
      alert('Please select an MRI scan first');
      return;
    }

    setIsPredicting(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await API.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setPredictionResult(response.data);
      console.log('Prediction result:', response.data);
    } catch (error: any) {
      console.error('Prediction error:', error);
      alert(error.response?.data?.error || 'Failed to detect tumor. Please try again.');
    } finally {
      setIsPredicting(false);
    }
  };

  const handleGenerateHeatmap = async () => {
    if (!selectedFile) {
      alert('Please select an MRI scan first');
      return;
    }

    if (!predictionResult) {
      alert('Please detect tumor first before generating heatmap');
      return;
    }

    setIsGeneratingHeatmap(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await API.post('/predict', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Use the gradcam image from response if available
      if (response.data.gradcam_url) {
        setHeatmapUrl(response.data.gradcam_url);
      }
    } catch (error: any) {
      console.error('Heatmap error:', error);
      alert('Failed to generate heatmap. Please try again.');
    } finally {
      setIsGeneratingHeatmap(false);
    }
  };

  return (
    <div className="bg-white/70 backdrop-blur-lg rounded-2xl p-4 md:p-6 shadow-xl border border-teal-100 mb-4">
      <h2 className="text-teal-900 mb-4 text-lg md:text-xl">Upload MRI Scan</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 mb-4 md:mb-6">
        <div className="border-2 border-dashed border-teal-300 rounded-2xl p-6 md:p-8 bg-teal-50/50 hover:bg-teal-50 transition-all cursor-pointer flex flex-col items-center justify-center min-h-[200px]">
          <Upload className="w-10 h-10 md:w-12 md:h-12 text-teal-500 mb-3" />
          <p className="text-teal-700 mb-2 text-center text-sm md:text-base">Drag & drop your MRI scan here</p>
          <p className="text-teal-500 text-xs md:text-sm mb-4">or</p>
          <button 
            onClick={handleBrowseClick}
            className="px-4 md:px-6 py-2 bg-gradient-to-r from-teal-500 to-teal-600 text-white rounded-xl hover:shadow-lg transition-all text-sm md:text-base"
          >
            Browse Files
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            className="hidden"
          />
          {selectedFile && (
            <p className="text-teal-600 text-xs mt-2">Selected: {selectedFile.name}</p>
          )}
        </div>

        <div className="bg-gray-900 rounded-2xl overflow-hidden flex items-center justify-center min-h-[200px]">
          {heatmapUrl ? (
            <img
              src={heatmapUrl}
              alt="MRI Brain Scan Heatmap"
              className="w-full h-full object-cover"
            />
          ) : previewUrl ? (
            <img
              src={previewUrl}
              alt="MRI Brain Scan Preview"
              className="w-full h-full object-cover"
            />
          ) : (
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=400&h=400&fit=crop"
              alt="MRI Brain Scan Preview"
              className="w-full h-full object-cover"
            />
          )}
        </div>
      </div>

      {/* Prediction Result Display */}
      {predictionResult && (
        <div className="mb-4 p-4 bg-teal-100 rounded-xl">
          <h3 className="font-semibold text-teal-900">Prediction Result:</h3>
          <p className="text-teal-800">Tumor Type: <strong>{predictionResult.prediction}</strong></p>
          <p className="text-teal-700">Confidence: {(predictionResult.confidence * 100).toFixed(2)}%</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <button 
          onClick={handleDetectTumor}
          disabled={isPredicting || !selectedFile}
          className="group bg-gradient-to-br from-teal-500 to-teal-600 rounded-2xl p-4 md:p-6 text-white hover:shadow-2xl hover:scale-105 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          <div className="flex items-start gap-3">
            <div className="p-2 md:p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              {isPredicting ? (
                <Loader2 className="w-5 h-5 md:w-6 md:h-6 animate-spin" />
              ) : (
                <Brain className="w-5 h-5 md:w-6 md:h-6" />
              )}
            </div>
            <div className="flex-1">
              <h3 className="mb-1 md:mb-2 text-sm md:text-base">
                {isPredicting ? 'Detecting...' : 'Detect Tumor Type'}
              </h3>
              <p className="text-white/90 text-xs md:text-sm">Identify type of tumor using AI model</p>
            </div>
          </div>
        </button>

        <button 
          onClick={handleGenerateHeatmap}
          disabled={isGeneratingHeatmap || !predictionResult}
          className="group bg-gradient-to-br from-teal-400 to-emerald-500 rounded-2xl p-4 md:p-6 text-white hover:shadow-2xl hover:scale-105 transition-all text-left disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
        >
          <div className="flex items-start gap-3">
            <div className="p-2 md:p-3 bg-white/20 rounded-xl backdrop-blur-sm">
              {isGeneratingHeatmap ? (
                <Loader2 className="w-5 h-5 md:w-6 md:h-6 animate-spin" />
              ) : (
                <MapPin className="w-5 h-5 md:w-6 md:h-6" />
              )}
            </div>
            <div className="flex-1">
              <h3 className="mb-1 md:mb-2 text-sm md:text-base">
                {isGeneratingHeatmap ? 'Generating...' : 'Generate Heatmap'}
              </h3>
              <p className="text-white/90 text-xs md:text-sm">Show heatmap highlighting tumor regions</p>
            </div>
          </div>
        </button>
      </div>

    </div>
  );
}
