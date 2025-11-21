'use client';

import styles from './Header.module.css';

export default function Header() {
    return (
        <header className={styles.header}>
            <div className={styles.searchBar}>
                <span className={styles.searchIcon}>🔍</span>
                <input
                    type="text"
                    placeholder="Search..."
                    className={styles.searchInput}
                />
            </div>
            <div className={styles.userSection}>
                <button className={styles.notificationBtn}>
                    <span className={styles.notificationIcon}>🔔</span>
                    <span className={styles.badge}>3</span>
                </button>
                <div className={styles.userProfile}>
                    <div className={styles.avatar}>K</div>
                    <span className={styles.userName}>Kunal</span>
                </div>
            </div>
        </header>
    );
}
