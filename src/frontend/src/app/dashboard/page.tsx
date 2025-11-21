import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import StatsWidget from '@/components/StatsWidget';
import styles from './dashboard.module.css';

export default function Dashboard() {
    return (
        <div className={styles.container}>
            <Sidebar />
            <div className={styles.main}>
                <Header />
                <div className={styles.content}>
                    <div className={styles.pageHeader}>
                        <h1 className={styles.pageTitle}>Dashboard</h1>
                        <p className={styles.pageSubtitle}>Welcome back, Kunal! Here&apos;s what&apos;s happening with your projects.</p>
                    </div>

                    <div className={styles.statsGrid}>
                        <StatsWidget
                            title="Total Documents"
                            value="1,234"
                            change="+12.5%"
                            icon="📄"
                            trend="up"
                        />
                        <StatsWidget
                            title="Active Queries"
                            value="89"
                            change="+5.2%"
                            icon="🔍"
                            trend="up"
                        />
                        <StatsWidget
                            title="Graph Nodes"
                            value="5,678"
                            change="-2.1%"
                            icon="🕸️"
                            trend="down"
                        />
                        <StatsWidget
                            title="API Calls"
                            value="12.4K"
                            change="+18.3%"
                            icon="⚡"
                            trend="up"
                        />
                    </div>

                    <div className={styles.recentActivity}>
                        <h2 className={styles.sectionTitle}>Recent Activity</h2>
                        <div className={styles.activityList}>
                            <div className={styles.activityItem}>
                                <div className={styles.activityIcon}>📊</div>
                                <div className={styles.activityContent}>
                                    <h3 className={styles.activityTitle}>Document indexed successfully</h3>
                                    <p className={styles.activityTime}>2 minutes ago</p>
                                </div>
                            </div>
                            <div className={styles.activityItem}>
                                <div className={styles.activityIcon}>🔍</div>
                                <div className={styles.activityContent}>
                                    <h3 className={styles.activityTitle}>New query processed</h3>
                                    <p className={styles.activityTime}>15 minutes ago</p>
                                </div>
                            </div>
                            <div className={styles.activityItem}>
                                <div className={styles.activityIcon}>⚙️</div>
                                <div className={styles.activityContent}>
                                    <h3 className={styles.activityTitle}>System optimization completed</h3>
                                    <p className={styles.activityTime}>1 hour ago</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
