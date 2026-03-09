import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.container}>
      <nav className={styles.nav}>
        <div className={styles.logo}>
          Auto<span className="gradient-text">Vuln</span>
        </div>
        <div className={styles.navLinks}>
          <a href="#" className={styles.navLink}>Platform</a>
          <a href="#" className={styles.navLink}>Solutions</a>
          <a href="#" className={styles.navLink}>Pricing</a>
          <a href="#" className={styles.navLink}>Documentation</a>
        </div>
        <div className={styles.navActions}>
          <button className="btn btn-secondary">Sign In</button>
          <button className="btn btn-primary">Get Started</button>
        </div>
      </nav>

      <main className={styles.hero}>
        <div className={styles.orb1}></div>
        <div className={styles.orb2}></div>

        <div className={`${styles.heroContent} animate-fade-in`}>
          <div className={styles.badge}>v2.0 Beta Live</div>

          <h1 className={styles.title}>
            Automated <br />
            <span className="gradient-text">Vulnerability Assessment</span>
          </h1>

          <p className={styles.description}>
            Continuously monitor your entire attack surface globally. Detect vulnerabilities faster, prioritize risks precisely, and remediate autonomously using AI-driven engines.
          </p>

          <div className={styles.heroActions}>
            <button className="btn btn-primary">
              Start Free Scan
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12H19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                <path d="M12 5L19 12L12 19" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
            <button className="btn btn-secondary">
              Book Demo
            </button>
          </div>
        </div>

        <div className={styles.heroVisual}>
          <div className={`${styles.dashboardMockup} glass animate-float`}>
            <div className={styles.mockupHeader}>
              <div className={styles.mockupTitle}>Live Scan Engine</div>
              <div className={styles.statusIndicator}>
                <div className={styles.dot}></div>
                Scanning
              </div>
            </div>

            <div className={styles.statsGrid}>
              <div className={styles.statCard}>
                <span className={styles.statLabel}>Critical Findings</span>
                <span className={`${styles.statValue} ${styles.danger}`}>3</span>
              </div>
              <div className={styles.statCard}>
                <span className={styles.statLabel}>High Risks</span>
                <span className={`${styles.statValue} ${styles.warning}`}>12</span>
              </div>
              <div className={styles.statCard}>
                <span className={styles.statLabel}>Secured Assets</span>
                <span className={`${styles.statValue} ${styles.success}`}>842</span>
              </div>
            </div>

            <div className={styles.scanProgress}>
              <div className={styles.progressHeader}>
                <span>Current Phase: Deep Analysis</span>
                <span>68%</span>
              </div>
              <div className={styles.progressBar}>
                <div className={styles.progressFill}></div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
