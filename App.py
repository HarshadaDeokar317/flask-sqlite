from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

#con = sqlite3.connect("Record.db")
#Database opened successfully


#con.execute("create table Student(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,lname TEXT, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
#Table created successfully

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/details", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            lname = request.form["lname"]
            email = request.form["email"]
            password = request.form["password"]
           # address = request.form["address"]
            with sqlite3.connect("Record.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Student (name,lname,email,password) values (?,?,?,?)", (name,lname,email,password))
                con.commit()
                msg = "Student successfully Added"
        except:
            con.rollback()
            return render_template("duplicate.html")

    return render_template("success.html", msg=msg)
    con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("Record.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Student")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


#Update-----------------------------------------------------------

@app.route("/Update")
def update():
    con = sqlite3.connect("Record.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Student")
    rows = cur.fetchall()
    return render_template("update.html", rows=rows)


@app.route("/updaterecord", methods=["POST", "GET"])
def updaterecod():
    msg = "msg"
    if request.method == "POST":
        try:
            id = request.form["id"]

            name = request.form["name"]
            lname = request.form["lname"]
            email = request.form["email"]
            password = request.form["password"]
           # address = request.form["address"]
            with sqlite3.connect("Record.db") as con:
                cur = con.cursor()
                cur.execute("update Student set name=?,lname=?,email=?,password=? where id=?",
                            (name,lname,email,password,id))

                con.commit()
                msg = "Student successfully updated"
        except:
            con.rollback()
            msg = "We can not update the student."
        finally:
            return render_template("update_record.html", msg=msg)
            con.close()



#Delete---------------------------------------------------------
@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("Record.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Student where id = ?", id)
            msg = "record successfully deleted"
        except:
            msg = "Record can't be deleted"
        finally:
            return render_template("delete_record.html", msg=msg)





if __name__ == '__main__':
    app.run(debug=True,host="localhost",port="5002")
