import pymysql


class DbUtil:
    instance = None

    def __init__(self, host='121.4.40.110', port=3301, user='canteen_admin', pwd='canteen_admin', db='db_exp',
                 charset='utf8'):
        self._conn = pymysql.connect(host=host, port=port, user=user, passwd=pwd, db=db, charset=charset)
        self._cur = self._conn.cursor()

    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        else:
            cls.instance = DbUtil()
            return cls.instance

    def send_flower(self):
        conn = pymysql.connect(host='121.4.40.110', port=3301, user='dachuang', passwd='DaChuang.2020', db='dachuangBG',
                               charset='utf8')
        cur = conn.cursor()
        sql = "update flowers " \
              "set flower_db_exp_4=flower_db_exp_4+1 " \
              "where id=1"
        cur.execute(sql)
        conn.commit()
        conn.close()

    def get_recent_order(self):
        sql = 'select prd_name, concat(canteen_name, store_floor, "楼"), prd_price, prd_amount ' \
              'from orders, product, prd_order, store, canteen ' \
              'where order_status=1' \
              '     and orders.order_id=prd_order.order_id' \
              '     and prd_order.prd_id=product.prd_id' \
              '     and product.store_id=store.store_id' \
              '     and store.canteen_id=canteen.canteen_id ' \
              'order by modified_time desc'
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_one_prd_randomly(self):
        sql = 'select prd_name, prd_intro, prd_price, prd_amount ' \
              'from product ' \
              'where prd_status=1 ' \
              'order by rand() LIMIT 1'
        self._cur.execute(sql)
        res = self._cur.fetchall()
        return res

    def get_user_id(self, user_name):
        sql = "select user_id " \
              "from users " \
              "where user_name=\'{}\'" \
            .format(user_name)
        self._cur.execute(sql)
        res = self._cur.fetchall()
        return res[0][0]

    def get_user_orders(self, user_name):
        sql = 'select orders.order_id, concat(canteen_name, store_floor, "楼 ", store_name), ' \
              'GROUP_CONCAT(prd_name SEPARATOR \',\') prd_names , total, ' \
              'order_status, concat(comment_level, " 分: ", comment_content)' \
              'from users, store, canteen, orders left join cmt on orders.order_id=cmt.order_id, prd_order, product ' \
              'where users.user_id=orders.user_id ' \
              '     and user_name=\'{}\' ' \
              '     and orders.store_id=store.store_id ' \
              '     and store.canteen_id=canteen.canteen_id ' \
              '     and orders.order_id=prd_order.order_id ' \
              '     and product.prd_id=prd_order.prd_id ' \
              'group by orders.order_id ' \
              'order by orders.modified_time desc' \
            .format(user_name)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_canteen_info(self, canteen_id=-1):
        if canteen_id != -1:
            sql = "select canteen_name, AVG(comment_level) , canteen_pic " \
                  "from canteen, store, orders, cmt " \
                  "where cmt.order_id=orders.order_id " \
                  "     and orders.store_id=store.store_id " \
                  "     and canteen.canteen_id=store.canteen_id " \
                  "     and canteen.canteen_id={} " \
                  "group by canteen_name".format(canteen_id)
        else:
            sql = "select canteen_name, AVG(comment_level) " \
                  "from canteen, store, orders, cmt " \
                  "where cmt.order_id=orders.order_id " \
                  "     and orders.store_id=store.store_id " \
                  "     and canteen.canteen_id=store.canteen_id " \
                  "group by canteen_name"
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_canteen_comment(self, canteen_id):
        sql = "select loc, comment_level, comment_content " \
              "from canteen_info " \
              "where canteen_id={}" \
            .format(canteen_id)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_canteen_top(self, canteen_id):
        sql = "select prd_name, concat(store_floor, ' 楼'), store_name, prd_price, prd_amount " \
              "from product, store " \
              "where product.store_id=store.store_id " \
              "     and store.canteen_id={} " \
              "order by prd_amount desc" \
            .format(canteen_id)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_store_prd(self, store_name):
        sql = "select prd_id, prd_name, prd_intro, prd_price, prd_amount " \
              "from product, store " \
              "where product.store_id=store.store_id " \
              "     and store_name=\'{}\' " \
              "     and prd_status=1 " \
              "order by prd_amount desc" \
            .format(store_name)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_admin_info(self, admin_name):
        sql = "select canteen_access, store_access " \
              "from admin " \
              "where admin_name=\'{}\'".format(admin_name)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_not_finished_order(self, canteen_id=-1, store_id=-1):
        if canteen_id == -1:
            sql = "select orders.order_id, canteen_name, store_name, " \
                  "GROUP_CONCAT(prd_name SEPARATOR ',') prd_names, orders.total, orders.create_time " \
                  "from orders, prd_order, product, store, canteen " \
                  "where orders.store_id=store.store_id " \
                  "     and store.canteen_id=canteen.canteen_id " \
                  "     and prd_order.order_id=orders.order_id " \
                  "     and prd_order.prd_id=product.prd_id " \
                  "     and orders.order_status=0 " \
                  "group by orders.order_id " \
                  "order by create_time "
        elif store_id == -1:
            sql = "select orders.order_id, canteen_name, store_name, GROUP_CONCAT(prd_name SEPARATOR ',') prd_names " \
                  "from orders, prd_order, product, store, canteen " \
                  "where orders.store_id=store.store_id " \
                  "     and store.canteen_id=canteen.canteen_id " \
                  "     and prd_order.order_id=orders.order_id " \
                  "     and prd_order.prd_id=product.prd_id " \
                  "     and orders.order_status=0 " \
                  "     and canteen.canteen_id={} " \
                  "group by orders.order_id " \
                  "order by create_time".format(canteen_id)
        else:
            sql = "select orders.order_id, canteen_name, store_name, GROUP_CONCAT(prd_name SEPARATOR ',') prd_names " \
                  "from orders, prd_order, product, store, canteen " \
                  "where orders.store_id=store.store_id " \
                  "     and store.canteen_id=canteen.canteen_id " \
                  "     and prd_order.order_id=orders.order_id " \
                  "     and prd_order.prd_id=product.prd_id " \
                  "     and orders.order_status=0 " \
                  "     and canteen.canteen_id={} " \
                  "     and store.store_id={} " \
                  "group by orders.order_id " \
                  "order by create_time".format(canteen_id, store_id)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_admin_comment(self, canteen_id=-1, store_id=-1):
        if canteen_id == -1:
            sql = "select canteen_name, loc, comment_level, comment_content " \
                  "from canteen_info, canteen " \
                  "where canteen_info.canteen_id=canteen.canteen_id " \
                  "order by comment_time desc"
        elif store_id == -1:
            sql = "select canteen_name, loc, comment_level, comment_content " \
                  "from canteen_info, canteen " \
                  "where canteen_info.canteen_id=canteen.canteen_id " \
                  "     and canteen_info.canteen_id={} " \
                  "order by comment_time desc".format(canteen_id)
        else:
            sql = "select canteen_name, loc, comment_level, comment_content " \
                  "from canteen_info, canteen " \
                  "where canteen_info.canteen_id=canteen.canteen_id " \
                  "     and canteen_info.canteen_id={} " \
                  "     and canteen_info.store_id={} " \
                  "order by comment_time desc".format(canteen_id, store_id)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def get_admin_order(self, canteen_id=-1, store_id=-1):
        if canteen_id == -1:
            sql = 'select canteen_name, concat(canteen_name, store_floor, "楼 ", store_name),' \
                  'GROUP_CONCAT(prd_name SEPARATOR \',\') prd_names, total, ' \
                  'concat(comment_level, " 分: ", comment_content)' \
                  'from store, canteen, orders left join cmt on orders.order_id=cmt.order_id, prd_order, product ' \
                  'where orders.store_id=store.store_id ' \
                  '     and store.canteen_id=canteen.canteen_id ' \
                  '     and orders.order_id=prd_order.order_id ' \
                  '     and product.prd_id=prd_order.prd_id ' \
                  'group by orders.order_id ' \
                  'order by orders.modified_time desc'
        elif store_id == -1:
            sql = 'select canteen_name, concat(canteen_name, store_floor, "楼 ", store_name),' \
                  'GROUP_CONCAT(prd_name SEPARATOR \',\') prd_names, total, ' \
                  'concat(comment_level, " 分: ", comment_content)' \
                  'from store, canteen, orders left join cmt on orders.order_id=cmt.order_id, prd_order, product ' \
                  'where orders.store_id=store.store_id ' \
                  '     and store.canteen_id=canteen.canteen_id ' \
                  '     and orders.order_id=prd_order.order_id ' \
                  '     and product.prd_id=prd_order.prd_id ' \
                  '     and canteen.canteen_id={} ' \
                  'group by orders.order_id ' \
                  'order by orders.modified_time desc'.format(canteen_id)
        else:
            sql = 'select canteen_name, concat(canteen_name, store_floor, "楼 ", store_name),' \
                  'GROUP_CONCAT(prd_name SEPARATOR \',\') prd_names, total, ' \
                  'concat(comment_level, " 分: ", comment_content)' \
                  'from store, canteen, orders left join cmt on orders.order_id=cmt.order_id, prd_order, product ' \
                  'where orders.store_id=store.store_id ' \
                  '     and store.canteen_id=canteen.canteen_id ' \
                  '     and orders.order_id=prd_order.order_id ' \
                  '     and product.prd_id=prd_order.prd_id ' \
                  '     and canteen.canteen_id={}' \
                  '     and orders.store_id={} ' \
                  'group by orders.order_id ' \
                  'order by orders.modified_time desc'.format(canteen_id, store_id)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    '''
        data 格式:
        --0:user_id
        --1:store_id
        --2:total
        --3:prds
        ------0:prd0
        ------1:prd1
        ...
    '''

    def add_order(self, data):
        sql = "insert into orders(user_id, store_id, total) " \
              "values({}, {}, {})" \
            .format(data[0], data[1], data[2])
        self._cur.execute(sql)
        order_id = self._cur.lastrowid
        prds = data[3]

        for prd in prds:
            sql = "insert into prd_order(order_id, prd_id) " \
                  "value({}, {})".format(order_id, prd)
            self._cur.execute(sql)
        self.db_commit()

    def add_comment(self, data):
        sql = "insert into cmt(order_id, comment_content, comment_level) " \
              "values(%s, %s, %s)"
        self._cur.execute(sql, data)

    def query(self, table_name, column_name, condition):
        sql = "select * from {} where {}='{}'".format(table_name, column_name, condition)
        count = self._cur.execute(sql)
        res = self._cur.fetchall()
        return count, res

    def add_user(self, data):
        sql = "insert into users (user_name, user_psw) " \
              "values (%s, %s)"
        self._cur.execute(sql, data)

    def update_order_status(self, order_id):
        sql = "update orders " \
              "set order_status=1 " \
              "where orders.order_id={}" \
            .format(order_id)
        print(sql)
        self._cur.execute(sql)

    def db_commit(self):
        self._conn.commit()

    def db_rollback(self):
        self._conn.rollback()


if __name__ == '__main__':
    db = DbUtil()
    # print(db.get_canteen_info(1))
    print(db.get_admin_info('admin'))
    # print(db.get_canteen_info())
    # db.add_comment((2, "test", 3))
    # db.db_commit()
    # del db
