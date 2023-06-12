import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="siddu",
    database="twitter"
)

cursor = db.cursor()

######## CREATING THE TABLE
# cursor.execute("CREATE TABLE twitterdata(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), bio TEXT, following FLOAT, followers FLOAT, location VARCHAR(50), website VARCHAR(50))")

def insert_twitter_data(name, bio, following, followers, location, website):
    # Convert following and followers count datatype to float
    def convert_to_float(data):
        if "K" in data:
            data = float(data[:-1])
            data *= 1000
        elif "M" in data:
            data = float(data[:-1])
            data *= 1_000_000
        elif "," in data:
            data = float(data.replace(",",""))
        return data
    
    # Function call
    following = convert_to_float(following)
    followers = convert_to_float(followers)

    # Inserting the values into table
    cursor.execute("INSERT INTO twitterdata (name, bio, following, followers, location, website) VALUES (%s, %s, %s, %s, %s, %s)", (name, bio, following, followers, location, website))
    db.commit()
    print("Database insertion Success!")