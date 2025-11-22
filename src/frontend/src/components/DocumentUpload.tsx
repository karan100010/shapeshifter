'use client';

import { useState, useRef, DragEvent, ChangeEvent } from 'react';
import styles from './DocumentUpload.module.css';
import { api } from '@/lib/api';

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

    const [driveId, setDriveId] = useState('');

    const handleDriveUpload = async () => {
        if (!driveId) return;
        try {
            const result = await api.uploadFromGoogleDrive(driveId);
            // Create a dummy file entry to show in UI
            const dummyFile = new File([], result.filename);
            const newEntry: UploadedFile = {
                id: `${Date.now()}-gdrive-${driveId}`,
                file: dummyFile,
                progress: 100,
                status: 'success',
                error: undefined,
            };
            setFiles(prev => [...prev, newEntry]);
            // Notify parent if needed
            if (onUploadComplete) {
                onUploadComplete([dummyFile]);
            }
            setDriveId('');
        } catch (error) {
            console.error('Google Drive upload failed:', error);
            // Optionally show error to user
        }
    };

    // Existing code continues below

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
                uploadFile(uploadedFile.id, uploadedFile.file);
            }
        });
    };

    const uploadFile = async (fileId: string, file: File) => {
        try {
            await api.uploadFile(file);

            setFiles(prev => prev.map(f => {
                if (f.id === fileId) {
                    return {
                        ...f,
                        progress: 100,
                        status: 'success'
                    };
                }
                return f;
            }));

            // Check if all files are uploaded
            setFiles(currentFiles => {
                const allCompleted = currentFiles.every(f => f.status === 'success' || f.status === 'error');
                if (allCompleted && onUploadComplete) {
                    const successfulFiles = currentFiles
                        .filter(f => f.status === 'success')
                        .map(f => f.file);
                    if (successfulFiles.length > 0) {
                        onUploadComplete(successfulFiles);
                    }
                }
                return currentFiles;
            });

        } catch (error) {
            console.error('Upload failed:', error);
            setFiles(prev => prev.map(f => {
                if (f.id === fileId) {
                    return {
                        ...f,
                        status: 'error',
                        error: 'Upload failed'
                    };
                }
                return f;
            }));
        }
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

            <div className={styles.googleDriveSection}>
                <h4>Or import from Google Drive</h4>
                <div className={styles.driveInputGroup}>
                    <input
                        type="text"
                        placeholder="Enter Google Drive File ID"
                        value={driveId}
                        onChange={(e) => setDriveId(e.target.value)}
                        className={styles.driveInput}
                    />
                    <button
                        onClick={handleDriveUpload}
                        disabled={!driveId}
                        className={styles.driveButton}
                    >
                        Import
                    </button>
                </div>
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
