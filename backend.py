import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

def log_in(user_code, pw):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Users WHERE user_name = ?', (user_code,))
    user_info = cursor.fetchone()
    # print(user_info)
    conn.close()
    
    if user_info is None:
        # print("No user found. You may need to register first.")
        return False, False
    elif pw == user_info[2] and user_info[3] == "student":
        # print("Login successful!")
        return True, "student"
    elif pw == user_info[2] and user_info[3] == "admin":
        return True, "admin"
    else:
        # print("Invalid password.")
        return False, False

def register(username, password,role = "student"):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Users WHERE user_name = ?', (username,))
    if cursor.fetchone():
        print("Username already exists.")
        return False

    cursor.execute('INSERT INTO Users (user_name, password, role) VALUES (?, ?, ?)', (username, password, role))
    conn.commit()
    print("Registration successful.")
    return True


## functions for student
def get_course_list(): ##view course list
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """
        SELECT
            c.course_type,
            c.course_num
        FROM
            Courses c
        """
    cursor.execute(query)
    lst = cursor.fetchall()
    conn.commit()
    cursor.close()
    # return lst
    course_lst = defaultdict(list)
    for i in range(len(lst)):
        course_lst[lst[i][0]].append(lst[i][1])
    # course_lst = [lst[i][0] for i in range(len(lst))]
    return course_lst

def get_scores_and_comments(course_type, course_num): ##view others ratings and comments to a certain course
    """
        student can view others ratings and comments by inputting the course code (e.g CSC 3170)"""
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    query = """
    SELECT c.courseid 
    FROM Courses c
    WHERE
    c.course_type = ? AND c.course_num = ?;
    """
    cursor.execute(query, (course_type, course_num))
    courseid = cursor.fetchone()[0]

    query = """
    SELECT 
        c.description,
        c.course_name,
        r.year,
        r.semester,
        r.rating, 
        r.comment
    FROM 
        Courses c
    LEFT JOIN 
        Reviews r ON r.courseid = c.courseid
    WHERE 
        c.courseid = ? ;
    """
    cursor.execute(query, (courseid,))

    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    
    return results

def add_course_review(course_type, course_num, user_name, rating, comment, semester, enrolled_year):##add ratings and comments to a certain course

    """
        student can add ratings and comments to a certain course"""
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT u.userid
                    FROM Users u
                    WHERE u.user_name = ?""",(user_name,))
    u = cursor.fetchall()
    userid = u[0][0]

    cursor.execute("""
        SELECT courseid FROM Courses
        WHERE course_type = ? AND course_num = ?;
    """, (course_type, course_num))

    courseid_result = cursor.fetchone()
    print(courseid_result)
    
    course_id = courseid_result[0]

    review_date = datetime.now().strftime("%Y-%m-%d")
    print(course_id, userid,  enrolled_year, semester, rating, comment, review_date)
    cursor.execute("""
        INSERT INTO Reviews (courseid, userid, year, semester, rating, comment, review_date)
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, (course_id, userid,  enrolled_year, semester, rating, comment, review_date))
    conn.commit()
    cursor.close()

def add_bookmark_db(user_name, course_type, course_num):##add bookmark to a certain course
    """
        student can add bookmark to a certain course"""

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT u.userid
                    FROM Users u
                    WHERE u.user_name = ?""",(user_name,))
    u = cursor.fetchall()
    user_id = u[0][0]

    cursor.execute("""
        SELECT courseid FROM Courses
        WHERE course_type = ? AND course_num = ?
    """, (course_type, course_num))
    course_id_result = cursor.fetchone()
    
    if course_id_result:
        course_id = course_id_result[0]
        
        cursor.execute("""
            SELECT 1 FROM Bookmarks
            WHERE userid = ? AND courseid = ?
        """, (user_id, course_id))
        existing_bookmark = cursor.fetchone()
        
        if not existing_bookmark:
            cursor.execute("""
                INSERT INTO Bookmarks (userid, courseid)
                VALUES (?, ?)
            """, (user_id, course_id))
            conn.commit()
            print("add successfully")
            cursor.close()
            return True
        else:
            print("already exist")
            cursor.close()
            return None

def view_bookmarks(user_name):## view my bookmark collection
    """
        a student can view his/her bookmark collection"""
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""SELECT u.userid
                    FROM Users u
                    WHERE u.user_name = ?""",(user_name,))
    u = cursor.fetchall()
    user_id = u[0][0]
    cursor.execute("""
        SELECT c.course_type, c.course_num, c.course_name, AVG(r.rating) as average_rating
        FROM Bookmarks b
        JOIN Courses c ON b.courseid = c.courseid
        LEFT JOIN Reviews r ON c.courseid = r.courseid
        WHERE b.userid = ?
        GROUP BY c.courseid
    """, (user_id,))
    
    bookmarks = cursor.fetchall()
    conn.commit()
    cursor.close()
    if bookmarks:
        total = []
        for bookmark in bookmarks:
            course_type, course_num, course_name, average_rating = bookmark
            average_rating = average_rating if average_rating is not None else "no ratings"
            total.append((course_type, course_num, course_name, average_rating))
        return total
    else:
        return None
    
def remove_bookmark(user_name, course_type, course_num): ##remove bookmark(s) in my bookmark collection
    """
            a student can remove bookmark(s) in his/her bookmark collection"""

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT u.userid
                    FROM Users u
                    WHERE u.user_name = ?""",(user_name,))
    u = cursor.fetchall()
    user_id = u[0][0]
    cursor.execute("""
        SELECT courseid FROM Courses
        WHERE course_type = ? AND course_num = ?
    """, (course_type, course_num))
    course_id = cursor.fetchone()
    
    if course_id:
        cursor.execute("""
            DELETE FROM Bookmarks
            WHERE userid = ? AND courseid = ?
        """, (user_id, course_id[0]))
        conn.commit()
        cursor.close()
        # print("remove  successfully")

def get_course_rankings(): ##view the course rankings by average ratings
    """
        a student can view the course rankings by average ratings"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            c.course_type, 
            c.course_num, 
            c.course_name, 
            AVG(r.rating) as average_rating
        FROM 
            Courses c
        JOIN 
            Reviews r ON c.courseid = r.courseid
        GROUP BY 
            c.courseid
        ORDER BY 
            average_rating DESC
        LIMIT 10;
    """)
    
    top_courses = cursor.fetchall()
    conn.commit()
    cursor.close()
    
    return top_courses

def get_my_reviews(user_account):  ## see my rating history
    """
        a student can view self rating and comments history"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """
    SELECT
        c.course_type,
        c.course_num,
        c.course_name,
        r.year,
        r.semester,
        r.rating,
        r.comment,
        r.review_date
    FROM
        Courses c
    JOIN
        Reviews r ON c.courseid = r.courseid
    JOIN
        Users u ON r.userid = u.userid
    WHERE
        u.user_name = ?
    """
    cursor.execute(query, (user_account,))
    
    reviews = cursor.fetchall()

    review_list = []
    for row in reviews:
        review = {
            'course_type': row[0],
            'course_num': row[1],
            'course_name': row[2],
            'year': row[3],
            'semester': row[4],
            'rating': row[5],
            'comment': row[6],
            'review_date': row[7]
        }
        review_list.append(review)
    
    cursor.close()
    
    return review_list

def update_course_review(user_name, course_type, course_num, new_rating, new_comment):##modify my rating or comment to a certain course
    """
        a student can update/modify one's rating or comment to a certain course"""

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute(""" SELECT userid From Users
                   WHERE user_name = ?;""",(user_name,))
    user_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT courseid FROM Courses
        WHERE course_type = ? AND course_num = ?;
    """, (course_type, course_num))
    course_id_result = cursor.fetchone()
    
    if course_id_result is None:
        print("No course found with the given type and number.")
        return
    
    course_id = course_id_result[0]
        
   
    cursor.execute("""
        SELECT reviewid FROM Reviews
        WHERE courseid = ? AND userid = ?;
    """, (course_id, user_id))
    review_id_result = cursor.fetchone()
    
    review_id = review_id_result[0]

    cursor.execute("""
        UPDATE Reviews
        SET rating = ?, comment = ?, review_date = ?
        WHERE reviewid = ?;
    """, (new_rating, new_comment, datetime.now().strftime("%Y-%m-%d"), review_id))

    conn.commit()
    cursor.close()


## functions for admin
def get_course_info(): ## view all course info
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT course_type, course_num, course_name, description FROM Courses ORDER BY course_type")
    conn.commit()
    courses = cursor.fetchall()
    cursor.close()
    return courses

def add_new_course(course_type, course_num, course_name, description): ## add new course and its info
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO Courses (course_type, course_num, course_name, description)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(insert_query, (course_type, course_num, course_name, description))

    conn.commit()
    cursor.close()
    course_id = cursor.lastrowid
    return course_id

def delete_outdated_course(course_type, course_num): ## remove the course that will not open anymore
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    delete_query = """
    DELETE FROM Courses
    WHERE course_type = ? AND course_num = ?
    """
    cursor.execute(delete_query, (course_type, course_num))

    conn.commit()
    cursor.close()

def get_all_reviews(): ## see all students' ratings and comments
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = """
    SELECT
        c.course_type,
        c.course_num,
        c.course_name,
        r.year,
        r.semester,
        r.rating,
        r.comment,
        r.review_date
    FROM
        Courses c
    JOIN
        Reviews r ON c.courseid = r.courseid
    JOIN
        Users u ON r.userid = u.userid
    ORDER BY 
        c.course_type
    """
    cursor.execute(query)
    
    reviews = cursor.fetchall()
    cursor.close()
    return reviews

def delete_records_older_than_three_years(): ## tidy up the database by removing records that is more than 2 years ago
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    

    current_date = datetime.now()
    three_years_ago = current_date - timedelta(days=3*365)

    cursor.execute("""
                DELETE FROM Reviews
                WHERE review_date <= ? 
                OR CAST(SUBSTR(year, 1, 4) AS INTEGER) <= ?
        """, (three_years_ago.strftime('%Y-%m-%d'), three_years_ago.year - 3))
                
    conn.commit()
    cursor.close()

