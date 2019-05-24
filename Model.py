from cx_Oracle import *
class Model:
    def __init__(self):
        self.song_dict={}
        self.db_status=True
        self.conn=None
        self.cur=None
        try:
            my_dsn=makedsn("DESKTOP-INVLS7L",1521,sid="xe")
            self.conn=connect("mouzikka/music@"+str(my_dsn))
            print("connected successfully to DB")
            self.cur=self.conn.cursor()
        except DatabaseError as e:
            self.db_status=False
            print("Exception")
            print(e)

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
            print("cursor closed successfully")
        if self.conn is not None:
            self.conn.close()
            print("successfully disconnected from DB")

    def add_song(self,song_name,song_path):
        self.song_dict[song_name]=song_path
        print("song name:",song_name)
        print("song added:",self.song_dict[song_name])

    def get_song_path(self,song_name):
        return self.song_dict[song_name]

    def remove_song(self,song_name):
        self.song_dict.pop(song_name)
        print(self.song_dict)

    def search_song_in_favourites(self,song_name):
        self.cur.execute("select song_name from myfavourites where song_name=:1",(song_name,))
        song_tuple=self.cur.fetchone()
        if song_tuple is None:
            return False
        else:
            return True

    def add_song_to_favourites(self,song_name,song_path):
        if(self.search_song_in_favourites(song_name))==True:
            return "Song already present in your favourites"
        self.cur.execute("select max(song_id) from myfavourites")
        last_song_id=self.cur.fetchone()[0]
        next_song_id=1
        if last_song_id is not None:
            next_song_id=last_song_id+1
        self.cur.execute("insert into myfavourites values(:1,:2,:3)",(next_song_id,song_name,song_path))
        self.conn.commit()
        return"Song added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("select song_name,song_path from myfavourites")
        songs_present=False
        for song_name, song_path in self.cur:
            self.song_dict[song_name]=song_path
            songs_present=True
        if songs_present==True:
            return "List populated from favourites"
        else:
            return "No songs present in your favourites"

    def remove_song_from_favourites(self,song_name):
        self.cur.execute("delete from myfavourites where song_name=:1",(song_name,))
        n=self.cur.rowcount
        if n==0:
            return "Song not present in your favourites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from your favourites"

