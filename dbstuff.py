import psycopg2
import parsetable as ps
import requests

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

    def find_user_upd(self,name, v_time):
        self.cur.execute("select * from usatu where name = %s and upd = %s",
                         (name, v_time))
        ans = self.cur.fetchall()
        return ans

    def get_spec_list(self, spec):
        self.cur.execute("select * from usatu where spec=%s and upd =(select max(upd) from usatu) order by agreed desc, advantage desc, usatu.sum desc",(spec,))
        #select * from usatu where spec=%s and upd =(select max(upd) from usatu)
        ans = self.cur.fetchall()
        return ans

    def get_spec_list_upd(self, spec, v_time):
        self.cur.execute(
            "select * from usatu where spec=%s and upd = %s order by agreed desc, advantage desc, usatu.sum desc",
            (spec, v_time))
        ans = self.cur.fetchall()
        return ans

    def insert_user(self, abitur, spec, cTime):
        self.cur.execute(
            "INSERT INTO USATU (name,sum,math,inf,rus,inv, agreed, advantage, original, spec, upd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (abitur[1], abitur[2], abitur[3], abitur[4], abitur[5], abitur[6], abitur[7], abitur[8], abitur[9], spec,
             cTime)
        )
        self.conn.commit()

    def insert_all(self, cTime):
        s = requests.Session()
        s.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        s.headers['Referer'] = ps.url
        csrf = ps.set_csrftoken(s)
        count = 0
        for key in ps.specValue:
            page_data = ps.request_page(s, key, csrf)
            print(ps.specValue[key])
            usrs = ps.get_users(page_data)
            for usr in usrs:
                self.insert_user( usr, key, cTime)
                count += 1
        print('inserted {}'.format(count))

    def get_subs(self):
        self.cur.execute("select * from subs")
        ans = self.cur.fetchall()
        return ans

    def get_closest_upd(self, v_time):
        self.cur.execute("select upd from usatu where upd<=%s order by upd desc limit 1", (v_time,))
        ans = self.cur.fetchone()
        return ans

    def insert_sub(self, name, id):
        self.cur.execute(
            "INSERT INTO subs (name, t_id) VALUES (%s, %s)",
            (name, id)
        )
        self.conn.commit()

    def delete_sub(self, id):
        self.cur.execute(
            "delete from subs where t_id = '%s'",
            (id, )
        )
        self.conn.commit()
if __name__ == '__main__':
    q = DbQuery()
    print(q.get_spec_list('168'))
    print(q.find_user('Симаков Максим Владимирович'))