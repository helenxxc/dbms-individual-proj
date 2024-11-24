import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from backend import  *


def handle_login():
    global current_account
    account = account_entry.get()
    password = password_entry.get()
    flag, user = log_in(account, password)
    current_account = account
    if flag and user == "student":
        messagebox.showinfo("", f"Login Successful. Welcome {account}!")
        student_site()  # Open the new window for further functions
    elif flag and user == "admin":
        messagebox.showinfo("", f"Login Successful. Welcome {account}!")
        admin_site()
    else:
        messagebox.showerror("Login Failed", "Invalid account or password.")

def open_registration_window():
    # Create a new window for registration
    reg_window = tk.Toplevel(root)
    reg_window.title("Register New Account")
    reg_window.geometry("300x200")
    reg_window.configure(bg="#e0e0e0")

    # Label and entry for new account
    tk.Label(reg_window, text="New Account:", font=("Helvetica", 12), bg="#e0e0e0").pack(pady=5)
    new_account_entry = tk.Entry(reg_window, font=("Helvetica", 12))
    new_account_entry.pack(pady=5)

    # Label and entry for new password
    tk.Label(reg_window, text="New Password:", font=("Helvetica", 12), bg="#e0e0e0").pack(pady=5)
    new_password_entry = tk.Entry(reg_window, font=("Helvetica", 12))
    new_password_entry.pack(pady=5)

    # Confirm button to add new user to database
    def confirm_registration():
        new_account = new_account_entry.get()
        new_password = new_password_entry.get()
        
        # Basic validation
        if not new_account or not new_password:
            messagebox.showerror("Registration Failed", "Please fill out all fields.")
            return
        
        
        if register(new_account, new_password):
            messagebox.showinfo("Registration Successful", "Account created successfully!")
            reg_window.destroy()  # Close the registration window after successful registration
        else:
            messagebox.showerror("Registration Failed", "Account already exists.")

    # Confirm button
    confirm_button = tk.Button(reg_window, text="Confirm", font=("Helvetica", 12, "bold"), bg="#1a73e8", fg="white", command=confirm_registration)
    confirm_button.pack(pady=20)

def student_site():
    new_window = tk.Toplevel(root)
    new_window.title("Student Site")
    new_window.geometry("600x400")
    new_window.configure(bg="#e0e0e0")
    
    # Portfolio label
    portfolio_label = tk.Label(new_window, text=f"User {current_account}", font=("Helvetica", 18, "bold"), bg="#e0e0e0")
    portfolio_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    # Button frame
    button_frame = tk.Frame(new_window, bg="white")
    button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nw")
    
    # "My comment history" button
    comment_button = tk.Button(button_frame, text="My comment history", font=("Helvetica", 12), bg="#6699FF", fg="white", width=20,command=open_comment_history)
    comment_button.grid(row=0, column=0, pady=5)
    
    # "My bookmarks" button
    bookmark_button = tk.Button(button_frame, text="My bookmarks", font=("Helvetica", 12), bg="#6699FF", fg="white", width=20,command=open_bookmarks)
    bookmark_button.grid(row=1, column=0, pady=5)
    
    # "Course Rankings" button
    rankings_button = tk.Button(button_frame, text="Course Rankings", font=("Helvetica", 12), bg="#6699FF", fg="white", width=20,command=open_course_rankings)
    rankings_button.grid(row=2, column=0, pady=5)
    
    # Filter frame
    filter_frame = tk.Frame(new_window, bg="white", bd=1, relief="solid")
    filter_frame.grid(row=1, column=1, padx=20, pady=10, sticky="ne")

    # "Course list" title
    course_list_label = tk.Label(filter_frame, text="Course list:", font=("Helvetica", 16, "bold"), fg="#6699FF", bg="white")
    course_list_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Course code dropdown
    course_info = get_course_list()
    course_lst_dropdown = list(course_info.keys())

    course_code_label = tk.Label(filter_frame, text="Course code", font=("Helvetica", 12), fg="#6699FF", bg="white")
    course_code_label.grid(row=1, column=0, pady=5, padx=10, sticky="w")
    
    global course_code_var
    course_code_var = tk.StringVar()
    course_code_dropdown = ttk.Combobox(filter_frame, textvariable=course_code_var, values=course_lst_dropdown, width=18,state="readonly")
    course_code_dropdown.grid(row=1, column=1, pady=5, padx=10)

    # Course number dropdown
    course_no_label = tk.Label(filter_frame, text="Course No.", font=("Helvetica", 12), fg="#6699FF", bg="white")
    course_no_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
    
    global course_no_var
    course_no_var = tk.StringVar()
    course_no_dropdown = ttk.Combobox(filter_frame, textvariable=course_no_var, values=[], width=18,state="readonly")
    course_no_dropdown.grid(row=2, column=1, pady=5, padx=10)

    def update_course_no(*arg):
        selected_code = course_code_var.get()
        course_nos = course_info.get(selected_code, [])
        course_no_dropdown["values"] = course_nos
        # course_no_dropdown.set("Select Course No.") 

    course_code_var.trace("w", update_course_no)

    # Confirm searching button
    search_button = tk.Button(filter_frame, text="Confirm searching", font=("Helvetica", 12), bg="#6699FF", fg="white", width=15,command= open_confirm_searching)
    search_button.grid(row=3, column=0, columnspan=2, pady=15)

def wrap_text(text, line_length=100):
    wrapped_lines = []
    while len(text) > line_length:
        wrapped_lines.append(text[:line_length])
        text = text[line_length:]
    wrapped_lines.append(text)
    return '\n'.join(wrapped_lines)

def open_confirm_searching():
    course_type = course_code_var.get()
    course_num = course_no_var.get()
    results = get_scores_and_comments(course_type, course_num) 

    result_window = tk.Toplevel(root)
    result_window.title("Search Results")
    result_window.geometry("900x400")


    course_basic = tk.Label(
        result_window,
        text=f"Course: {course_type+course_num}    {results[0][1]}",
        font=("Helvetica", 14, "bold"),
        bg="#e0e0e0"
    )
    course_basic.pack(pady=(20,10))

    course_intr = tk.Label(
        result_window,
        text=wrap_text(results[0][0],150),
        font=("Helvetica", 9),
        bg="#e0e0e0"
    )
    course_intr.pack(pady=(20,10))


    tree = ttk.Treeview(result_window, columns=("year", "semester", "rating", "comment"), show="headings",height=8)
    tree.heading("year", text="year")
    tree.column("year", width=15)
    tree.heading("semester", text="semester")
    tree.column("semester", width=10)
    tree.heading("rating", text="rating")
    tree.column("rating", width=10)
    tree.heading("comment", text="comment")
    tree.column("comment", width=600)

    
    for row in results:
        tree.insert("", tk.END, values=row[2:])
    
    tree.pack(fill="both", expand=True, padx=20, pady=10)

    button_frame = tk.Frame(result_window)
    button_frame.pack(pady=10)

    add_review_button = tk.Button(button_frame, text="Add Review", command=lambda: add_review(result_window, course_type, course_num))
    add_review_button.grid(row=0, column=0, padx=10)

        

    add_bookmark_button = tk.Button(button_frame, text="Add Bookmark", command=lambda: add_bookmark(course_type, course_num))
    add_bookmark_button.grid(row=0, column=1, padx=10)

def add_review(parent_window, course_type, course_num):
    review_window = tk.Toplevel(parent_window)
    review_window.title("Add Review")
    review_window.geometry("300x300")

    # Rating Entry
    tk.Label(review_window, text="Rating:").pack(pady=5)
    rating_entry = ttk.Combobox(review_window, values=[1,2,3,4,5], width=20,state="readonly")
    rating_entry.pack(pady=5)

    # Comment Entry
    tk.Label(review_window, text="Comment:").pack(pady=5)
    comment_entry = tk.Entry(review_window, width=80)
    comment_entry.pack(pady=5)

    # Semester Dropdown
    tk.Label(review_window, text="Semester").pack(pady=5)
    semester_dropdown = ttk.Combobox(review_window, values=["summer", "fall", "spring"], width=20,state="readonly")
    semester_dropdown.pack(pady=5)

    # Academic Year Dropdown
    tk.Label(review_window, text="Academic Year").pack(pady=5)
    year_dropdown = ttk.Combobox(review_window, values=["2022-2023", "2023-2024", "2024-2025", "2025-2026", "2026-2027"], width=20,state="readonly")
    year_dropdown.pack(pady=5)


    def confirm_review():
        rating = rating_entry.get()
        comment = comment_entry.get()
        semester = semester_dropdown.get()
        enrolled_year = year_dropdown.get()

        if not rating or not comment or not semester or not enrolled_year:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        add_course_review(course_type, course_num, current_account, rating, comment, semester, enrolled_year)
        messagebox.showinfo("Success", "Review added successfully.")
        
        review_window.destroy()

    # Confirm Button
    confirm_button = tk.Button(review_window, text="Confirm", command=confirm_review)
    confirm_button.pack(pady=10)

def add_bookmark(course_type, course_num):

    tmp = add_bookmark_db(current_account, course_type, course_num)
    if tmp == None:
        messagebox.showerror("Error", f"Bookmark already exist")
    else:
        messagebox.showinfo("Success", "Course bookmarked successfully.")
   
def open_bookmarks():
    bookmark_window = tk.Toplevel(root)
    bookmark_window.title("My Bookmarks")
    bookmark_window.geometry("900x300")


    title_label = tk.Label(bookmark_window, text="My Bookmarks", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    columns = ("Course Type","Course Number", "Course Name", "Rating")
    tree = ttk.Treeview(bookmark_window, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    bookmarks = view_bookmarks(current_account)
    for item in bookmarks:
        tree.insert("", "end", values=item)

    vsb = ttk.Scrollbar(bookmark_window, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(bookmark_window, orient="horizontal", command=tree.xview)
    hsb.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hsb.set)

    def show_context_menu(event):
        selected_item = tree.identify_row(event.y)
        if selected_item:
            context_menu.post(event.x_root, event.y_root)
            context_menu.entryconfig("Unbookmark", command=lambda: unbookmark_item(selected_item))

    def unbookmark_item(item):
        item_data = tree.item(item, "values")
        confirm = messagebox.askyesno("Unbookmark", f"Are you sure you want to unbookmark '{item_data[0]+item_data[1]}'?")
        if confirm:
            tree.delete(item)
            remove_bookmark(current_account, item_data[0], item_data[1])
            messagebox.showinfo("Unbookmark", f"'{item_data[0]+item_data[1]}' has been removed from bookmarks.")


    tree.bind("<Button-3>", show_context_menu)


    context_menu = tk.Menu(bookmark_window, tearoff=0)
    context_menu.add_command(label="Unbookmark")

def open_course_rankings():
    ranking_window = tk.Toplevel(root)
    ranking_window.title("Course Rankings")
    ranking_window.geometry("900x300")
    
    title_label = tk.Label(ranking_window, text="Course Rankings", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)
    
    dat = get_course_rankings()
    columns = ("Code", "Number", "Course Name", "Rating")
    tree = ttk.Treeview(ranking_window, columns=columns, show="headings")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")
    

    for course in dat:
        tree.insert("", "end", values=course)
    
    vsb = ttk.Scrollbar(ranking_window, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

def open_comment_history():
    comment_window = tk.Toplevel(root)
    comment_window.title("My Comment History")
    comment_window.geometry("1200x400")

    tree = ttk.Treeview(comment_window, columns=("course_type", "course_num", "course_name", "year", "semester", 
                                                 "rating", "comment", "review_date"), show="headings", height=10)
    tree.heading("course_type", text="Course Type")
    tree.heading("course_num", text="Course Number")
    tree.heading("course_name", text="Course Name")
    tree.heading("year", text="Year")
    tree.heading("semester", text="Semester")
    tree.heading("rating", text="Rating")
    tree.heading("comment", text="Comment")
    tree.heading("review_date", text="Review Date")
    tree.pack(fill="both", expand=True)

    comments_data = get_my_reviews(current_account)
    for comment in comments_data:
        tree.insert("", tk.END, values=(comment['course_type'], comment['course_num'], comment['course_name'], 
                                        comment['year'], comment['semester'], comment['rating'], 
                                        comment['comment'], comment['review_date']))
    
    vsb = ttk.Scrollbar(comment_window, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    hsb = ttk.Scrollbar(comment_window, orient="horizontal", command=tree.xview)
    hsb.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hsb.set)
    
    def edit_record(event):
        item_id = tree.focus()
        column = tree.identify_column(event.x)
        
        if column == "#6": 
            edit_rating(item_id)
        elif column == "#7":  
            edit_comment(item_id)

    def edit_rating(item_id):
        rating_window = tk.Toplevel(comment_window)
        rating_window.title("Edit Rating")
        rating_window.geometry("500x300")
        
        tk.Label(rating_window, text="New Rating:").pack(pady=10)
        rating_var = tk.IntVar()
        rating_entry = tk.Entry(rating_window, textvariable=rating_var)
        rating_entry.pack(pady=10)
        
        def save_rating():
            new_rating = rating_var.get()
            tree.set(item_id, "rating", new_rating)
            line = tree.item(item_id, "values")
            update_course_review(current_account, line[0], line[1], new_rating, line[6])
            rating_window.destroy()
        
        tk.Button(rating_window, text="Save", command=save_rating).pack(pady=10)

    def edit_comment(item_id):
        cmt_window = tk.Toplevel(comment_window)
        cmt_window.title("Edit Comment")
        cmt_window.geometry("500x300")
        
        tk.Label(cmt_window, text="New Comment:").pack(pady=10)
        comment_var = tk.StringVar()
        comment_entry = tk.Entry(cmt_window, textvariable=comment_var, width=50)
        comment_entry.pack(pady=10)
        
        def save_comment():
            new_comment = comment_var.get()
            tree.set(item_id, "comment", new_comment)  
            line = tree.item(item_id, "values")
            update_course_review(current_account, line[0], line[1], line[5], new_comment)
            cmt_window.destroy()
        
        tk.Button(cmt_window, text="Save", command=save_comment).pack(pady=10)

    tree.bind("<Double-1>", edit_record)

def admin_site():
    admin_window = tk.Toplevel(root)
    admin_window.title("Student Site")
    admin_window.geometry("600x400")
    admin_window.configure(bg="#e0e0e0")

    tk.Label(admin_window, text=f"\nAdmin id: {current_account}", font=("Helvetica", 18, "bold"), bg="#e0e0e0").pack(pady=10)

    frame_left = tk.Frame(admin_window, bg="white", bd=2, relief="groove")
    frame_left.place(relx=0.25, rely=0.5, anchor="center", width=200, height=125)

    frame_right = tk.Frame(admin_window, bg="white", bd=2, relief="groove")
    frame_right.place(relx=0.75, rely=0.5, anchor="center", width=200, height=125)

    def show_course_info():
        course_window = tk.Toplevel(admin_window)
        course_window.title("Course Info")
        course_window.geometry("1200x500")

        courses = get_course_info()

        tree = ttk.Treeview(course_window, columns=("type", "number", "name", "description"), show="headings")
        tree.heading("type", text="Course Type")
        tree.heading("number", text="Course Number")
        tree.heading("name", text="Course Name")
        tree.heading("description", text="Description")
        tree.column("type", width=10)
        tree.column("number", width=10)
        tree.column("name",width=20)
        tree.column("description", width=400)
        tree.pack(fill=tk.BOTH, expand=True)

        for course in courses:
            tree.insert("", "end", values=course)

    def modify_course():
        modify_window = tk.Toplevel(admin_window)
        modify_window.title("Course Modify")
        modify_window.geometry("500x600")


        tk.Label(modify_window, text="Course Type").pack(pady=5)
        course_type_entry = tk.Entry(modify_window)
        course_type_entry.pack(pady=5)

        tk.Label(modify_window, text="Course Number").pack(pady=5)
        course_num_entry = tk.Entry(modify_window)
        course_num_entry.pack(pady=5)

        tk.Label(modify_window, text="Course Name").pack(pady=5)
        course_name_entry = tk.Entry(modify_window)
        course_name_entry.pack(pady=5)

        tk.Label(modify_window, text="Description").pack(pady=5)
        description_entry = tk.Entry(modify_window, width=30)
        description_entry.pack(pady=5)


        def insert_course():
            course_type = course_type_entry.get()
            course_num = course_num_entry.get()
            course_name = course_name_entry.get()
            description = description_entry.get()

            if not course_type or not course_num or not course_name or not description:
                messagebox.showerror("Error", "Please enter all fields.")
                return

            add_new_course(course_type, course_num, course_name, description)

            messagebox.showinfo("Success", "Course added successfully.")


        def delete_course():
            course_type = course_type_entry.get()
            course_num = course_num_entry.get()

            if not course_type or not course_num:
                messagebox.showerror("Error", "Please enter course type and number.")
                return

            delete_outdated_course(course_type,course_num)

            messagebox.showinfo("", "The course has been deleted.")

        tk.Button(modify_window, text="Insert New Course", command=insert_course).pack(pady=10)
        tk.Button(modify_window, text="Delete Outdated Course", command=delete_course).pack(pady=10)

    def show_comment_info():
        comment_window = tk.Toplevel(admin_window)
        comment_window.title("Comment Info")
        comment_window.geometry("1500x500")

        comments = get_all_reviews()


        tree = ttk.Treeview(comment_window, columns=("course_type", "course_num", "course_name","year","semester","rating", "comment", "review_date"), show="headings")
        tree.heading("course_type", text="Code")
        tree.heading("course_num", text="No.")
        tree.heading("course_name", text="Title")
        tree.heading("year", text="Year")
        tree.heading("semester", text="Semester")
        tree.heading("rating", text="Rating")
        tree.heading("comment", text="Comment")
        tree.heading("review_date", text="Review Date")

        tree.column("course_type", width=10)
        tree.column("course_num", width=10)
        tree.column("course_name", width=50)
        tree.column("year",width=15)
        tree.column("semester", width=10)
        tree.column("rating", width=10)
        tree.column("comment",width=600)
        tree.column("review_date", width=20)
        tree.pack(fill=tk.BOTH, expand=True)

        for comment in comments:
            tree.insert("", "end", values=comment)

    # Clear Outdated Data 
    def clear_outdated_history():
        delete_records_older_than_three_years()
        messagebox.showinfo("Success", "Outdated reviews cleared successfully.")


    tk.Button(frame_left, text="Course Info", command=show_course_info, bg="#6699FF", fg="white").pack(pady=10, fill=tk.X)
    tk.Button(frame_left, text="Course Modify", command=modify_course,bg="#6699FF", fg="white").pack(pady=10, fill=tk.X)


    tk.Button(frame_right, text="Comment Info", command=show_comment_info, bg="#87CEEB", fg="white").pack(pady=10, fill=tk.X)
    tk.Button(frame_right, text="Clear Outdated History", command=clear_outdated_history, bg="#87CEEB", fg="white").pack(pady=10, fill=tk.X)




# Create the main window
root = tk.Tk()
root.title("Course rating System")
root.geometry("500x400")
root.configure(bg="#e0e0e0")

# Title label
title_label = tk.Label(
    root, text="Course Rating System",
    font=("Helvetica", 16, "bold"), bg="#e0e0e0"
)
title_label.pack(pady=(10, 20))

# Account label and entry
account_label = tk.Label(root, text="Account:", font=("Helvetica", 12), bg="#e0e0e0")
account_label.pack(anchor="w", padx=80)
account_entry = tk.Entry(root, font=("Helvetica", 12))
account_entry.pack(padx=80, pady=(0, 10))
# account = account_entry.get()   ## user_account

# Password label and entry
password_label = tk.Label(root, text="Password:", font=("Helvetica", 12), bg="#e0e0e0")
password_label.pack(anchor="w", padx=80)
password_entry = tk.Entry(root, font=("Helvetica", 12))
password_entry.pack(padx=80, pady=(0, 10))

# Login button
login_button = tk.Button(root, text="Login", font=("Helvetica", 12, "bold"), bg="#1a73e8", fg="white", width=10,command=handle_login)
login_button.pack(pady=(20, 10))

# Register button 
register_button = tk.Button(root, text="Register", font=("Helvetica", 12,"bold"), bg="#1a73e8", fg="white", width=10, command=open_registration_window)
register_button.pack(pady=(20, 10))


root.mainloop()