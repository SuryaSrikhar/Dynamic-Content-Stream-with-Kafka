from flask import Flask, request, jsonify, render_template
import sqlite3

DB = "control.db"
app = Flask(__name__, template_folder="templates")

def query(q, args=(), one=False):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(q, args)
    rows = cur.fetchall()
    con.commit()
    con.close()
    return (rows[0] if rows else None) if one else rows

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/topics", methods=["POST", "GET"])
def topics():
    if request.method == "POST":
        name = request.json.get("name")
        if not name:
            return jsonify({"error": "name required"}), 400
        query("INSERT OR IGNORE INTO topics(name,status) VALUES(?,?)", (name, "pending"))
        return jsonify({"status": "pending"})
    rows = query("SELECT name,status FROM topics")
    return jsonify([{"name": r[0], "status": r[1]} for r in rows])

@app.route("/topics/<topic>/approve", methods=["POST"])
def approve(topic):
    query("UPDATE topics SET status='approved' WHERE name=?", (topic,))
    return jsonify({"status": "approved"})

@app.route("/subscribe", methods=["POST"])
def subscribe():
    u = request.json.get("username")
    t = request.json.get("topic")
    if not u or not t:
        return jsonify({"error": "username and topic required"}), 400
    query("INSERT OR IGNORE INTO user_subscriptions(username,topic_name) VALUES(?,?)", (u, t))
    return jsonify({"subscribed": True})

if __name__ == "__main__":
    app.run(port=5000)
    
    
    
