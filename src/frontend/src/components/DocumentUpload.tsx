'use client';

import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import styles from './DocumentUpload.module.css';

interface UploadedFile {
    id: string;
    file: File;
    progress: number;
    status: 'uploading' | 'success' | 'error';
    error?: string;
}

interface DocumentUploadProps {
    onUploadComplete?: (files: File[]) => void;
    maxFileSize?: number; // in MB
    acceptedTypes?: string[];
}

export default function DocumentUpload({
    onUploadComplete,
    maxFileSize = 10,
    acceptedTypes = ['.pdf', '.txt', '.docx', '.doc']
}: DocumentUploadProps) {
    const [files, setFiles] = useState<UploadedFile[]>([]);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const validateFile = (file: File): string | null => {
        // Check file size
        if (file.size > maxFileSize * 1024 * 1024) {
            return `File size exceeds ${maxFileSize}MB limit`;
        }

        // Check file type
        const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
        if (!acceptedTypes.includes(fileExtension)) {
            return `File type not supported. Accepted types: ${acceptedTypes.join(', ')}`;
        }

        return null;
    };

    const handleFiles = (fileList: FileList | null) => {
        if (!fileList) return;

        const newFiles: UploadedFile[] = Array.from(fileList).map(file => {
            const error = validateFile(file);
            return {
                id: `${Date.now()}-${file.name}`,
                file,
                progress: 0,
                status: error ? 'error' : 'uploading',
                error: error || undefined
            };
        });

        setFiles(prev => [...prev, ...newFiles]);

        // Simulate upload for valid files
        newFiles.forEach(uploadedFile => {
            if (uploadedFile.status === 'uploading') {
                simulateUpload(uploadedFile.id);
            }
        });
    };

    const simulateUpload = (fileId: string) => {
        const interval = setInterval(() => {
            setFiles(prev => prev.map(f => {
                if (f.id === fileId) {
                    const newProgress = Math.min(f.progress + 10, 100);
                    return {
                        ...f,
                        progress: newProgress,
                        status: newProgress === 100 ? 'success' : 'uploading'
                    };
                }
                return f;
            }));
        }, 200);

        setTimeout(() => {
            clearInterval(interval);
            setFiles(prev => {
                const completedFiles = prev.filter(f => f.status === 'success').map(f => f.file);
                if (completedFiles.length > 0 && onUploadComplete) {
                    onUploadComplete(completedFiles);
                }
                return prev;
            });
        }, 2200);
    };

    const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };

    const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    };

    const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        handleFiles(e.dataTransfer.files);
    };

    const handleFileInput = (e: ChangeEvent<HTMLInputElement>) => {
        handleFiles(e.target.files);
    };

    const handleBrowseClick = () => {
        fileInputRef.current?.click();
    };

    const removeFile = (fileId: string) => {
        setFiles(prev => prev.filter(f => f.id !== fileId));
    };

    const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    };

    return (
        <div className={styles.container}>
            <div
                className={`${styles.dropzone} ${isDragging ? styles.dragging : ''}`}
                onDragEnter={handleDragEnter}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <div className={styles.uploadIcon}>📁</div>
                <h3 className={styles.uploadTitle}>Drop files here or click to browse</h3>
                <p className={styles.uploadSubtitle}>
                    Supported formats: {acceptedTypes.join(', ')} (Max {maxFileSize}MB)
                </p>
                <button className={styles.browseBtn} onClick={handleBrowseClick}>
                    Browse Files
                </button>
                <input
                    ref={fileInputRef}
                    type="file"
                    multiple
                    accept={acceptedTypes.join(',')}
                    onChange={handleFileInput}
                    className={styles.fileInput}
                />
            </div>

            {files.length > 0 && (
                <div className={styles.fileList}>
                    <h4 className={styles.fileListTitle}>Uploaded Files ({files.length})</h4>
                    {files.map(uploadedFile => (
                        <div key={uploadedFile.id} className={styles.fileItem}>
                            <div className={styles.fileIcon}>
                                {uploadedFile.status === 'success' && '✅'}
                                {uploadedFile.status === 'error' && '❌'}
                                {uploadedFile.status === 'uploading' && '⏳'}
                            </div>
                            <div className={styles.fileInfo}>
                                <div className={styles.fileName}>{uploadedFile.file.name}</div>
                                <div className={styles.fileSize}>{formatFileSize(uploadedFile.file.size)}</div>
                                {uploadedFile.error && (
                                    <div className={styles.fileError}>{uploadedFile.error}</div>
                                )}
                                {uploadedFile.status === 'uploading' && (
                                    <div className={styles.progressBar}>
                                        <div
                                            className={styles.progressFill}
                                            style={{ width: `${uploadedFile.progress}%` }}
                                        />
                                    </div>
                                )}
                            </div>
                            <button
                                className={styles.removeBtn}
                                onClick={() => removeFile(uploadedFile.id)}
                                aria-label="Remove file"
                            >
                                ×
                            </button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
