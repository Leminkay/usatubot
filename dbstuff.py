import psycopg2


class DbQuery:

    def __init__(self):
        self.conn = psycopg2.connect(dbname='Bank', user='postgres', password='12345', host='localhost')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def find_user(self, name):
        self.cur.execute("select * from usatu where name = %s and upd =(select max(upd) from usatu)",
                         (name,))
        ans = self.cur.fetchall()
        return ans

    def get_spec_list(self, spec):
        self.cur.execute("select * from usatu where spec=%s and upd =(select max(upd) from usatu) order by advantage desc, usatu.sum desc",(spec,))
        # в бд данные вроде бы отсорчены в нужном порядке из-за порядка заполнения во время парсинга, но ордер всеравно сделол
        #select * from usatu where spec=%s and upd =(select max(upd) from usatu)
        ans = self.cur.fetchall()
        return ans


if __name__ == '__main__':
    q = DbQuery()
    print(q.get_spec_list('165'))