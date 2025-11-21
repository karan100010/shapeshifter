'use client';

import styles from './StatsWidget.module.css';

interface StatsWidgetProps {
    title: string;
    value: string | number;
    change?: string;
    icon: string;
    trend?: 'up' | 'down';
}

export default function StatsWidget({ title, value, change, icon, trend }: StatsWidgetProps) {
    return (
        <div className={styles.widget}>
            <div className={styles.iconContainer}>
                <span className={styles.icon}>{icon}</span>
            </div>
            <div className={styles.content}>
                <h3 className={styles.title}>{title.toUpperCase()}</h3>
                <p className={styles.value}>{value}</p>
                {change && (
                    <div className={`${styles.change} ${styles[trend || 'up']}`}>
                        <span className={styles.arrow}>{trend === 'down' ? '↓' : '↑'}</span>
                        <span>{change}</span>
                    </div>
                )}
            </div>
        </div>
    );
}
