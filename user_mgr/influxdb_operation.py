from influxdb import InfluxDBClient

def influxdb_query(query_string,host='localhost', port=8086):
    user='root'
    password = 'root'
    dbname = 'libvirtdb'
    query = query_string
    client = InfluxDBClient(host, port, user, password, dbname)
    result = client.query(query)
    return result