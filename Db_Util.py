import pymysql
# from DBUtils.PooledDB import PooledDB
class DBUtil:
    def __init__(self,localhost = 'localhost',port=3306,username='root',password='',databasename='face_info'):
        self.db = pymysql.connect(localhost,username,password,databasename)
        self.cursor = self.db.cursor()
        # self.pool = PooledDB(
        #     # 使用链接数据库的模块import pymysql
        #     creator=pymysql,
        #     # 连接池允许的最大连接数，0和None表示不限制连接数
        #     maxconnections=6,
        #     # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        #     mincached=2,
        #     # 链接池中最多闲置的链接，0和None不限制
        #     maxcached=5,
        #     # 链接池中最多共享的链接数量，0和None表示全部共享。
        #     # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
        #     # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
        #     maxshared=3,
        #     # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        #     blocking=True,
        #     # 一个链接最多被重复使用的次数，None表示无限制
        #     maxusage=None,
        #     # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        #     setsession=[],
        #     # ping MySQL服务端，检查是否服务可用。
        #     #  如：0 = None = never, 1 = default = whenever it is requested,
        #     # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        #     ping=0,
        #
        #     # 数据库信息
        #     host=localhost,
        #     port=int(port),
        #     user=username,
        #     password=password,
        #     database=databasename,
        #     charset='utf8'
        # )
    def get_db(self):
        return self.db
    def get_cursor(self):
        return self.cursor
    def get_db_cursor(self):
        return self.get_db(),self.get_cursor()
    def close_connection(self):
        # if self.cursor is None:
        #     self.cursor.close()
        # if self.db is None:
        #     self.db.close()
        pass
    def Listall(self,tablename):
        sql = "select * from "+tablename
        #print(sql)
        self.cursor.execute(sql)
        listall = self.cursor.fetchall()
        self.close_connection()
        return listall
    def ListMany(self,tablename,value):
        sql = 'select * from '+tablename
        self.cursor.execute()
        res = self.cursor.fetchmany(value)
        return res
    def selectOne(self,tablename,column):
        sql="select  "+column+" from "+tablename
        self.cursor.execute(sql)
        data=self.cursor.fetchone()

        self.close_connection()
        return data
    def findById(self,tablename,column,value):
        sql = "select face_name from "+tablename+" where "+column+" = %s"%(value)
        print(sql)
        self.cursor.execute(sql)

        data = self.cursor.fetchall()
        self.close_connection()
        return data
    def insetOne(self,sql,params):
        # res = 0
        # try:
        #     res = self.cursor.execute(sql,params)
        #     #self.cursor.execute(sql)
        #     self.db.commit()
        #
        # except (Exception):
        #     print('ERROR')
        #
        #     self.db.rollback()
        # finally:
        #     self.close_connection()
        #     if res ==1:
        #         print("插入成功")
        self.cursor.execute(sql, params)
        self.db.commit()
    def deleteOneById(self,tableName,colunm,value):
        res = 0
        sql = "delete from "+tableName+" where "+colunm+" = %d"%(value)
        print(sql)
        try:
            res = self.cursor.execute(sql)
            self.db.commit()
        except:
            print('ERROR')
            self.db.rollback()
        finally:
            self.close_connection()
            if res==1:
                print("删除成功")
    def update(self,sql):
        res = 0
        try:
            res =self.cursor.execute(sql)
            self.db.commit()
        except:
            print('ERROE')
            self.db.rollback()
        finally:
            self.close_connection()
            if res==1:
                print("更新成功")
            elif res==0:
                print("更新失败")
    def get_count(self,tablename):
        sql = 'select count(*) from '+tablename
        print(sql)
        self.cursor.execute(sql)
        count = self.cursor.fetchone()[0]
        self.close_connection()
        return count
    def deleteBySql(self,sql):
        res = 0
        try:
            res = self.cursor.execute(sql)
            self.db.commit()
        except:
            print('ERROR')
            self.db.rollback()
        finally:
            if res==1:
                print("删除成功")
            elif res==0:
                print("删除失败")
            self.close_connection()
    def get_OneColumn_Count(self,tableName,column,value):
        sql = "select count(*) from "+tableName+" where "+column+"="+value
        print(sql)
        self.cursor.execute(sql)
        count = self.cursor.fetchall()[0][0]
        self.close_connection()
        return count
    def get_ManyColunm_Count(self,tableName,colunm1,value1,colunm2,value2):
        sql = "select count(*) from "+tableName+" where "+colunm1+" = "+value1+" and "+colunm2+" = "+"'"+value2+"'"
        print(sql)
        self.cursor.execute(sql)
        count = self.cursor.fetchall()
        self.close_connection()
        return count
    def getMaxId(self,tableName):
        sql = "select max(id) from "+tableName
        print(sql)
        self.cursor.execute(sql)
        return self.cursor.fetchall()[0][0]
    def close_all(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()

