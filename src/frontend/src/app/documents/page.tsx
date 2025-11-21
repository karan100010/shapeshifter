'use client';

import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import DocumentUpload from '@/components/DocumentUpload';
import styles from './documents.module.css';

export default function DocumentsPage() {
    const handleUploadComplete = (files: File[]) => {
        console.log('Files uploaded:', files);
        // TODO: Send files to backend API
    };

    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.main}>
                <Header />
                <div className={styles.content}>
                    <div className={styles.pageHeader}>
                        <h1 className={styles.pageTitle}>Documents</h1>
                        <p className={styles.pageSubtitle}>
                            Upload and manage your documents for RAG processing
                        </p>
                    </div>

                    <DocumentUpload
                        onUploadComplete={handleUploadComplete}
                        maxFileSize={10}
                        acceptedTypes={['.pdf', '.txt', '.docx', '.doc']}
                    />

                    <div className={styles.infoSection}>
                        <h3 className={styles.infoTitle}>📚 Supported Features</h3>
                        <ul className={styles.featureList}>
                            <li>✅ Drag and drop multiple files</li>
                            <li>✅ PDF, TXT, DOCX file formats</li>
                            <li>✅ File size validation (up to 10MB)</li>
                            <li>✅ Real-time upload progress</li>
                            <li>✅ Error handling and validation</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}
