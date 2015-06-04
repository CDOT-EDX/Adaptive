f = open('../../MySQL_Conf.txt')

db_name = f.readline().strip()
db_user = f.readline().strip()
db_password = f.readline().strip()
db_host = f.readline().strip()

print db_name
print db_user
print db_password
print db_host
