/* SQLite */
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Reviews;
DROP TABLE IF EXISTS Bookmarks;

CREATE TABLE Users (
    userid INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name VARCHAR(6) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
);

CREATE TABLE Courses (
    courseid INTEGER PRIMARY KEY AUTOINCREMENT,
    course_type VARCHAR(3) NOT NULL,
    course_num VARCHAR(4) NOT NULL,
    course_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE Reviews (
    reviewid INTEGER PRIMARY KEY AUTOINCREMENT,
    courseid INTEGER,
    userid INTEGER,
    year TEXT CHECK (year GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]'),
    semester VARCHAR(6) CHECK (semester IN ('spring', 'fall', 'summer')),
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    review_date DATE,
    FOREIGN KEY (courseid) REFERENCES Courses(courseid),
    FOREIGN KEY (userid) REFERENCES Users(userid)
);

CREATE TABLE Bookmarks (
    bookmarkid INTEGER PRIMARY KEY AUTOINCREMENT,
    userid INTEGER,
    courseid INTEGER,
    FOREIGN KEY (userid) REFERENCES Users(userid),
    FOREIGN KEY (courseid) REFERENCES Courses(courseid)
);

SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';

/* insert 5 students info */
INSERT INTO Users (user_name, password, role) VALUES ('259359', 'asd2345', 'student');
INSERT INTO Users (user_name, password, role) VALUES ('335789', 'hjk231', 'student');
INSERT INTO Users (user_name, password, role) VALUES ('226353', '2j3491', 'student');
INSERT INTO Users (user_name, password, role) VALUES ('146544', '9ga2341', 'student');
INSERT INTO Users (user_name, password, role) VALUES ('333626', 'aef2333', 'student');
/* insert 1 admin info */
INSERT INTO Users (user_name, password, role) VALUES ('000001', 'iamadmin', 'admin');


INSERT INTO Courses (course_type, course_num, course_name, description)
VALUES 
('CSC', '3100', 'Data Structure', 'This course provides a comprehensive overview of data structures and their applications in computer science. Students will learn about various types of data structures such as arrays, linked lists, stacks, queues, trees, graphs, and hash tables.'),
('DDA', '3005', 'Numerical Methods', 'In this course, students will explore the fundamental numerical methods used to solve mathematical problems that cannot be solved analytically. Topics include root finding, interpolation, numerical differentiation and integration, and solving systems of linear equations.'),
('DDA', '3020', 'Machine Learning', 'Students will gain an understanding of machine learning algorithms and techniques for pattern recognition, classification, regression, clustering, and dimensionality reduction. The course covers both supervised and unsupervised learning approaches.'),
('DDA', '4002', 'Stochastic Simulation', 'This course introduces students to stochastic simulation methods for modeling complex systems with random components. Topics include Monte Carlo simulations, Markov chain models, queuing theory, and discrete-event simulation.'),
('DDA', '4210', 'Advanced Machine Learning', 'Building upon the foundation laid in DDA 3020, this course delves deeper into advanced topics in machine learning such as deep neural networks, reinforcement learning, and natural language processing.'),
('MAT', '3007', 'Optimization', 'Students will study optimization techniques including linear programming, nonlinear programming, dynamic programming, and integer programming. Applications are drawn from various fields such as operations research, economics, and engineering.'),
('STA', '2004', 'Mathematical Statistics', 'This course covers statistical inference principles, probability distributions, sampling distributions, point estimation, confidence intervals, hypothesis testing, and regression analysis.'),
('STA', '4001', 'Stochastic Processes', 'Students will learn about stochastic processes, which are mathematical models for random phenomena evolving over time or space. Topics include Markov chains, Poisson processes, Brownian motion, and renewal theory.'),
('FIN', '3080', 'Investment Analysis and Portfolio Management', 'This course provides a comprehensive overview of investment analysis and portfolio management techniques. Students will learn how to evaluate securities, construct portfolios, manage risk, and make informed investment decisions.'),
('FMA', '4200', 'Financial Data Analysis', 'In this course, students will gain an understanding of financial data analysis methods and tools used in the finance industry. Topics include time series analysis, regression models, and forecasting techniques.'),
('FMA', '4800', 'Financial Computation', 'The Financial Computation course focuses on computational methods for solving complex financial problems. It covers topics such as numerical methods, optimization algorithms, and simulation techniques.'),
('STA', '4002', 'Multivariate Techniques with Business Applications', 'This course introduces multivariate statistical techniques and their applications in business settings. Students will learn about factor analysis, cluster analysis, and discriminant analysis.'),
('STA', '4003', 'Time Series', 'The Time Series course explores the analysis and modeling of time-dependent data. Students will study various time series models and learn how to apply them to real-world scenarios.'),
('STA', '4020', 'Statistical Modelling in Financial Markets', 'This course delves into statistical modeling techniques specifically tailored for financial markets. Students will analyze market trends, assess risks, and develop predictive models.'),
('CSC', '3050', 'Computer Architecture', 'This course provides a comprehensive overview of computer architecture, covering topics such as instruction set architectures, processor design, memory hierarchy, and input/output systems.'),
('CSC', '3150', 'Operating System', 'In this course, students will learn about the fundamental concepts of operating systems, including process management, memory management, file systems, device drivers, and security.'),
('CSC', '3160', 'Fundamentals of Speech and Language Processing', 'The course introduces students to the basic principles of speech recognition and natural language processing. It covers topics like phonetics, acoustic modeling, language models, and machine learning techniques for speech and text data.'),
('CSC', '3170', 'Database System', 'Students in this course will gain an understanding of database management systems, including relational databases, SQL, indexing, query optimization, transaction processing, and concurrency control.'),
('CSC', '4001', 'Software Engineering', 'This advanced course focuses on software engineering methodologies, project management, requirements analysis, system design, implementation, testing, and maintenance.');



INSERT INTO Bookmarks (userid, courseid)
VALUES
(1, 9),
(1, 13),
(1, 1),
(3, 15),
(3, 16),
(4, 8),
(2,2),
(4, 9);


INSERT INTO Reviews (courseid, userid, year, semester, rating, comment, review_date)
VALUES
(2, 1, '2021-2022', 'spring', 4, 'The teacher was excellent', '2021-05-08'),
(2, 2, '2023-2024', 'fall', 5, 'The content was slightly difficult, but if studied hard, one should be able to achieve an A range', '2023-11-08'),
(16, 3, '2022-2023', 'spring', 3, 'Too hard. low grade..', '2022-05-23'),
(3, 2, '2022-2023', 'fall', 4, 'The course was very informative and well-structured.', '2022-12-30'),
(7, 5, '2022-2023', 'fall', 4, 'The workload was manageable and the assignments were helpful.', '2023-01-08'),
(6, 1, '2023-2024', 'fall', 5, 'I found the course challenging but rewarding in the end. Also, the prof.wang is so nice', '2023-12-29'),
(4, 1, '2022-2023', 'fall', 4, 'workload kind of small.', '2023-01-18'),
(12, 5, '2022-2023', 'fall', 3, 'difficult...', '2023-02-08'),
(9, 3, '2023-2024', 'fall', 3, 'workload is large. and group work...', '2023-12-29');


SELECT * FROM Users;
SELECT * FROM Courses;
SELECT * FROM Bookmarks;
SELECT * FROM Reviews;




