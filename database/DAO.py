from database.DB_connect import DBConnect
from model.arco import Arco
from model.artista import Artista
from model.playlist import Playlist
from model.traccia import Traccia


class DAO():

    @staticmethod
    def getAllCountries():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.Country
                from customer c
                where c.Country is not null
                order by c.Country
                """

        cursor.execute(query)

        for row in cursor:
            results.append(row["Country"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                
select distinct a.*
from artist a , album a2 , track t 
where a.ArtistId = a2.ArtistId and a2.AlbumId = t.AlbumId 
                
                """

        cursor.execute(query)

        for row in cursor:
            results.append(Artista(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getTracksFromArtistId(artistId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
select t.* 
from album a , artist a2 , track t 
where a.ArtistId =a2.ArtistId and t.AlbumId =a.AlbumId and a2.ArtistId = %s
                

                """

        cursor.execute(query,(artistId,))

        for row in cursor:
            results.append(Traccia(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPlaylistFromArtistId(artistId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select  distinct p2.*
from playlisttrack p, track t , album a , artist a2, playlist p2 
where p.TrackId  = t.TrackId and t.AlbumId =a.AlbumId and a.ArtistId =a2.ArtistId and p.PlaylistId =p2.PlaylistId 
and a2.ArtistId = %s



                """

        cursor.execute(query, (artistId,))

        for row in cursor:
            results.append(Playlist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(idMapArtisti):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
select a.ArtistId as id1, a2.ArtistId as id2 , count(distinct p.PlaylistId) as peso
from playlisttrack p , playlisttrack p2, track t , track t2 , album al , album al2 , artist a, artist a2
where p.PlaylistId = p2.PlaylistId 
and p.TrackId = t.TrackId and al.AlbumId = t.AlbumId and al.ArtistId = a.ArtistId 
and p2.TrackId = t2.TrackId and al2.AlbumId = t2.AlbumId and al2.ArtistId = a2.ArtistId 
and a.ArtistId < a2.ArtistId 
group by  a.ArtistId, a2.ArtistId 
                

                """

        cursor.execute(query)

        for row in cursor:
            results.append(Arco(idMapArtisti[row["id1"]], idMapArtisti[row["id2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results