DROP SCHEMA IF EXISTS financeBrosDB;
CREATE SCHEMA financeBrosDB;
USE financeBrosDB;

CREATE TABLE IF NOT EXISTS users (
    user_id INT NOT NULL,
    SSN VARCHAR(255) UNIQUE NOT NULL,
    f_name VARCHAR(255) NOT NULL,
    l_name VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    banned BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20) UNIQUE NOT NULL,
    DOB DATETIME NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS stock (
    ticker VARCHAR(10) NOT NULL,
    sharePrice DECIMAL(10, 2) NOT NULL ,
    stockName VARCHAR(255) NOT NULL,
    beta DECIMAL(50, 6) NOT NULL,
    PRIMARY KEY (ticker)
);

CREATE TABLE IF NOT EXISTS personalPortfolio (
    portfolio_id INT NOT NULL,
    beta DECIMAL(50, 6) NOT NULL,
    liquidated_Value DECIMAL(20, 2) NOT NULL,
    P_L DECIMAL(10, 2) NOT NULL DEFAULT 0,
    user_id INT NOT NULL,
    PRIMARY KEY (portfolio_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS portfolioStocks (
    portfolio_id INT NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    primary key (portfolio_id, ticker),
    FOREIGN KEY (ticker)
        REFERENCES stock(ticker)
        ON UPDATE cascade ON DELETE cascade,
    FOREIGN KEY (portfolio_id)
        REFERENCES personalPortfolio(portfolio_id)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS verifiedPublicProfile (
    verified_user_id INT NOT NULL,
    kpi_id INT NOT NULL,
    photo_url VARCHAR(255),
    verified_username VARCHAR(255),
    biography varchar(2500),
    user_id INT NOT NULL,
    PRIMARY KEY (verified_user_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS verifiedPrivateProfile (
    verified_user_id INT NOT NULL,
    kpi_id INT,
    photo_url VARCHAR(255),
    verified_username VARCHAR(255),
    biography varchar(2500),
    user_id INT NOT NULL,
    PRIMARY KEY (verified_user_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS follows (
    following_id INT,
    follower_id INT,
    timestamp DATETIME,
    count INT,
    user_id INT,
    PRIMARY KEY (following_id, follower_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE cascade,
    FOREIGN KEY (follower_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE cascade,
    FOREIGN KEY (following_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE cascade
);

CREATE TABLE IF NOT EXISTS dashboardFeed (
    dashboard_feed_id INT NOT NULL,
    startTime DATETIME,
    endTime DATETIME,
    Kpi_id INT,
    updatedTime DATETIME DEFAULT CURRENT_TIMESTAMP
                    ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    PRIMARY KEY (dashboard_feed_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_id INT UNIQUE AUTO_INCREMENT,
    text TEXT,
    likes INT,
    timeCreated DATETIME DEFAULT CURRENT_TIMESTAMP,
    firstViewedAt DATETIME,
    lastViewedAt DATETIME,
    viewedAtResponseTime INT,
    user_id INT NOT NULL,
    PRIMARY KEY (notification_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS dashboardNotifications (
    notification_id INT NOT NULL,
    dashboard_feed_id INT AUTO_INCREMENT,
    PRIMARY KEY (notification_id, dashboard_feed_id),
    FOREIGN KEY (notification_id)
        REFERENCES notifications(notification_id)
        ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (dashboard_feed_id)
        REFERENCES dashboardFeed(dashboard_feed_id)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS userNotifications (
    user_id INT NOT NULL,
    notification_id INT NOT NULL,
    PRIMARY KEY (user_id, notification_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
        ON UPDATE cascade ON DELETE restrict,
    FOREIGN KEY (notification_id)
        REFERENCES notifications(notification_id)
        ON UPDATE cascade ON DELETE restrict
);

CREATE TABLE IF NOT EXISTS userMetrics (
    user_metric_ID INT NOT NULL,
    dmStartTime DATETIME,
    dmEndTime DATETIME,
    mStartTime DATETIME,
    mEndTime DATETIME,
    activeUsers INT,
    user_id INT NOT NULL,
    PRIMARY KEY (user_metric_ID),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INT NOT NULL,
    f_name VARCHAR(255),
    l_name VARCHAR(255),
    city VARCHAR(255),
    start_date DATETIME,
    DOB DATETIME,
    user_metric_id INT NOT NULL,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (user_metric_id)
        REFERENCES userMetrics(user_metric_ID)
);