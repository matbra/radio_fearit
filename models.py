# models.py
import peewee

database = peewee.MySQLDatabase('radio_fearit', host="lvps83-169-2-231.dedicated.hosteurope.de", user="radio_fearit", passwd="Unf17m4*")


########################################################################
# class RadioFearit(peewee.Model):
#     """
#     ORM model of the Artist table
#     """
    # name = peewee.CharField()

    # class Meta:
        # database = database


########################################################################
class Words(peewee.Model):
    """
    ORM model of album table
    """
    # id = peewee.IntegerField()
    date = peewee.DateTimeField(default=peewee.datetime.datetime.now)
    word = peewee.CharField()

    class Meta:
        database = database


if __name__ == "__main__":
    try:
        Words.create_table()
    except peewee.OperationalError:
        print("Words table already exists!")

    # try:
    #     Album.create_table()
    # except peewee.OperationalError:
    #     print
    #     "Album table already exists!"